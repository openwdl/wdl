import sys
import json
import wdl2_parser

valid_types = ['int', 'array', 'set', 'string', 'uri', 'file']
container_types = ['array', 'set']

class cli_param_type:
    def __init__(self, type_name, container_type_name=None):
        self.__dict__.update(locals())
        if type_name not in valid_types:
            raise wdl2_parser.SyntaxError('{0} is not a valid type'.format(type))
        if container_type_name is not None and container_type_name not in container_types:
            raise wdl2_parser.SyntaxError('{0}[{1}] is an invalid type'.format(container_type_name, type))
    def __str__(self):
        return '{0}'.format(self.type_name) if not self.container_type_name else '{0}[{1}]'.format(self.container_type_name, self.type_name)
    def __repr__(self): return self.__str__()

class cli_param:
    def __init__(self, name, attrs, qualifier):
        self.__dict__.update(locals())
    def __str__(self):
        return '[param name={} qualifier={} attrs={}]'.format(self.name, self.qualifier, self.attrs)
    def __repr__(self):
        return '<{}>'.format(self.name)

def parse_command_attr(ast):
    name = ast.attr('key').source_string
    value_ast = ast.attr('value')
    if isinstance(value_ast, wdl2_parser.Terminal):
        value = value_ast.source_string
    elif value_ast.name == 'Type':
        type_name = value_ast.attr('name').source_string
        try:
            sub = value_ast.attr('sub').source_string
        except:
            sub = None
        value = cli_param_type(sub, type_name) if sub else cli_param_type(type_name)
    if name != 'type' and isinstance(value, cli_param_type):
        raise wdl2_parser.SyntaxError('Types are only allowed on "type" attributes, not "{0}"'.format(name))
    return (name, value)

def get_command(ast):
    command = []
    for section in ast.attr('sections'):
        if section.name == 'Command':
            for cmd_part in section.attr('parts'):
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

if sys.argv[1] == 'analyze':
    with open(sys.argv[2]) as fp:
        try:
            ast = wdl2_parser.parse(fp.read()).ast()
            command = get_command(ast)
            print('Short Form:')
            print(command)
            print('\nLong Form:')
            for i, part in enumerate(command):
                print('({}) {}'.format(i, part))
        except wdl2_parser.SyntaxError as e:
            print(e)

elif sys.argv[1] == 'run':
    with open(sys.argv[2]) as fp:
        try:
            ast = wdl2_parser.parse(fp.read()).ast()
            command = get_command(ast)
        except wdl2_parser.SyntaxError as e:
            print(e)
    with open(sys.argv[3]) as fp:
        params = json.loads(fp.read())
    real_command = []
    for part in command:
        if isinstance(part, str):
            real_command.append(part)
        elif isinstance(part, cli_param):
            param_value = params[part.name]
            if part.attrs['type'].container_type_name is not None:
                if not isinstance(param_value, list):
                    print("Parameter {} requires type {}, got {}".format(part.name, part.attrs['type'], param_value))
                    sys.exit(-1)
                for item in param_value:
                    try: check_type(item, part.attrs['type'].type_name)
                    except:
                        print("Parameter {} requires type {}, got: {}".format(part.name, part.attrs['type'], param_value))
                        sys.exit(-1)
                prefix = part.attrs['prefix'].strip('\'"') if 'prefix' in part.attrs else ''
                real_command.append('{0}{1}'.format(prefix, part.attrs['sep'].strip('\'"').join([str(x) for x in param_value])))
            else:
                try: check_type(param_value, part.attrs['type'].type_name)
                except:
                    print("Parameter {} requires type {}, got: {}".format(part.name, part.attrs['type'], param_value))
                    sys.exit(-1)
                prefix = part.attrs['prefix'].strip('\'"') if 'prefix' in part.attrs else ''
                real_command.append('{0}{1}'.format(prefix, param_value))
    print(' '.join(real_command))
