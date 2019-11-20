# WDL JavaScript Parser

This directory provides a parser implemented in javascript. The parser is built on top of the Base [WDLBaseLexer.js](src/WDLBaseLexer.js)

# Requirements
- Node.js
- npm

# Building

Building is easy, simply run npm. This will download all of the libraries required for running the parser as well
as building the parser from the grammar in the parent directory

```bash
npm install
```

# Running tests

There are a number of tests packaged under the `test/` directory. These can be run using npm

```bash
npm test
```
