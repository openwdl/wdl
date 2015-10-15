import wdl.binding

def load(fp, resource):
    return wdl.binding.parse_document(fp.read(), resource)

def loads(s):
    return wdl.binding.parse_document(s, "string")

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
