# PyWDL

A Python implementation of a WDL parser and language bindings.

For Scala language bindings, use [Cromwell](http://github.com/broadinstitute/cromwell).

<!---toc start-->

* [PyWDL](#pywdl)
* [Installation](#installation)
* [Language Bindings](#language-bindings)
  * [Abstract syntax trees (ASTs)](#abstract-syntax-trees-asts)
    * [wdl.parser.Ast](#wdlparserast)
    * [wdl.parser.Terminal](#wdlparserterminal)
    * [wdl.parser.AstList](#wdlparserastlist)
  * [Working with expressions](#working-with-expressions)
* [Command Line Usage](#command-line-usage)

<!---toc end-->

# Installation

PyWDL works with Python 2 or Python 3. Install via `setup.py`:

```
$ python setup.py install
```

Or via pip:

```
$ pip install wdl
```

# Language Bindings

The main `wdl` package provides an interface to turn WDL source code into native Python objects.  This means that a `workflow {}` block in WDL would become a `Workflow` object in Python and a `task {}` block becomes a `Task` object.

To parse WDL source code into a `WdlDocument` object, import the `wdl` package and load a WDL string with `wdl.loads("wdl code")` or WDL from a file-like object using `wdl.load(fp, resource_name)`.

For example:

```python
import wdl
import wdl.values

wdl_code = """
task my_task {
  File file
  command {
    ./my_binary --input=${file} > results
  }
  output {
    File results = "results"
  }
}

workflow my_wf {
  call my_task
}
"""

# Use the language bindings to parse WDL into Python objects
wdl_namespace = wdl.loads(wdl_code)

for workflow in wdl_namespace.workflows:
    print('Workflow "{}":'.format(workflow.name))
    for call in workflow.calls():
        print('    Call: {} (task {})'.format(call.name, call.task.name))

for task in wdl_namespace.tasks:
    name = task.name
    abstract_command = task.command
    def lookup(name):
        if name == 'file': return wdl.values.WdlFile('/path/to/file.txt')
    instantated_command = task.command.instantiate(lookup)
    print('Task "{}":'.format(name))
    print('    Abstract Command: {}'.format(abstract_command))
    print('    Instantiated Command: {}'.format(instantated_command))
```

Using the language bindings as shown above is the recommended way to use PyWDL.  One can also directly access the parser to parse WDL source code into an abstract syntax tree using the `wdl.parser` package:

```python
import wdl.parser

wdl_code = """
task my_task {
  File file
  command {
    ./my_binary --input=${file} > results
  }
  output {
    File results = "results"
  }
}

workflow my_wf {
  call my_task
}
"""

# Parse source code into abstract syntax tree
ast = wdl.parser.parse(wdl_code).ast()

# Print out abstract syntax tree
print(ast.dumps(indent=2))

# Access the first task definition, print out its name
print(ast.attr('definitions')[0].attr('name').source_string)

# Find all 'Task' ASTs
task_asts = wdl.find_asts(ast, 'Task')
for task_ast in task_asts:
    print(task_ast.dumps(indent=2))

# Find all 'Workflow' ASTs
workflow_asts = wdl.find_asts(ast, 'Workflow')
for workflow_ast in workflow_asts:
    print(workflow_ast.dumps(indent=2))
```

## Abstract syntax trees (ASTs)

An AST is the output of the parsing algorithm.  It is a tree structure in which the root node is always a `Document` AST

The best way to get started working with ASTs is to visualize them by using the `wdl parse` subcommand to see the AST as text.  For example, consider the following WDL file

example.wdl
```
task a {
  command {./foo_bin}
}
task b {
  command {./bar_bin}
}
task c {
  command {./baz_bin}
}
workflow w {}
```

Then, use the command line to parse and output the AST:

```
$ wdl parse example.wdl
(Document:
  imports=[],
  definitions=[
    (Task:
      name=<string:1:6 identifier "YQ==">,
      declarations=[],
      sections=[
        (RawCommand:
          parts=[
            <string:2:12 cmd_part "Li9mb29fYmlu">
          ]
        )
      ]
    ),
    (Task:
      name=<string:4:6 identifier "Yg==">,
      declarations=[],
      sections=[
        (RawCommand:
          parts=[
            <string:5:12 cmd_part "Li9iYXJfYmlu">
          ]
        )
      ]
    ),
    (Task:
      name=<string:7:6 identifier "Yw==">,
      declarations=[],
      sections=[
        (RawCommand:
          parts=[
            <string:8:12 cmd_part "Li9iYXpfYmlu">
          ]
        )
      ]
    ),
    (Workflow:
      name=<string:10:10 identifier "dw==">,
      body=[]
    )
  ]
)
```

Programmatically, if one wanted to traverse this AST to pull out data:

```python
import wdl.parser
import wdl

with open('example.wdl') as fp:
    ast = wdl.parser.parse(fp.read()).ast()

task_a = ast.attr('definitions')[0]
task_b = ast.attr('definitions')[1]
task_c = ast.attr('definitions')[2]

for ast in task_a.attr('sections'):
    if ast.name == 'RawCommand':
        task_a_command = ast

for ast in task_a_command.attr('parts'):
    if isinstance(ast, wdl.parser.Terminal):
        print('command string: ' + ast.source_string)
    else:
        print('command parameter: ' + ast.dumps())
```

### wdl.parser.Ast

The `Ast` class is a syntax tree with a name and children nodes.

Attributes:

* `name` is a string that refers to the type of AST, (e.g. `Workflow`, `Task`, `Document`, `RawCommand`)
* `attributes` is a dictionary where the keys are the name of the attribute and the values can be one of three types: `Ast`, `AstList`, `Terminal`.

Methods:

* `def attr(self, name)`.  `ast.attr('name')` is the same as `ast.attributes['name']`.
* `def dumps(self, indent=None, b64_source=True)` - returns a String representation of this AstList.  the `indent` parameter takes an integer for the indent level.  Omitting this value will cause there to be no new-lines in the resulting string.  `b64_source` will be passed to recursive invocations of `dumps`.

### wdl.parser.Terminal

The `wdl.parser.Terminal` object represents a literal piece of the original source code.  This always shows up as leaf nodes on `Ast` objects

Attributes:

* `source_string` - String segment from the source code.
* `line` - Line number where `source_string` was in source code.
* `col` - Column number where `source_string` was in source code.
* `resource` - Name of the location for the source code.  Usually a file system path or perhaps URI.
* `id` - Numeric identifier, unique to the top level `Ast`.  Used mostly internally.
* `str` - String identifier of this terminal.  Used mostly internally.

Methods:

* `def dumps(self, b64_source=True, **kwargs)` - return a String representation of this terminal.  `b64_source` means that the source code will be base64 encoded because sometimes the source contains newlines or special characters that make it difficult to read when a whole AST is string-ified.

### wdl.parser.AstList

`class AstList(list)` represents a sequence of `Ast`, `AstList`, and `Terminal` objects

Methods:

* `def dumps(self, indent=None, b64_source=True)` - returns a String representation of this AstList.  the `indent` parameter takes an integer for the indent level.  Omitting this value will cause there to be no new-lines in the resulting string.  `b64_source` will be passed to recursive invocations of `dumps`.

## Working with expressions

Parsing a WDL file will result in unevaluated expressions.  For example:

```
workflow test {
  Int a = (1 + 2) * 3
  call my_task {
    input: var=a*2, var2="file"+".txt"
  }
}
```

This workflow definition has three expressions in it: `(1 + 2) * 3`, `a*2`, and `"file"+".txt"`.

Expressions are stored in `wdl.binding.Expression` object.  The AST for the expression is stored in this object.

Expressions can be evaluated with the `eval()` method on the `Expression` class.

```python
import wdl

# Manually parse expression into wdl.binding.Expression
expression = wdl.parse_expr("(1 + 2) * 3")

# Evaluate the expression.
# Returns a WdlValue, specifically a WdlIntegerValue(9)
evaluated = expression.eval()

# Get the Python value
print(evaluated.value)
```

Sometimes expressions contain references to variables or functions.  In order for these to be resolved, one must pass a lookup function and an implementation of the functions that you want to support:

```python
import wdl
from wdl.values import WdlInteger, WdlUndefined

def test_lookup(identifier):
    if identifier == 'var':
        return WdlInteger(4)
    else:
        return WdlUndefined

def test_functions():
    def add_one(parameters):
        # assume at least one parameter exists, for simplicity
        return WdlInteger(parameters[0].value + 1)
    def get_function(name):
        if name == 'add_one': return add_one
        else: raise EvalException("Function {} not defined".format(name))
    return get_function

# WdlInteger(12)
print(wdl.parse_expr("var * 3").eval(test_lookup))

# WdlInteger(8)
print(wdl.parse_expr("var + var").eval(test_lookup))

# WdlInteger(9)
print(wdl.parse_expr("add_one(var + var)").eval(test_lookup, test_functions()))
```

# Command Line Usage

```
$ wdl --help
usage: wdl [-h] [--version] [--debug] [--no-color] {run,parse} ...

Workflow Description Language (WDL)

positional arguments:
  {runarse}  WDL Actions
    run        Run you a WDL
    parse      Parse a WDL file, print parse tree

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  --debug      Open the floodgates
  --no-color   Don't colorize output
```

Parse a WDL file:

```
$ wdl parse examples/ex2.wdl
(Document:
  definitions=[
    (Task:
      name=<ex2.wdl:1:6 identifier "c2NhdHRlcl90YXNr">,
      declarations=[],
      sections=[
        (RawCommand:
...
```
