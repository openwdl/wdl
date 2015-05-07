from wdl.binding import *
from wdl.util import *
import wdl.parser
import re
import subprocess
import tempfile
import uuid
import json
from xtermcolor import colorize

def lookup_function(symbol_table, scope, scatter_vars=[], index=None):
    def lookup(var):
        for node in scope_hierarchy(scope):
            val = symbol_table.get(node, var)
            if not isinstance(val, WdlUndefined):
                if var in scatter_vars:
                    return val.value[index]
                return val
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
        if len(parameters) != 1 or not isinstance(parameters[0], WdlStringValue):
            raise EvalException("tsv() expects one string parameter")
        file_path = parameters[0].value
        if file_path == 'stdout':
            stdout = execution_context.stdout.strip('\n')
            lines = stdout.split('\n') if len(stdout) else []
            lines = [WdlStringValue(x) for x in lines]
            return WdlArrayValue(lines)

    def read_int(parameters):
        if len(parameters) != 1 or not isinstance(parameters[0], WdlStringValue):
            raise EvalException("read_int() expects one string parameter")
        file_path = parameters[0].value
        with open(os.path.join(execution_context.cwd, file_path)) as fp:
            contents = fp.read().strip('\n')
            if len(contents):
                return WdlIntegerValue(int(contents.split('\n')[0]))
        raise EvalException("read_int(): empty file found")

    def read_boolean(parameters):
        if len(parameters) != 1 or not isinstance(parameters[0], WdlStringValue):
            raise EvalException("read_boolean() expects one string parameter")
        file_path = parameters[0].value
        with open(os.path.join(execution_context.cwd, file_path)) as fp:
            contents = fp.read().strip('\n')
            if len(contents):
                line = contents.split('\n')[0].lower()
                return WdlBooleanValue(True if line in ['1', 'true'] else False)
        raise EvalException("read_boolean(): empty file found")

    def strlen(parameters):
        return WdlIntegerValue(len(parameters[0].value))

    def get_function(name):
        if name == 'tsv': return tsv
        elif name == 'read_int': return read_int
        elif name == 'read_boolean': return read_boolean
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
        missing_inputs = self.symbol_table.missing_inputs()
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

                    # Build up parameter list for this task
                    parameters = {}
                    for entry in self.symbol_table.get_inputs(fqn):
                        (scope, name, _, value, type, io) = entry
                        scatter_node = call.get_scatter_parent()
                        scatter_vars = [] if scatter_node is None else [scatter_node.item]
                        value = self.symbol_table.eval_entry(entry, scatter_vars, index)
                        parameters[name] = value

                    # Do not run if any inputs are WdlUndefined
                    if any(map(lambda x: isinstance(x, WdlUndefined), parameters.values())):
                        print('\n -- Skipping task "{}": some inputs not defined'.format(call.name))
                        continue

                    print('\n -- running task: {}'.format(colorize(call.name, ansi=26)))
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
                value = eval(output.expression, functions=engine_functions(execution_context))
                if isinstance(value.type, WdlFileType):
                    value = WdlFileValue(os.path.join(execution_context.cwd, value.value))
                self.symbol_table.set(execution_context.call, output.name, value, execution_context.index)

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
                    self.append([node.fully_qualified_name, decl.name, None, eval(decl.expression.ast, lookup_function(self, node), engine_functions()), decl.type, 'input'])
                for child in node.body: populate(child)
            if isinstance(node, Call):
                for task_input in node.task.inputs:
                    value = '%expr:' + expr_str(node.inputs[task_input.name].ast) if task_input.name in node.inputs else WdlUndefined()
                    self.append([node.fully_qualified_name, task_input.name, None, value, task_input.type, 'input'])
                for task_output in node.task.outputs:
                    value = '%expr:' + expr_str(node.outputs[task_input.name].ast) if task_input.name in node.outputs else WdlUndefined()
                    # TODO: Instead of constructing type like this, do something like parse_type('Array[{}]'.format(...)) ???
                    type = WdlArrayType(task_output.type) if len(re.findall(r'\._s\d+', node.fully_qualified_name)) > 0 else task_output.type
                    self.append([node.fully_qualified_name, task_output.name, None, value, type, 'output'])
        populate(root)

    def set(self, scope, name, value, index=None):
        entry = self._get_entry(scope, name)
        if index is not None:
            entry[3][index] = value

            # Once the ScatterOutput is fully populated, replace it with a WdlArrayValue
            # TODO: this is probably not very scalable
            if isinstance(entry[3], ScatterOutput):
                if all(map(lambda x: not isinstance(x, WdlUndefined), entry[3])):
                    entry[3] = WdlArrayValue([x for x in entry[3]])
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
        return [entry for entry in self._get_entries(scope) if entry[5] == 'input']

    def missing_inputs(self):
        missing = {}
        for entry in [entry for entry in self if entry[5] == 'input']:
            value = self.eval_entry(entry)
            if isinstance(value, WdlUndefined):
                missing['{}.{}'.format(entry[0], entry[1])] = entry[4]

    def is_scatter_var(self, call, var):
        if isinstance(call, str): call = self.resolve_fqn(call)
        scatter_node = call.get_scatter_parent()
        if scatter_node is not None and scatter_node.item == var:
            return True
        return False

    def _get_entry(self, scope, name):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)
        lookup_entry = None
        for entry in self:
            if entry[0] == scope.fully_qualified_name and entry[1] == name:
                if (lookup_entry is not None and lookup_entry[2] < entry[2]) or lookup_entry is None:
                    lookup_entry = entry
        return lookup_entry

    def _get_entries(self, scope):
        if isinstance(scope, str): scope = self.resolve_fqn(scope)
        entries = {}
        for entry in self:
            (entry_scope, entry_name, entry_iter) = (entry[0], entry[1], entry[2])
            if entry_scope == scope.fully_qualified_name:
                if ((entry_name in entries and entries[entry_name][2] < entry_iter) or entry_name not in entries):
                    entries[entry_name] = entry
        return list(entries.values())

    def _get_call_as_object(self, scope):
        entries = self._get_entries(scope)
        entries = list(filter(lambda x: x[5] == 'output', entries))
        values = {e[1]: self.eval_entry(e[3]) for e in entries}
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
