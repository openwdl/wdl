import wdl.binding

def load(fp, resource):
    return wdl.binding.parse_document(fp.read(), resource)

def loads(s):
    return wdl.binding.parse_document(s, "string")
