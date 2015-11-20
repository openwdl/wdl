from wdl.binding import parse_namespace, Expression
import wdl.parser

def load(fp, resource):
    return parse_namespace(fp.read(), resource)

def loads(s):
    return parse_namespace(s, "string")

def find_asts(ast_root, name):
    nodes = []
    if isinstance(ast_root, wdl.parser.AstList):
        for node in ast_root:
            nodes.extend(find_asts(node, name))
    elif isinstance(ast_root, wdl.parser.Ast):
        if ast_root.name == name:
            nodes.append(ast_root)
        for attr_name, attr in ast_root.attributes.items():
            nodes.extend(find_asts(attr, name))
    return nodes

def parse_expr(expr_string):
    ctx = wdl.parser.ParserContext(wdl.parser.lex(expr_string, 'string'), wdl.parser.DefaultSyntaxErrorHandler())
    return Expression(wdl.parser.parse_e(ctx).ast())
