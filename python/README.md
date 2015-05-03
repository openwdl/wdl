PyWDL
=====

A Python implementation of a WDL parser and language bindings.  Also provides a local execution engine.

Installation
------------

Install via `setup.py` or via pip and PyPI:

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

wdl_file = 'examples/ex2.wdl'
with open(wdl_file) as fp:
    wdl_contents = fp.read()

# Parse source code into abstract syntax tree
ast = wdl.parser.parse(wdl_contents, wdl_file).ast()

# Print out abstract syntax tree
print(ast.dumps(indent=2))

# Access the first task definition, print out its name
print(ast.attr('definitions')[0].attr('name').source_string)

# Use the language bindings
wdl_document = wdl.binding.parse_document(wdl_contents)
print(wdl_document.tasks)
print(wdl_document.workflows)

```

### Command Line Usage

```
$ wdl --help
usage: wdl [-h] [--version] [--debug] [--no-color] {runarse} ...

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
