import wdl
import pytest
from wdl.values import *

static_expressions = [
    # Integers
    ("1+2", WdlInteger(3)),
    (""" 1 + "String" """, WdlString("1String")),
    ("1+2.3", WdlFloat(3.3)),
    ("3-5", WdlInteger(-2)),
    ("10-6.7", WdlFloat(3.3)),
    ("8 * 7", WdlInteger(56)),
    ("5 * 7.2", WdlFloat(36.0)),
    ("80 / 6", WdlInteger(13)),
    ("25/2.0", WdlFloat(12.5)),
    ("10 % 3", WdlInteger(1)),
    ("10 % 3.5", WdlFloat(3.0)),
    (" 24 == 24 ", WdlBoolean(True)),
    (" 24 == 26 ", WdlBoolean(False)),
    (" 1 != 0 ", WdlBoolean(True)),
    (" 1 != 1 ", WdlBoolean(False)),
    ("4 < 3", WdlBoolean(False)),
    ("3 < 4", WdlBoolean(True)),
    ("4 < 5.0", WdlBoolean(True)),
    ("3 <= 4", WdlBoolean(True)),
    ("3 <= 3.0", WdlBoolean(True)),
    ("4 > 3", WdlBoolean(True)),
    ("4 > 3.0", WdlBoolean(True)),
    ("4 >= 4", WdlBoolean(True)),
    ("4 >= 4.0", WdlBoolean(True)),
    ("-1 + -3", WdlInteger(-4)),
    ("+1", WdlInteger(1)),

    # Floats
    ("1.0+2", WdlFloat(3.0)),
    (""" 1.0 + "String" """, WdlString("1.0String")),
    ("1.0+2.3", WdlFloat(3.3)),
    ("3.0-5", WdlFloat(-2.0)),
    ("10.0-6.7", WdlFloat(3.3)),
    ("8.0 * 7", WdlFloat(56.0)),
    ("5.0 * 7.2", WdlFloat(36.0)),
    ("25.0 / 4", WdlFloat(6.25)),
    ("25.0/2.0", WdlFloat(12.5)),
    ("10.0 % 3", WdlFloat(1.0)),
    ("10.0 % 3.5", WdlFloat(3.0)),
    ("24.0 == 24 ", WdlBoolean(True)),
    ("24.0 == 24.0 ", WdlBoolean(True)),
    ("24.0 == 26 ", WdlBoolean(False)),
    ("1.0 != 0 ", WdlBoolean(True)),
    ("1.0 != 0.0 ", WdlBoolean(True)),
    ("1.0 != 1 ", WdlBoolean(False)),
    ("4.0 < 3", WdlBoolean(False)),
    ("4.0 < 3.0", WdlBoolean(False)),
    ("3.0 < 4", WdlBoolean(True)),
    ("4.0 < 5.0", WdlBoolean(True)),
    ("3.0 <= 4", WdlBoolean(True)),
    ("3.0 <= 3.0", WdlBoolean(True)),
    ("4.0 > 3", WdlBoolean(True)),
    ("4.0 > 3.0", WdlBoolean(True)),
    ("4.0 >= 4", WdlBoolean(True)),
    ("4.0 >= 4.0", WdlBoolean(True)),
    ("+1.0", WdlFloat(1.0)),
    ("-1.0", WdlFloat(-1.0)),

    # Booleans
    ("false == false ", WdlBoolean(True)),
    ("false == true ", WdlBoolean(False)),
    ("true != false ", WdlBoolean(True)),
    ("true != true ", WdlBoolean(False)),
    ("true < false", WdlBoolean(False)),
    ("false <= false ", WdlBoolean(True)),
    ("true <= false", WdlBoolean(False)),
    ("true > false", WdlBoolean(True)),
    ("false >= false ", WdlBoolean(True)),
    ("false >= true ", WdlBoolean(False)),
    ("false || true ", WdlBoolean(True)),
    ("false || false ", WdlBoolean(False)),
    ("false && true ", WdlBoolean(False)),
    ("true && true ", WdlBoolean(True)),
    ("!true", WdlBoolean(False)),
    ("!false", WdlBoolean(True)),

    # Strings
    (""" "String" + 456 """, WdlString("String456")),
    (""" "hello" + " world" """, WdlString("hello world")),
    (""" "hello" + 2.1 """, WdlString("hello2.1")),
    (""" "hello" == "hello" """, WdlBoolean(True)),
    (""" "hello" == "hello2" """, WdlBoolean(False)),
    (""" "hello" != "hello" """, WdlBoolean(False)),
    (""" "hello" != "hello2" """, WdlBoolean(True)),
    (""" "abc" < "def" """, WdlBoolean(True)),
    (""" "abc" <= "def" """, WdlBoolean(True)),
    (""" "abc" > "def" """, WdlBoolean(False)),
    (""" "abc" >= "def" """, WdlBoolean(False)),

    # Order of Operations
    ("1+2*3", WdlInteger(7)),
    ("1+2==3", WdlBoolean(True)),
    ("(1+2)*3", WdlInteger(9))
]

@pytest.mark.parametrize("expression,value", static_expressions)
def test_static_expressions(expression, value):
    assert wdl.parse_expr(expression).eval() == value
