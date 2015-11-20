from wdl.types import *

class EvalException(Exception): pass

def assert_type(value, types): return value.type.__class__  in types

class WdlValue:
    def __init__(self, value):
        self.value = value
        self.check_compatible(value)
    def __str__(self):
        return '[{}: {}]'.format(self.type, str(self.value))
    def as_string(self): return str(self.value)
    def __str__(self): return '[Wdl{}: {}]'.format(self.type.wdl_string(), self.as_string())
    def __eq__(self, other): return self.__class__ == other.__class__ and self.value == other.value

class WdlUndefined(WdlValue):
    def __init__(self): self.type = None
    def __str__(self): return repr(self)

class WdlString(WdlValue):
    type = WdlStringType()
    def check_compatible(self, value):
        if not isinstance(value, str):
            raise WdlValueException("WdlString must hold a python 'str'")
    def add(self, wdl_value):
        if isinstance(wdl_value.type, WdlPrimitiveType):
            return WdlString(self.value + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlInteger(WdlValue):
    type = WdlIntegerType()
    def check_compatible(self, value):
        if not isinstance(value, int):
            raise WdlValueException("WdlInteger must hold a python 'int'")
    def add(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value + wdl_value.value)
        if assert_type(wdl_value, [WdlFloatType]):
            return WdlFloat(self.value + wdl_value.value)
        if assert_type(wdl_value, [WdlStringType, WdlFile, WdlUri]):
            return WdlString(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))
    def subtract(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value - wdl_value.value)
        if assert_type(wdl_value, [WdlFloatType]):
            return WdlFloat(self.value - wdl_value.value)
        raise EvalException("Cannot subtract: {} + {}".format(self.type, wdl_value.type))
    def multiply(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value * wdl_value.value)
        if assert_type(wdl_value, [WdlFloatType]):
            return WdlFloat(self.value * wdl_value.value)
        raise EvalException("Cannot multiply: {} + {}".format(self.type, wdl_value.type))
    def divide(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType, WdlFloatType]):
            return WdlFloat(self.value / wdl_value.value)
        raise EvalException("Cannot divide: {} + {}".format(self.type, wdl_value.type))
    def mod(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value % wdl_value.value)
        if assert_type(wdl_value, [WdlFloatType]):
            return WdlFloat(self.value % wdl_value.value)
        raise EvalException("Cannot modulus divide: {} + {}".format(self.type, wdl_value.type))

class WdlBoolean(WdlValue):
    type = WdlBooleanType()
    def check_compatible(self, value):
        if not isinstance(value, bool):
            raise WdlValueException("WdlBoolean must hold a python 'bool'")
    def add(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value + wdl_value.value)
        if assert_type(wdl_value, [WdlFloatType]):
            return WdlFloat(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlFloat(WdlValue):
    type = WdlFloatType()
    def check_compatible(self, value):
        if not isinstance(value, float):
            raise WdlValueException("WdlFloat must hold a python 'float'")
    def add(self, wdl_value):
        if assert_type(wdl_value, [WdlIntegerType, WdlBooleanType, WdlFloatType]):
            return WdlFloat(self.value + wdl_value.value)
        if assert_type(wdl_value, [WdlStringType, WdlFile, WdlUri]):
            return WdlString(str(self.value) + str(wdl_value.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, wdl_value.type))

class WdlFile(WdlValue):
    type = WdlFileType()
    def check_compatible(self, value):
        pass # TODO: implement

class WdlUri(WdlValue):
    type = WdlUriType()
    def check_compatible(self, value):
        pass # TODO: implement

class WdlArray(WdlValue):
    def __init__(self, subtype, value):
        if not isinstance(value, list):
            raise WdlValueException("WdlArray must be a Python 'list'")
        if not all(type(x.type) == type(subtype) for x in value):
            raise WdlValueException("WdlArray must contain elements of the same type: {}".format(value))
        self.type = WdlArrayType(subtype)
        self.subtype = subtype
        self.value = value
    def flatten(self):
        flat = lambda l: [item for sublist in l for item in sublist.value]
        if not isinstance(self.type.subtype, WdlArrayType):
            raise WdlValueException("Cannot flatten {} (type {})".format(self.value, self.type))
        return WdlArray(self.subtype.subtype, flat(self.value))
    def __str__(self):
        return '[{}: {}]'.format(self.type, ', '.join([str(x) for x in self.value]))

class WdlMap(WdlValue):
    def __init__(self, value):
        if not isinstance(value, dict):
            raise WdlValueException("WdlMap must be a Python 'dict'")
        if not all(type(x) == WdlPrimitiveType for x in value.keys()):
            raise WdlValueException("WdlMap must contain WdlPrimitiveValues keys")
        if not all(type(x) == WdlPrimitiveType for x in value.values()):
            raise WdlValueException("WdlMap must contain WdlPrimitiveValues values")
        if not all(type(x) == type(value[0]) for x in value.keys()):
            raise WdlValueException("WdlMap must contain keys of the same type: {}".format(value))
        if not all(type(x) == type(value[0]) for x in value.values()):
            raise WdlValueException("WdlMap must contain values of the same type: {}".format(value))
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
