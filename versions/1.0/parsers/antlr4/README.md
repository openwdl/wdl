# ANTLR Grammars and Parsers

This directory contains the grammars ([WdlLexer.g4](WdlLexer.g4)[WdlParser.g4](WdlParser.g4)) which define the WDL specification for the current development
version. The grammars are written as an [EBNF](https://tomassetti.me/ebnf/) using ANTLR4 and aim to be easily readable and accessible for new contributors. 

## Getting Started

[ANTLR](https://github.com/antlr/antlr4) is a widely used and supported parser generator for reading, processing and executing structured text. It defines both a grammar syntax and a tool kit
for producing parsers of a variety different languages. It is very feature rich and is actively developed and maintained by an active community of contributors.

ANTLR is written in java, but has a variety of other runtime libraries that enable it to be used to generate parses in 8 different languages.


### Requirements:

- Java(7+)
- antlr4
- Python3 if you plan on building the python targets
- Node.js (0.12.7) if you plan on building the JavaScript targets
- The [runtimes](https://github.com/antlr/antlr4/blob/master/doc/targets.md) for each target you wish to build.

### Resources:

- [ANTLR4 Github](https://github.com/antlr/antlr4)
- [Mega Tutorial](https://tomassetti.me/antlr-mega-tutorial/)
- [Grammar Examples](https://github.com/antlr/grammars-v4)
- [Definitive Reference](https://www.oreilly.com/library/view/the-definitive-antlr/9781941222621/)


# Getting Started

To install ANTRL4 locally, please follow the [getting started guide](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

# The Grammar

The grammar is divided into two distinct components, a [Lexer](WdlLexer.g4) and a  [Parser](WdlParser.g4). The Lexer is used to define the vocabulary which describes the WDL language in a series of tokens. The parser defines a set of rules which uses the token vocabulary to derive a parse tree of an input script of file. 

## Parsers

The grammars themselves cannot be used to parse a WDL as is, they first must be converted into a parser in one of the supported target languages. Currently
Java, Python3, and JavaScript are supported. For Python and JavaScript you can use the `antlr4` command line tool to generate the required code that is used in the Parsers. For the java target, the easiest way to generate the code is to use the `mvn` plugin defined directly within the `pom.xml`. 

For each language please refer to the corresponding directory for build instructions

### Contributing new Target Languages

Adding new language support for additional targets is relatively easy. Simply select one fo the 8 languages supported by `ANTLR` create a new directory, and then implement the `WDLBaseLexer` in that language according. If the target language does not use `this` or `self` then you may need to add a new `lexer` with the appropriate instance references.

## Visitors and Listeners

ANTLR Provides two different types of ways to interact with the parser, Listeners and Visitors. Both of these classes are implemented during the build step for each language as stubs. Listeners allow you to do an action upon entering a rule, whereas Visitors allow you to transform the output and return something different.

If you would like to use either the listener or visitor, you will need to extend the base classes that are generated and implement the methods that you require.
For some more information on how listeners and visitors work, please see the following resources:

- [Listeners](https://github.com/antlr/antlr4/blob/master/doc/listeners.md) 

# Testing

Each Language describes how to run its own tests. The tests all use the [example files](examples) to test out the parser's ability to lex and parse a document. Currently, there are two sets of simple tests implemented for each language, parse success and parse failure tests.
 
 When run, each language will list the examples directory. All files ending in `.wdl` will be expected to parse properly, while all files ending in `.error` will be expected to fail.
 
 Additional test cases can easily be added by adding a new `.wdl` or `wdl.error` file to the examples directory. Additionally, tests may be added to each language according to the specific specification they are using. its important to note, that tests are a Work in progress and will only get better over time