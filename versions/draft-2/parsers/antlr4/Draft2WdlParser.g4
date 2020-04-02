parser grammar Draft2WdlParser;


options { tokenVocab=Draft2WdlLexer; }


map_type
	: MAP LBRACK wdl_type COMMA wdl_type RBRACK
	;

array_type
	: ARRAY LBRACK wdl_type RBRACK PLUS?
	;

pair_type
	: PAIR LBRACK wdl_type COMMA wdl_type RBRACK
	;

type_base
	: array_type
	| map_type
	| pair_type
	| (STRING | FILE | BOOLEAN | OBJECT | INT | FLOAT)
	;

wdl_type
  : (type_base OPTIONAL | type_base)
  ;


unbound_decls
	: wdl_type Identifier
	;

bound_decls
	: wdl_type Identifier EQUAL expr
	;

any_decls
	: unbound_decls
	| bound_decls
	;

number
	: IntLiteral
	| FloatLiteral
	;

expression_placeholder_option
  : BoolLiteral EQUAL (string | number)
  | DEFAULT EQUAL (string | number)
  | SEP EQUAL (string | number)
  ;


string_part
  : StringPart*
  ;

string_expr_part
  : StringCommandStart (expression_placeholder_option)* expr RBRACE
  ;

string_expr_with_string_part
  : string_expr_part string_part
  ;

string
  : DQUOTE string_part string_expr_with_string_part* DQUOTE
  | SQUOTE string_part string_expr_with_string_part* SQUOTE
  ;

primitive_literal
	: BoolLiteral
	| number
	| string
	| Identifier
	;

expr
	: expr_infix
	;

expr_infix
	: expr_infix0 #infix0
	;

expr_infix0
	: expr_infix0 OR expr_infix1 #lor
	| expr_infix1 #infix1
	;

expr_infix1
	: expr_infix1 AND expr_infix2 #land
	| expr_infix2 #infix2
	;

expr_infix2
	: expr_infix2 EQUALITY expr_infix3 #eqeq
	| expr_infix2 NOTEQUAL expr_infix3 #neq
	| expr_infix2 LTE expr_infix3 #lte
	| expr_infix2 GTE expr_infix3 #gte
	| expr_infix2 LT expr_infix3 #lt
	| expr_infix2 GT expr_infix3 #gt
	| expr_infix3 #infix3
	;

expr_infix3
	: expr_infix3 PLUS expr_infix4 #add
	| expr_infix3 MINUS expr_infix4 #sub
	| expr_infix4 #infix4
	;

expr_infix4
	: expr_infix4 STAR expr_infix5 #mul
	| expr_infix4 DIVIDE expr_infix5 #divide
	| expr_infix4 MOD expr_infix5 #mod
	| expr_infix5 #infix5
	;

expr_infix5
	: expr_core
	;

expr_core
	: LPAREN expr RPAREN #expression_group
	| primitive_literal #primitives
	| LBRACK (expr (COMMA expr)*)* RBRACK #array_literal
	| LPAREN expr COMMA expr RPAREN #pair_literal
	| LBRACE (expr COLON expr (COMMA expr COLON expr)*)* RBRACE #map_literal
	| OBJECT_LITERAL LBRACE (Identifier COLON expr (COMMA Identifier COLON expr)*)* RBRACE #object_literal
	| NOT expr #negate
	| (PLUS | MINUS) expr #unirarysigned
	| expr_core LBRACK expr RBRACK #at
	| IF expr THEN expr ELSE expr #ifthenelse
	| Identifier LPAREN (expr (COMMA expr)*)? RPAREN #apply
	| Identifier #left_name
	| expr_core DOT Identifier #get_name
	;

import_alias
	: ALIAS Identifier AS Identifier
	;

import_as
    : AS Identifier
    ;

import_doc
	: IMPORT string import_as? (import_alias)*
	;

meta_kv
	: Identifier COLON string
	;


parameter_meta
	: PARAMETERMETA LBRACE meta_kv* RBRACE
	;

meta
    :  META LBRACE meta_kv* RBRACE
    ;

task_runtime_kv
    : Identifier COLON expr
	;

task_runtime
	: RUNTIME LBRACE (task_runtime_kv)* RBRACE
	;

task_input
	: (any_decls)*
	;

task_output
	: OUTPUT LBRACE (bound_decls)* RBRACE
	;

task_command_string_part
    : CommandStringPart*
    ;

task_command_expr_part
    : StringCommandStart  (expression_placeholder_option)* expr RBRACE
    ;

task_command_expr_with_string
    : task_command_expr_part task_command_string_part
    ;

task_command
  : COMMAND task_command_string_part task_command_expr_with_string* EndCommand
  | HEREDOC_COMMAND task_command_string_part task_command_expr_with_string* EndCommand
  ;

task_element
  : task_output
  | task_command
  | task_runtime
  | parameter_meta
  | meta
  | any_decls
  ;

task
	: TASK Identifier LBRACE task_input (task_element)+ RBRACE
	;


inner_workflow_element
	: bound_decls
	| call
	| scatter
	| conditional
	;

call_alias
	: AS Identifier
	;

call_input
	: Identifier EQUAL expr
	;

call_inputs
	: INPUT COLON (call_input (COMMA call_input)*)
	;

call_body
	: LBRACE call_inputs? RBRACE
	;

call
	: CALL Identifier call_alias?  call_body?
	;


scatter
	: SCATTER LPAREN Identifier In expr RPAREN LBRACE inner_workflow_element* RBRACE
	;

conditional
	: IF LPAREN expr RPAREN LBRACE inner_workflow_element* RBRACE
	;

workflow_input
	: (any_decls)*
	;

workflow_output
	: OUTPUT LBRACE (bound_decls)* RBRACE
	;

workflow_element
  : workflow_output #output
  | inner_workflow_element #inner_element
  | parameter_meta #parameter_meta_element
  | meta #meta_element
  ;

workflow
	: WORKFLOW Identifier LBRACE workflow_input workflow_element* RBRACE
	;

document_element
	: import_doc
	| task
	;

document
	: document_element* (workflow document_element*)? EOF
	;