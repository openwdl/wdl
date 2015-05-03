import wdl.parser
from copy import deepcopy
import re
import os

class BindingException(Exception): pass
class EvalException(Exception): pass

class Document:
    def __init__(self, tasks, workflows, ast):
        self.__dict__.update(locals())

class Expression:
    def __init__(self, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return expr_str(self.ast) if self.ast else str(None)

class Task:
    def __init__(self, name, command, output_list, runtime, parameter_meta, meta, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return '[Task name={} command={}]'.format(self.name, self.command)

class CommandLine:
    def __init__(self, parts, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return ' '.join([str(part) for part in self.parts])

class RawCommandLine:
    def __init__(self, parts, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return ''.join([str(part) for part in self.parts])

class CommandLineVariable:
    def __init__(self, name, type, prefix, attributes, postfix_qualifier, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return '[CommandLineVariable name={}, type={}, postfix={}]'.format(self.name, self.type, self.postfix_qualifier)

class Type:
    def __init__(self, name, subtypes, ast):
        self.__dict__.update(locals())
    def is_primitive(self):
        return self.name not in ['array', 'map']
    def is_tsv_serializable(self):
        if self.is_primitive():
            return False
        if self.name == 'array' and len(self.subtypes) == 1 and self.subtypes[0].is_primitive():
            return True
        if self.name == 'map' and len(self.subtypes) == 2 and self.subtypes[0].is_primitive() and self.subtypes[1].is_primitive():
            return True
    def is_json_serializable(self):
        if self.is_primitive():
            return False
        return True
    def __str__(self):
        string = self.name
        if self.subtypes and len(self.subtypes):
            string += '[{}]'.format(','.join([str(subtype) for subtype in self.subtypes]))
        return string

# Scope has: body, declarations, parent, prefix, name
class Scope:
    def __init__(self, name, declarations, body):
        self.__dict__.update(locals())
        self.parent = None
        for decl in declarations:
            decl.parent = self
        for element in body:
            element.parent = self
    def get_parents(self):
        def get_parents_r(node):
            if node is None: return []
            r = [node]
            r.extend(get_parents_r(node.parent))
            return r
        return get_parents_r(self)
    def __getattr__(self, name):
        if name == 'fully_qualified_name':
            if self.parent is None:
                return self.name
            return self.parent.fully_qualified_name + '.' + self.name

class Workflow(Scope):
    def __init__(self, name, declarations, body, ast):
        self.__dict__.update(locals())
        super(Workflow, self).__init__(name, declarations, body)
    def get(self, fqn):
        def get_r(node, fqn):
            if node.fully_qualified_name == fqn:
                return node
            for element in node.body:
                if isinstance(element, Scope):
                    sub = get_r(element, fqn)
                    if sub: return sub
        return get_r(self, fqn)

class Call(Scope):
    def __init__(self, task, alias, declarations, inputs, outputs, ast):
        self.__dict__.update(locals())
        super(Call, self).__init__(alias if alias else task.name, declarations, [task])
        for output in task.output_list:
            output.parent = self
        for part in task.command.parts:
            if isinstance(part, CommandLineVariable):
                part.parent = self
    def get_scatter_parent(self, node=None):
        parents = self.get_parents()
        for parent in parents:
            if isinstance(parent, Scatter):
                return parent
    def __self__(self):
        return '[Call alias={}]'.format(self.alias)

class Declaration:
    def __init__(self, name, type, expression, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return '{} {} = {}'.format(self.type, self.name, expr_str(self.expression))

class WhileLoop(Scope):
    def __init__(self, expression, declarations, body, ast):
        self.__dict__.update(locals())
        super(WhileLoop, self).__init__('_w' + str(ast.id), declarations, body)

class Scatter(Scope):
    def __init__(self, item, collection, declarations, body, ast):
        self.__dict__.update(locals())
        super(Scatter, self).__init__('_s' + str(ast.id), declarations, body)
    def get_flatten_count(self):
        # TODO: revisit this algorithm
        count = 0
        collection = self.collection.ast.source_string
        for node in self.get_parents():
            if isinstance(node, Scatter):
                if node.item == collection:
                    collection = node.collection.ast.source_string
                    count += 1
            if isinstance(node, Scope):
                for decl in node.declarations:
                    if decl.name == collection:
                        (var, type) = (decl.name, decl.type)
                        for i in range(count):
                            type = type.subtypes[0]
                        return (var, type, count)

def get_nodes(ast_root, name):
    nodes = []
    if isinstance(ast_root, wdl.parser.AstList):
        for node in ast_root:
            nodes.extend(get_nodes(node, name))
    elif isinstance(ast_root, wdl.parser.Ast):
        if ast_root.name == name:
            nodes.append(ast_root)
        for attr_name, attr in ast_root.attributes.items():
            nodes.extend(get_nodes(attr, name))
    return nodes

def assign_ids(ast_root, id=0):
    if isinstance(ast_root, wdl.parser.AstList):
        ast_root.id = id
        for index, node in enumerate(ast_root):
            assign_ids(node, id+index)
    elif isinstance(ast_root, wdl.parser.Ast):
        ast_root.id = id
        for index, attr in enumerate(ast_root.attributes.values()):
            assign_ids(attr, id+index)
    elif isinstance(ast_root, wdl.parser.Terminal):
        ast_root.id = id

def parse(string):
    ast = wdl.parser.parse(string).ast()
    # TODO: Do further syntax checks
    assign_ids(ast)
    return ast

# Binding functions

def get_tasks(ast):
    return [parse_task(task_ast) for task_ast in get_nodes(ast, 'Task')]

def get_workflows(ast, tasks):
    return [parse_workflow(wf_ast, tasks) for wf_ast in get_nodes(ast, 'Workflow')]

def parse_task(ast):
    name = ast.attr('name').source_string
    command_ast = get_nodes(ast, 'Command')
    if command_ast:
        command = parse_command(command_ast[0])
    else:
        command_ast = get_nodes(ast, 'RawCommand')
        command = parse_raw_command(command_ast[0])
    output_list = [parse_output(output_ast) for output_ast in get_nodes(ast, 'Output')]
    runtime_asts = get_nodes(ast, 'Runtime')
    runtime = parse_runtime(runtime_asts[0]) if len(runtime_asts) else {}
    return Task(name, command, output_list, runtime, {}, {}, ast)

def parse_workflow(ast, tasks):
    body = []
    declarations = []
    name = ast.attr('name').source_string
    for body_ast in ast.attr('body'):
        if body_ast.name == 'Declaration':
            declarations.append(parse_declaration(body_ast))
        else:
            body.append(parse_body_element(body_ast, tasks))
    return Workflow(name, declarations, body, ast)

def parse_runtime(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Runtime':
        raise BindingException('Expecting a "Runtime" AST')
    runtime = {}
    for attr in ast.attr('map'):
        runtime[attr.attr('key').source_string] = Expression(attr.attr('value'))
    return runtime

def parse_declaration(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Declaration':
        raise BindingException('Expecting a "Declaration" AST')
    type = parse_type(ast.attr('type'))
    name = ast.attr('name').source_string
    expression = Expression(ast.attr('expression'))
    return Declaration(name, type, expression, ast)

def parse_body_element(ast, tasks):
    if ast.name == 'Call':
        return parse_call(ast, tasks)
    elif ast.name == 'Workflow':
        return parse_workflow(ast, tasks)
    elif ast.name == 'WhileLoop':
        return parse_while_loop(ast, tasks)
    elif ast.name == 'Scatter':
        return parse_scatter(ast, tasks)
    else:
        raise BindingException("unknown ast: " + ast.name)

def parse_while_loop(ast, tasks):
    expression = Expression(ast.attr('expression'))
    body = []
    declarations = []
    for body_ast in ast.attr('body'):
        if body_ast.name == 'Declaration':
            declarations.append(parse_declaration(body_ast))
        else:
            body.append(parse_body_element(body_ast, tasks))
    return WhileLoop(expression, declarations, body, ast)

def parse_scatter(ast, tasks):
    collection = Expression(ast.attr('collection'))
    item = ast.attr('item').source_string
    body = []
    declarations = []
    for body_ast in ast.attr('body'):
        if body_ast.name == 'Declaration':
            declarations.append(parse_declaration(body_ast))
        else:
            body.append(parse_body_element(body_ast, tasks))
    return Scatter(item, collection, declarations, body, ast)

def parse_call(ast, tasks):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Call':
        raise BindingException('Expecting a "Call" AST')
    task_name = ast.attr('task').source_string
    alias = ast.attr('alias').source_string if ast.attr('alias') else None
    declarations = [parse_declaration(decl_ast) for decl_ast in get_nodes(ast, 'Declaration')]

    task_copy = None
    for task in tasks:
        if task.name == task_name:
            task_copy = deepcopy(task)
    if task_copy is None:
        raise BindingException('Could not find task with name: ' + task_name)

    inputs = {}
    try:
        for mapping in get_nodes(ast, 'Inputs')[0].attr('map'):
            inputs[mapping.attr('key').source_string] = Expression(mapping.attr('value'))
    except IndexError:
        pass

    outputs = {}
    try:
        for mapping in get_nodes(ast, 'Outputs')[0].attr('map'):
            outputs[mapping.attr('key').source_string] = Expression(mapping.attr('value'))
    except IndexError:
        pass

    return Call(task_copy, alias, declarations, inputs, outputs, ast)

def parse_command_variable_attrs(ast):
    attrs = {}
    for x in ast:
        attrs[x.attr('key').source_string] = x.attr('value').source_string
    return attrs

def parse_command_variable(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'CommandParameter':
        raise BindingException('Expecting a "CommandParameter" AST')
    type_ast = ast.attr('type') if ast.attr('type') else wdl.parser.Terminal(wdl.parser.terminals['type'], 'type', 'string', 'fake', ast.attr('name').line, ast.attr('name').col)
    return CommandLineVariable(
        ast.attr('name').source_string,
        parse_type(type_ast),
        ast.attr('prefix').source_string if ast.attr('prefix') else None,
        parse_command_variable_attrs(ast.attr('attributes')),
        ast.attr('postfix').source_string if ast.attr('postfix') else None,
        ast
    )

def parse_command(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Command':
        raise BindingException('Expecting a "Command" AST')
    parts = []
    for node in ast.attr('parts'):
        if isinstance(node, wdl.parser.Terminal):
            part = node.source_string
            if (part[0] == "'" and part[-1] == "'") or (part[0] == '"' and part[-1] == '"'):
                part = part[1:-1]
            parts.append(part)
        if isinstance(node, wdl.parser.Ast) and node.name == 'CommandParameter':
            parts.append(parse_command_variable(node))
    return CommandLine(parts, ast)

def parse_raw_command(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'RawCommand':
        raise BindingException('Expecting a "RawCommand" AST')
    parts = []
    for node in ast.attr('parts'):
        if isinstance(node, wdl.parser.Terminal):
            parts.append(node.source_string)
        if isinstance(node, wdl.parser.Ast) and node.name == 'CommandParameter':
            parts.append(parse_command_variable(node))
    return RawCommandLine(parts, ast)

def parse_output(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Output':
        raise BindingException('Expecting an "Output" AST')
    type = parse_type(ast.attr('type'))
    var = ast.attr('var').source_string
    expression = ast.attr('expression')
    return Declaration(var, type, expression, ast)

def parse_type(ast):
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str != 'type':
            raise BindingException('Expecting an "Type" AST')
        return Type(ast.source_string, None, ast)
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Type':
        raise BindingException('Expecting an "Type" AST')
    name = ast.attr('name').source_string
    subtypes = [parse_type(subtype_ast) for subtype_ast in ast.attr('subtype')]
    return Type(name, subtypes, ast)

def parse_document(string):
    ast = parse(string)
    tasks = get_tasks(ast)
    workflows = get_workflows(ast, tasks)
    return Document(tasks, workflows, ast)

binary_operators = [
    'Add', 'Subtract', 'Multiply', 'Divide', 'Remainder', 'Equals',
    'NotEquals', 'LessThan', 'LessThanOrEqual', 'GreaterThan',
    'GreaterThanOrEqual'
]

unary_operators = [
    'LogicalNot', 'UnaryPlus', 'UnaryMinus'
]

class WdlUndefined:
    def __str__(self):
        return 'undefined'

class WdlObject:
    def set(self, key, value):
        self.__dict__[key] = value
    def get(self, key):
        return self.__dict__[key]
    def __str__(self):
        return str(self.__dict__)

def eval(ast, lookup=lambda var: None, ctx=None):
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str == 'integer':
            return int(ast.source_string)
        elif ast.str == 'string':
            return ast.source_string
        elif ast.str == 'boolean':
            return True if ast.source_string == 'true' else False
        elif ast.str == 'identifier':
            symbol = lookup(ast.source_string)
            if symbol is None:
                return WdlUndefined()
            return symbol
    elif isinstance(ast, wdl.parser.Ast):
        if ast.name in binary_operators:
            lhs = eval(ast.attr('lhs'), lookup, ctx)
            if isinstance(lhs, WdlUndefined): return lhs

            rhs = eval(ast.attr('rhs'), lookup, ctx)
            if isinstance(rhs, WdlUndefined): return rhs

            # TODO: do type checking to make sure running
            # the specified operator on the operands is allowed
            # for now, just assume it is

            if ast.name == 'Add': return lhs + rhs
            if ast.name == 'Subtract': return lhs - rhs
            if ast.name == 'Multiply': return lhs * rhs
            if ast.name == 'Divide': return lhs / rhs
            if ast.name == 'Remainder': return lhs % rhs
            if ast.name == 'Equals': return lhs == rhs
            if ast.name == 'NotEquals': return lhs != rhs
            if ast.name == 'LessThan': return lhs < rhs
            if ast.name == 'LessThanOrEqual': return lhs <= rhs
            if ast.name == 'GreaterThan': return lhs > rhs
            if ast.name == 'GreaterThanOrEqual': return lhs >= rhs
        if ast.name in unary_operators:
            expr = eval(ast.attr('expression'), lookup, ctx)
            if isinstance(expr, WdlUndefined): return expr

            if ast.name == 'LogicalNot': return not expr
            if ast.name == 'UnaryPlus': return +expr
            if ast.name == 'UnaryMinus': return -expr
        if ast.name == 'ObjectLiteral':
            obj = WdlObject()
            for member in ast.attr('map'):
                key = member.attr('key').source_string
                value = eval(member.attr('value'), lookup, ctx)
                if value is None or isinstance(value, WdlUndefined):
                    raise EvalException('Cannot evaluate expression')
                obj.set(key, value)
            return obj
        if ast.name == 'ArrayIndex':
            array = ast.attr('lhs')
            index = eval(ast.attr('rhs'), lookup, ctx)
            raise EvalException('ArrayIndex not implemented yet')
        if ast.name == 'MemberAccess':
            object = eval(ast.attr('lhs'), lookup, ctx)
            member = ast.attr('rhs')

            if isinstance(object, WdlUndefined):
                return object
            if not isinstance(member, wdl.parser.Terminal) or member.str != 'identifier':
                # TODO: maybe enforce this in the grammar?
                raise EvalException('rhs needs to be an identifier')

            member = member.source_string
            return object.get(member)
        if ast.name == 'FunctionCall':
            function = ast.attr('name').source_string
            parameters = [eval(x, lookup, ctx) for x in ast.attr('params')]
            if function == 'strlen' and len(parameters) == 1 and isinstance(parameters[0], str):
                return len(parameters[0])
            if function == 'tsv' and len(parameters) == 1 and isinstance(parameters[0], str):
                return process_tsv(parameters[0], ctx)
            if function in ['read_int', 'read_boolean'] and len(parameters) == 1 and isinstance(parameters[0], str):
                val = process_read(parameters[0], ctx)
                if function == 'read_int':
                    return cast(val, 'int')
                if function == 'read_boolean':
                    return cast(val, 'boolean')
            raise EvalException('Function "{}" is not defined'.format(function))

def process_tsv(file_path, ctx):
    if file_path == 'stdout':
        stdout = ctx.stdout.strip('\n')
        return stdout.split('\n') if len(stdout) else []

def process_read(file_path, ctx):
    with open(os.path.join(ctx.cwd, file_path)) as fp:
        contents = fp.read().strip('\n')
        return contents.split('\n')[0] if len(contents) else []

class CastException: pass

def cast(var, type):
    if str(type) == 'boolean':
        if var not in ['true', 'false']:
            raise CastException('cannot cast {} as {}'.format(var, type))
        return True if var == 'true' else False
    if str(type) == 'int':
        try:
            return int(var)
        except ValueError:
            raise CastException('cannot cast {} as {}'.format(var, type))
    return var

def expr_str(ast):
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str == 'string':
            return '"{}"'.format(ast.source_string)
        return ast.source_string
    elif isinstance(ast, wdl.parser.Ast):
        if ast.name == 'Add':
            return '{}+{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'Subtract':
            return '{}-{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'Multiply':
            return '{}*{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'Divide':
            return '{}/{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'Remainder':
            return '{}%{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'Equals':
            return '{}=={}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'NotEquals':
            return '{}!={}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'LessThan':
            return '{}<{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'LessThanOrEqual':
            return '{}<={}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'GreaterThan':
            return '{}>{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'GreaterThanOrEqual':
            return '{}>={}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'LogicalNot':
            return '!{}'.format(expr_str(ast.attr('expression')))
        if ast.name == 'UnaryPlus':
            return '+{}'.format(expr_str(ast.attr('expression')))
        if ast.name == 'UnaryMinus':
            return '-{}'.format(expr_str(ast.attr('expression')))
        if ast.name == 'FunctionCall':
            return '{}({})'.format(expr_str(ast.attr('name')), ','.join([expr_str(param) for param in ast.attr('params')]))
        if ast.name == 'ArrayIndex':
            return '{}[{}]'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
        if ast.name == 'MemberAccess':
            return '{}.{}'.format(expr_str(ast.attr('lhs')), expr_str(ast.attr('rhs')))
