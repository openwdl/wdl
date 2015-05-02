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

Example usage as a Python module:

```python
import wdl.parser
import wdl.binding

wdl_contents = open("examples/ex1.wdl").read()

ast = wdl.parser.parse(wdl_contents, "ex1.wdl").ast()

# Print out abstract syntax tree
print(ast.dumps(indent=2))

# Access the first task definition, print out its name
print(ast.attr('definitions')[0].attr('name').source_string)

# Use the language bindings
wdl_document = wdl.binding.parse_document(wdl_contents)
print(wdl_document.tasks)
print(wdl_document.workflows)
```
