import sys
import os
import re
import base64
import argparse
import json
from collections import OrderedDict
# Common Code #
def parse_tree_string(parsetree, indent=None, b64_source=True, indent_level=0):
    indent_str = (' ' * indent * indent_level) if indent else ''
    if isinstance(parsetree, ParseTree):
        children = [parse_tree_string(child, indent, b64_source, indent_level+1) for child in parsetree.children]
        if indent is None or len(children) == 0:
            return '{0}({1}: {2})'.format(indent_str, parsetree.nonterminal, ', '.join(children))
        else:
            return '{0}({1}:\n{2}\n{3})'.format(
                indent_str,
                parsetree.nonterminal,
                ',\n'.join(children),
                indent_str
            )
    elif isinstance(parsetree, Terminal):
        return indent_str + parsetree.dumps(b64_source=b64_source)
def ast_string(ast, indent=None, b64_source=True, indent_level=0):
    indent_str = (' ' * indent * indent_level) if indent else ''
    next_indent_str = (' ' * indent * (indent_level+1)) if indent else ''
    if isinstance(ast, Ast):
        children = OrderedDict([(k, ast_string(v, indent, b64_source, indent_level+1)) for k, v in ast.attributes.items()])
        if indent is None:
            return '({0}: {1})'.format(
                ast.name,
                ', '.join('{0}={1}'.format(k, v) for k, v in children.items())
            )
        else:
            return '({0}:\n{1}\n{2})'.format(
                ast.name,
                ',\n'.join(['{0}{1}={2}'.format(next_indent_str, k, v) for k, v in children.items()]),
                indent_str
            )
    elif isinstance(ast, list):
        children = [ast_string(element, indent, b64_source, indent_level+1) for element in ast]
        if indent is None or len(children) == 0:
            return '[{0}]'.format(', '.join(children))
        else:
            return '[\n{1}\n{0}]'.format(
                indent_str,
                ',\n'.join(['{0}{1}'.format(next_indent_str, child) for child in children]),
            )
    elif isinstance(ast, Terminal):
        return ast.dumps(b64_source=b64_source)
class Terminal:
  def __init__(self, id, str, source_string, resource, line, col):
      self.__dict__.update(locals())
  def getId(self):
      return self.id
  def ast(self):
      return self
  def dumps(self, b64_source=True, json=False, **kwargs):
      if not b64_source and json:
          raise Exception('b64_source must be set to True if json=True')
      source_string = base64.b64encode(self.source_string.encode('utf-8')).decode('utf-8') if b64_source else self.source_string
      if json:
          json_fmt = '"terminal": "{0}", "resource": "{1}", "line": {2}, "col": {3}, "source_string": "{4}"'
          return '{' + json_fmt.format(self.str, self.resource, self.line, self.col, source_string) + '}'
      else:
          return '<{} (line {} col {}) `{}`>'.format(self.str, self.line, self.col, source_string)
  def __str__(self):
      return self.dumps()
class NonTerminal():
  def __init__(self, id, str):
    self.__dict__.update(locals())
    self.list = False
  def __str__(self):
    return self.str
class AstTransform:
  pass
class AstTransformSubstitution(AstTransform):
  def __init__(self, idx):
    self.__dict__.update(locals())
  def __repr__(self):
    return '$' + str(self.idx)
  def __str__(self):
    return self.__repr__()
class AstTransformNodeCreator(AstTransform):
  def __init__( self, name, parameters ):
    self.__dict__.update(locals())
  def __repr__( self ):
    return self.name + '( ' + ', '.join(['%s=$%s' % (k,str(v)) for k,v in self.parameters.items()]) + ' )'
  def __str__(self):
    return self.__repr__()
class AstList(list):
  def ast(self):
      retval = []
      for ast in self:
          retval.append(ast.ast())
      return retval
  def dumps(self, indent=None, b64_source=True):
      args = locals()
      del args['self']
      return ast_string(self, **args)
class ParseTree():
  def __init__(self, nonterminal):
      self.__dict__.update(locals())
      self.children = []
      self.astTransform = None
      self.isExpr = False
      self.isNud = False
      self.isPrefix = False
      self.isInfix = False
      self.nudMorphemeCount = 0
      self.isExprNud = False # true for rules like _expr := {_expr} + {...}
      self.listSeparator = None
      self.list = False
  def add( self, tree ):
      self.children.append( tree )
  def ast( self ):
      if self.list == 'slist' or self.list == 'nlist':
          if len(self.children) == 0:
              return AstList()
          offset = 1 if self.children[0] == self.listSeparator else 0
          first = self.children[offset].ast()
          r = AstList()
          if first is not None:
              r.append(first)
          r.extend(self.children[offset+1].ast())
          return r
      elif self.list == 'otlist':
          if len(self.children) == 0:
              return AstList()
          r = AstList()
          if self.children[0] != self.listSeparator:
              r.append(self.children[0].ast())
          r.extend(self.children[1].ast())
          return r
      elif self.list == 'tlist':
          if len(self.children) == 0:
              return AstList()
          r = AstList([self.children[0].ast()])
          r.extend(self.children[2].ast())
          return r
      elif self.list == 'mlist':
          r = AstList()
          if len(self.children) == 0:
              return r
          lastElement = len(self.children) - 1
          for i in range(lastElement):
              r.append(self.children[i].ast())
          r.extend(self.children[lastElement].ast())
          return r
      elif self.isExpr:
          if isinstance(self.astTransform, AstTransformSubstitution):
              return self.children[self.astTransform.idx].ast()
          elif isinstance(self.astTransform, AstTransformNodeCreator):
              parameters = OrderedDict()
              for name, idx in self.astTransform.parameters.items():
                  if idx == '$':
                      child = self.children[0]
                  elif isinstance(self.children[0], ParseTree) and \
                       self.children[0].isNud and \
                       not self.children[0].isPrefix and \
                       not self.isExprNud and \
                       not self.isInfix:
                      if idx < self.children[0].nudMorphemeCount:
                          child = self.children[0].children[idx]
                      else:
                          index = idx - self.children[0].nudMorphemeCount + 1
                          child = self.children[index]
                  elif len(self.children) == 1 and not isinstance(self.children[0], ParseTree) and not isinstance(self.children[0], list):
                      return self.children[0]
                  else:
                      child = self.children[idx]
                  parameters[name] = child.ast()
              return Ast(self.astTransform.name, parameters)
      else:
          if isinstance(self.astTransform, AstTransformSubstitution):
              return self.children[self.astTransform.idx].ast()
          elif isinstance(self.astTransform, AstTransformNodeCreator):
              parameters = OrderedDict()
              for name, idx in self.astTransform.parameters.items():
                  parameters[name] = self.children[idx].ast()
              return Ast(self.astTransform.name, parameters)
          elif len(self.children):
              return self.children[0].ast()
          else:
              return None
  def dumps(self, indent=None, b64_source=True):
      args = locals()
      del args['self']
      return parse_tree_string(self, **args)
class Ast():
    def __init__(self, name, attributes):
        self.__dict__.update(locals())
    def attr(self, attr):
        return self.attributes[attr]
    def dumps(self, indent=None, b64_source=True):
        args = locals()
        del args['self']
        return ast_string(self, **args)
class SyntaxError(Exception):
    def __init__(self, message):
        self.__dict__.update(locals())
    def __str__(self):
        return self.message
class TokenStream(list):
    def __init__(self, arg=[]):
        super().__init__(arg)
        self.index = 0
    def advance(self):
        self.index += 1
        return self.current()
    def last(self):
        return self[-1]
    def json(self):
        if len(self) == 0:
            return '[]'
        tokens_json = []
        json_fmt = '"terminal": "{terminal}", "resource": "{resource}", "line": {line}, "col": {col}, "source_string": "{source_string}"'
        for token in self:
            tokens_json.append(token.dumps(json=True, b64_source=True))
        return '[\n    ' + ',\n    '.join(tokens_json) + '\n]'
    def current(self):
        try:
            return self[self.index]
        except IndexError:
            return None
class DefaultSyntaxErrorHandler:
    def __init__(self):
        self.errors = []
    def _error(self, string):
        error = SyntaxError(string)
        self.errors.append(error)
        return error
    def unexpected_eof(self):
        return self._error("Error: unexpected end of file")
    def excess_tokens(self):
        return self._error("Finished parsing without consuming all tokens.")
    def unexpected_symbol(self, nonterminal, actual_terminal, expected_terminals, rule):
        return self._error("Unexpected symbol (line {line}, col {col}) when parsing parse_{nt}.  Expected {expected}, got {actual}.".format(
            line=actual_terminal.line,
            col=actual_terminal.col,
            nt=nonterminal,
            expected=', '.join(expected_terminals),
            actual=actual_terminal
        ))
    def no_more_tokens(self, nonterminal, expected_terminal, last_terminal):
        return self._error("No more tokens.  Expecting " + expected_terminal)
    def invalid_terminal(self, nonterminal, invalid_terminal):
        return self._error("Invalid symbol ID: {} ({})".format(invalid_terminal.id, invalid_terminal.string))
    def unrecognized_token(self, string, line, col):
        lines = string.split('\n')
        bad_line = lines[line-1]
        return self._error('Unrecognized token on line {}, column {}:\n\n{}\n{}'.format(
            line, col, bad_line, ''.join([' ' for x in range(col-1)]) + '^'
        ))
class ParserContext:
  def __init__(self, tokens, errors):
    self.__dict__.update(locals())
    self.nonterminal_string = None
    self.rule_string = None
# Parser Code #
terminals = {
    0: 'command',
    1: 'rsquare',
    2: 'rbrace',
    3: 'qmark',
    4: 'type',
    5: 'runtime',
    6: 'outputs',
    7: 'task',
    8: 'identifier',
    9: 'cmd_param_end',
    10: 'cmd_part',
    11: 'lbrace',
    12: 'cmd_attr_hint',
    13: 'equals',
    14: 'colon',
    15: 'string',
    16: 'cmd_param_start',
    17: 'lsquare',
    18: 'asterisk',
    19: 'arrow',
    'command': 0,
    'rsquare': 1,
    'rbrace': 2,
    'qmark': 3,
    'type': 4,
    'runtime': 5,
    'outputs': 6,
    'task': 7,
    'identifier': 8,
    'cmd_param_end': 9,
    'cmd_part': 10,
    'lbrace': 11,
    'cmd_attr_hint': 12,
    'equals': 13,
    'colon': 14,
    'string': 15,
    'cmd_param_start': 16,
    'lsquare': 17,
    'asterisk': 18,
    'arrow': 19,
}
# table[nonterminal][terminal] = rule
table = [
    [-1, -1, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, 19, -1, -1, -1, -1, 18, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1],
    [-1, -1, 29, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, -1],
    [-1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, -1, 1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, -1, -1, -1],
    [-1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, -1],
    [3, -1, -1, -1, -1, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1, -1, 10, -1, -1, -1],
    [-1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1],
    [-1, -1, 7, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, 6, -1, -1, -1],
    [-1, -1, -1, 13, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1],
]
nonterminal_first = {
    20: [15, -1],
    21: [12],
    22: [8],
    23: [-1, 17],
    24: [16],
    25: [8, -1],
    26: [7],
    27: [17],
    28: [5],
    29: [0],
    30: [0, 6, -1, 5],
    31: [6],
    32: [-1, 12],
    33: [15],
    34: [3, 18],
    35: [0, 6, 5],
    36: [10, 16],
    37: [15, 4],
    38: [10, 16, -1],
    39: [-1, 3, 18],
}
nonterminal_follow = {
    20: [2],
    21: [8, 12],
    22: [8, 2],
    23: [8, 12],
    24: [10, 16, 2],
    25: [2],
    26: [-1],
    27: [8, 12],
    28: [0, 2, 5, 6],
    29: [0, 2, 5, 6],
    30: [2],
    31: [0, 2, 5, 6],
    32: [8],
    33: [15, 2],
    34: [9],
    35: [0, 6, 2, 5],
    36: [10, 16, 2],
    37: [8, 12],
    38: [2],
    39: [9],
}
rule_first = {
    0: [0, 6, 5],
    1: [-1],
    2: [7],
    3: [0],
    4: [6],
    5: [5],
    6: [10, 16],
    7: [-1],
    8: [0],
    9: [10],
    10: [16],
    11: [12],
    12: [-1],
    13: [3, 18],
    14: [-1],
    15: [16],
    16: [12],
    17: [15],
    18: [17],
    19: [-1],
    20: [4],
    21: [17],
    22: [3],
    23: [18],
    24: [15],
    25: [-1],
    26: [6],
    27: [15],
    28: [8],
    29: [-1],
    30: [5],
    31: [8],
}
nonterminal_rules = {
    20: [
        "$_gen5 = $output_kv $_gen5",
        "$_gen5 = :_empty",
    ],
    21: [
        "$cmd_param_kv = :cmd_attr_hint :identifier :equals $cmd_param_value -> CommandParameterAttr( key=$1, value=$3 )",
    ],
    22: [
        "$runtime_kv = :identifier :colon :string -> RuntimeAttribute( key=$0, value=$2 )",
    ],
    23: [
        "$_gen4 = $sub_type",
        "$_gen4 = :_empty",
    ],
    24: [
        "$cmd_param = :cmd_param_start $_gen2 :identifier $_gen3 :cmd_param_end -> CommandParameter( name=$2, attributes=$1, qualifier=$3 )",
    ],
    25: [
        "$_gen6 = $runtime_kv $_gen6",
        "$_gen6 = :_empty",
    ],
    26: [
        "$task = :task :identifier :lbrace $_gen0 :rbrace -> Task( name=$1, sections=$3 )",
    ],
    27: [
        "$sub_type = :lsquare :type :rsquare -> $1",
    ],
    28: [
        "$runtime = :runtime :lbrace $_gen6 :rbrace -> RuntimeAttributes( attributes=$0 )",
    ],
    29: [
        "$command = :command :lbrace $_gen1 :rbrace -> Command( parts=$2 )",
    ],
    30: [
        "$_gen0 = $sections $_gen0",
        "$_gen0 = :_empty",
    ],
    31: [
        "$outputs = :outputs :lbrace $_gen5 :rbrace -> Outputs( attributes=$0 )",
    ],
    32: [
        "$_gen2 = $cmd_param_kv $_gen2",
        "$_gen2 = :_empty",
    ],
    33: [
        "$output_kv = :string :arrow :identifier -> OutputAttribute( key=$0, value=$2 )",
    ],
    34: [
        "$qualifier = :qmark",
        "$qualifier = :asterisk",
    ],
    35: [
        "$sections = $command",
        "$sections = $outputs",
        "$sections = $runtime",
    ],
    36: [
        "$command_part = :cmd_part",
        "$command_part = $cmd_param",
    ],
    37: [
        "$cmd_param_value = :string",
        "$cmd_param_value = :type $_gen4 -> Type( name=$0, sub=$1 )",
    ],
    38: [
        "$_gen1 = $command_part $_gen1",
        "$_gen1 = :_empty",
    ],
    39: [
        "$_gen3 = $qualifier",
        "$_gen3 = :_empty",
    ],
}
rules = {
    0: "$_gen0 = $sections $_gen0",
    1: "$_gen0 = :_empty",
    2: "$task = :task :identifier :lbrace $_gen0 :rbrace -> Task( name=$1, sections=$3 )",
    3: "$sections = $command",
    4: "$sections = $outputs",
    5: "$sections = $runtime",
    6: "$_gen1 = $command_part $_gen1",
    7: "$_gen1 = :_empty",
    8: "$command = :command :lbrace $_gen1 :rbrace -> Command( parts=$2 )",
    9: "$command_part = :cmd_part",
    10: "$command_part = $cmd_param",
    11: "$_gen2 = $cmd_param_kv $_gen2",
    12: "$_gen2 = :_empty",
    13: "$_gen3 = $qualifier",
    14: "$_gen3 = :_empty",
    15: "$cmd_param = :cmd_param_start $_gen2 :identifier $_gen3 :cmd_param_end -> CommandParameter( name=$2, attributes=$1, qualifier=$3 )",
    16: "$cmd_param_kv = :cmd_attr_hint :identifier :equals $cmd_param_value -> CommandParameterAttr( key=$1, value=$3 )",
    17: "$cmd_param_value = :string",
    18: "$_gen4 = $sub_type",
    19: "$_gen4 = :_empty",
    20: "$cmd_param_value = :type $_gen4 -> Type( name=$0, sub=$1 )",
    21: "$sub_type = :lsquare :type :rsquare -> $1",
    22: "$qualifier = :qmark",
    23: "$qualifier = :asterisk",
    24: "$_gen5 = $output_kv $_gen5",
    25: "$_gen5 = :_empty",
    26: "$outputs = :outputs :lbrace $_gen5 :rbrace -> Outputs( attributes=$0 )",
    27: "$output_kv = :string :arrow :identifier -> OutputAttribute( key=$0, value=$2 )",
    28: "$_gen6 = $runtime_kv $_gen6",
    29: "$_gen6 = :_empty",
    30: "$runtime = :runtime :lbrace $_gen6 :rbrace -> RuntimeAttributes( attributes=$0 )",
    31: "$runtime_kv = :identifier :colon :string -> RuntimeAttribute( key=$0, value=$2 )",
}
def is_terminal(id): return isinstance(id, int) and 0 <= id <= 19
def parse(tokens, errors=None, start=None):
    if errors is None:
        errors = DefaultSyntaxErrorHandler()
    if isinstance(tokens, str):
        tokens = lex(tokens, '<string>', errors)
    ctx = ParserContext(tokens, errors)
    tree = parse_task(ctx)
    if tokens.current() != None:
        raise ctx.errors.excess_tokens()
    return tree
def expect(ctx, terminal_id):
    current = ctx.tokens.current()
    if not current:
        raise ctx.errors.no_more_tokens(ctx.nonterminal, terminals[terminal_id], ctx.tokens.last())
    if current.id != terminal_id:
        raise ctx.errors.unexpected_symbol(ctx.nonterminal, current, [terminals[terminal_id]], ctx.rule)
    next = ctx.tokens.advance()
    if next and not is_terminal(next.id):
        raise ctx.errors.invalid_terminal(ctx.nonterminal, next)
    return current
def parse__gen5(ctx):
    current = ctx.tokens.current()
    rule = table[0][current.id] if current else -1
    tree = ParseTree(NonTerminal(20, '_gen5'))
    ctx.nonterminal = "_gen5"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[20] and current.id not in nonterminal_first[20]:
        return tree
    if current == None:
        return tree
    if rule == 24: # $_gen5 = $output_kv $_gen5
        ctx.rule = rules[24]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_output_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen5(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_cmd_param_kv(ctx):
    current = ctx.tokens.current()
    rule = table[1][current.id] if current else -1
    tree = ParseTree(NonTerminal(21, 'cmd_param_kv'))
    ctx.nonterminal = "cmd_param_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 16: # $cmd_param_kv = :cmd_attr_hint :identifier :equals $cmd_param_value -> CommandParameterAttr( key=$1, value=$3 )
        ctx.rule = rules[16]
        ast_parameters = OrderedDict([
            ('key', 1),
            ('value', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameterAttr', ast_parameters)
        t = expect(ctx, 12) # :cmd_attr_hint
        tree.add(t)
        t = expect(ctx, 8) # :identifier
        tree.add(t)
        t = expect(ctx, 13) # :equals
        tree.add(t)
        subtree = parse_cmd_param_value(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[21] if x >=0],
      rules[16]
    )
def parse_runtime_kv(ctx):
    current = ctx.tokens.current()
    rule = table[2][current.id] if current else -1
    tree = ParseTree(NonTerminal(22, 'runtime_kv'))
    ctx.nonterminal = "runtime_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 31: # $runtime_kv = :identifier :colon :string -> RuntimeAttribute( key=$0, value=$2 )
        ctx.rule = rules[31]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('RuntimeAttribute', ast_parameters)
        t = expect(ctx, 8) # :identifier
        tree.add(t)
        t = expect(ctx, 14) # :colon
        tree.add(t)
        t = expect(ctx, 15) # :string
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[22] if x >=0],
      rules[31]
    )
def parse__gen4(ctx):
    current = ctx.tokens.current()
    rule = table[3][current.id] if current else -1
    tree = ParseTree(NonTerminal(23, '_gen4'))
    ctx.nonterminal = "_gen4"
    tree.list = False
    if current != None and current.id in nonterminal_follow[23] and current.id not in nonterminal_first[23]:
        return tree
    if current == None:
        return tree
    if rule == 18: # $_gen4 = $sub_type
        ctx.rule = rules[18]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_sub_type(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_cmd_param(ctx):
    current = ctx.tokens.current()
    rule = table[4][current.id] if current else -1
    tree = ParseTree(NonTerminal(24, 'cmd_param'))
    ctx.nonterminal = "cmd_param"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 15: # $cmd_param = :cmd_param_start $_gen2 :identifier $_gen3 :cmd_param_end -> CommandParameter( name=$2, attributes=$1, qualifier=$3 )
        ctx.rule = rules[15]
        ast_parameters = OrderedDict([
            ('name', 2),
            ('attributes', 1),
            ('qualifier', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameter', ast_parameters)
        t = expect(ctx, 16) # :cmd_param_start
        tree.add(t)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        t = expect(ctx, 8) # :identifier
        tree.add(t)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        t = expect(ctx, 9) # :cmd_param_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[24] if x >=0],
      rules[15]
    )
def parse__gen6(ctx):
    current = ctx.tokens.current()
    rule = table[5][current.id] if current else -1
    tree = ParseTree(NonTerminal(25, '_gen6'))
    ctx.nonterminal = "_gen6"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[25] and current.id not in nonterminal_first[25]:
        return tree
    if current == None:
        return tree
    if rule == 28: # $_gen6 = $runtime_kv $_gen6
        ctx.rule = rules[28]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_runtime_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen6(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_task(ctx):
    current = ctx.tokens.current()
    rule = table[6][current.id] if current else -1
    tree = ParseTree(NonTerminal(26, 'task'))
    ctx.nonterminal = "task"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 2: # $task = :task :identifier :lbrace $_gen0 :rbrace -> Task( name=$1, sections=$3 )
        ctx.rule = rules[2]
        ast_parameters = OrderedDict([
            ('name', 1),
            ('sections', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Task', ast_parameters)
        t = expect(ctx, 7) # :task
        tree.add(t)
        t = expect(ctx, 8) # :identifier
        tree.add(t)
        t = expect(ctx, 11) # :lbrace
        tree.add(t)
        subtree = parse__gen0(ctx)
        tree.add(subtree)
        t = expect(ctx, 2) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[26] if x >=0],
      rules[2]
    )
def parse_sub_type(ctx):
    current = ctx.tokens.current()
    rule = table[7][current.id] if current else -1
    tree = ParseTree(NonTerminal(27, 'sub_type'))
    ctx.nonterminal = "sub_type"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 21: # $sub_type = :lsquare :type :rsquare -> $1
        ctx.rule = rules[21]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 17) # :lsquare
        tree.add(t)
        t = expect(ctx, 4) # :type
        tree.add(t)
        t = expect(ctx, 1) # :rsquare
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[27] if x >=0],
      rules[21]
    )
def parse_runtime(ctx):
    current = ctx.tokens.current()
    rule = table[8][current.id] if current else -1
    tree = ParseTree(NonTerminal(28, 'runtime'))
    ctx.nonterminal = "runtime"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 30: # $runtime = :runtime :lbrace $_gen6 :rbrace -> RuntimeAttributes( attributes=$0 )
        ctx.rule = rules[30]
        ast_parameters = OrderedDict([
            ('attributes', 0),
        ])
        tree.astTransform = AstTransformNodeCreator('RuntimeAttributes', ast_parameters)
        t = expect(ctx, 5) # :runtime
        tree.add(t)
        t = expect(ctx, 11) # :lbrace
        tree.add(t)
        subtree = parse__gen6(ctx)
        tree.add(subtree)
        t = expect(ctx, 2) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[28] if x >=0],
      rules[30]
    )
def parse_command(ctx):
    current = ctx.tokens.current()
    rule = table[9][current.id] if current else -1
    tree = ParseTree(NonTerminal(29, 'command'))
    ctx.nonterminal = "command"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 8: # $command = :command :lbrace $_gen1 :rbrace -> Command( parts=$2 )
        ctx.rule = rules[8]
        ast_parameters = OrderedDict([
            ('parts', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Command', ast_parameters)
        t = expect(ctx, 0) # :command
        tree.add(t)
        t = expect(ctx, 11) # :lbrace
        tree.add(t)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        t = expect(ctx, 2) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[29] if x >=0],
      rules[8]
    )
def parse__gen0(ctx):
    current = ctx.tokens.current()
    rule = table[10][current.id] if current else -1
    tree = ParseTree(NonTerminal(30, '_gen0'))
    ctx.nonterminal = "_gen0"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[30] and current.id not in nonterminal_first[30]:
        return tree
    if current == None:
        return tree
    if rule == 0: # $_gen0 = $sections $_gen0
        ctx.rule = rules[0]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_sections(ctx)
        tree.add(subtree)
        subtree = parse__gen0(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_outputs(ctx):
    current = ctx.tokens.current()
    rule = table[11][current.id] if current else -1
    tree = ParseTree(NonTerminal(31, 'outputs'))
    ctx.nonterminal = "outputs"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 26: # $outputs = :outputs :lbrace $_gen5 :rbrace -> Outputs( attributes=$0 )
        ctx.rule = rules[26]
        ast_parameters = OrderedDict([
            ('attributes', 0),
        ])
        tree.astTransform = AstTransformNodeCreator('Outputs', ast_parameters)
        t = expect(ctx, 6) # :outputs
        tree.add(t)
        t = expect(ctx, 11) # :lbrace
        tree.add(t)
        subtree = parse__gen5(ctx)
        tree.add(subtree)
        t = expect(ctx, 2) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[31] if x >=0],
      rules[26]
    )
def parse__gen2(ctx):
    current = ctx.tokens.current()
    rule = table[12][current.id] if current else -1
    tree = ParseTree(NonTerminal(32, '_gen2'))
    ctx.nonterminal = "_gen2"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[32] and current.id not in nonterminal_first[32]:
        return tree
    if current == None:
        return tree
    if rule == 11: # $_gen2 = $cmd_param_kv $_gen2
        ctx.rule = rules[11]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_output_kv(ctx):
    current = ctx.tokens.current()
    rule = table[13][current.id] if current else -1
    tree = ParseTree(NonTerminal(33, 'output_kv'))
    ctx.nonterminal = "output_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 27: # $output_kv = :string :arrow :identifier -> OutputAttribute( key=$0, value=$2 )
        ctx.rule = rules[27]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('OutputAttribute', ast_parameters)
        t = expect(ctx, 15) # :string
        tree.add(t)
        t = expect(ctx, 19) # :arrow
        tree.add(t)
        t = expect(ctx, 8) # :identifier
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[33] if x >=0],
      rules[27]
    )
def parse_qualifier(ctx):
    current = ctx.tokens.current()
    rule = table[14][current.id] if current else -1
    tree = ParseTree(NonTerminal(34, 'qualifier'))
    ctx.nonterminal = "qualifier"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 22: # $qualifier = :qmark
        ctx.rule = rules[22]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 3) # :qmark
        tree.add(t)
        return tree
    elif rule == 23: # $qualifier = :asterisk
        ctx.rule = rules[23]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 18) # :asterisk
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[34] if x >=0],
      rules[23]
    )
def parse_sections(ctx):
    current = ctx.tokens.current()
    rule = table[15][current.id] if current else -1
    tree = ParseTree(NonTerminal(35, 'sections'))
    ctx.nonterminal = "sections"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 3: # $sections = $command
        ctx.rule = rules[3]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command(ctx)
        tree.add(subtree)
        return tree
    elif rule == 4: # $sections = $outputs
        ctx.rule = rules[4]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_outputs(ctx)
        tree.add(subtree)
        return tree
    elif rule == 5: # $sections = $runtime
        ctx.rule = rules[5]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_runtime(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[35] if x >=0],
      rules[5]
    )
def parse_command_part(ctx):
    current = ctx.tokens.current()
    rule = table[16][current.id] if current else -1
    tree = ParseTree(NonTerminal(36, 'command_part'))
    ctx.nonterminal = "command_part"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 9: # $command_part = :cmd_part
        ctx.rule = rules[9]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 10) # :cmd_part
        tree.add(t)
        return tree
    elif rule == 10: # $command_part = $cmd_param
        ctx.rule = rules[10]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[36] if x >=0],
      rules[10]
    )
def parse_cmd_param_value(ctx):
    current = ctx.tokens.current()
    rule = table[17][current.id] if current else -1
    tree = ParseTree(NonTerminal(37, 'cmd_param_value'))
    ctx.nonterminal = "cmd_param_value"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 17: # $cmd_param_value = :string
        ctx.rule = rules[17]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 15) # :string
        tree.add(t)
        return tree
    elif rule == 20: # $cmd_param_value = :type $_gen4 -> Type( name=$0, sub=$1 )
        ctx.rule = rules[20]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('sub', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('Type', ast_parameters)
        t = expect(ctx, 4) # :type
        tree.add(t)
        subtree = parse__gen4(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[37] if x >=0],
      rules[20]
    )
def parse__gen1(ctx):
    current = ctx.tokens.current()
    rule = table[18][current.id] if current else -1
    tree = ParseTree(NonTerminal(38, '_gen1'))
    ctx.nonterminal = "_gen1"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[38] and current.id not in nonterminal_first[38]:
        return tree
    if current == None:
        return tree
    if rule == 6: # $_gen1 = $command_part $_gen1
        ctx.rule = rules[6]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command_part(ctx)
        tree.add(subtree)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen3(ctx):
    current = ctx.tokens.current()
    rule = table[19][current.id] if current else -1
    tree = ParseTree(NonTerminal(39, '_gen3'))
    ctx.nonterminal = "_gen3"
    tree.list = False
    if current != None and current.id in nonterminal_follow[39] and current.id not in nonterminal_first[39]:
        return tree
    if current == None:
        return tree
    if rule == 13: # $_gen3 = $qualifier
        ctx.rule = rules[13]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_qualifier(ctx)
        tree.add(subtree)
        return tree
    return tree
# Lexer Code #
# START USER CODE
# END USER CODE
def emit(ctx, terminal, source_string, line, col):
    if terminal:
        ctx.tokens.append(Terminal(terminals[terminal], terminal, source_string, ctx.resource, line, col))
def default_action(ctx, terminal, source_string, line, col):
    emit(ctx, terminal, source_string, line, col)
def init():
    return {}
def destroy(context):
    pass
class LexerStackPush:
    def __init__(self, mode):
        self.mode = mode
class LexerAction:
    def __init__(self, action):
        self.action = action
class LexerContext:
    def __init__(self, string, resource, errors, user_context):
        self.__dict__.update(locals())
        self.stack = ['default']
        self.line = 1
        self.col = 1
        self.tokens = []
        self.user_context = user_context
        self.re_match = None # https://docs.python.org/3/library/re.html#match-objects
class HermesLexer:
    regex = {
        'default': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'task'), [
              # (terminal, group, function)
              ('task', 0, None),
          ]),
          (re.compile(r'(command)\s*(\{)'), [
              # (terminal, group, function)
              ('command', 1, None),
              ('lbrace', 2, None),
              LexerStackPush('command'),
          ]),
          (re.compile(r'(outputs)\s*(\{)'), [
              # (terminal, group, function)
              ('outputs', 1, None),
              ('lbrace', 2, None),
              LexerStackPush('outputs'),
          ]),
          (re.compile(r'(runtime)\s*(\{)'), [
              # (terminal, group, function)
              ('runtime', 1, None),
              ('lbrace', 2, None),
              LexerStackPush('runtime'),
          ]),
          (re.compile(r'[a-zA-Z0-9_-]+'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
          (re.compile(r'\{'), [
              # (terminal, group, function)
              ('lbrace', 0, None),
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('rbrace', 0, None),
          ]),
        ]),
        'command': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\\\s*\r?\n'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('rbrace', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'\${'), [
              # (terminal, group, function)
              ('cmd_param_start', 0, None),
              LexerStackPush('cmd_param'),
          ]),
          (re.compile(r'"[^\"]+"'), [
              # (terminal, group, function)
              ('cmd_part', 0, None),
          ]),
          (re.compile(r'\'[^\']+\''), [
              # (terminal, group, function)
              ('cmd_part', 0, None),
          ]),
          (re.compile(r'[^\s]+'), [
              # (terminal, group, function)
              ('cmd_part', 0, None),
          ]),
        ]),
        'cmd_param': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('cmd_param_end', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'array|int|uri|file'), [
              # (terminal, group, function)
              ('type', 0, None),
          ]),
          (re.compile(r'[a-zA-Z0-9_-]+(?=\s*=)'), [
              # (terminal, group, function)
              ('cmd_attr_hint', 0, None),
              ('identifier', 0, None),
          ]),
          (re.compile(r'[a-zA-Z0-9_-]+'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
          (re.compile(r'='), [
              # (terminal, group, function)
              ('equals', 0, None),
          ]),
          (re.compile(r'\?'), [
              # (terminal, group, function)
              ('qmark', 0, None),
          ]),
          (re.compile(r'\*'), [
              # (terminal, group, function)
              ('asterisk', 0, None),
          ]),
          (re.compile(r'\['), [
              # (terminal, group, function)
              ('lsquare', 0, None),
          ]),
          (re.compile(r'\]'), [
              # (terminal, group, function)
              ('rsquare', 0, None),
          ]),
          (re.compile(r'"[^\"]+"'), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
          (re.compile(r'\'[^\']+\''), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
        ]),
        'outputs': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('rbrace', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'"[^\"]+"'), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
          (re.compile(r'\'[^\']+\''), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
          (re.compile(r'->'), [
              # (terminal, group, function)
              ('arrow', 0, None),
          ]),
          (re.compile(r'[a-zA-Z0-9_-]+'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
        ]),
        'runtime': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('rbrace', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'"[^\"]+"'), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
          (re.compile(r'\'[^\']+\''), [
              # (terminal, group, function)
              ('string', 0, None),
          ]),
          (re.compile(r':'), [
              # (terminal, group, function)
              ('colon', 0, None),
          ]),
          (re.compile(r'[a-zA-Z0-9_-]+'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
        ]),
    }
    def _advance_line_col(self, string, length, line, col):
        for i in range(length):
            if string[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
        return (line, col)
    def _advance_string(self, ctx, string):
        (ctx.line, ctx.col) = self._advance_line_col(string, len(string), ctx.line, ctx.col)
        ctx.string = ctx.string[len(string):]
    def _next(self, ctx, debug=False):
        for regex, outputs in self.regex[ctx.stack[-1]].items():
            if debug:
                from xtermcolor import colorize
                token_count = len(ctx.tokens)
                print('{1} ({2}, {3}) regex: {0}'.format(
                    colorize(regex.pattern, ansi=40), colorize(ctx.string[:20].replace('\n', '\\n'), ansi=15), ctx.line, ctx.col)
                )
            match = regex.match(ctx.string)
            if match:
                ctx.re_match = match
                for output in outputs:
                    if isinstance(output, tuple):
                        (terminal, group, function) = output
                        function = function if function else default_action
                        source_string = match.group(group) if group is not None else ''
                        (group_line, group_col) = self._advance_line_col(ctx.string, match.start(group) if group else 0, ctx.line, ctx.col)
                        function(
                            ctx,
                            terminal,
                            source_string,
                            group_line,
                            group_col
                        )
                        if debug:
                            print('    matched: {}'.format(colorize(match.group(0).replace('\n', '\\n'), ansi=3)))
                            for token in ctx.tokens[token_count:]:
                                print('    emit: [{}] [{}, {}] [{}] stack:{} context:{}'.format(
                                    colorize(token.str, ansi=9),
                                    colorize(str(token.line), ansi=5),
                                    colorize(str(token.col), ansi=5),
                                    colorize(token.source_string, ansi=3),
                                    colorize(str(ctx.stack), ansi=4),
                                    colorize(str(ctx.user_context), ansi=13)
                                ))
                            token_count = len(ctx.tokens)
                    if isinstance(output, LexerStackPush):
                        ctx.stack.append(output.mode)
                        if debug:
                            print('    push on stack: {}'.format(colorize(output.mode, ansi=4)))
                    if isinstance(output, LexerAction):
                        if output.action == 'pop':
                            mode = ctx.stack.pop()
                            if debug:
                                print('    pop off stack: {}'.format(colorize(mode, ansi=4)))
                self._advance_string(ctx, match.group(0))
                return len(match.group(0)) > 0
        return False
    def lex(self, string, resource, errors=None, debug=False):
        if errors is None:
            errors = DefaultSyntaxErrorHandler()
        string_copy = string
        user_context = init()
        ctx = LexerContext(string, resource, errors, user_context)
        while len(ctx.string):
            matched = self._next(ctx, debug)
            if matched == False:
                raise ctx.errors.unrecognized_token(string_copy, ctx.line, ctx.col)
        destroy(ctx.user_context)
        return ctx.tokens
def lex(source, resource, errors=None, debug=False):
    return TokenStream(HermesLexer().lex(source, resource, errors, debug))
