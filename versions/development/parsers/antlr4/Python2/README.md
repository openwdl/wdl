# WDL Python2 Parser

This directory provides a parser implemented in Python2. The parser is built on top of the Base [WDLBaseLexer.py](WdlParser/WDLBaseLexer.py)

# Requirements
- python2

# Installing the runtime

```bash
pip install antlr4-python2-runtime
```

# Building


Building is easy, simply run make. This will generate the grammar, as well as run the python setup.py install command

```bash
make
```

# Running tests

There are a number of tests packaged under the `test/` directory. These can be run using npm

```bash
make test
```
