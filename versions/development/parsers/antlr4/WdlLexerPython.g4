lexer grammar WdlLexerPython;

channels { WdlComments, SkipChannel }

options {
  superClass = WDLBaseLexer;
}

// Keywords
VERSION: 'version' ' '+ 'development';
IMPORT: 'import';
WORKFLOW: 'workflow';
TASK: 'task';
STRUCT: 'struct';
SCATTER: 'scatter';
CALL: 'call';
IF: 'if';
THEN: 'then';
ELSE: 'else';
ALIAS: 'alias';
AS: 'as';
In: 'in';
INPUT: 'input';
OUTPUT: 'output';
PARAMETERMETA: 'parameter_meta';
META: 'meta';
COMMAND: 'command';
HINTS: 'hints';
RUNTIME: 'runtime';
RUNTIMECPU: 'cpu';
RUNTIMECONTAINER: 'container';
RUNTIMEMEMORY: 'memory';
RUNTIMEGPU: 'gpu';
RUNTIMEDISKS: 'disks';
RUNTIMEMAXRETRIES: 'maxRetries';
RUNTIMERETURNCODES: 'returnCodes';
BOOLEAN: 'Boolean';
INT: 'Int';
FLOAT: 'Float';
STRING: 'String';
FILE: 'File';
DIRECTORY: 'Directory';
ARRAY: 'Array';
MAP: 'Map';
PAIR: 'Pair';
LEFT: 'left';
RIGHT: 'right';
AFTER: 'after';

// Symbols
LPAREN: '(';
RPAREN: ')';
LBRACE
  : '{' {this.IsCommand()}? {this.PushCommandAndBrackEnter();}
  | '{' {this.PushCurlBrackOnEnter(0);}
  ;
RBRACE: '}' {this.PopModeOnCurlBracketClose();};
LBRACK: '[';
RBRACK: ']';
ESC: '\\';
COLON: ':';
LT: '<';
GT: '>';
GTE: '>=';
LTE: '<=';
EQUALITY: '==';
NOTEQUAL: '!=';
EQUAL: '=';
AND: '&&';
OR: '||';
OPTIONAL: '?';
STAR: '*';
PLUS: '+';
MINUS: '-';
DOLLAR: '$';
COMMA: ',';
SEMI: ';';
DOT: '.';
NOT: '!';
TILDE: '~';
DIVIDE: '/';
MOD: '%';
HEREDOCSTART: '<<<' -> pushMode(HereDocCommand);
SQUOTE: '\'' -> pushMode(SquoteInterpolatedString);
DQUOTE: '"' -> pushMode(DquoteInterpolatedString);

// Primitive Literals
NONELITERAL: 'None';
IntLiteral
	: Digits
	| SignedDigits
	;
FloatLiteral
	: FloatFragment
	| SignedFloatFragment
	;
BoolLiteral
	: 'true'
	| 'false'
	;


WHITESPACE
	: [ \t\r\n]+ -> channel(HIDDEN)
	;

COMMENT
	: '#' ~[\r\n]* -> channel(HIDDEN)
	;

Identifier: CompleteIdentifier ( DOT CompleteIdentifier)*;


mode SquoteInterpolatedString;


SQuoteEscapedChar: '\\' . -> type(SQuoteStringPart);
SQuoteDollarString: '$'  -> type(SQuoteStringPart);
SQuoteTildeString: '~' -> type(SQuoteStringPart);
SQuoteCurlyString: '{' -> type(SQuoteStringPart);
SQuoteCommandStart: ('${' | '~{' ) {this.PushCurlBrackOnEnter(1);} -> pushMode(DEFAULT_MODE);
SQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
EndSquote: '\'' ->  popMode, type(SQUOTE);
SQuoteStringPart: ~[$~{\r\n']+;

mode DquoteInterpolatedString;

DQuoteEscapedChar: '\\' . -> type(DQuoteStringPart);
DQuoteTildeString: '~' -> type(DQuoteStringPart);
DQuoteDollarString: '$' -> type(DQuoteStringPart);
DQUoteCurlString: '{' -> type(DQuoteStringPart);
DQuoteCommandStart: ('${' | '~{' ) {this.PushCurlBrackOnEnter(1);} -> pushMode(DEFAULT_MODE);
DQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
EndDQuote: '"' ->  popMode, type(DQUOTE);
DQuoteStringPart: ~[$~{\r\n"]+;


mode HereDocCommand;

HereDocUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
HereDocEscapedChar: '\\' . -> type(HereDocStringPart);
HereDocTildeString: '~' -> type(HereDocStringPart);
HereDocCurlyString: '{' -> type(HereDocStringPart);
HereDocCurlyStringCommand: ('${' | '~{' ) {this.PushCurlBrackOnEnter(1);} -> pushMode(DEFAULT_MODE);
HereDocEscapedEnd: '\\>>>' -> type(HereDocStringPart);
EndHereDocCommand: '>>>' -> popMode;
HereDocEscape: ( '>' | '>>' | '>>>>' '>'*) -> type(HereDocStringPart);
HereDocStringPart: ~[~{>]+;

mode Command;

CommandEscapedChar: '\\' . -> type(CommandStringPart);
CommandUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
CommandTildeString: '~'  -> type(CommandStringPart);
CommandDollarString: '$' -> type(CommandStringPart);
CommandCurlyString: '{' -> type(CommandStringPart);
CommandCurlyStringCommand:  ('${' | '~{' ) {this.PushCurlBrackOnEnter(1);} -> pushMode(DEFAULT_MODE);
EndCommand: '}' {this.PopCurlBrackOnClose();} -> popMode;
CommandStringPart: ~[$~{}]+;


// Fragments

fragment CompleteIdentifier
	: IdentifierStart IdentifierFollow*
	;

fragment IdentifierStart
	: [a-zA-Z]
	;

fragment IdentifierFollow
	: [a-zA-Z0-9_]+
	;

fragment EscapeSequence
    : '\\' [btnfr"'\\]
    | '\\' ([0-3]? [0-7])? [0-7]
    | '\\' UnicodeEsc
    ;

fragment UnicodeEsc
   : 'u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?
   ;

fragment HexDigit
   : [0-9a-fA-F]
   ;

fragment Digit
	: [0-9]
	;

fragment Digits
	: Digit+
	;

fragment Decimals
	: Digits '.' Digits? | '.' Digits
	;

fragment SignedDigits
	: ('+' | '-' ) Digits
	;

fragment FloatFragment
	: Digits EXP?
	| Decimals EXP?
	;

fragment SignedFloatFragment
	: ('+' |'e') FloatFragment
	;

fragment EXP
	: ('e'|'E') SignedDigits
	;




