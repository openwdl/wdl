# Grammars and Parsers

At the moment, WDL is transitioning away from `Hermes` as its primary grammar definition and parser generation tool and moving
towards [Antlr4](https://www.antlr.org/). The motivation for this transition was to provide a grammar language which would 
be more familiar to more people as well as employing a well supported and actively developed tool for generating the parsers.
Antlr4 grammars are written as an EBNF and the tool itself supports 9 different target languages currently. 

Please note that hermes grammars will be removed from the specification at some point in the future, and this feature should
be considered deprecated.

