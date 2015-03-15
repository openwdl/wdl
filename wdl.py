import sys
import json
import hermes

with open('wdl2.hgr') as fp:
    wdl2_parser = hermes.compile(fp.read())

container_types = ['array', 'set']
primitive_types = ['int', 'string', 'uri', 'file']
all_types = container_types + primitive_types

class cli_param_type:
    def __init__(self, type_name, sub_type=None):
        self.__dict__.update(locals())
        if type_name not in all_types:
            raise wdl2_parser.SyntaxError('{0} is not a valid type'.format(type))
        if sub_type is not None and type_name not in container_types:
            raise wdl2_parser.SyntaxError('{0}[{1}] is an invalid type'.format(type_name, sub_type))
    def __str__(self):
        return '{0}'.format(self.type_name) if not self.sub_type else '{0}[{1}]'.format(self.type_name, self.sub_type)
    def __repr__(self): return self.__str__()

class cli_param:
    def __init__(self, name, attrs, qualifier):
        self.__dict__.update(locals())
    def __str__(self):
        return '[param name={} qualifier={} attrs={}]'.format(self.name, self.qualifier, self.attrs)
    def __repr__(self):
        return '<{}>'.format(self.name)

def get_ast(root, name):
    asts = []
    if isinstance(root, wdl2_parser.Terminal):
        return asts
    elif isinstance(root, wdl2_parser.Ast):
        if root.name == name:
            asts.append(root)
        for attr_name, attr_value in root.attributes.items():
            asts.extend(get_ast(attr_value, name))
    elif isinstance(root, wdl2_parser.AstList):
        for member_ast in root:
            asts.extend(get_ast(member_ast, name))
    return asts

def parse_command_attr(ast):
    name = ast.attr('key').source_string
    value_ast = ast.attr('value')
    if isinstance(value_ast, wdl2_parser.Terminal):
        value = value_ast.source_string
    elif value_ast.name == 'Type':
        value = cli_param_type(value_ast.attr('name').source_string)
    elif value_ast.name == 'CollectionType':
        value = cli_param_type(value_ast.attr('collection').source_string, value_ast.attr('member').source_string)
    if name != 'type' and isinstance(value, cli_param_type):
        raise wdl2_parser.SyntaxError('Types are only allowed on "type" attributes, not "{0}"'.format(name))
    return (name, value)

def get_command(ast):
    command = []
    command_ast = get_ast(ast, 'Command')
    if len(command_ast) != 1:
        raise wdl2_parser.SyntaxError("Expecting only one 'command' section")
    command_ast = command_ast[0]
    for cmd_part in command_ast.attr('parts'):
        if isinstance(cmd_part, wdl2_parser.Terminal):
            command.append(cmd_part.source_string)
        elif cmd_part.name == 'CommandParameter':
            name = cmd_part.attr('name').source_string
            qualifier = cmd_part.attr('qualifier').source_string if cmd_part.attr('qualifier') else None
            attrs = []
            for attribute_ast in cmd_part.attr('attributes'):
                attrs.append(parse_command_attr(attribute_ast))
            attrs = dict(attrs)
            if 'type' not in attrs:
                attrs['type'] = cli_param_type('string')
            command.append(cli_param(name, attrs, qualifier))
    return command

def check_type(item, type_name):
    from urllib.parse import urlparse
    if type_name == 'int':
        if not isinstance(item, int): raise Exception('not int')
    if type_name == 'string':
        if not isinstance(item, str): raise Exception('not string')
    if type_name == 'uri':
        p = urlparse(item)
        if p.scheme not in ['http', 'gs', 'file']: raise Exception('not valid URI')
    if type_name == 'file':
        p = urlparse(item)
        if p.scheme not in ['file']: raise Exception('not valid file')

def get_task_ast(filepath):
    with open(filepath) as fp:
        try:
            return wdl2_parser.parse(fp.read()).ast()
        except wdl2_parser.SyntaxError as e:
            print(e)
            sys.exit(-1)

if sys.argv[1] == 'analyze':
    ast = get_task_ast(sys.argv[2])
    command = get_command(ast)
    print('Short Form:')
    print(command)
    print('\nLong Form:')
    for i, part in enumerate(command):
        print('({}) {}'.format(i, part))

elif sys.argv[1] == 'run':
    ast = get_task_ast(sys.argv[2])
    command = get_command(ast)
    with open(sys.argv[3]) as fp:
        params = json.loads(fp.read())
    real_command = []
    for part in command:
        if isinstance(part, str):
            real_command.append(part)
        elif isinstance(part, cli_param):
            param_value = params[part.name]
            if part.attrs['type'].type_name in container_types:
                if not isinstance(param_value, list):
                    print("Parameter {} requires type {}, got {}".format(part.name, part.attrs['type'], param_value))
                    sys.exit(-1)
                if part.attrs['type'].sub_type is not None:
                    for item in param_value:
                        try:
                            check_type(item, part.attrs['type'].sub_type)
                        except:
                            print("Parameter {} requires type {}, got: {}".format(part.name, part.attrs['type'], param_value))
                            sys.exit(-1)
                prefix = part.attrs['prefix'] if 'prefix' in part.attrs else ''
                real_command.append('{0}{1}'.format(prefix, part.attrs['sep'].join([str(x) for x in param_value])))
            else:
                try:
                    check_type(param_value, part.attrs['type'].type_name)
                except:
                    print("Parameter {} requires type {}, got: {}".format(part.name, part.attrs['type'], param_value))
                    sys.exit(-1)
                prefix = part.attrs['prefix'] if 'prefix' in part.attrs else ''
                real_command.append('{0}{1}'.format(prefix, param_value))
    print(' '.join(real_command))
