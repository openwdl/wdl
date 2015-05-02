from wdl.binding import *
import wdl.parser
import re
import subprocess
import tempfile
import uuid
import json
from xtermcolor import colorize

def md_table(table, header):
    max_len = 64
    col_size = [len(x) for x in header]
    def trunc(s):
        return s[:max_len-3] + '...' if len(s) >= max_len else s
    for row in table:
        for index, cell in enumerate(row):
            if len(str(cell)) > col_size[index]:
                col_size[index] = min(len(str(cell)), max_len)
    def make_row(row):
        return '|{}|'.format('|'.join([trunc(str(x)).ljust(col_size[i]) if x is not None else ' ' * col_size[i] for i,x in enumerate(row)]))
    r = make_row(header) + '\n'
    r += '|{}|'.format('|'.join(['-' * col_size[i] for i,x in enumerate(col_size)])) + '\n'
    r += '\n'.join([make_row(x) for x in table])
    return r

class MissingInputsException(Exception):
    def __init__(self, missing):
        self.__dict__.update(locals())

class EngineException(Exception): pass

class ExecutionContext:
    def __init__(self, fqn, call, index, pid, rc, stdout, stderr, cwd):
        self.__dict__.update(locals())

class Job:
    def __init__(self, workflow):
        self.dir = os.path.abspath('workflow_{}_{}'.format(workflow.name, str(uuid.uuid4()).split('-')[0]))
        self.symbol_table = SymbolTable(workflow)
        self.execution_table = ExecutionTable(workflow, self.symbol_table, 2)

class ExecutionTable(list):
    def __init__(self, root, symbol_table, extra=0):
        self.__dict__.update(locals())
        self.populate(self.root)
        self.terminal_states = ['successful', 'failed', 'error', 'skipped']
    def is_finished(self):
        for entry in self:
            if entry[1] not in self.terminal_states:
                return False
        return True
    def populate(self, node=None, iteration=None):
        if node is None: node = self.root
        if isinstance(node, Call):
            index = None
            scatter = node.get_scatter_parent()
            if scatter:
                scattered_item = self.symbol_table.get(self.symbol_table.get_fully_qualified_name(scatter.item, node))
                if isinstance(scattered_item, list):
                    for index in range(len(scattered_item)):
                        self.add(node.fully_qualified_name, index, iteration)
            else:
                self.add(node.fully_qualified_name, None, iteration)
            if iteration is not None:
                for (name, value, type, io) in self.symbol_table.get_iteration_entries_by_prefix(node.fully_qualified_name):
                    iteration_entry = name.replace(node.fully_qualified_name, '{}._i{}'.format(node.fully_qualified_name, iteration))
                    self.symbol_table.append([iteration_entry, value, type, io])
        if isinstance(node, Workflow) or isinstance(node, Scatter):
            for element in node.body:
                self.populate(element, iteration)
        if isinstance(node, WhileLoop):
            self.add(node.fully_qualified_name, None, iteration)
    def contains(self, search_fqn, search_index):
        for (fqn, status, index, iter, _, _) in self:
            if search_fqn == fqn and search_index == index:
                return True
    def add(self, fqn, index, iteration):
        init_iteration = 0 if self.is_loop(fqn) else None
        if iteration is not None:
            fqn = fqn + '._i' + str(iteration)
        if not self.contains(fqn, index):
            row = [fqn, 'not_started', index, init_iteration]
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
    def get_latest_iteration(self, prefix):
        iteration = None
        found = False
        for entry in self:
            if entry[0] == prefix:
                found = True
            if entry[0].startswith(prefix):
                match = re.match(r'{}\._i(\d+)$'.format(prefix), entry[0])
                if match:
                    if iteration is None or int(match.group(1)) > iteration:
                        iteration = int(match.group(1))
        if iteration is not None: return '{}._i{}'.format(prefix, iteration)
        if found: return prefix
        return None
    def count(self, fqn):
        fqn = self.get_latest_iteration(fqn)
        count = 0
        for entry in self:
            if entry[0] == fqn:
                count += 1
        return count
    def is_loop(self, fqn):
        return re.search('_w\d+$', fqn)
    def get(self, fqn):
        for entry in self:
            if entry[0] == fqn:
                return entry
    def loop_iteration_status(self, fqn): # not_started, running, successful, failed
        # TODO: pass in loop object instead of fqn
        if not self.is_loop(fqn):
            raise Exception('Not a loop')
        iteration_fqn = fqn + '.'
        jobs = []
        loop = self.get(fqn)
        for entry in self:
            if entry[0].startswith(iteration_fqn):
                jobs.append(entry)
        if loop[3] == 0 and loop[2] == 'not_started':
            return 'not_started'
        else:
            for job_entry in jobs:
                if job_entry[1] in ['failed', 'skipped', 'error']:
                    return 'failed'
                if job_entry[1] in ['not_started', 'started']:
                    return 'running'
            return 'successful'
    def add_loop_iteration(self, loop):
        fqn = loop.fully_qualified_name
        loop_entry = self.get(fqn)
        loop_entry[3] += 1
        for node in loop.body:
            self.populate(node, iteration=loop_entry[3])
    def __str__(self):
        return md_table(self, ['Name', 'Status', 'Index', 'Iter', 'PID', 'rc'])

class SymbolTable(list):
    def __init__(self, root):
        self.root = root
        # TODO: is prefix needed?
        def populate(node, prefix=None):
            if isinstance(node, Scatter):
                fqn = '{}.{}'.format(node.fully_qualified_name, node.item)
                (var, type, flatten_count) = node.get_flatten_count()
                var = self.get_fully_qualified_name(var, node)
                # TODO: set the type correctly
                if flatten_count == 0:
                    self.append([fqn, '%ref:'+var, type, 'input'])
                else:
                    self.append([fqn, '%flatten:{}:{}'.format(flatten_count, var), type, 'input'])
            if isinstance(node, Scope):
                for decl in node.declarations:
                    self.append(['{}.{}'.format(
                        node.fully_qualified_name, decl.name),
                        eval(decl.expression.ast, lookup_function(self, node)),
                        decl.type,
                        'input'
                    ])
                    # TODO: check that the type matches for above statement
                for element in node.body:
                    populate(element, node.fully_qualified_name)
            if isinstance(node, Task):
                for cmd_part in node.command.parts:
                    if isinstance(cmd_part, CommandLineVariable):
                        self.append(['{}.{}'.format(prefix, cmd_part.name), None, cmd_part.type, 'input'])
                for output in node.output_list:
                    fqn = '{}.{}'.format(prefix, output.name)
                    scatter_output = len(re.findall(r'\._s\d+', fqn)) > 0
                    output_type = output.type
                    if scatter_output:
                        output_type = Type('array', [output.type], output.type.ast)
                    self.append([fqn, None, output_type, 'output'])
            if isinstance(node, Call):
                for input_name, expression in node.inputs.items():
                    input_name = '{}.{}'.format(node.fully_qualified_name, input_name)
                    for index, x in enumerate(self):
                        if x[0] == input_name:
                            if isinstance(expression.ast, wdl.parser.Terminal) and expression.ast.str == 'identifier':
                                self[index][1] = '%ref:' + self.get_fully_qualified_name(expression.ast.source_string, node.parent)
                            else:
                                value = eval(expression.ast, lookup_function(self, node))
                                self[index][1] = value if not isinstance(value, WdlUndefined) else '%expr:' + expr_str(expression.ast)

                for output_name, expression in node.outputs.items():
                    output_name = self.get_fully_qualified_name(output_name, node.parent)
                    reference = self.get_fully_qualified_name(expression.ast.source_string, node)
                    for index, x in enumerate(self):
                        if x[0] == reference:
                            if isinstance(expression.ast, wdl.parser.Terminal) and expression.ast.str == 'identifier':
                                self[index][1] = '%ref:' + output_name
                            else:
                                self[index][1] = eval(expression.ast, lookup_function(self, node))
        populate(root)
    def get_fully_qualified_name(self, var, scope, iteration=None):
        if scope is None:
            return None
        if not isinstance(scope, Scope):
            return self.get_fully_qualified_name(var, scope.parent)
        iteration_str = '._i{}'.format(iteration) if iteration is not None else ''
        fqn = '{}{}.{}'.format(scope.fully_qualified_name, iteration_str, var)
        for entry in self:
            if entry[0] == fqn:
                return fqn
        return self.get_fully_qualified_name(var, scope.parent)
    def is_task(self, prefix, name):
        for entry in self.get_prefix(prefix):
            match = re.match(r'^({}\.(.*?).{})\.([^\.]+)$'.format(prefix, name), entry[0])
            if match:
                return match.group(1)
        return None
    def deref(self, key):
        for entry in self:
            if entry[0] == key:
                if isinstance(entry[1], str) and entry[1].startswith('%ref:'):
                    return self.deref(entry[1].replace('%ref:', ''))
                return key
        return None
    def set(self, key, value, index=None, scatter_count=None):
        key = self.deref(key)
        for entry in self:
            if entry[0] == key:
                if index is not None:
                    if entry[1] is None: entry[1] = [None] * scatter_count
                    entry[1][index] = value
                else:
                    entry[1] = value
                return True
        raise EngineException("Symbol table entry not found: " + str(key))
    def missing_inputs(self):
        missing = {}
        for (name, value, type, io) in self:
            if io == 'input' and value is None:
                missing[name] = str(type)

        if len(missing):
            return missing
        return None
    def is_scatter_var(self, call, var):
        # TODO: this assumes the call can only use the variable from the nearest Scatter parent
        scatter_node = call.get_scatter_parent()
        if scatter_node is None:
            return False
        # Nearest enclosing scatter item
        scatter_item = self.get_fully_qualified_name(scatter_node.item, call)
        if var in call.inputs:
            expr = call.inputs[var].ast
            if isinstance(expr, wdl.parser.Terminal) and expr.str == 'identifier':
                val_fqn = self.get_fully_qualified_name(expr.source_string, call)
                if val_fqn == scatter_item:
                    return val_fqn
        return False
    def get_iteration_entries_by_prefix(self, prefix):
        # TODO: revisit this
        entries = []
        for entry in self:
            if entry[0].startswith(prefix) and '._i' not in entry[0]:
                entries.append(entry)
        return entries
    def get_scope(self, name):
        def all_scopes(root):
            if not isinstance(root, Scope): return []
            scopes = [root]
            for element in root.body:
                scopes.extend(all_scopes(element))
            return scopes
        longest_match = None
        for scope in all_scopes(self.root):
            if re.match(r'^{}'.format(scope.fully_qualified_name), name):
                if longest_match is None or len(scope.fully_qualified_name) > len(longest_match.fully_qualified_name):
                    longest_match = scope
        return longest_match
    def get(self, var, evaluate=True):
        for entry in self:
            (name, value, type, io) = entry
            if name == var:
                if isinstance(value, str) and value.startswith('%ref:'):
                    return self.get(re.sub('^%ref:', '', value))
                if evaluate and isinstance(value, str) and value.startswith('%expr:'):
                    expr_string = re.sub('^%expr:', '', value)
                    tokens = wdl.parser.lex(expr_string, 'string')
                    parser_ctx = wdl.parser.ParserContext(tokens, wdl.parser.DefaultSyntaxErrorHandler(expr_string, 'string'))
                    expr = wdl.parser.parse_e(parser_ctx).ast()
                    scope = self.get_scope(name)
                    # TODO: this is duplicated from post_process
                    try:
                        iteration = re.findall(r'._i(\d+)', var)[-1]
                    except IndexError:
                        iteration = None
                    return eval(expr, lookup_function(self, scope, iteration))
                if isinstance(value, str) and value.startswith('%flatten:'):
                    match = re.match('^%flatten:(\d+):(.*)$', value)
                    count = int(match.group(1))
                    value = self.get(match.group(2))
                    if value:
                        flat = lambda l: [item for sublist in l for item in sublist]
                        for i in range(count):
                            value = flat(value)
                        entry[1] = value
                        return value
                else:
                    return value
        return None
    def get_prefix(self, fqn_prefix, io_type='any', evaluate=False):
        inputs = []
        for (name, value, type, io) in self:
            if name.startswith(fqn_prefix) and (io == io_type or io_type == 'any'):
                inputs.append([name, self.get(name, evaluate), type, io])
        return inputs
    def get_inputs(self, fqn_prefix):
        return self.get_prefix(fqn_prefix, 'input', evaluate=True)
    def get_outputs(self, fqn_prefix):
        return self.get_prefix(fqn_prefix, 'output', evaluate=True)
    def __str__(self):
        return md_table(self, ['Name', 'Value', 'Type', 'I/O'])

def lookup_function(table, scope, iteration=None):
    def lookup(var):
        cscope = scope
        while cscope:
            if not isinstance(cscope, Scope):
                cscope = cscope.parent
                continue
            task_prefix = table.is_task(cscope.fully_qualified_name, var)
            if task_prefix:
                if iteration is not None:
                    task_prefix = task_prefix + '._i' + str(iteration)
                # Return an object with attributes being the outputs of that task
                obj = WdlObject()
                for output in table.get_outputs(task_prefix):
                    value = table.get(output[0])
                    obj.set(re.match(r'.*\.(.*)$', output[0]).group(1), value if value is not None else WdlUndefined())
                return obj
            else:
                cvar = '{}.{}'.format(cscope.fully_qualified_name, var)
                cvar = table.deref(cvar)
                for entry in table:
                    if entry[0] == cvar:
                        return entry[1]
            cscope = cscope.parent
    return lookup

def strip_leading_ws(string):
    string = string.strip('\n').rstrip(' \n')
    ws_count = []
    for line in string.split('\n'):
        match = re.match('^[\ \t]+', line)
        if match:
            ws_count.append(len(match.group(0)))
    if len(ws_count):
        trim_amount = min(ws_count)
        return '\n'.join([line[trim_amount:] for line in string.split('\n')])
    return string

def run_subprocess(command, docker=None, cwd='.'):
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

def post_process(job, execution_context):
    status = 'successful' if execution_context.rc == 0 else 'failed'
    execution_context.fqn = job.execution_table.get_latest_iteration(execution_context.fqn)
    job.execution_table.set_status(execution_context.fqn, execution_context.index, status)
    job.execution_table.set_column(execution_context.fqn, execution_context.index, 4, execution_context.pid)
    job.execution_table.set_column(execution_context.fqn, execution_context.index, 5, execution_context.rc)
    try:
        iteration = re.findall(r'._i(\d+)', execution_context.fqn)[-1]
    except IndexError:
        iteration = None
    if status == 'successful':
        for output in execution_context.call.task.output_list:
            value = eval(output.expression, ctx=execution_context)
            if str(output.type) == 'file':
                value = os.path.join(execution_context.cwd, value)
            job.symbol_table.set(
                job.symbol_table.get_fully_qualified_name(output.name, execution_context.call, iteration),
                value,
                execution_context.index,
                job.execution_table.count(execution_context.fqn)
            )
        for output, expr in execution_context.call.outputs.items():
            output_fqn = job.symbol_table.get_fully_qualified_name(output, execution_context.call)
            output_value = eval(expr.ast, lookup=lookup_function(job.symbol_table, execution_context.call))
            job.symbol_table.set(output_fqn, output_value)

class CommandPartValue:
    def __init__(self, name, type, value):
        self.__dict__.update(locals())
    def __str__(self):
        return 'CommandPartValue: {} {} = {}'.format(self.type, self.name, self.value)

def run(wdl_file, inputs=None):
    with open(wdl_file) as fp:
        wdl_document = parse_document(fp.read())

    workflow = wdl_document.workflows[0]
    job = Job(workflow)
    if inputs:
        for k, v in inputs.items():
            job.symbol_table.set(k, v)
    missing_inputs = job.symbol_table.missing_inputs()
    if missing_inputs:
        raise MissingInputsException(missing_inputs)

    job.execution_table.populate()
    print('\n -- symbols')
    print(job.symbol_table)
    print('\n -- exec table')
    print(job.execution_table)
    print('\n -- job dir')
    print(job.dir)

    os.mkdir(job.dir)

    while not job.execution_table.is_finished():
        print(' -- loop start')
        for (fqn, status, index, iter, _, _) in job.execution_table:
            if job.execution_table.is_loop(fqn):
                loop = workflow.get(fqn)
                iteration_status = job.execution_table.loop_iteration_status(fqn)
                if iteration_status == 'failed':
                    job.execution_table.set_status(fqn, index, 'failed')
                elif iteration_status in ['not_started', 'successful']:
                    while_expr = eval(loop.expression.ast, lookup=lookup_function(job.symbol_table, loop))
                    if while_expr == False:
                        job.execution_table.set_status(fqn, index, 'successful')
                    elif while_expr == True:
                        job.execution_table.add_loop_iteration(loop)
                        job.execution_table.set_status(fqn, index, 'started')
                        print('\n -- exec table (add loop iteration)')
                        print(job.execution_table)
            elif status not in job.execution_table.terminal_states:
                inputs = job.symbol_table.get_inputs(fqn)
                call = workflow.get(re.sub(r'._i\d+$', '', fqn))
                ready = True
                param_dict = {}
                for (name, value, type, io)  in inputs:
                    if value is None or isinstance(value, WdlUndefined):
                        ready = False
                    name = re.sub('^'+fqn+'.', '', name)
                    param_dict[name] = CommandPartValue(name, type, value)
                if ready:
                    print('\n -- run task: {}'.format(colorize(call.name, ansi=26)))
                    job_cwd = os.path.join(job.dir, fqn)
                    if index is not None:
                        job_cwd = os.path.join(job_cwd, str(index))
                    os.makedirs(job_cwd)
                    cmd = []
                    for part in call.task.command.parts:
                        if isinstance(part, str):
                            cmd.append(part)
                        elif isinstance(part, CommandLineVariable):
                            scatter_var = job.symbol_table.is_scatter_var(call, part.name)
                            if scatter_var:
                                value = str(job.symbol_table.get(scatter_var)[index])
                            else:
                                # TODO is part.type compatible with param_dict[part.name].type
                                cmd_value = param_dict[part.name]
                                if cmd_value.type.is_primitive():
                                    if part.postfix_qualifier in ['+', '*']:
                                        value = part.attributes['sep'].join([cmd_value.value] if not isinstance(cmd_value.value, list) else cmd_value.value)
                                    else:
                                        value = str(cmd_value.value)
                                elif cmd_value.type.is_tsv_serializable():
                                    pass
                                elif cmd_value.type.is_json_serializable():
                                    value = os.path.join(job_cwd, cmd_value.name + '.json')
                                    with open(value, 'w') as fp:
                                        fp.write(json.dumps(cmd_value.value))
                            if str(part.type) == 'file' and value[0] != '/':
                                value = os.path.abspath(value)
                            cmd.append(value)
                    cmd_separator = '' if isinstance(call.task.command, RawCommandLine) else ' '
                    cmd_string = strip_leading_ws(cmd_separator.join(cmd))
                    docker = eval(call.task.runtime['docker'].ast, lookup_function(job.symbol_table, call)) if 'docker' in call.task.runtime else None
                    (pid, rc, stdout, stderr) = run_subprocess(cmd_string, docker=docker, cwd=job_cwd)
                    execution_context = ExecutionContext(fqn, call, index, pid, rc, stdout, stderr, job_cwd)
                    post_process(job, execution_context)

        print('\n -- symbols')
        print(job.symbol_table)
        print('\n -- exec table')
        print(job.execution_table)
    print('\nJob finished.  Job directory is:')
    print(job.dir)
