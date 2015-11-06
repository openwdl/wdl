PyWDL
=====

A Python implementation of a WDL parser and language bindings.

For Scala language bindings, use [Cromwell](http://github.com/broadinstitute/cromwell).

Installation
------------

PyWDL will work with Python 2 or Python 3. Install via `setup.py` or via pip and PyPI:

```
$ python setup.py install
$ pip install wdl
```

Usage
-----

### Python Module

PyWDL can be used as a Python module by importing the `wdl` package and loading a string with `wdl.loads("wdl code")` or from a file-like object using `wdl.load(fp, resource_name)`.

For example:

```python
import wdl

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
wdl_document = wdl.loads(wdl_code)

for workflow in wdl_document.workflows:
    print('Workflow "{}":'.format(workflow.name))
    for call in workflow.calls():
        print('    Call: {} (task {})'.format(call.name, call.task.name))

for task in wdl_document.tasks:
    name = task.name
    abstract_command = task.command
    instantated_command = task.command.instantiate(params={
        'file': '/path/to/file.txt'
    })
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

#### Working with expressions

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
from wdl.binding import WdlIntegerValue

def test_lookup(identifier):
    if identifier == 'var':
        return WdlIntegerValue(4)
    else:
        return WdlUndefined

def test_functions():
    def add_one(parameters):
        if len(parameters) != 1 or not parameters[0].__class__ in [WdlIntegerValue]:
            raise EvalException("add_one(): expecting one Integer parameter")
        return WdlIntegerValue(parameters[0].value + 1)
    def get_function(name):
        if name == 'add_one': return add_one
        else: raise EvalException("Function {} not defined".format(name))
    return get_function

# WdlIntegerValue(12)
print(wdl.parse_expr("var * 3").eval(test_lookup))

# WdlIntegerValue(8)
print(wdl.parse_expr("var + var").eval(test_lookup))

# WdlIntegerValue(9)
print(wdl.parse_expr("add_one(var + var)").eval(test_lookup, test_functions()))
```

### Command Line Usage

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
