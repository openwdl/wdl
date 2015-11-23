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
    def __eq__(self, rhs): return self.__class__ == rhs.__class__ and self.value == rhs.value
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
        if not isinstance(value, str):
            raise WdlValueException("WdlString must hold a python 'str'")
    def add(self, rhs):
        if isinstance(rhs.type, WdlPrimitiveType):
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
            raise WdlValueException("WdlInteger must hold a python 'int'")
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
            raise WdlValueException("WdlBoolean must hold a python 'bool'")
    def add(self, rhs):
        if assert_type(rhs, [WdlIntegerType, WdlBooleanType]):
            return WdlInteger(self.value + rhs.value)
        if assert_type(rhs, [WdlFloatType]):
            return WdlFloat(str(self.value) + str(rhs.value))
        raise EvalException("Cannot add: {} + {}".format(self.type, rhs.type))
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
            raise WdlValueException("WdlFloat must hold a python 'float'")
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
