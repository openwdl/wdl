lexer grammar WdlLexer;

channels { WdlComments, SkipChannel }

options {
  superClass = WDLBaseLexer;
}

// Keywords
VERSION: 'version';
CURRENT_VERSION: ('development' | '2.0');
IMPORT: 'import';
WORKFLOW: 'workflow';
TASK: 'task';
STRUCT: 'struct';
SCATTER: 'scatter';
CALL: 'call';
INPUTS: 'inputs';
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
ARRAY: 'Array';
MAP: 'Map';
PAIR: 'Pair';
LEFT: 'left';
RIGHT: 'right';

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
SQUOTE: '\'' {this.StartSQuoteInterpolatedString();};
DQUOTE: '"' {this.StartDQuoteInterpolatedString();};

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

SQuoteTildeString: '~' -> type(SQuoteStringPart);
SQuoteDollarString: '$'  -> type(SQuoteStringPart);
SQuoteCurlyStringCommand: '{' {this.IsAnyInterpolationStart()}? {this.PushCurlBrackOnEnter(1);} -> channel(SkipChannel), pushMode(DEFAULT_MODE);
SQuoteCurlyString: '{' -> type(SQuoteStringPart);
SQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
SQuoteEscapedChar: '\\' . -> type(SQuoteStringPart);
EndSquote: '\'' {this.FinishSQuoteInterpolatedString();} ->  type(SQUOTE);
SQuoteStringPart: ~[$~{\r\n']+;

mode DquoteInterpolatedString;

DQuoteTildeString: '~' -> type(DQuoteStringPart);
DQuoteDollarString: '$' -> type(DQuoteStringPart);
DQuoteCurlyStringCommand: '{' {this.IsAnyInterpolationStart()}? {this.PushCurlBrackOnEnter(1);} -> channel(SkipChannel), pushMode(DEFAULT_MODE);
DQUoteCurlString: '{' -> type(DQuoteStringPart);
DQuoteUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
DQuoteEscapedChar: '\\' . -> type(DQuoteStringPart);
EndDQuote: '"' {this.FinishDQuoteInterpolatedString();}->  type(DQUOTE);
DQuoteStringPart: ~[$~{\r\n"]+;


mode HereDocCommand;

HereDocTildeString: '~' -> type(HereDocStringPart);
HereDocCurlyStringCommand: '{' {this.IsInterpolationStart()}? {this.PushCurlBrackOnEnter(1);} -> channel(SkipChannel), pushMode(DEFAULT_MODE);
HereDocCurlyString: '{' -> type(HereDocStringPart);
HereDocUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
HereDocEscapedChar: '\\' . -> type(HereDocStringPart);
HereDocEscapedEnd: '\\>>>' -> type(HereDocStringPart);
EndHereDocCommand: '>>>' -> popMode;
HereDocEscape: ( '>' | '>>' | '>>>>' '>'*) -> type(HereDocStringPart);
HereDocStringPart: ~[~{>]+;

mode Command;

CommandTildeString: '~'  -> type(CommandStringPart);
CommandDollarString: '$' -> type(CommandStringPart);
CommandCurlyStringCommand: '{' {this.IsAnyInterpolationStart()}? {this.PushCurlBrackOnEnter(1);} -> channel(SkipChannel), pushMode(DEFAULT_MODE);
CommandCurlyString: '{' -> type(CommandStringPart);
EndCommand: '}' {this.PopCurlBrackOnClose();} -> popMode;
CommandUnicodeEscape: '\\u' (HexDigit (HexDigit (HexDigit HexDigit?)?)?)?;
CommandEscapedChar: '\\' . -> type(CommandStringPart);
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




