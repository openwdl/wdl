from wdl.binding import *
from wdl.util import *
import wdl.parser
import re
import subprocess
import tempfile
import uuid
import json
import sys
from xtermcolor import colorize

def lookup_function(symbol_table, scope, scatter_vars=[], index=None):
    def lookup(var):
        if var in scatter_vars:
            for s in scope_hierarchy(scope):
                val = symbol_table.get(s, var)
                if not isinstance(val, WdlUndefined):
                    if var in scatter_vars:
                        return val.value[index]
                    return val
            return WdlUndefined()

        for s in scope_hierarchy(scope):
            for d in s.declarations:
                if d.name == var:
                    return symbol_table.get(s, var)
            for c in s.calls():
                if c.fully_qualified_name == '{}.{}'.format(c.parent.fully_qualified_name, var):
                    return symbol_table.get(c.parent.fully_qualified_name, var)
        return WdlUndefined()
    return lookup

class MissingInputsException(Exception):
    def __init__(self, missing):
        self.__dict__.update(locals())

class EngineException(Exception): pass

class ExecutionContext:
    def __init__(self, fqn, call, index, pid, rc, stdout, stderr, cwd):
        self.__dict__.update(locals())

class ScatterOutput(list):
    def __str__(self):
        return '[ScatterOutput: {}]'.format(', '.join([str(x) for x in self]))

def engine_functions(execution_context=None):
    def tsv(parameters):
        if len(parameters) != 1 or not parameters[0].__class__ in [WdlFileValue, WdlStringValue]:
            raise EvalException("tsv(): expecting one String or File parameter")

        def _tsv(abspath):
            with open(abspath) as fp:
                contents = fp.read().strip('\n')
            lines = contents.split('\n') if len(contents) else []
            if len(lines) == 0:
                if isinstance(execution_context.type, WdlArrayType):
                    return WdlArrayValue(execution_context.type.subtype, [])
                if isinstance(execution_context.type, WdlMapType):
                    return WdlMapType(execution_context.type.key_type, execution_context.type.value_type, {})

            # Determine number of columns, error if they do not match expected type.
            rows = [line.split('\t') for line in lines]
            columns = set([len(row) for row in rows])
            if len(columns) != 1:
                raise EvalException("tsv(): File contains rows with mixed number of columns")
            columns = next(iter(columns))
            if isinstance(execution_context.type, WdlArrayType):
                if columns != 1:
                    raise EvalException("tsv(): Array types expect a one-column TSV")
                array_elements = [python_to_wdl_value(row[0], execution_context.type.subtype) for row in rows]
                return WdlArrayValue(execution_context.type.subtype, array_elements)
            # Otherwise, if columns == 1, output an Array, columns == 2 output a Map
            raise EvalException("Bad value")

        if isinstance(parameters[0], WdlStringValue):
            return _tsv(os.path.join(execution_context.cwd, parameters[0].value))
        if isinstance(parameters[0], WdlFileValue):
            return _tsv(parameters[0].value)

    def read_int(parameters):
        if len(parameters) != 1 or not parameters[0].__class__ in [WdlFileValue, WdlStringValue]:
            raise EvalException("read_int(): expecting one String or File parameter")
        def _read_int(abspath):
            with open(abspath) as fp:
                contents = fp.read().strip('\n')
            if len(contents):
                try:
                    return WdlIntegerValue(int(contents.split('\n')[0]))
                except ValueError:
                    raise EvalException("read_int(): First line of file is not an integer: " + abspath)
            raise EvalException("read_int(): empty file found: " + abspath)
        if isinstance(parameters[0], WdlStringValue):
            return _read_int(os.path.join(execution_context.cwd, parameters[0].value))
        if isinstance(parameters[0], WdlFileValue):
            return _read_int(parameters[0].value)

    def read_boolean(parameters):
        if len(parameters) != 1 or not parameters[0].__class__ in [WdlFileValue, WdlStringValue]:
            raise EvalException("read_boolean(): expecting one String or File parameter")
        def _read_boolean(abspath):
            with open(abspath) as fp:
                contents = fp.read().strip('\n')
            if len(contents):
                line = contents.split('\n')[0].lower()
                return WdlBooleanValue(True if line in ['1', 'true'] else False)
            raise EvalException("read_boolean(): empty file found: " + abspath)
        if isinstance(parameters[0], WdlStringValue):
            return _read_boolean(os.path.join(execution_context.cwd, parameters[0].value))
        if isinstance(parameters[0], WdlFileValue):
            return _read_boolean(parameters[0].value)

    def read_string(parameters):
        if len(parameters) != 1 or not parameters[0].__class__ in [WdlFileValue, WdlStringValue]:
            raise EvalException("read_string(): expecting one String or File parameter")
        def _read_string(abspath):
            with open(abspath) as fp:
                contents = fp.read().strip('\n')
            if len(contents):
                return WdlStringValue(contents.split('\n')[0])
            raise EvalException("read_string(): empty file found: " + abspath)
        if isinstance(parameters[0], WdlStringValue):
            return _read_string(os.path.join(execution_context.cwd, parameters[0].value))
        if isinstance(parameters[0], WdlFileValue):
            return _read_string(parameters[0].value)

    def stdout(parameters):
        if len(parameters) != 0:
            raise EvalException("stdout() expects zero parameters")
        return WdlFileValue(os.path.join(execution_context.cwd, "stdout"))

    def stderr(parameters):
        if len(parameters) != 0:
            raise EvalException("stderr() expects zero parameters")
        return WdlFileValue(os.path.join(execution_context.cwd, "stderr"))

    def strlen(parameters):
        return WdlIntegerValue(len(parameters[0].value))

    def get_function(name):
        if name == 'tsv': return tsv
        elif name == 'read_int': return read_int
        elif name == 'read_boolean': return read_boolean
        elif name == 'read_string': return read_string
        elif name == 'stdout': return stdout
        elif name == 'stderr': return stderr
        elif name == 'strlen': return strlen
        else: raise EvalException("Function {} not defined".format(name))

    return get_function

class WorkflowExecutor:
    def __init__(self, workflow, inputs={}):
        self.dir = os.path.abspath('workflow_{}_{}'.format(workflow.name, str(uuid.uuid4()).split('-')[0]))
        self.workflow = workflow
        self.inputs = inputs

        # Construct the initial symbol table
        self.symbol_table = SymbolTable(workflow)

        # Load user inputs into symbol table
        for k, v in inputs.items():
            (scope, name) = k.rsplit('.', 1)
            entry = self.symbol_table._get_entry(scope, name)
            wdl_type = entry[4]
            self.symbol_table.set(scope, name, python_to_wdl_value(v, wdl_type))

        # Return error if any inputs are missing
        missing_inputs = self.symbol_table.missing_inputs(workflow)
        if missing_inputs:
            raise MissingInputsException(missing_inputs)

        # Construct the initial execution table
        self.execution_table = ExecutionTable(workflow, self.symbol_table, extra=2)

        print('\n -- symbol table (initial)')
        print(self.symbol_table)
        print('\n -- execution table (initial)')
        print(self.execution_table)

    def execute(self):
        print('\n -- running workflow: {}'.format(self.workflow.name))
        print('\n -- job dir: {}'.format(self.dir))
        os.mkdir(self.dir)

        while not self.execution_table.is_finished():
            for (fqn, status, index, _, _, _) in self.execution_table:
                if status == 'not_started':
                    call = self.symbol_table.resolve_fqn(fqn)

                    skipped = False
                    upstream_calls = call.upstream()
                    for upstream in upstream_calls:
                        upstream_call_status = self.execution_table.aggregate_status(upstream)
                        if upstream_call_status in ['failed', 'error', 'skipped']:
                            self.execution_table.set_status(fqn, None, 'skipped')
                        if upstream_call_status != 'successful':
                            skipped = True
                    if skipped: continue

                    # Build up parameter list for this task
                    parameters = {}
                    for entry in self.symbol_table.get_inputs(fqn):
                        (scope, name, _, value, type, io) = entry
                        scatter_node = call.get_scatter_parent()
                        scatter_vars = [] if scatter_node is None else [scatter_node.item]
                        value = self.symbol_table.eval_entry(entry, scatter_vars, index)
                        parameters[name] = value

                    print('\n -- Running task: {}'.format(colorize(call.name, ansi=26)))
                    job_cwd = os.path.join(self.dir, fqn, str(index) if index is not None else '')
                    os.makedirs(job_cwd)
                    cmd_string = call.task.command.instantiate(parameters, job_cwd)
                    docker = eval(call.task.runtime['docker'].ast, lookup_function(self.symbol_table, call)).value if 'docker' in call.task.runtime else None
                    (pid, rc, stdout, stderr) = self.run_subprocess(cmd_string, docker=docker, cwd=job_cwd)
                    execution_context = ExecutionContext(fqn, call, index, pid, rc, stdout, stderr, job_cwd)
                    self.post_process(execution_context)

            print('\n -- symbols')
            print(self.symbol_table)
            print('\n -- exec table')
            print(self.execution_table)

    def run_subprocess(self, command, docker=None, cwd='.'):
        if docker:
            command = 'docker run -v {}:/root -w /root {} bash -c "{}"'.format(cwd, docker, command)
        print(colorize(command, ansi=9))
        proc = subprocess.Popen(
            command,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            cwd=cwd
        )
        stdout, stderr = proc.communicate()
        print(colorize('rc = {}'.format(proc.returncode), ansi=1 if proc.returncode!=0 else 2))
        with open(os.path.join(cwd, 'stdout'), 'w') as fp:
            fp.write(stdout.strip(' \n'))
        with open(os.path.join(cwd, 'stderr'), 'w') as fp:
            fp.write(stderr.strip(' \n'))
        return (proc.pid, proc.returncode, stdout.strip(' \n'), stderr.strip(' \n'))

    def post_process(self, execution_context):
        status = 'successful' if execution_context.rc == 0 else 'failed'
        self.execution_table.set_status(execution_context.fqn, execution_context.index, status)
        self.execution_table.set_column(execution_context.fqn, execution_context.index, 4, execution_context.pid)
        self.execution_table.set_column(execution_context.fqn, execution_context.index, 5, execution_context.rc)
        if status == 'successful':
            for output in execution_context.call.task.outputs:
                execution_context.type = output.type
                value = eval(output.expression, functions=engine_functions(execution_context))
                if isinstance(value.type, WdlFileType):
                    value = WdlFileValue(os.path.join(execution_context.cwd, value.value))
                self.symbol_table.set(execution_context.call, output.name, value, execution_context.index, io='output')

class ExecutionTable(list):
    def __init__(self, root, symbol_table, extra=0):
        self.__dict__.update(locals())
        self.populate(self.root)
        self.terminal_states = ['successful', 'failed', 'error', 'skipped']
    def is_finished(self):
        return all(map(lambda x: x in self.terminal_states, [entry[1] for entry in self]))
    def populate(self, node=None):
        if isinstance(node, Call):
            index = None
            scatter = node.get_scatter_parent()
            if scatter:
                scattered_item = self.symbol_table.get(scatter, scatter.item)
                if isinstance(scattered_item, WdlArrayValue):
                    for call_output in node.task.outputs:
                        self.symbol_table.set(node, call_output.name, ScatterOutput([WdlUndefined()] * len(scattered_item.value)))
                    for index in range(len(scattered_item.value)):
                        self.add(node.fully_qualified_name, index)
            else:
                self.add(node.fully_qualified_name, None)
        if isinstance(node, Workflow) or isinstance(node, Scatter):
            for element in node.body:
                self.populate(element)
    def contains(self, fqn, index):
        return any(map(lambda x: x[0] == fqn and x[2] == index, self))
    def add(self, fqn, index):
        if not self.contains(fqn, index):
            row = [fqn, 'not_started', index, None]
            row.extend([None]*self.extra)
            self.append(row)
    def set_status(self, fqn, index, status):
        for entry in self:
            if entry[0] == fqn and entry[2] == index:
                entry[1] = status
    def set_column(self, fqn, index, column, value):
        for entry in self:
            if entry[0] == fqn and entry[2] == index:
                entry[column] = value
    def get(self, fqn):
        for entry in self:
            if entry[0] == fqn:
                return entry
    def aggregate_status(self, call_name):
        statuses = []
        for entry in self:
            if entry[0].endswith('.{}'.format(call_name)):
                statuses.append(entry[1])
        # TODO: clean this up?
        if 'failed' in statuses: return 'failed'
        elif 'error' in statuses: return 'error'
        elif 'skipped' in statuses: return 'skipped'
        elif 'not_started' in statuses: return 'not_started'
        return 'successful'
    def __str__(self):
        return md_table(self, ['Name', 'Status', 'Index', 'Iter', 'PID', 'rc'])

class SymbolTable(list):
    def __init__(self, root):
        self.id = 0
        self.root = root
        def populate(node):
            if isinstance(node, Scatter):
                (var, type, flatten_count) = node.get_flatten_count()
                self.append([node.fully_qualified_name, node.item, None, '%flatten:{}:{}'.format(flatten_count, var), type, 'input'])
            if isinstance(node, Scope):
                for decl in node.declarations:
                    if decl.expression.ast is None:
                        value = WdlUndefined()
                    else:
                        value = eval(decl.expression.ast, lookup_function(self, node), engine_functions())
                    self.append([node.fully_qualified_name, decl.name, None, value, decl.type, 'input'])
                for child in node.body:
                    populate(child)
            if isinstance(node, Call):
                for task_input in node.task.inputs:
                    value = '%expr:' + expr_str(node.inputs[task_input.name].ast) if task_input.name in node.inputs else WdlUndefined()
                    self.append([node.fully_qualified_name, task_input.name, None, value, task_input.type, 'input'])
                for task_output in node.task.outputs:
                    value = '%expr:' + expr_str(node.outputs[task_output.name].ast) if task_output.name in node.outputs else WdlUndefined()
                    # TODO: Instead of constructing type like this, do something like parse_type('Array[{}]'.format(...)) ???
                    type = WdlArrayType(task_output.type) if len(re.findall(r'\._s\d+', node.fully_qualified_name)) > 0 else task_output.type
                    self.append([node.fully_qualified_name, task_output.name, None, value, type, 'output'])
        populate(root)

    def set(self, scope, name, value, index=None, io='all'):
        entry = self._get_entry(scope, name, io)
        if index is not None:
            entry[3][index] = value

            # Once the ScatterOutput is fully populated, replace it with a WdlArrayValue
            # TODO: this is probably not very scalable
            if isinstance(entry[3], ScatterOutput):
                if all(map(lambda x: not isinstance(x, WdlUndefined), entry[3])):
                    entry[3] = WdlArrayValue(entry[3][0].type, [x for x in entry[3]])
        else:
            entry[3] = value

    # Get the evaluated value of a parameter
    def get(self, scope, name):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)

        call_fqn = '{}.{}'.format(scope.fully_qualified_name, name)
        call = self.resolve_fqn(call_fqn)
        if isinstance(call, Call):
            return self._get_call_as_object(call_fqn)

        entry = self._get_entry(scope, name)
        if entry is not None:
            return self.eval_entry(entry)
        return WdlUndefined()

    # Traverse scope hierarchy starting from 'scope' until 'name' is found.
    # Returns the scope object where 'name' is defined
    def resolve_name(self, scope, name):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)
        for node in scope_hierarchy(scope):
            for entry in self._get_entries(node):
                if entry[1] == name:
                    return self.resolve_fqn(entry[0])
        return None

    def get_inputs(self, scope):
        return [entry for entry in self._get_entries(scope, io='input')]

    def missing_inputs(self, workflow):
        missing = {}
        for entry in [entry for entry in self if entry[5] == 'input']:
            value = entry[3]
            scope = workflow.get(entry[0])
            optional = False
            if isinstance(scope, Call):
                inputs = {i.name: i for i in scope.task.inputs}
                if entry[1] in inputs:
                    optional = inputs[entry[1]].is_optional()
            if isinstance(value, WdlUndefined) and not optional:
                missing['{}.{}'.format(entry[0], entry[1])] = str(entry[4])
        return missing

    def is_scatter_var(self, call, var):
        if isinstance(call, str): call = self.resolve_fqn(call)
        scatter_node = call.get_scatter_parent()
        if scatter_node is not None and scatter_node.item == var:
            return True
        return False

    def _get_entry(self, scope, name, io='all'):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)
        if io not in ['all', 'input', 'output']: raise Exception('bad value')
        lookup_entry = None
        for entry in self:
            if io != 'all' and io != entry[5]:
                continue
            if entry[0] == scope.fully_qualified_name and entry[1] == name:
                if (lookup_entry is not None and lookup_entry[2] < entry[2]) or lookup_entry is None:
                    lookup_entry = entry
        return lookup_entry

    def _get_entries(self, scope, io='all'):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)
        if io not in ['all', 'input', 'output']: raise Exception('bad value')
        entries = {}
        for entry in self:
            (entry_scope, entry_name, entry_iter, entry_io) = (entry[0], entry[1], entry[2], entry[5])
            if io != 'all' and io != entry_io:
                continue
            if entry_scope == scope.fully_qualified_name:
                key = '{}_{}'.format(entry_name, entry_io)
                if (key in entries and entries[key][2] < entry_iter) or key not in entries:
                    entries[key] = entry
        return list(entries.values())

    def _get_call_as_object(self, scope):
        entries = self._get_entries(scope, io='output')
        values = {e[1]: self.eval_entry(e) for e in entries}
        for k, v in values.items():
            if isinstance(v, WdlUndefined): return WdlUndefined()
        return WdlObject(values)

    def eval_entry(self, entry, scatter_vars=[], index=None):
        value = entry[3]
        scope = self.resolve_fqn(entry[0])
        if isinstance(value, str) and value.startswith('%expr:'):
            expression = parse_expr(value.replace('%expr:', ''))
            return eval(expression.ast, lookup_function(self, scope, scatter_vars, index))
        if isinstance(value, str) and value.startswith('%flatten:'):
            match = re.match('^%flatten:(\d+):(.*)$', value)
            count = int(match.group(1))
            expression = parse_expr(match.group(2))
            value = eval(expression.ast, lookup_function(self, scope, scatter_vars, index))
            if isinstance(value, WdlArrayValue):
                for i in range(count):
                    value = value.flatten()
                return value
            return WdlUndefined()
        if isinstance(value, list):
            for item in value:
                if isinstance(item, WdlUndefined):
                    return WdlUndefined()
        return value

    def resolve_fqn(self, fqn):
        def resolve_fqn_r(node):
            if node.fully_qualified_name == fqn: return node
            resolved = None
            for child in node.body:
                resolved = resolve_fqn_r(child)
                if resolved is not None: break
            return resolved
        return resolve_fqn_r(self.root)

    def __str__(self):
        return md_table(self, ['Scope', 'Name', 'Iter', 'Value', 'Type', 'I/O'])

class CommandPartValue:
    def __init__(self, name, type, value):
        self.__dict__.update(locals())
    def __str__(self):
        return 'CommandPartValue: {} {} = {}'.format(self.type, self.name, self.value)

def run(wdl_file, inputs={}):
    with open(wdl_file) as fp:
        wdl_document = parse_document(fp.read())
    workflow = wdl_document.workflows[0]
    wf_exec = WorkflowExecutor(workflow, inputs)
    wf_exec.execute()
    print('\nWorkflow finished.  Workflow directory is:')
    print(wf_exec.dir)
