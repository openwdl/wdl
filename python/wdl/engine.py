from wdl.binding import *
from wdl.util import *
import re
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ETree
import time
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

class LocalProcState:
    def __init__(self, pid, cwd, outputs, proc):
        self.__dict__.update(locals())

class SGEProcState:
    def __init__(self, pid, cwd, outputs, retcode, status_file):
        self.__dict__.update(locals())

class SGERunner:
    def __init__(self, min_refresh_seconds=1):
        self.__dict__.update(locals())
        self.last_state_refresh = None
        self.pid_to_state = {}

    # TODO: this state should probably live in execution table, not in runner
    def get_cwd(self, pid):
        return self.pid_to_state[pid].cwd

    def run(self, cmd_string, docker, cwd):
        if docker:
            cmd_string = 'docker run -v {}:/root -w /root {} bash -c "{}"'.format(cwd, docker, cmd_string)

        # TODO: previously these files were having trailing whitespace stripped when written.  Need to move that to when they're read
        stdout_path = os.path.join(cwd, 'stdout')
        stderr_path = os.path.join(cwd, 'stderr')
        status_file = os.path.join(cwd, 'status')

        print(colorize(cmd_string, ansi=9))
        with tempfile.NamedTemporaryFile(prefix="command", suffix=".sh", dir=cwd, delete=False,mode='w+t') as fd:
            script_name = fd.name
            fd.write("#!/bin/sh\n")
            fd.write(cmd_string)
            fd.write("\necho $? > {}\n".format(status_file))

        job_name = "job"

        cmd = ["qsub", "-N", job_name, "-V", "-b", "n", "-cwd", "-o", stdout_path, "-e", stderr_path, script_name]
        print(colorize("executing qsub command: {}".format(" ".join(cmd)), ansi=9))
        handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=cwd)
        stdout, stderr = handle.communicate()
        stdout = stdout.decode("utf-8")

        bjob_id_pattern = re.compile("Your job (\\d+) \\(.* has been submitted.*")
        sge_job_id = None
        for line in stdout.split("\n"):
            m = bjob_id_pattern.match(line)
            if m != None:
                sge_job_id = m.group(1)

        if sge_job_id == None:
            raise Exception("Could not parse output from qsub: %s" % stdout)


        print(colorize("Started as SGE job {}".format(sge_job_id), ansi=9))
        self.pid_to_state[sge_job_id] = SGEProcState(sge_job_id, cwd, (stdout_path, stderr_path), None, status_file)
        return sge_job_id

    def _get_job_states(self):
        handle = subprocess.Popen(["qstat", "-xml"], stdout=subprocess.PIPE)
        stdout, stderr = handle.communicate()

        doc = ETree.fromstring(stdout)
        job_list = doc.findall(".//job_list")

        active_jobs = {}
        for job in job_list:
            job_id = job.find("JB_job_number").text

            state = job.attrib['state']
            if state == "running":
                active_jobs[job_id] = "running"
            elif state == "pending":
                active_jobs[job_id] = "pending"
            else:
                active_jobs[job_id] = "queued-unknown"
        return active_jobs

    def _update_job_states(self):
        unseen = set(self.pid_to_state.keys())
        active_jobs = self._get_job_states()
        for job_id, state in active_jobs.items():
            if not job_id in self.pid_to_state:
                continue
            state = self.pid_to_state[job_id]
            state.status = state
            unseen.remove(job_id)

        # those jobs which are not in the qstat output have either succeeded or failed
        # look on the filesystem for status file which should be there if successful
        for job_id in unseen:
            state = self.pid_to_state[job_id]
            with open(state.status_file, "rt") as fd:
                retcode = int(fd.read().strip())
            if retcode == 0:
                state.status = "successful"
            else:
                state.status = "failed"
            state.retcode = retcode

        self.last_state_refresh = time.time()

    def get_rc(self, pid):
        now = time.time()
        if self.last_state_refresh is None or now - self.last_state_refresh > self.min_refresh_seconds:
            self._update_job_states()
        return self.pid_to_state[pid].retcode

    def get_outputs(self, pid):
        return [open(x).read() for x in self.pid_to_state[pid].outputs]
    

class LocalRunner:
    def __init__(self):
        self.pid_to_state = {}
    
    # TODO: this state should probably live in execution table, not in runner
    def get_cwd(self, pid):
        return self.pid_to_state[pid].cwd
        
    def run(self, cmd_string, docker, cwd):
        if docker:
            cmd_string = 'docker run -v {}:/root -w /root {} bash -c "{}"'.format(cwd, docker, cmd_string)

        # TODO: previously these files were having trailing whitespace stripped when written.  Need to move that to when they're read
        stdout_path = os.path.join(cwd, 'stdout')
        stderr_path = os.path.join(cwd, 'stderr')
        stdout_file = open(stdout_path, 'w')
        stderr_file = open(stderr_path, 'w')
            
        print(colorize(cmd_string, ansi=9))
        proc = subprocess.Popen(
            cmd_string,
            shell=True,
            universal_newlines=True,
            stdout=stdout_file,
            stderr=stderr_file,
            close_fds=True,
            cwd=cwd
        )

        pid = proc.pid
        print(colorize("Started as pid {}".format(pid), ansi=9))
        self.pid_to_state[pid] = LocalProcState(pid, cwd, (stdout_path, stderr_path), proc)
        return pid

    def get_rc(self, pid):
        proc = self.pid_to_state[pid].proc
        return proc.poll()

    def get_outputs(self, pid):
        outputs = self.pid_to_state[pid].outputs
        return [open(x).read() for x in outputs]

class WorkflowExecutor:
    def __init__(self, workflow, inputs, runner):
        self.dir = os.path.abspath('workflow_{}_{}'.format(workflow.name, str(uuid.uuid4()).split('-')[0]))
        self.workflow = workflow
        self.inputs = inputs
        self.runner = runner

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

    def _execute_next(self, ):
        updates = 0
        
        for (fqn, status, index, _, _, _) in self.execution_table:
            if status == 'not_started':
                call = self.symbol_table.resolve_fqn(fqn)

                skipped = False
                upstream_calls = call.upstream()
                print ("fqn {} upstream {}".format(fqn, upstream_calls))
                for upstream in upstream_calls:
                    upstream_call_status = self.execution_table.aggregate_status(upstream)
                    print ("upstream {} status {}".format(upstream, upstream_call_status))
                    if upstream_call_status in ['failed', 'error', 'skipped', 'started']:
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
                pid = self.runner.run(cmd_string, docker=docker, cwd=job_cwd)
                self.execution_table.set_status(fqn, index, "started")
                self.execution_table.set_column(fqn, index, 4, pid)
                updates += 1
                
        return updates
        
    def _post_process_next(self):
        updates = 0
        
        for (fqn, status, index, _, pid, _) in self.execution_table:
            if status == "started":
                rc = self.runner.get_rc(pid)
                if rc == None: # still running
                    continue
                
                stdout, stderr = self.runner.get_outputs(pid)
                job_cwd = self.runner.get_cwd(pid)
                call = self.symbol_table.resolve_fqn(fqn)
                execution_context = ExecutionContext(fqn, call, index, pid, rc, stdout, stderr, job_cwd)
                self.post_process(execution_context)
                updates += 1

        return updates

    def execute(self, max_sleep_secs=30):
        print('\n -- running workflow: {}'.format(self.workflow.name))
        print('\n -- job dir: {}'.format(self.dir))
        os.mkdir(self.dir)

        sleep_secs = 1
        while not self.execution_table.is_finished():
            updates = 0
            
            updates += self._execute_next()
            updates += self._post_process_next()
            print('\n -- symbols')
            print(self.symbol_table)
            print('\n -- exec table')
            print(self.execution_table)

            if updates == 0:
                print("\n {} sleeping for {} seconds\n".format(time.asctime(), sleep_secs))
                time.sleep(sleep_secs)
                # backoff polling frequency if nothing has changed
                sleep_secs = min(max_sleep_secs, sleep_secs * 2)
            else:
                sleep_secs = 1

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
        elif 'started' in statuses: return 'started'
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

def run(wdl_file, run_service_name="local", inputs={}):
    with open(wdl_file) as fp:
        wdl_document = parse_document(fp.read(), wdl_file)

    workflow = wdl_document.workflows[0]
    runner = {"local": LocalRunner, "sge": SGERunner}[run_service_name]
    wf_exec = WorkflowExecutor(workflow, inputs, runner())
    wf_exec.execute()
    print('\nWorkflow finished.  Workflow directory is:')
    print(wf_exec.dir)
