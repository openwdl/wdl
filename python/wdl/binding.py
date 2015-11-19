import wdl.parser
import wdl.util
from wdl.types import *
from wdl.values import *
import os
import json
import re

def scope_hierarchy(scope):
    if scope is None: return []
    return [scope] + scope_hierarchy(scope.parent)

class BindingException(Exception): pass
class TaskNotFoundException(Exception): pass
class WdlValueException(Exception): pass
class EvalException(Exception): pass

class FullyQualifiedName(object):
    def __init__(self, fqn, namespace):
        self.__dict__.update(locals())
    def __str__(self):
        return '[FullyQualifiedName: {}, {}]'.format(self.fqn, str(namespace))

class WdlNamespace(object):
    def __init__(self, source_location, source_wdl, tasks, workflows, ast):
        self.__dict__.update(locals())
    def task(self, name):
        for task in self.tasks:
            if task.name == name: return task
        raise TaskNotFoundException("Could not find task with name {}".format(name))
    def resolve(self, fqn):
        # TODO: finish
        try:
            (name, sub_fqn) = fqn.split('.', 1)
        except ValueError:
            (name, sub_fqn) = (fqn, '')

        for task in tasks:
            if task.name == name and sub_fqn == '': return FullyQualifiedName(fqn, task)
            if workflow.name == name and sub_fqn == '': return FullyQualifiedName(fqn, workflow)
    def __str__(self):
        return '[WdlNamespace tasks={} workflows={}]'.format(
            ','.join([t.name for t in self.tasks]),
            ','.join([w.name for w in self.workflows])
        )

class Expression(object):
    def __init__(self, ast):
        self.__dict__.update(locals())
    def eval(self, lookup=lambda var: None, functions=None):
        return eval(self.ast, lookup, functions)
    def wdl_string(self):
        return expr_str(self.ast) if self.ast else str(None)
    def __str__(self):
        return '[Expression {}]'.format(self.wdl_string())

class Task(object):
    def __init__(self, name, declarations, command, outputs, runtime, parameter_meta, meta, ast):
        self.__dict__.update(locals())
    def __getattr__(self, name):
        if name == 'inputs':
            return [decl for decl in self.declarations if decl.expression is not None]
    def __str__(self):
        return '[Task name={}]'.format(self.name)

class Command(object):
    def __init__(self, parts, ast):
        self.__dict__.update(locals())
    def instantiate(self, lookup_function=None, wdl_functions=None):
        cmd = []
        for part in self.parts:
            if isinstance(part, CommandString):
                cmd.append(part.string)
            elif isinstance(part, CommandExpressionTag):
                value = part.expression.eval(lookup_function, wdl_functions)
                if isinstance(value, WdlValue) and isinstance(value.type, WdlPrimitiveType):
                    value = value.as_string()
                elif isinstance(value, WdlArray) and isinstance(value.subtype, WdlPrimitiveType) and 'sep' in part.attributes:
                    value = parts.attributes['sep'].join(x.as_string() for x in value)
                else:
                    raise EvalException('Could not string-ify: {}'.format(value))
                cmd.append(value)
        return wdl.util.strip_leading_ws(''.join(cmd))
    def wdl_string(self):
        return wdl.util.strip_leading_ws(''.join([part.wdl_string() for part in self.parts]))
    def __str__(self):
        return '[Command: {}]'.format(self.wdl_string().replace('\n', '\\n').replace('\r', '\\r'))

class CommandPart: pass

class CommandExpressionTag(CommandPart):
    def __init__(self, attributes, expression, ast):
        self.__dict__.update(locals())
    def wdl_string(self):
        attr_string = ', '.join(self.attributes)
        return '${' + '{}{}'.format(attr_string, self.expression.wdl_string()) + '}'
    def __str__(self):
        return '[CommandExpressionTag: {}]'.format(self.wdl_string())

class CommandString(CommandPart):
    def __init__(self, string, terminal):
        self.__dict__.update(locals())
    def wdl_string(self):
        return self.string
    def __str__(self):
        return '[CommandString: {}]'.format(self.string)

# Scope has: body, declarations, parent, prefix, name
class Scope(object):
    def __init__(self, name, declarations, body):
        self.__dict__.update(locals())
        self.parent = None
        for element in body:
            element.parent = self
    def __getattr__(self, name):
        if name == 'fully_qualified_name':
            if self.parent is None:
                return self.name
            return self.parent.fully_qualified_name + '.' + self.name
    def calls(self):
        def calls_r(node):
            if isinstance(node, Call):
                return [node]
            if isinstance(node, Scope):
                call_list = []
                for element in node.body:
                    call_list.extend(calls_r(element))
                return call_list
        return calls_r(self)

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
    def __init__(self, task, alias, inputs, ast):
        self.__dict__.update(locals())
        super(Call, self).__init__(alias if alias else task.name, [], [])
    def upstream(self):
        # TODO: this assumes MemberAccess always refers to other calls
        up = []
        for expression in self.inputs.values():
            for node in wdl.find_asts(expression.ast, "MemberAccess"):
                up.append(node.attr('lhs').source_string)
        return up
    def get_scatter_parent(self, node=None):
        for parent in scope_hierarchy(self):
            if isinstance(parent, Scatter):
                return parent
    def __self__(self):
        return '[Call alias={}]'.format(self.alias)

class Declaration(object):
    def __init__(self, name, type, expression, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return '[Declaration type={}, name={}, expr={}]'.format(self.type, self.name, expr_str(self.expression))
    def wdl_string(self):
        return '{} {}{}'.format(self.type.wdl_string(), self.name, ' = {}'.format(self.expression.wdl_string()) if self.expression else '')

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
        for node in scope_hierarchy(self):
            if isinstance(node, Scatter):
                if node.item == collection:
                    collection = node.collection.ast.source_string
                    count += 1
            if isinstance(node, Scope):
                for decl in node.declarations:
                    if decl.name == collection:
                        (var, type) = (decl.name, decl.type)
                        for i in range(count):
                            type = type.subtype
                        return (var, type, count)

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

# Binding functions

def parse_namespace(string, resource):
    errors = wdl.parser.DefaultSyntaxErrorHandler()
    tokens = wdl.parser.lex(string, resource, errors)
    ast = wdl.parser.parse(tokens).ast()
    assign_ids(ast)
    tasks = [parse_task(task_ast) for task_ast in wdl.find_asts(ast, 'Task')]
    workflows = [parse_workflow(wf_ast, tasks) for wf_ast in wdl.find_asts(ast, 'Workflow')]
    return WdlNamespace(resource, string, tasks, workflows, ast)

def parse_task(ast):
    name = ast.attr('name').source_string
    declarations = [parse_declaration(d) for d in ast.attr('declarations')]
    command_ast = wdl.find_asts(ast, 'RawCommand')
    command = parse_command(command_ast[0])
    outputs = [parse_output(output_ast) for output_ast in wdl.find_asts(ast, 'Output')]
    runtime_asts = wdl.find_asts(ast, 'Runtime')
    runtime = parse_runtime(runtime_asts[0]) if len(runtime_asts) else {}
    return Task(name, declarations, command, outputs, runtime, {}, {}, ast)

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
    expression = Expression(ast.attr('expression')) if ast.attr('expression') else None
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

    for task in tasks:
        if task.name == task_name:
            break

    if task is None:
        raise BindingException('Could not find task with name: ' + task_name)

    inputs = {}
    try:
        for mapping in wdl.find_asts(ast, 'Inputs')[0].attr('map'):
            inputs[mapping.attr('key').source_string] = Expression(mapping.attr('value'))
    except IndexError:
        pass

    return Call(task, alias, inputs, ast)

def parse_command_line_expr_attrs(ast):
    attrs = {}
    for x in ast:
        attrs[x.attr('key').source_string] = x.attr('value').source_string
    return attrs

def parse_command_line_expr(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'CommandParameter':
        raise BindingException('Expecting a "CommandParameter" AST')
    return CommandExpressionTag(
        parse_command_line_expr_attrs(ast.attr('attributes')),
        Expression(ast.attr('expr')),
        ast
    )

def parse_command(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'RawCommand':
        raise BindingException('Expecting a "RawCommand" AST')
    parts = []
    for node in ast.attr('parts'):
        if isinstance(node, wdl.parser.Terminal):
            parts.append(CommandString(node.source_string, node))
        if isinstance(node, wdl.parser.Ast) and node.name == 'CommandParameter':
            parts.append(parse_command_line_expr(node))
    return Command(parts, ast)

def parse_output(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'Output':
        raise BindingException('Expecting an "Output" AST')
    type = parse_type(ast.attr('type'))
    var = ast.attr('var').source_string
    expression = Expression(ast.attr('expression'))
    return Declaration(var, type, expression, ast)

def parse_type(ast):
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str != 'type':
            raise BindingException('Expecting an "Type" AST')
        if ast.source_string == 'Int': return WdlIntegerType()
        elif ast.source_string == 'Boolean': return WdlBooleanType()
        elif ast.source_string == 'Float': return WdlFloatType()
        elif ast.source_string == 'String': return WdlStringType()
        elif ast.source_string == 'File': return WdlFileType()
        elif ast.source_string == 'Uri': return WdlUriType()
        else: raise BindingException("Unsupported Type: {}".format(ast.source_string))
    elif isinstance(ast, wdl.parser.Ast) and ast.name == 'Type':
        name = ast.attr('name').source_string
        if name == 'Array':
            subtypes = ast.attr('subtype')
            if len(subtypes) != 1:
                raise BindingException("Expecting only one subtype AST")
            return WdlArrayType(parse_type(subtypes[0]))
        if name == 'Map':
            subtypes = ast.attr('subtype')
            if len(subtypes) != 2:
                raise BindingException("Expecting only two subtype AST")
            return WdlMapType(parse_type(subtypes[0]), parse_type(subtypes[1]))
    else:
        raise BindingException('Expecting an "Type" AST')

def python_to_wdl_value(py_value, wdl_type):
    if isinstance(wdl_type, WdlStringType):
        return WdlString(py_value)
    if isinstance(wdl_type, WdlIntegerType):
        return WdlInteger(py_value)
    if isinstance(wdl_type, WdlFloatType):
        return WdlFloat(py_value)
    if isinstance(wdl_type, WdlBooleanType):
        return WdlBoolean(py_value)
    if isinstance(wdl_type, WdlFileType):
        return WdlFile(py_value)
    if isinstance(wdl_type, WdlUriType):
        return WdlUri(py_value)
    if isinstance(wdl_type, WdlArrayType):
        if not isinstance(py_value, list):
            raise WdlValueException("{} must be constructed from Python list, got {}".format(wdl_type, py_value))
        members = [python_to_wdl_value(x, wdl_type.subtype) for x in py_value]
        return WdlArray(wdl_type.subtype, members)
    if isinstance(wdl_type, WdlMapType):
        if not isinstance(py_value, list):
            raise WdlValueException("{} must be constructed from Python dict, got {}".format(wdl_type, py_value))
        members = {python_to_wdl_value(k): python_to_wdl_value(v) for k,v in py_value.items()}
        return WdlMap(members)

binary_operators = [
    'Add', 'Subtract', 'Multiply', 'Divide', 'Remainder', 'Equals',
    'NotEquals', 'LessThan', 'LessThanOrEqual', 'GreaterThan',
    'GreaterThanOrEqual'
]

unary_operators = [
    'LogicalNot', 'UnaryPlus', 'UnaryMinus'
]

def interpolate(string, lookup, functions):
    print('interpolate start', string)
    for expr_string in re.findall(r'\$\{.*?\}', string):
        expr = wdl.parse_expr(expr_string[2:-1])
        value = expr.eval(lookup, functions)
        string = string.replace(expr_string, value.as_string())
    print('interpolate end', string)
    return string

def eval(ast, lookup=lambda var: None, functions=None):
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str == 'integer':
            return WdlInteger(int(ast.source_string))
        if ast.str == 'float':
            return WdlFloat(float(ast.source_string))
        elif ast.str == 'string':
            return WdlString(interpolate(ast.source_string, lookup, functions))
        elif ast.str == 'boolean':
            return WdlBoolean(True if ast.source_string == 'true' else False)
        elif ast.str == 'identifier':
            symbol = lookup(ast.source_string)
            if symbol is None:
                return WdlUndefined()
            return symbol
    elif isinstance(ast, wdl.parser.Ast):
        if ast.name in binary_operators:
            lhs = eval(ast.attr('lhs'), lookup, functions)
            if isinstance(lhs, WdlUndefined): return lhs

            rhs = eval(ast.attr('rhs'), lookup, functions)
            if isinstance(rhs, WdlUndefined): return rhs

            if ast.name == 'Add': return lhs.add(rhs)
            if ast.name == 'Subtract': return lhs.subtract(rhs)
            if ast.name == 'Multiply': return lhs.multiply(rhs)
            if ast.name == 'Divide': return lhs.divide(rhs)
            if ast.name == 'Remainder': return lhs.mod(rhs)
            if ast.name == 'Equals': return lhs.is_equal(rhs)
            if ast.name == 'NotEquals': return not lhs.is_equal(rhs)
            if ast.name == 'LessThan': return lhs.less_than(rhs)
            if ast.name == 'LessThanOrEqual': return lhs.less_than(rhs) or lhs.is_equal(rhs)
            if ast.name == 'GreaterThan': return lhs.greater_than(rhs)
            if ast.name == 'GreaterThanOrEqual': return lhs.greater_than(rhs) or lhs.is_equal(rhs)
        if ast.name in unary_operators:
            expr = eval(ast.attr('expression'), lookup, functions)
            if isinstance(expr, WdlUndefined): return expr

            if ast.name == 'LogicalNot': return not expr
            if ast.name == 'UnaryPlus': return +expr
            if ast.name == 'UnaryMinus': return -expr
        if ast.name == 'ObjectLiteral':
            obj = WdlObject()
            for member in ast.attr('map'):
                key = member.attr('key').source_string
                value = eval(member.attr('value'), lookup, functions)
                if value is None or isinstance(value, WdlUndefined):
                    raise EvalException('Cannot evaluate expression')
                obj.set(key, value)
            return obj
        if ast.name == 'ArrayIndex':
            array = ast.attr('lhs')
            index = eval(ast.attr('rhs'), lookup, functions)
            raise EvalException('ArrayIndex not implemented yet')
        if ast.name == 'MemberAccess':
            object = eval(ast.attr('lhs'), lookup, functions)
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
            parameters = [eval(x, lookup, functions) for x in ast.attr('params')]
            return functions(function)(parameters)

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
