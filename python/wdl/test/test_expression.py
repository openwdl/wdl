import wdl
import pytest
from wdl.values import *

static_expressions = [
    # Integers
    ("1+2", WdlInteger(3)),
    (' 1 + "String" ', WdlString("1String")),
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
    (' 1.0 + "String" ', WdlString("1.0String")),
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
    (' "String" + 456 ', WdlString("String456")),
    (' "hello" + " world" ', WdlString("hello world")),
    (' "hello" + 2.1 ', WdlString("hello2.1")),
    (' "hello" == "hello" ', WdlBoolean(True)),
    (' "hello" == "hello2" ', WdlBoolean(False)),
    (' "hello" != "hello" ', WdlBoolean(False)),
    (' "hello" != "hello2" ', WdlBoolean(True)),
    (' "abc" < "def" ', WdlBoolean(True)),
    (' "abc" <= "def" ', WdlBoolean(True)),
    (' "abc" > "def" ', WdlBoolean(False)),
    (' "abc" >= "def" ', WdlBoolean(False)),

    # Order of Operations
    ("1+2*3", WdlInteger(7)),
    ("1+2==3", WdlBoolean(True)),
    ("(1+2)*3", WdlInteger(9))
]

bad_expressions = [
    # Integers
    ("1+true"),
    ("1-true"),
    (' 1-"s"  '),
    ("1*true"),
    (' 1*"s"  '),
    ("1 / 0"),
    ("1 / 0.0"),
    ("25/0.0"),
    ("1/true"),
    (' 1/"s"  '),
    ("1%false"),
    (' 1%"s"  '),
    ("1%0"),
    (" 24 == false "),
    (' 1 == "s"  '),
    (" 24 != false "),
    (' 1 != "s"  '),
    (" 24 < false "),
    (' 1 < "s"  '),
    (" 24 <= false "),
    (' 1 <= "s"  '),
    ("4 > false"),
    (' 1 > "s"  '),
    ("4 >= false"),
    (' 1 >= "s"  '),

    # Floats
    ("1.0+true"),
    ("1.0-true"),
    (' 1.0-"s"  '),
    ("1.0*true"),
    (' 1.0*"s"  '),
    ("1.0/true"),
    ("1.0/0.0"),
    ("1.0/0"),
    (' 1.0/"s"  '),
    ("10.0 % 0"),
    ("10.0 % 0.0"),
    ("1.0%false"),
    (' 1.0%"s"  '),
    ("24.0 == false "),
    (' 1.0 == "s"  '),
    ("24.0 != false "),
    (' 1.0 != "s"  '),
    ("24.0 < false "),
    (' 1.0 < "s"  '),
    ("24.0 <= false "),
    (' 1.0 <= "s"  '),
    ("4.0 > false"),
    (' 1.0 > "s"  '),
    ("4.0 >= false"),
    (' 1.0 >= "s"  '),

    # Booleans
    (' true + "String" '),
    ("true+2"),
    ("true+2.3"),
    ("false+true"),
    ("false-5"),
    ("false-6.6"),
    ("true-true"),
    (' true-"s"  '),
    ("false * 7"),
    ("false * 7.2"),
    ("false*true"),
    (' false*"s"  '),
    ("false / 4"),
    ("false/2.0"),
    ("false/true"),
    (' true/"s"  '),
    ("true % 3"),
    ("true % 3.5"),
    ("false%false"),
    (' true % "s"  '),
    ("true == 24 "),
    ("true == 24.0 "),
    ('true == "s"  '),
    ("true != 0 "),
    ("true != 0.0 "),
    ('true != "s"  '),
    ("true < 3"),
    ("true < 3.0"),
    ("true < 5.0"),
    ('true < "s"  '),
    ("true <= 4"),
    ("true <= 3.0"),
    ('true <= "s"  '),
    ("true > 3"),
    ("true > 3.0"),
    ("true >= 4"),
    ("true >= 4.0"),
    ('true >= "s"  '),
    ("true || 4"),
    ("true || 4.0"),
    ('true || "s"  '),
    ("true && 4"),
    ("true && 4.0"),
    ('true && "s"  '),

    # Strings
    (' "hello" + true '),
    (' "hello" == true '),
    (' "hello" != true '),
    (' "hello" < true '),
    (' "hello" > true ')
]

identifier_expressions = [
    # Lookup Variables
    ("a", WdlInteger(1)),
    ("a + 10", WdlInteger(11)),
    ("a + b", WdlInteger(3)),
    ("s + a", WdlString("s1")),
    ("o.key1", WdlString("value1")),
    ("o.key2", WdlInteger(9)),

    # Call Functions
    ("b(1)", WdlInteger(2)),
    ("b(1) + 10", WdlInteger(12)),
    (' append("hello ", "world") ', WdlString("hello world")),
    (' append("a", "b", "c", "d") ', WdlString("abcd")),

    # String Interpolation
    ("\"prefix.${a}.suffix\"", WdlString("prefix.1.suffix")),
    ("\"prefix.${a}${a}.suffix${a}\"", WdlString("prefix.11.suffix1")),
    ("\"${b}prefix.${b}${a}${a}.suffix${a}\"", WdlString("2prefix.211.suffix1")),
    ("\"${s}...${s}\"", WdlString("s...s")),

    # Array Indexing
    ("array_str[0]", WdlString("foo")),
    ("array_str[1]", WdlString("bar")),
    ("array_str[2]", WdlString("baz")),

    # Map Indexing
    ('map_str_int["a"]', WdlInteger(0)),
    ('map_str_int["b"]', WdlInteger(1)),
    ('map_str_int["c"]', WdlInteger(2)),

    # Files -- 'etc_f', 'etc2_f', and 'sudoers_f' are all variables that resolve to WdlFile
    ("etc_f + sudoers_s", WdlFile("/etc/sudoers")),
    (' "/foo" + etc_f ', WdlString("/foo/etc")),
    ("etc_f == etc_f", WdlBoolean(True)),
    ("etc_f == etc2_f", WdlBoolean(False)),
    ("etc_f != etc2_f", WdlBoolean(True)),
    ("etc_f == etc_s", WdlBoolean(True)),

    # String escaping
    (' "abc" ', WdlString("abc")),
    (' "a\\nb" ', WdlString("a\nb")),
    (' "a\\nb\\t" ', WdlString("a\nb\t")),
    (' "a\\n\\"b\\t\\"" ', WdlString("a\n\"b\t\"")),
    (' "be \u266f or be \u266e, just don\'t be \u266d" ', WdlString(u"be \u266f or be \u266e, just don't be \u266d"))
]

@pytest.mark.parametrize("expression,value", static_expressions)
def test_static_expressions(expression, value):
    assert wdl.parse_expr(expression).eval() == value

@pytest.mark.parametrize("expression", bad_expressions)
def test_bad_expressions(expression):
    with pytest.raises(Exception):
        assert wdl.parse_expr(expression).eval()

def lookup(name):
    if name == "a": return WdlInteger(1)
    if name == "b": return WdlInteger(2)
    if name == "s": return WdlString("s")
    if name == "array_str": return WdlArray(WdlStringType(), [WdlString(x) for x in ["foo", "bar", "baz"]])
    if name == "map_str_int": return WdlMap(WdlStringType(), WdlIntegerType(), {
      WdlString("a"): WdlInteger(0),
      WdlString("b"): WdlInteger(1),
      WdlString("c"): WdlInteger(2)
    })
    if name == "o": return WdlObject({"key1": WdlString("value1"), "key2": WdlInteger(9)})
    if name == "etc_f": return WdlFile("/etc")
    if name == "etc2_f": return WdlFile("/etc2")
    if name == "etc_s": return WdlString("/etc")
    if name == "sudoers_f": return WdlFile("/sudoers")
    if name == "sudoers_s": return WdlString("/sudoers")

def function(name):
    def append(parameters):
        return WdlString(''.join([p.value for p in parameters]))
    def b(parameters):
        return WdlInteger(parameters[0].value + 1)
    if name == 'append': return append
    elif name == 'b': return b

@pytest.mark.parametrize("expression,value", identifier_expressions)
def test_identifier_expressions(expression, value):
    actual = wdl.parse_expr(expression).eval(lookup, function)
    #print(actual.value, value.value)
    assert actual == value
