import wdl.parser
import wdl.util
import os
import json

def parse_document(string, resource):
    ast = parse(string, resource)
    tasks = get_tasks(ast)
    workflows = get_workflows(ast, tasks)
    return WdlDocument(resource, string, tasks, workflows, ast)

def parse(string, resource):
    errors = wdl.parser.DefaultSyntaxErrorHandler()
    tokens = wdl.parser.lex(string, resource, errors)
    ast = wdl.parser.parse(tokens).ast()
    assign_ids(ast)
    return ast

def scope_hierarchy(scope):
    if scope is None: return []
    return [scope] + scope_hierarchy(scope.parent)

class BindingException(Exception): pass
class WdlValueException(Exception): pass
class EvalException(Exception): pass

class WdlDocument:
    def __init__(self, source_location, source_wdl, tasks, workflows, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return '[WdlDocument tasks={} workflows={}]'.format(
            ','.join([t.name for t in self.tasks]),
            ','.join([w.name for w in self.workflows])
        )

class Expression:
    def __init__(self, ast):
        self.__dict__.update(locals())
    def __str__(self):
        return expr_str(self.ast) if self.ast else str(None)

class Task:
    def __init__(self, name, command, outputs, runtime, parameter_meta, meta, ast):
        self.__dict__.update(locals())
    def __getattr__(self, name):
        if name == 'inputs':
            return [part for part in self.command.parts if isinstance(part, TaskVariable)]
    def __str__(self):
        return '[Task name={} command={}]'.format(self.name, self.command)

class CommandLine:
    def __init__(self, parts, ast):
        self.__dict__.update(locals())
    def _stringify(self, wdl_value):
      if isinstance(wdl_value, WdlFileValue) and wdl_value.value[0] != '/':
          return os.path.abspath(wdl_value.value)
      return str(wdl_value.value)

    # TODO: honor lookup_function and wdl_functions
    def instantiate(self, params, lookup_function=None, wdl_functions=None):
        cmd = []
        for part in self.parts:
            if isinstance(part, CommandLineString):
                cmd.append(part.string)
            elif isinstance(part, TaskVariable):
                def lookup(s): return params[s]
                wdl_value = eval(part.expression, lookup, wdl_functions)
                cmd.append(wdl_value)
        return wdl.util.strip_leading_ws(''.join(cmd))
    def __str__(self):
        return wdl.util.strip_leading_ws(''.join([str(part) for part in self.parts]))

class CommandLinePart: pass

# TODO: rename this
class TaskVariable(CommandLinePart):
    def __init__(self, attributes, expression, ast):
        self.__dict__.update(locals())
    def __str__(self):
        attr_string = ', '.join(self.attributes)
        return '${' + '{}{}'.format(attr_string, self.expression) + '}'

class CommandLineString(CommandLinePart):
    def __init__(self, string, terminal):
        self.__dict__.update(locals())
    def __str__(self):
        return self.string

class WdlType: pass

class WdlPrimitiveType(WdlType):
    def __init__(self): pass
    def is_primitive(self): return True
    def is_tsv_serializable(self): return False
    def is_json_serializable(self): return False
    def __str__(self): return repr(self)

class WdlCompoundType(WdlType):
    def is_primitive(self): return False
    def __str__(self): return repr(self)

class WdlBooleanType(WdlPrimitiveType):
    def __repr__(self): return 'Boolean'

class WdlIntegerType(WdlPrimitiveType):
    def __repr__(self): return 'Int'

class WdlFloatType(WdlPrimitiveType):
    def __repr__(self): return 'Float'

class WdlStringType(WdlPrimitiveType):
    def __repr__(self): return 'String'

class WdlFileType(WdlPrimitiveType):
    def __repr__(self): return 'File'

class WdlUriType(WdlPrimitiveType):
    def __repr__(self): return 'Uri'

class WdlArrayType(WdlCompoundType):
    def __init__(self, subtype):
        self.subtype = subtype
    def is_tsv_serializable(self):
        return isinstance(self.subtype, WdlPrimitiveType)
    def is_json_serializable(self):
        return True
    def __repr__(self): return 'Array[{0}]'.format(repr(self.subtype))

class WdlMapType(WdlCompoundType):
    def __init__(self, key_type, value_type):
        self.__dict__.update(locals())
    def __repr__(self): return 'Map[{0}, {1}]'.format(repr(self.key_type), repr(self.value_type))

class WdlObjectType(WdlCompoundType):
    def __repr__(self): return 'Object'

# Scope has: body, declarations, parent, prefix, name
class Scope:
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
    def __init__(self, task, alias, declarations, inputs, outputs, ast):
        self.__dict__.update(locals())
        super(Call, self).__init__(alias if alias else task.name, declarations, [])
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

def get_tasks(ast):
    return [parse_task(task_ast) for task_ast in wdl.find_asts(ast, 'Task')]

def get_workflows(ast, tasks):
    return [parse_workflow(wf_ast, tasks) for wf_ast in wdl.find_asts(ast, 'Workflow')]

def parse_task(ast):
    name = ast.attr('name').source_string
    command_ast = wdl.find_asts(ast, 'RawCommand')
    command = parse_command(command_ast[0])
    outputs = [parse_output(output_ast) for output_ast in wdl.find_asts(ast, 'Output')]
    runtime_asts = wdl.find_asts(ast, 'Runtime')
    runtime = parse_runtime(runtime_asts[0]) if len(runtime_asts) else {}
    return Task(name, command, outputs, runtime, {}, {}, ast)

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
    declarations = [parse_declaration(decl_ast) for decl_ast in wdl.find_asts(ast, 'Declaration')]

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

    outputs = {}
    try:
        for mapping in wdl.find_asts(ast, 'Outputs')[0].attr('map'):
            outputs[mapping.attr('key').source_string] = Expression(mapping.attr('value'))
    except IndexError:
        pass

    return Call(task, alias, declarations, inputs, outputs, ast)

def parse_command_variable_attrs(ast):
    attrs = {}
    for x in ast:
        attrs[x.attr('key').source_string] = x.attr('value').source_string
    return attrs

def parse_command_variable(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'CommandParameter':
        raise BindingException('Expecting a "CommandParameter" AST')
    return TaskVariable(
        parse_command_variable_attrs(ast.attr('attributes')),
        Expression(ast.attr('expr')),
        ast
    )

def parse_command(ast):
    if not isinstance(ast, wdl.parser.Ast) or ast.name != 'RawCommand':
        raise BindingException('Expecting a "RawCommand" AST')
    parts = []
    for node in ast.attr('parts'):
        if isinstance(node, wdl.parser.Terminal):
            parts.append(CommandLineString(node.source_string, node))
        if isinstance(node, wdl.parser.Ast) and node.name == 'CommandParameter':
            parts.append(parse_command_variable(node))
    return CommandLine(parts, ast)

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

class WdlValue:
    def __init__(self, value):
        self.value = value
        self.check_compatible(value)
    def __str__(self):
        return '[{}: {}]'.format(self.type, str(self.value))

class WdlUndefined(WdlValue):
    def __init__(self): self.type = None
    def __repr__(self): return 'WdlUndefined'
    def __str__(self): return repr(self)

class WdlStringValue(WdlValue):
    type = WdlStringType()
    def check_compatible(self, value):
        if not isinstance(value, str):
            raise WdlValueException("WdlStringValue must hold a python 'str'")
    def add(self, wdl_value):
        if isinstance(wdl_value.type, WdlPrimitiveType):
            return WdlStringValue(self.value + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlIntegerValue(WdlValue):
    type = WdlIntegerType()
    def check_compatible(self, value):
        if not isinstance(value, int):
            raise WdlValueException("WdlIntegerValue must hold a python 'int'")
    def add(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType]:
            return WdlIntegerValue(self.value + wdl_value.value)
        if type(wdl_value.type) == WdlFloatType:
            return WdlFloatValue(self.value + wdl_value.value)
        if type(wdl_value.type) in [WdlStringType, WdlFileValue, WdlUriValue]:
            return WdlStringValue(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))
    def subtract(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType]:
            return WdlIntegerValue(self.value - wdl_value.value)
        if type(wdl_value.type) == WdlFloatType:
            return WdlFloatValue(self.value - wdl_value.value)
        raise EvalException("Cannot subtract: {} + {}".format(self.type, wdl_value.type))
    def multiply(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType]:
            return WdlIntegerValue(self.value * wdl_value.value)
        if type(wdl_value.type) == WdlFloatType:
            return WdlFloatValue(self.value * wdl_value.value)
        raise EvalException("Cannot multiply: {} + {}".format(self.type, wdl_value.type))
    def divide(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType, WdlFloatType]:
            return WdlFloatValue(self.value / wdl_value.value)
        raise EvalException("Cannot divide: {} + {}".format(self.type, wdl_value.type))
    def mod(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType]:
            return WdlIntegerValue(self.value % wdl_value.value)
        if type(wdl_value.type) == WdlFloatType:
            return WdlFloatValue(self.value % wdl_value.value)
        raise EvalException("Cannot modulus divide: {} + {}".format(self.type, wdl_value.type))

class WdlBooleanValue(WdlValue):
    type = WdlBooleanType()
    def check_compatible(self, value):
        if not isinstance(value, bool):
            raise WdlValueException("WdlBooleanValue must hold a python 'bool'")
    def add(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType]:
            return WdlIntegerValue(self.value + wdl_value.value)
        if type(wdl_value.type) in [WdlFloatType]:
            return WdlFloatValue(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlFloatValue(WdlValue):
    type = WdlFloatType()
    def check_compatible(self, value):
        if not isinstance(value, float):
            raise WdlValueException("WdlFloatValue must hold a python 'float'")
    def add(self, wdl_value):
        if type(wdl_value.type) in [WdlIntegerType, WdlBooleanType, WdlFloatType]:
            return WdlFloatValue(self.value + wdl_value.value)
        if type(wdl_value.type) in [WdlStringType, WdlFileValue, WdlUriValue]:
            return WdlStringValue(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlFileValue(WdlValue):
    type = WdlFileType()
    def check_compatible(self, value):
        pass # TODO: implement

class WdlUriValue(WdlValue):
    type = WdlUriType()
    def check_compatible(self, value):
        pass # TODO: implement

class WdlArrayValue(WdlValue):
    def __init__(self, subtype, value):
        if not isinstance(value, list):
            raise WdlValueException("WdlArrayValue must be a Python 'list'")
        if not all(type(x.type) == type(subtype) for x in value):
            raise WdlValueException("WdlArrayValue must contain elements of the same type: {}".format(value))
        self.type = WdlArrayType(subtype)
        self.subtype = subtype
        self.value = value
    def flatten(self):
        flat = lambda l: [item for sublist in l for item in sublist.value]
        if not isinstance(self.type.subtype, WdlArrayType):
            raise WdlValueException("Cannot flatten {} (type {})".format(self.value, self.type))
        return WdlArrayValue(self.subtype.subtype, flat(self.value))
    def __str__(self):
        return '[{}: {}]'.format(self.type, ', '.join([str(x) for x in self.value]))

class WdlMapValue(WdlValue):
    def __init__(self, value):
        if not isinstance(value, dict):
            raise WdlValueException("WdlMapValue must be a Python 'dict'")
        if not all(type(x) == WdlPrimitiveType for x in value.keys()):
            raise WdlValueException("WdlMapValue must contain WdlPrimitiveValues keys")
        if not all(type(x) == WdlPrimitiveType for x in value.values()):
            raise WdlValueException("WdlMapValue must contain WdlPrimitiveValues values")
        if not all(type(x) == type(value[0]) for x in value.keys()):
            raise WdlValueException("WdlMapValue must contain keys of the same type: {}".format(value))
        if not all(type(x) == type(value[0]) for x in value.values()):
            raise WdlValueException("WdlMapValue must contain values of the same type: {}".format(value))
        (k, v) = list(value.items())[0]
        self.type = WdlMapType(k.type, v.type)
        self.value = value

class WdlObject(WdlValue):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            self.set(k, v)
    def set(self, key, value):
        self.__dict__[key] = value
    def get(self, key):
        return self.__dict__[key]
    def __str__(self):
        return '[WdlObject: {}]'.format(str(self.__dict__))

def parse_expr(expr_string):
    ctx = wdl.parser.ParserContext(wdl.parser.lex(expr_string, 'string'), wdl.parser.DefaultSyntaxErrorHandler())
    return Expression(wdl.parser.parse_e(ctx).ast())

def python_to_wdl_value(py_value, wdl_type):
    if isinstance(wdl_type, WdlStringType):
        return WdlStringValue(py_value)
    if isinstance(wdl_type, WdlIntegerType):
        return WdlIntegerValue(py_value)
    if isinstance(wdl_type, WdlFloatType):
        return WdlFloatValue(py_value)
    if isinstance(wdl_type, WdlBooleanType):
        return WdlBooleanValue(py_value)
    if isinstance(wdl_type, WdlFileType):
        return WdlFileValue(py_value)
    if isinstance(wdl_type, WdlUriType):
        return WdlUriValue(py_value)
    if isinstance(wdl_type, WdlArrayType):
        if not isinstance(py_value, list):
            raise WdlValueException("{} must be constructed from Python list, got {}".format(wdl_type, py_value))
        members = [python_to_wdl_value(x, wdl_type.subtype) for x in py_value]
        return WdlArrayValue(wdl_type.subtype, members)
    if isinstance(wdl_type, WdlMapType):
        if not isinstance(py_value, list):
            raise WdlValueException("{} must be constructed from Python dict, got {}".format(wdl_type, py_value))
        members = {python_to_wdl_value(k): python_to_wdl_value(v) for k,v in py_value.items()}
        return WdlMapValue(members)

def wdl_value_to_python(wdl_value):
    if isinstance(wdl_value.type, WdlPrimitiveType):
        return wdl_value.value
    if isinstance(wdl_value.type, WdlArrayType):
        return [wdl_value_to_python(x) for x in wdl_value.value]

binary_operators = [
    'Add', 'Subtract', 'Multiply', 'Divide', 'Remainder', 'Equals',
    'NotEquals', 'LessThan', 'LessThanOrEqual', 'GreaterThan',
    'GreaterThanOrEqual'
]

unary_operators = [
    'LogicalNot', 'UnaryPlus', 'UnaryMinus'
]

def eval(ast, lookup=lambda var: None, functions=None):
    if isinstance(ast, Expression): return eval(ast.ast, lookup, functions)
    if isinstance(ast, wdl.parser.Terminal):
        if ast.str == 'integer':
            return WdlIntegerValue(int(ast.source_string))
        if ast.str == 'float':
            return WdlFloatValue(float(ast.source_string))
        elif ast.str == 'string':
            return WdlStringValue(ast.source_string)
        elif ast.str == 'boolean':
            return WdlBooleanValue(True if ast.source_string == 'true' else False)
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

            # TODO: do type checking to make sure running
            # the specified operator on the operands is allowed
            # for now, just assume it is

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
