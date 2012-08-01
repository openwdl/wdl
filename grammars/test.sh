cat 1.wdl | python Lexer.py | python ParserMain.py wdl ast
java Lexer 3.wdl > tokens ; cat tokens | java ParserMain wdl ast
