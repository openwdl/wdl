lexer grammar Draft2WdlLexer;

channels { WdlComments, SkipChannel }

// Keywords
IMPORT: 'import';
WORKFLOW: 'workflow';
TASK: 'task';
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

HEREDOC_COMMAND: 'command' ' '* '<<<' -> pushMode(HereDocCommand);
COMMAND: 'command' ' '* '{' -> pushMode(Command);

RUNTIME: 'runtime';
BOOLEAN: 'Boolean';
INT: 'Int';
FLOAT: 'Float';
STRING: 'String';
FILE: 'File';
ARRAY: 'Array';
MAP: 'Map';
PAIR: 'Pair';
OBJECT: 'Object';
OBJECT_LITERAL: 'object';

SEP: 'sep';
DEFAULT: 'default';


// Primitive Literals
IntLiteral
	: Digits
	| SignedDigits
	;
FloatLiteral
	: SignedFloatFragment
	| FloatFragment
	;
BoolLiteral
	: 'true'
	| 'false'
	;

// Symbols
LPAREN: '(';
RPAREN: ')';
LBRACE: '{' -> pushMode(DEFAULT_MODE);
RBRACE: '}' -> popMode;
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
DIVIDE: '/';
MOD: '%';
SQUOTE: '\'' -> pushMode(SquoteInterpolatedString);
DQUOTE: '"' -> pushMode(DquoteInterpolatedString);

WHITESPACE
	: [ \t\r\n]+ -> channel(HIDDEN)
	;

COMMENT
	: '#' ~[\r\n]* -> channel(HIDDEN)
	;

Identifier: CompleteIdentifier;


mode SquoteInterpolatedString;


SQuoteEscapedChar: '\\' . -> type(StringPart);
SQuoteDollarString: '$'  -> type(StringPart);
SQuoteCurlyString: '{' -> type(StringPart);
SQuoteCommandStart: ('${') -> pushMode(DEFAULT_MODE) , type(StringCommandStart);
SQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)? -> type(StringPart);
EndSquote: '\'' ->  popMode, type(SQUOTE);
StringPart: ~[${\r\n']+;

mode DquoteInterpolatedString;

DQuoteEscapedChar: '\\' . -> type(StringPart);
DQuoteDollarString: '$' -> type(StringPart);
DQUoteCurlString: '{' -> type(StringPart);
DQuoteCommandStart: ('${') -> pushMode(DEFAULT_MODE), type(StringCommandStart);
DQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?) -> type(StringPart);
EndDQuote: '"' ->  popMode, type(DQUOTE);
DQuoteStringPart: ~[${\r\n"]+ -> type(StringPart);


mode HereDocCommand;

HereDocUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
HereDocEscapedChar: '\\' . -> type(CommandStringPart);
HereDocCurlyString: '{' -> type(CommandStringPart);
HereDocEscapedEnd: '\\>>>' -> type(CommandStringPart);
EndHereDocCommand: '>>>' -> popMode, type(EndCommand);
HereDocEscape: ( '>' | '>>' | '>>>>' '>'*) -> type(CommandStringPart);
HereDocStringPart: ~[{>]+ -> type(CommandStringPart);

mode Command;

CommandEscapedChar: '\\' . -> type(CommandStringPart);
CommandUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
CommandDollarString: '$' -> type(CommandStringPart);
CommandCurlyString: '{' -> type(CommandStringPart);
StringCommandStart:  ('${') -> pushMode(DEFAULT_MODE);
EndCommand: '}' -> popMode;
CommandStringPart: ~[${}]+;

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