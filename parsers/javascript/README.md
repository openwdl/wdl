# WDL Parser for JS
 
`wdl_parser.js` is a JavaScript parser for WDL.

Usage example is provided at `sample.js`, which consumes a WDL script and prints AST to console

To run this example make sure that 
* [Node.JS](https://nodejs.org/en/download/) and NPM are installed
* Current folder is `javascript`

Run the following command:

```
#Replace <file.wdl> with a WDL file location. Also test cases could be used e.g. ./tests/cases/0/wdl
node sample.js <file.wdl>
```


# How to generate a parser

To run a generation command make sure that
* [Hermes Parser Generator](https://github.com/scottfrazer/hermes#installation) and all its dependencies are installed
* Current folder is `javascript`

To generate WDL parser run the following command:

```
python hermes generate ../../grammar.hgr --language=javascript --name=wdl --nodejs --header --directory .
```

`wdl_parser.js` will appear in a current folder

# Runnings tests

To tun the tests make sure that 
* [Node.JS](https://nodejs.org/en/download/) and NPM are installed
* Current folder is `javascript/tests`

Install dependencies

```
npm install
```

Run tests

```
npm run test
```

When tests are finished - results will be printed to the console, indicating state of test run for each folder in `javascript/tests/cases/`

Below is an example of a successful test run:

```
JS-WDL Parser
    √ should correctly generate ast for javascript/tests/cases/0 (53ms)
    √ should correctly generate ast for javascript/tests/cases/1
    √ should correctly generate ast for javascript/tests/cases/2
    √ should correctly generate ast for javascript/tests/cases/3
    √ should correctly generate ast for javascript/tests/cases/4
    √ should correctly generate ast for javascript/tests/cases/5


  6 passing (143ms)
```
