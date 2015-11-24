from wdl.types import *

class EvalException(Exception): pass

def assert_type(value, types): return value.type.__class__  in types

class WdlValue(object):
    def __init__(self, value):
        self.value = value
        self.check_compatible(value)
    def __str__(self):
        return '[{}: {}]'.format(self.type, str(self.value))
    def as_string(self): return str(self.value)
    def __str__(self): return '[Wdl{}: {}]'.format(self.type.wdl_string(), self.as_string())
    def __eq__(self, rhs): return (self.__class__, self.value) == (rhs.__class__, rhs.value)
    def __hash__(self): return hash((self.__class__, self.value))
    def __invalid(self, symbol, rhs): raise EvalException('Cannot perform operation: {} {} {}'.format(self.type.wdl_string(), symbol, rhs.type.wdl_string()))
    def __invalid_unary(self, symbol): raise EvalException('Cannot perform operation: {} {}'.format(symbol, self.type.wdl_string()))
    def add(self, rhs): return self.__invalid('+', rhs)
    def subtract(self, rhs): return self.__invalid('-', rhs)
    def multiply(self, rhs): return self.__invalid('*', rhs)
    def divide(self, rhs): return self.__invalid('/', rhs)
    def mod(self, rhs): return self.__invalid('%', rhs)
    def equal(self, rhs): return self.__invalid('==', rhs)
    def not_equal(self, rhs): return self.equal(rhs).logical_not()
    def greater_than(self, rhs): return self.__invalid('>', rhs)
    def greater_than_or_equal(self, rhs): return self.greater_than(rhs).logical_or(self.equal(rhs))
    def less_than(self, rhs): return self.__invalid('<', rhs)
    def less_than_or_equal(self, rhs): return self.less_than(rhs).logical_or(self.equal(rhs))
    def logical_or(self, rhs): return self.__invalid('||', rhs)
    def logical_and(self, rhs): return self.__invalid('&&', rhs)
    def logical_not(self): return self.__invalid_unary('!')
    def unary_plus(self): return self.__invalid_unary('+')
    def unary_negation(self): return self.__invalid_unary('-')

class WdlUndefined(WdlValue):
    def __init__(self): self.type = None
    def __str__(self): return repr(self)

class WdlString(WdlValue):
    type = WdlStringType()
    def check_compatible(self, value):
        if isinstance(value, unicode): value = value.encode('utf-8')
        if not isinstance(value, str):
            raise EvalException("WdlString must hold a python 'str': {}".format(value.encode('utf-8')))
    def add(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType, WdlStringType, WdlFileType]):
            return WdlString(self.value + str(rhs.value))
        super(WdlString, self).add(rhs)
    def equal(self, rhs):
        if assert_type(rhs, [WdlStringType]):
            return WdlBoolean(self.value == rhs.value)
        super(WdlString, self).equal(rhs)
    def greater_than(self, rhs):
        if assert_type(rhs, [WdlStringType]):
            return WdlBoolean(self.value > rhs.value)
        super(WdlString, self).equal(rhs)
    def less_than(self, rhs):
        if assert_type(rhs, [WdlStringType]):
            return WdlBoolean(self.value < rhs.value)
        super(WdlString, self).equal(rhs)

class WdlInteger(WdlValue):
    type = WdlIntegerType()
    def check_compatible(self, value):
        if not isinstance(value, int):
            raise EvalException("WdlInteger must hold a python 'int'")
    def add(self, rhs):
        if assert_type(rhs, [WdlIntegerType]):
            return WdlInteger(self.value + rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(self.value + rhs.value)
        if assert_type(rhs, [WdlStringType]):
            return WdlString(str(self.value) + rhs.value)
        super(WdlInteger, self).add(rhs)
    def subtract(self, rhs):
        if assert_type(rhs, [WdlIntegerType]):
            return WdlInteger(self.value - rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(self.value - rhs.value)
        super(WdlInteger, self).subtract(rhs)
    def multiply(self, rhs):
        if assert_type(rhs, [WdlIntegerType]):
            return WdlInteger(self.value * rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(self.value * rhs.value)
        super(WdlInteger, self).multiply(rhs)
    def divide(self, rhs):
        if assert_type(rhs, [WdlIntegerType]):
            return WdlInteger(self.value / rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(self.value / rhs.value)
        super(WdlInteger, self).divide(rhs)
    def mod(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value % rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(self.value % rhs.value)
        super(WdlInteger, self).mod(rhs)
    def equal(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value == rhs.value)
        super(WdlInteger, self).equal(rhs)
    def greater_than(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value > rhs.value)
        super(WdlInteger, self).greater_than(rhs)
    def less_than(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value < rhs.value)
        super(WdlInteger, self).less_than(rhs)
    def unary_negation(self):
        return WdlInteger(-self.value)
    def unary_plus(self):
        return WdlInteger(+self.value)

class WdlBoolean(WdlValue):
    type = WdlBooleanType()
    def check_compatible(self, value):
        if not isinstance(value, bool):
            raise EvalException("WdlBoolean must hold a python 'bool'")
    def greater_than(self, rhs):
        if assert_type(rhs, [WdlBooleanType]):
            return WdlBoolean(self.value > rhs.value)
        super(WdlBoolean, self).greater_than(rhs)
    def less_than(self, rhs):
        if assert_type(rhs, [WdlBooleanType]):
            return WdlBoolean(self.value < rhs.value)
        super(WdlBoolean, self).less_than(rhs)
    def equal(self, rhs):
        if assert_type(rhs, [WdlBooleanType]):
            return WdlBoolean(self.value == rhs.value)
        super(WdlBoolean, self).equal(rhs)
    def logical_or(self, rhs):
        if assert_type(rhs, [WdlBooleanType]):
            return WdlBoolean(self.value or rhs.value)
        super(WdlBoolean, self).logical_or(rhs)
    def logical_and(self, rhs):
        if assert_type(rhs, [WdlBooleanType]):
            return WdlBoolean(self.value and rhs.value)
        super(WdlBoolean, self).logical_and(rhs)
    def logical_not(self):
        return WdlBoolean(not self.value)

class WdlFloat(WdlValue):
    type = WdlFloatType()
    def check_compatible(self, value):
        if not isinstance(value, float):
            raise EvalException("WdlFloat must hold a python 'float'")
    def add(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlFloat(self.value + rhs.value)
        if assert_type(rhs, [WdlStringType]):
            return WdlString(str(self.value) + rhs.value)
        super(WdlFloat, self).add(rhs)
    def subtract(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlFloat(self.value - rhs.value)
        super(WdlFloat, self).subtract(rhs)
    def multiply(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlFloat(self.value * rhs.value)
        super(WdlFloat, self).multiply(rhs)
    def divide(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlFloat(self.value / rhs.value)
        super(WdlFloat, self).divide(rhs)
    def mod(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlFloat(self.value % rhs.value)
        super(WdlFloat, self).mod(rhs)
    def equal(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value == rhs.value)
        super(WdlFloat, self).greater_than(rhs)
    def greater_than(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value > rhs.value)
        super(WdlFloat, self).greater_than(rhs)
    def less_than(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlFloatType]):
            return WdlBoolean(self.value < rhs.value)
        super(WdlFloat, self).less_than(rhs)
    def unary_negation(self):
        return WdlFloat(-self.value)
    def unary_plus(self):
        return WdlFloat(+self.value)

class WdlFile(WdlString):
    type = WdlFileType()
    def check_compatible(self, value):
        if isinstance(value, unicode): value = value.encode('utf-8')
        if not isinstance(value, str):
            raise EvalException("WdlFile must hold a python 'str': {}".format(value.encode('utf-8')))
    def add(self, rhs):
        if assert_type(rhs, [WdlFileType, WdlStringType]):
            return WdlFile(self.value + str(rhs.value))
        super(WdlFile, self).add(rhs)
    def equal(self, rhs):
        if assert_type(rhs, [WdlFileType, WdlStringType]):
            return WdlBoolean(self.value == rhs.value)
        super(WdlFile, self).equal(rhs)
    def greater_than(self, rhs):
        if assert_type(rhs, [WdlFileType]):
            return WdlBoolean(self.value > rhs.value)
        super(WdlFile, self).equal(rhs)
    def less_than(self, rhs):
        if assert_type(rhs, [WdlFileType]):
            return WdlBoolean(self.value < rhs.value)
        super(WdlFile, self).equal(rhs)

class WdlUri(WdlValue):
    type = WdlUriType()
    def check_compatible(self, value):
        pass # TODO: implement

class WdlArray(WdlValue):
    def __init__(self, subtype, value):
        if not isinstance(value, list):
            raise EvalException("WdlArray must be a Python 'list'")
        if not all(type(x.type) == type(subtype) for x in value):
            raise EvalException("WdlArray must contain elements of the same type: {}".format(value))
        self.type = WdlArrayType(subtype)
        self.subtype = subtype
        self.value = value
    def __str__(self):
        return '[{}: {}]'.format(self.type, ', '.join([str(x) for x in self.value]))

class WdlMap(WdlValue):
    def __init__(self, key_type, value_type, value):
        if not isinstance(value, dict):
            raise EvalException("WdlMap must be a Python 'dict'")
        if not isinstance(key_type, WdlPrimitiveType):
            raise EvalException("WdlMap must contain WdlPrimitive keys")
        if not isinstance(value_type, WdlPrimitiveType):
            raise EvalException("WdlMap must contain WdlPrimitive values")
        if not all(isinstance(k.type, key_type.__class__) for k in value.keys()):
            raise EvalException("WdlMap must contain keys of the same type: {}".format(value))
        if not all(isinstance(v.type, value_type.__class__) for v in value.values()):
            raise EvalException("WdlMap must contain values of the same type: {}".format(value))
        (k, v) = list(value.items())[0]
        self.type = WdlMapType(key_type, value_type)
        self.key_type = key_type
        self.value_type = value_type
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
