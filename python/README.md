PyWDL
=====

A Python implementation of a WDL parser and language bindings.  Also provides a local execution engine.

WARNING
-------

This implementation is out of date with the specification.  It was meant as a prototype and may be updated in the future to make it more robust

For a better implementation of WDL, use [Cromwell](http://github.com/broadinstitute/cromwell).

Installation
------------

PyWDL requires [Python 3](https://www.python.org/downloads/release/python-343/). Install via `setup.py` or via pip and PyPI:

```
$ python setup.py install
$ pip install wdl
```

Usage
-----

### Python Module

```python
import wdl.parser
import wdl.binding

wdl_file = 'examples/5.wdl'
with open(wdl_file) as fp:
    wdl_contents = fp.read()

# Parse source code into abstract syntax tree
ast = wdl.parser.parse(wdl_contents).ast()

# Print out abstract syntax tree
print(ast.dumps(indent=2))

# Access the first task definition, print out its name
first_task_name = ast.attr('definitions')[0].attr('name').source_string

# Use the language bindings to parse WDL into Python objects
wdl_document = wdl.loads(wdl_contents)

for task in wdl_document.tasks:
    task_ast_str = task.ast.dumps(indent=2)
    name = task.name
    command = task.command
    print('Task "{}" has command: {}'.format(name, command))

print(wdl_document.workflows)
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

Run a workflow locally:

```
$ wdl run examples/ex2.wdl --inputs=examples/ex2.json
```

Get a sample JSON file of all the workflow's inputs by omitting the `--inputs` flag.  The runner will calculate the workflow inputs and output a JSON file to fill out

```
$ wdl run examples/ex2.wdl
Your workflow cannot be run because it is missing some inputs!
Use the template below to specify the inputs.  Keep the keys as-is and change the values to match the type specified
Then, pass this file in as the --inputs option:

{
    "wf.files": "array[file]",
    "wf.count": "int"
}
```
