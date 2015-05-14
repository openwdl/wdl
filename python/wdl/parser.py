import sys
import os
import re
import base64
import argparse
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
  def dumps(self, b64_source=True, **kwargs):
      source_string = base64.b64encode(self.source_string.encode('utf-8')).decode('utf-8') if b64_source else self.source_string
      return '<{resource}:{line}:{col} {terminal} "{source}">'.format(
          resource=self.resource,
          line=self.line,
          col=self.col,
          terminal=self.str,
          source=source_string
      )
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
    0: 'type_e',
    1: 'while',
    2: 'not',
    3: 'object',
    4: 'dot',
    5: 'double_equal',
    6: 'qmark',
    7: 'meta',
    8: 'call',
    9: 'cmd_param_end',
    10: 'boolean',
    11: 'lparen',
    12: 'lt',
    13: 'not_equal',
    14: 'cmd_part',
    15: 'percent',
    16: 'plus',
    17: 'equal',
    18: 'rbrace',
    19: 'raw_command',
    20: 'if',
    21: 'gteq',
    22: 'runtime',
    23: 'input',
    24: 'rparen',
    25: 'double_ampersand',
    26: 'rsquare',
    27: 'raw_cmd_start',
    28: 'output',
    29: 'parameter_meta',
    30: 'as',
    31: 'slash',
    32: 'double_pipe',
    33: 'comma',
    34: 'e',
    35: 'asterisk',
    36: 'dquote_string',
    37: 'cmd_param_start',
    38: 'raw_cmd_end',
    39: 'string',
    40: 'scatter',
    41: 'gt',
    42: 'colon',
    43: 'dash',
    44: 'cmd_attr_hint',
    45: 'task',
    46: 'type',
    47: 'float',
    48: 'lbrace',
    49: 'lsquare',
    50: 'workflow',
    51: 'in',
    52: 'identifier',
    53: 'squote_string',
    54: 'lteq',
    55: 'integer',
    'type_e': 0,
    'while': 1,
    'not': 2,
    'object': 3,
    'dot': 4,
    'double_equal': 5,
    'qmark': 6,
    'meta': 7,
    'call': 8,
    'cmd_param_end': 9,
    'boolean': 10,
    'lparen': 11,
    'lt': 12,
    'not_equal': 13,
    'cmd_part': 14,
    'percent': 15,
    'plus': 16,
    'equal': 17,
    'rbrace': 18,
    'raw_command': 19,
    'if': 20,
    'gteq': 21,
    'runtime': 22,
    'input': 23,
    'rparen': 24,
    'double_ampersand': 25,
    'rsquare': 26,
    'raw_cmd_start': 27,
    'output': 28,
    'parameter_meta': 29,
    'as': 30,
    'slash': 31,
    'double_pipe': 32,
    'comma': 33,
    'e': 34,
    'asterisk': 35,
    'dquote_string': 36,
    'cmd_param_start': 37,
    'raw_cmd_end': 38,
    'string': 39,
    'scatter': 40,
    'gt': 41,
    'colon': 42,
    'dash': 43,
    'cmd_attr_hint': 44,
    'task': 45,
    'type': 46,
    'float': 47,
    'lbrace': 48,
    'lsquare': 49,
    'workflow': 50,
    'in': 51,
    'identifier': 52,
    'squote_string': 53,
    'lteq': 54,
    'integer': 55,
}
# table[nonterminal][terminal] = rule
table = [
    [-1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, 12, -1, -1, -1, -1, -1, 11, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [53, 53, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, 53, -1, -1, -1, -1, -1, -1, -1, -1, -1, 52, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, 53, -1, 53, -1, -1, -1, -1, -1, -1, -1],
    [57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 58, -1, -1, -1, -1, 58, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 102, 102, -1, -1, -1, -1, -1, -1, 102, 102, -1, -1, -1, -1, 102, -1, -1, -1, -1, -1, -1, -1, 105, -1, -1, -1, -1, -1, -1, -1, -1, -1, 102, -1, 102, -1, -1, 102, -1, -1, -1, 102, -1, -1, -1, 102, -1, -1, -1, -1, 102, 102, -1, 102],
    [24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, 25, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 104, -1, -1, -1, -1, -1, -1, -1, -1, 103, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [77, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 77, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 40, -1, -1, -1],
    [48, 49, -1, -1, -1, -1, -1, -1, 47, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 50, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 67, -1, -1, -1, -1, 67, -1, -1, -1, -1, 67, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 64, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 79, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [76, 76, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1, -1, -1, -1, -1, -1, 75, 76, -1, 76, -1, -1, 76, -1, -1, -1, -1, 76, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1, -1, -1, 76, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 26, -1, -1, 27, -1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 7, -1, -1, 7, -1, -1, -1, -1, -1, 7, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, 6, -1, -1, -1, -1, -1, 6, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 43, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, -1, 63, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, -1, -1, -1, -1, 66, -1, -1, -1, -1, 66, -1, -1, -1, -1, 65, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 74, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 69, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 56, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 82, -1, -1, -1, -1, -1, -1, 81, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 73, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 111, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 110, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, -1, -1, -1, 59, -1, -1, -1, -1, 59, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 70, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1],
    [80, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 83, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 80, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 72, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1],
    [55, 55, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, 55, -1, 54, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [44, 44, -1, -1, -1, -1, -1, -1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, 45, -1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 44, -1, -1, -1, -1, -1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 112, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 109, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 71, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 68, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 78, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]
nonterminal_first = {
    56: [28, 19, 29, 7, 22],
    57: [-1, 30],
    58: [0, -1, 46],
    59: [2, 34, 3, 36, 39, 10, 11, 16, 43, 47, 52, 53, -1, 55],
    60: [0, -1, 46],
    61: [-1, 33],
    62: [0, 46],
    63: [44],
    64: [-1, 52],
    65: [0, 20, 1, 40, 46, 8],
    66: [-1, 52],
    67: [52],
    68: [29],
    69: [6, 35, 16],
    70: [17, -1],
    71: [-1, 6, 35, 16],
    72: [28, 29, 22, -1, 7, 19],
    73: [-1],
    74: [52],
    75: [-1, 44],
    76: [23, 28],
    77: [45, -1, 50],
    78: [45],
    79: [-1, 33],
    80: [40],
    81: [28],
    82: [48],
    83: [7],
    84: [8],
    85: [22],
    86: [-1, 33],
    87: [20],
    88: [37, 14],
    89: [-1, 33],
    90: [-1, 39],
    91: [-1, 23, 28],
    92: [45, -1, 50],
    93: [52],
    94: [19],
    95: [37],
    96: [45, 50],
    97: [48],
    98: [0, -1, 46],
    99: [1],
    100: [50],
    101: [-1, 48],
    102: [],
    103: [28],
    104: [0, 46],
    105: [0, -1, 46],
    106: [0, 20, 1, 46, 8, 40, -1],
    107: [-1, 52],
    108: [30],
    109: [-1, 37, 14],
    110: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    111: [0, 46],
    112: [23],
    113: [17],
}
nonterminal_follow = {
    56: [19, 18, 29, 22, 7, 28],
    57: [0, 20, 1, 18, 46, 8, 48, 40],
    58: [23, 28],
    59: [24],
    60: [52],
    61: [24],
    62: [0, 20, 1, 18, 28, 40, 46, 23, 8],
    63: [39, 44],
    64: [18],
    65: [0, 20, 1, 18, 40, 46, 8],
    66: [18, 23, 28],
    67: [18, 33],
    68: [18, 22, 7, 28, 29, 19],
    69: [9],
    70: [0, 20, 1, 18, 46, 23, 8, 28, 40],
    71: [9],
    72: [18],
    73: [19, 28, 29, 7, 22],
    74: [18, 52],
    75: [39],
    76: [18, 23, 28],
    77: [-1],
    78: [45, -1, 50],
    79: [18, 23, 28],
    80: [0, 20, 1, 18, 46, 8, 40],
    81: [18, 23, 28],
    82: [0, 20, 1, 18, 46, 8, 40],
    83: [18, 22, 7, 28, 29, 19],
    84: [0, 20, 1, 18, 46, 8, 40],
    85: [18, 22, 7, 28, 29, 19],
    86: [26],
    87: [0, 20, 1, 18, 46, 8, 40],
    88: [37, 14, 38],
    89: [18],
    90: [0, 46],
    91: [18],
    92: [-1],
    93: [18, 33, 23, 28],
    94: [18, 22, 7, 28, 29, 19],
    95: [37, 14, 38],
    96: [45, -1, 50],
    97: [18, 22, 7, 28, 29, 19],
    98: [26],
    99: [0, 20, 1, 18, 46, 8, 40],
    100: [45, -1, 50],
    101: [0, 20, 1, 18, 46, 8, 40],
    102: [28, 22, 29, 7, 19],
    103: [18, 22, 7, 28, 29, 19],
    104: [0, 46, 18],
    105: [18],
    106: [18],
    107: [18],
    108: [0, 20, 1, 18, 46, 8, 48, 40],
    109: [38],
    110: [0, 32, 1, 33, 35, 5, 39, 8, 40, 12, 15, 13, 41, 16, 18, 21, 43, 20, 44, 46, 23, 24, 25, 26, 28, 52, 54, 31],
    111: [33, 52, 26],
    112: [18, 23, 28],
    113: [0, 20, 1, 18, 46, 23, 8, 28, 40],
}
rule_first = {
    0: [45, 50],
    1: [-1],
    2: [45, -1, 50],
    3: [50],
    4: [45],
    5: [],
    6: [-1],
    7: [22, 28, 29, 7, 19],
    8: [-1],
    9: [45],
    10: [19],
    11: [28],
    12: [22],
    13: [29],
    14: [7],
    15: [37, 14],
    16: [-1],
    17: [19],
    18: [14],
    19: [37],
    20: [44],
    21: [-1],
    22: [39],
    23: [-1],
    24: [0, 46],
    25: [-1],
    26: [6, 35, 16],
    27: [-1],
    28: [37],
    29: [44],
    30: [6],
    31: [16],
    32: [35],
    33: [0, 46],
    34: [-1],
    35: [28],
    36: [0, 46],
    37: [22],
    38: [29],
    39: [7],
    40: [52],
    41: [-1],
    42: [48],
    43: [52],
    44: [0, 20, 1, 40, 46, 8],
    45: [-1],
    46: [50],
    47: [8],
    48: [0, 46],
    49: [1],
    50: [20],
    51: [40],
    52: [30],
    53: [-1],
    54: [48],
    55: [-1],
    56: [8],
    57: [0, 46],
    58: [-1],
    59: [23, 28],
    60: [-1],
    61: [48],
    62: [23],
    63: [28],
    64: [52],
    65: [33],
    66: [-1],
    67: [-1],
    68: [23],
    69: [28],
    70: [52],
    71: [30],
    72: [1],
    73: [20],
    74: [40],
    75: [17],
    76: [-1],
    77: [0, 46],
    78: [17],
    79: [52],
    80: [0, 46],
    81: [33],
    82: [-1],
    83: [-1],
    84: [46],
    85: [46],
    86: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    87: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    88: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    89: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    90: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    91: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    92: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    93: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    94: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    95: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    96: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    97: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    98: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    99: [2],
    100: [16],
    101: [43],
    102: [43, 2, 34, 3, 47, 36, 39, 10, 52, 53, 11, 55, 16],
    103: [33],
    104: [-1],
    105: [-1],
    106: [52],
    107: [52],
    108: [52],
    109: [52],
    110: [33],
    111: [-1],
    112: [-1],
    113: [3],
    114: [11],
    115: [39],
    116: [52],
    117: [10],
    118: [55],
    119: [47],
    120: [36],
    121: [53],
}
nonterminal_rules = {
    56: [
        "$sections = $command",
        "$sections = $outputs",
        "$sections = $runtime",
        "$sections = $parameter_meta",
        "$sections = $meta",
    ],
    57: [
        "$_gen11 = $alias",
        "$_gen11 = :_empty",
    ],
    58: [
        "$_gen13 = $declaration $_gen13",
        "$_gen13 = :_empty",
    ],
    59: [
        "$_gen20 = $e $_gen21",
        "$_gen20 = :_empty",
    ],
    60: [
        "$_gen6 = $type_e",
        "$_gen6 = :_empty",
    ],
    61: [
        "$_gen21 = :comma $e $_gen21",
        "$_gen21 = :_empty",
    ],
    62: [
        "$declaration = $type_e :identifier $_gen17 -> Declaration( type=$0, name=$1, expression=$2 )",
    ],
    63: [
        "$cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )",
    ],
    64: [
        "$_gen9 = $kv $_gen9",
        "$_gen9 = :_empty",
    ],
    65: [
        "$wf_body_element = $call",
        "$wf_body_element = $declaration",
        "$wf_body_element = $while_loop",
        "$wf_body_element = $if_stmt",
        "$wf_body_element = $scatter",
    ],
    66: [
        "$_gen15 = $mapping $_gen16",
        "$_gen15 = :_empty",
    ],
    67: [
        "$object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )",
    ],
    68: [
        "$parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )",
    ],
    69: [
        "$postfix_quantifier = :qmark",
        "$postfix_quantifier = :plus",
        "$postfix_quantifier = :asterisk",
    ],
    70: [
        "$_gen17 = $setter",
        "$_gen17 = :_empty",
    ],
    71: [
        "$_gen7 = $postfix_quantifier",
        "$_gen7 = :_empty",
    ],
    72: [
        "$_gen2 = $sections $_gen2",
        "$_gen2 = :_empty",
    ],
    73: [
        "$_gen1 = $declarations $_gen1",
        "$_gen1 = :_empty",
    ],
    74: [
        "$kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )",
    ],
    75: [
        "$_gen4 = $cmd_param_kv $_gen4",
        "$_gen4 = :_empty",
    ],
    76: [
        "$call_body_element = $call_input",
        "$call_body_element = $call_output",
    ],
    77: [
        "$document = $_gen0 -> Document( definitions=$0 )",
    ],
    78: [
        "$task = :task :identifier :lbrace $_gen1 $_gen2 :rbrace -> Task( name=$1, declarations=$3, sections=$4 )",
    ],
    79: [
        "$_gen16 = :comma $mapping $_gen16",
        "$_gen16 = :_empty",
    ],
    80: [
        "$scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen10 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )",
    ],
    81: [
        "$call_output = :output :colon $_gen15 -> Outputs( map=$2 )",
    ],
    82: [
        "$call_body = :lbrace $_gen13 $_gen14 :rbrace -> CallBody( declarations=$1, io=$2 )",
    ],
    83: [
        "$meta = :meta $map -> Meta( map=$1 )",
    ],
    84: [
        "$call = :call :identifier $_gen11 $_gen12 -> Call( task=$1, alias=$2, body=$3 )",
    ],
    85: [
        "$runtime = :runtime $map -> Runtime( map=$1 )",
    ],
    86: [
        "$_gen19 = :comma $type_e $_gen19",
        "$_gen19 = :_empty",
    ],
    87: [
        "$if_stmt = :if :lparen $e :rparen :lbrace $_gen10 :rbrace -> If( expression=$2, body=$5 )",
    ],
    88: [
        "$command_part = :cmd_part",
        "$command_part = $cmd_param",
    ],
    89: [
        "$_gen23 = :comma $object_kv $_gen23",
        "$_gen23 = :_empty",
    ],
    90: [
        "$_gen5 = :string",
        "$_gen5 = :_empty",
    ],
    91: [
        "$_gen14 = $call_body_element $_gen14",
        "$_gen14 = :_empty",
    ],
    92: [
        "$_gen0 = $workflow_or_task $_gen0",
        "$_gen0 = :_empty",
    ],
    93: [
        "$mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )",
    ],
    94: [
        "$command = :raw_command :raw_cmd_start $_gen3 :raw_cmd_end -> RawCommand( parts=$2 )",
    ],
    95: [
        "$cmd_param = :cmd_param_start $_gen4 $_gen5 $_gen6 :identifier $_gen7 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )",
    ],
    96: [
        "$workflow_or_task = $workflow",
        "$workflow_or_task = $task",
    ],
    97: [
        "$map = :lbrace $_gen9 :rbrace -> $1",
    ],
    98: [
        "$_gen18 = $type_e $_gen19",
        "$_gen18 = :_empty",
    ],
    99: [
        "$while_loop = :while :lparen $e :rparen :lbrace $_gen10 :rbrace -> WhileLoop( expression=$2, body=$5 )",
    ],
    100: [
        "$workflow = :workflow :identifier :lbrace $_gen10 :rbrace -> Workflow( name=$1, body=$3 )",
    ],
    101: [
        "$_gen12 = $call_body",
        "$_gen12 = :_empty",
    ],
    102: [
    ],
    103: [
        "$outputs = :output :lbrace $_gen8 :rbrace -> Outputs( attributes=$2 )",
    ],
    104: [
        "$output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )",
    ],
    105: [
        "$_gen8 = $output_kv $_gen8",
        "$_gen8 = :_empty",
    ],
    106: [
        "$_gen10 = $wf_body_element $_gen10",
        "$_gen10 = :_empty",
    ],
    107: [
        "$_gen22 = $object_kv $_gen23",
        "$_gen22 = :_empty",
    ],
    108: [
        "$alias = :as :identifier -> $1",
    ],
    109: [
        "$_gen3 = $command_part $_gen3",
        "$_gen3 = :_empty",
    ],
    110: [
        "$e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )",
        "$e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )",
        "$e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )",
        "$e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )",
        "$e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )",
        "$e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )",
        "$e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )",
        "$e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )",
        "$e = $e :plus $e -> Add( lhs=$0, rhs=$2 )",
        "$e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )",
        "$e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )",
        "$e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )",
        "$e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )",
        "$e = :not $e -> LogicalNot( expression=$1 )",
        "$e = :plus $e -> UnaryPlus( expression=$1 )",
        "$e = :dash $e -> UnaryNegation( expression=$1 )",
        "$e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )",
        "$e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )",
        "$e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )",
        "$e = :object :lbrace $_gen22 :rbrace -> ObjectLiteral( map=$2 )",
        "$e = :lparen $e :rparen -> $1",
        "$e = :string",
        "$e = :identifier",
        "$e = :boolean",
        "$e = :integer",
        "$e = :float",
        "$e = :dquote_string",
        "$e = :squote_string",
    ],
    111: [
        "$type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )",
        "$type_e = :type",
    ],
    112: [
        "$call_input = :input :colon $_gen15 -> Inputs( map=$2 )",
    ],
    113: [
        "$setter = :equal $e -> $1",
    ],
}
rules = {
    0: "$_gen0 = $workflow_or_task $_gen0",
    1: "$_gen0 = :_empty",
    2: "$document = $_gen0 -> Document( definitions=$0 )",
    3: "$workflow_or_task = $workflow",
    4: "$workflow_or_task = $task",
    5: "$_gen1 = $declarations $_gen1",
    6: "$_gen1 = :_empty",
    7: "$_gen2 = $sections $_gen2",
    8: "$_gen2 = :_empty",
    9: "$task = :task :identifier :lbrace $_gen1 $_gen2 :rbrace -> Task( name=$1, declarations=$3, sections=$4 )",
    10: "$sections = $command",
    11: "$sections = $outputs",
    12: "$sections = $runtime",
    13: "$sections = $parameter_meta",
    14: "$sections = $meta",
    15: "$_gen3 = $command_part $_gen3",
    16: "$_gen3 = :_empty",
    17: "$command = :raw_command :raw_cmd_start $_gen3 :raw_cmd_end -> RawCommand( parts=$2 )",
    18: "$command_part = :cmd_part",
    19: "$command_part = $cmd_param",
    20: "$_gen4 = $cmd_param_kv $_gen4",
    21: "$_gen4 = :_empty",
    22: "$_gen5 = :string",
    23: "$_gen5 = :_empty",
    24: "$_gen6 = $type_e",
    25: "$_gen6 = :_empty",
    26: "$_gen7 = $postfix_quantifier",
    27: "$_gen7 = :_empty",
    28: "$cmd_param = :cmd_param_start $_gen4 $_gen5 $_gen6 :identifier $_gen7 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )",
    29: "$cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )",
    30: "$postfix_quantifier = :qmark",
    31: "$postfix_quantifier = :plus",
    32: "$postfix_quantifier = :asterisk",
    33: "$_gen8 = $output_kv $_gen8",
    34: "$_gen8 = :_empty",
    35: "$outputs = :output :lbrace $_gen8 :rbrace -> Outputs( attributes=$2 )",
    36: "$output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )",
    37: "$runtime = :runtime $map -> Runtime( map=$1 )",
    38: "$parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )",
    39: "$meta = :meta $map -> Meta( map=$1 )",
    40: "$_gen9 = $kv $_gen9",
    41: "$_gen9 = :_empty",
    42: "$map = :lbrace $_gen9 :rbrace -> $1",
    43: "$kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )",
    44: "$_gen10 = $wf_body_element $_gen10",
    45: "$_gen10 = :_empty",
    46: "$workflow = :workflow :identifier :lbrace $_gen10 :rbrace -> Workflow( name=$1, body=$3 )",
    47: "$wf_body_element = $call",
    48: "$wf_body_element = $declaration",
    49: "$wf_body_element = $while_loop",
    50: "$wf_body_element = $if_stmt",
    51: "$wf_body_element = $scatter",
    52: "$_gen11 = $alias",
    53: "$_gen11 = :_empty",
    54: "$_gen12 = $call_body",
    55: "$_gen12 = :_empty",
    56: "$call = :call :identifier $_gen11 $_gen12 -> Call( task=$1, alias=$2, body=$3 )",
    57: "$_gen13 = $declaration $_gen13",
    58: "$_gen13 = :_empty",
    59: "$_gen14 = $call_body_element $_gen14",
    60: "$_gen14 = :_empty",
    61: "$call_body = :lbrace $_gen13 $_gen14 :rbrace -> CallBody( declarations=$1, io=$2 )",
    62: "$call_body_element = $call_input",
    63: "$call_body_element = $call_output",
    64: "$_gen15 = $mapping $_gen16",
    65: "$_gen16 = :comma $mapping $_gen16",
    66: "$_gen16 = :_empty",
    67: "$_gen15 = :_empty",
    68: "$call_input = :input :colon $_gen15 -> Inputs( map=$2 )",
    69: "$call_output = :output :colon $_gen15 -> Outputs( map=$2 )",
    70: "$mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )",
    71: "$alias = :as :identifier -> $1",
    72: "$while_loop = :while :lparen $e :rparen :lbrace $_gen10 :rbrace -> WhileLoop( expression=$2, body=$5 )",
    73: "$if_stmt = :if :lparen $e :rparen :lbrace $_gen10 :rbrace -> If( expression=$2, body=$5 )",
    74: "$scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen10 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )",
    75: "$_gen17 = $setter",
    76: "$_gen17 = :_empty",
    77: "$declaration = $type_e :identifier $_gen17 -> Declaration( type=$0, name=$1, expression=$2 )",
    78: "$setter = :equal $e -> $1",
    79: "$object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )",
    80: "$_gen18 = $type_e $_gen19",
    81: "$_gen19 = :comma $type_e $_gen19",
    82: "$_gen19 = :_empty",
    83: "$_gen18 = :_empty",
    84: "$type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )",
    85: "$type_e = :type",
    86: "$e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )",
    87: "$e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )",
    88: "$e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )",
    89: "$e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )",
    90: "$e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )",
    91: "$e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )",
    92: "$e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )",
    93: "$e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )",
    94: "$e = $e :plus $e -> Add( lhs=$0, rhs=$2 )",
    95: "$e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )",
    96: "$e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )",
    97: "$e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )",
    98: "$e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )",
    99: "$e = :not $e -> LogicalNot( expression=$1 )",
    100: "$e = :plus $e -> UnaryPlus( expression=$1 )",
    101: "$e = :dash $e -> UnaryNegation( expression=$1 )",
    102: "$_gen20 = $e $_gen21",
    103: "$_gen21 = :comma $e $_gen21",
    104: "$_gen21 = :_empty",
    105: "$_gen20 = :_empty",
    106: "$e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )",
    107: "$e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )",
    108: "$e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )",
    109: "$_gen22 = $object_kv $_gen23",
    110: "$_gen23 = :comma $object_kv $_gen23",
    111: "$_gen23 = :_empty",
    112: "$_gen22 = :_empty",
    113: "$e = :object :lbrace $_gen22 :rbrace -> ObjectLiteral( map=$2 )",
    114: "$e = :lparen $e :rparen -> $1",
    115: "$e = :string",
    116: "$e = :identifier",
    117: "$e = :boolean",
    118: "$e = :integer",
    119: "$e = :float",
    120: "$e = :dquote_string",
    121: "$e = :squote_string",
}
def is_terminal(id): return isinstance(id, int) and 0 <= id <= 55
def parse(tokens, errors=None, start=None):
    if errors is None:
        errors = DefaultSyntaxErrorHandler()
    if isinstance(tokens, str):
        tokens = lex(tokens, 'string', errors)
    ctx = ParserContext(tokens, errors)
    tree = parse_document(ctx)
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
# START definitions for expression parser: type_e
infix_binding_power_type_e = {
    49: 1000, # $type_e = :type <=> :lsquare list($type_e, :comma) :rsquare -> Type( name=$0, subtype=$2 )
}
prefix_binding_power_type_e = {
}
def get_infix_binding_power_type_e(terminal_id):
    try:
        return infix_binding_power_type_e[terminal_id]
    except:
        return 0
def get_prefix_binding_power_type_e(terminal_id):
    try:
        return prefix_binding_power_type_e[terminal_id]
    except:
        return 0
def parse_type_e(ctx):
    return parse_type_e_internal(ctx, rbp=0)
def parse_type_e_internal(ctx, rbp=0):
    left = nud_type_e(ctx)
    if isinstance(left, ParseTree):
        left.isExpr = True
        left.isNud = True
    while ctx.tokens.current() and rbp < get_infix_binding_power_type_e(ctx.tokens.current().id):
        left = led_type_e(left, ctx)
    if left:
        left.isExpr = True
    return left
def nud_type_e(ctx):
    tree = ParseTree(NonTerminal(111, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if not current:
        return tree
    if current.id in rule_first[84]:
        # $type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[84]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 46))
    elif current.id in rule_first[85]:
        # $type_e = :type
        ctx.rule = rules[85]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 46))
    return tree
def led_type_e(left, ctx):
    tree = ParseTree(NonTerminal(111, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if current.id == 49: # :lsquare
        # $type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[84]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('subtype', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Type', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 49)) # :lsquare
        tree.add(parse__gen18(ctx))
        tree.add(expect(ctx, 26)) # :rsquare
    return tree
# END definitions for expression parser: type_e
# START definitions for expression parser: e
infix_binding_power_e = {
    32: 2000, # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
    25: 3000, # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
    5: 4000, # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
    13: 4000, # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
    12: 5000, # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
    54: 5000, # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
    41: 5000, # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
    21: 5000, # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
    16: 6000, # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
    43: 6000, # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
    35: 7000, # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
    31: 7000, # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
    15: 7000, # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
    11: 9000, # $e = :identifier <=> :lparen list($e, :comma) :rparen -> FunctionCall( name=$0, params=$2 )
    49: 10000, # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
    4: 11000, # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
}
prefix_binding_power_e = {
    2: 8000, # $e = :not $e -> LogicalNot( expression=$1 )
    16: 8000, # $e = :plus $e -> UnaryPlus( expression=$1 )
    43: 8000, # $e = :dash $e -> UnaryNegation( expression=$1 )
}
def get_infix_binding_power_e(terminal_id):
    try:
        return infix_binding_power_e[terminal_id]
    except:
        return 0
def get_prefix_binding_power_e(terminal_id):
    try:
        return prefix_binding_power_e[terminal_id]
    except:
        return 0
def parse_e(ctx):
    return parse_e_internal(ctx, rbp=0)
def parse_e_internal(ctx, rbp=0):
    left = nud_e(ctx)
    if isinstance(left, ParseTree):
        left.isExpr = True
        left.isNud = True
    while ctx.tokens.current() and rbp < get_infix_binding_power_e(ctx.tokens.current().id):
        left = led_e(left, ctx)
    if left:
        left.isExpr = True
    return left
def nud_e(ctx):
    tree = ParseTree(NonTerminal(110, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if not current:
        return tree
    elif current.id in rule_first[99]:
        # $e = :not $e -> LogicalNot( expression=$1 )
        ctx.rule = rules[99]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 2))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(2)))
        tree.isPrefix = True
    elif current.id in rule_first[100]:
        # $e = :plus $e -> UnaryPlus( expression=$1 )
        ctx.rule = rules[100]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 16))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(16)))
        tree.isPrefix = True
    elif current.id in rule_first[101]:
        # $e = :dash $e -> UnaryNegation( expression=$1 )
        ctx.rule = rules[101]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 43))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(43)))
        tree.isPrefix = True
    elif current.id in rule_first[106]:
        # $e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[106]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 52))
    elif current.id in rule_first[107]:
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[107]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 52))
    elif current.id in rule_first[108]:
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[108]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 52))
    elif current.id in rule_first[113]:
        # $e = :object :lbrace $_gen22 :rbrace -> ObjectLiteral( map=$2 )
        ctx.rule = rules[113]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ObjectLiteral', ast_parameters)
        tree.nudMorphemeCount = 4
        tree.add(expect(ctx, 3))
        tree.add(expect(ctx, 48))
        tree.add(parse__gen22(ctx))
        tree.add(expect(ctx, 18))
    elif current.id in rule_first[114]:
        # $e = :lparen $e :rparen -> $1
        ctx.rule = rules[114]
        tree.astTransform = AstTransformSubstitution(1)
        tree.nudMorphemeCount = 3
        tree.add(expect(ctx, 11))
        tree.add(parse_e(ctx))
        tree.add(expect(ctx, 24))
    elif current.id in rule_first[115]:
        # $e = :string
        ctx.rule = rules[115]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 39))
    elif current.id in rule_first[116]:
        # $e = :identifier
        ctx.rule = rules[116]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 52))
    elif current.id in rule_first[117]:
        # $e = :boolean
        ctx.rule = rules[117]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 10))
    elif current.id in rule_first[118]:
        # $e = :integer
        ctx.rule = rules[118]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 55))
    elif current.id in rule_first[119]:
        # $e = :float
        ctx.rule = rules[119]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 47))
    elif current.id in rule_first[120]:
        # $e = :dquote_string
        ctx.rule = rules[120]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 36))
    elif current.id in rule_first[121]:
        # $e = :squote_string
        ctx.rule = rules[121]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 53))
    return tree
def led_e(left, ctx):
    tree = ParseTree(NonTerminal(110, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if current.id == 32: # :double_pipe
        # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
        ctx.rule = rules[86]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalOr', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 32)) # :double_pipe
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(32) - modifier))
    if current.id == 25: # :double_ampersand
        # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
        ctx.rule = rules[87]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalAnd', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 25)) # :double_ampersand
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(25) - modifier))
    if current.id == 5: # :double_equal
        # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
        ctx.rule = rules[88]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Equals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 5)) # :double_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(5) - modifier))
    if current.id == 13: # :not_equal
        # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
        ctx.rule = rules[89]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('NotEquals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 13)) # :not_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(13) - modifier))
    if current.id == 12: # :lt
        # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[90]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 12)) # :lt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(12) - modifier))
    if current.id == 54: # :lteq
        # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[91]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 54)) # :lteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(54) - modifier))
    if current.id == 41: # :gt
        # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[92]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 41)) # :gt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(41) - modifier))
    if current.id == 21: # :gteq
        # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[93]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 21)) # :gteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(21) - modifier))
    if current.id == 16: # :plus
        # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
        ctx.rule = rules[94]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Add', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 16)) # :plus
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(16) - modifier))
    if current.id == 43: # :dash
        # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
        ctx.rule = rules[95]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Subtract', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 43)) # :dash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(43) - modifier))
    if current.id == 35: # :asterisk
        # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
        ctx.rule = rules[96]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Multiply', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 35)) # :asterisk
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(35) - modifier))
    if current.id == 31: # :slash
        # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
        ctx.rule = rules[97]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Divide', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 31)) # :slash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(31) - modifier))
    if current.id == 15: # :percent
        # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
        ctx.rule = rules[98]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Remainder', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 15)) # :percent
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(15) - modifier))
    if current.id == 11: # :lparen
        # $e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[106]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('params', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('FunctionCall', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 11)) # :lparen
        tree.add(parse__gen20(ctx))
        tree.add(expect(ctx, 24)) # :rparen
    if current.id == 49: # :lsquare
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[107]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ArrayIndex', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 49)) # :lsquare
        modifier = 0
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(49) - modifier))
        tree.add(expect(ctx, 26)) # :rsquare
    if current.id == 4: # :dot
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[108]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('MemberAccess', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 4)) # :dot
        tree.add(expect(ctx, 52)) # :identifier
    return tree
# END definitions for expression parser: e
def parse_sections(ctx):
    current = ctx.tokens.current()
    rule = table[0][current.id] if current else -1
    tree = ParseTree(NonTerminal(56, 'sections'))
    ctx.nonterminal = "sections"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 10: # $sections = $command
        ctx.rule = rules[10]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command(ctx)
        tree.add(subtree)
        return tree
    elif rule == 11: # $sections = $outputs
        ctx.rule = rules[11]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_outputs(ctx)
        tree.add(subtree)
        return tree
    elif rule == 12: # $sections = $runtime
        ctx.rule = rules[12]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_runtime(ctx)
        tree.add(subtree)
        return tree
    elif rule == 13: # $sections = $parameter_meta
        ctx.rule = rules[13]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_parameter_meta(ctx)
        tree.add(subtree)
        return tree
    elif rule == 14: # $sections = $meta
        ctx.rule = rules[14]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_meta(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[56] if x >=0],
      rules[14]
    )
def parse__gen11(ctx):
    current = ctx.tokens.current()
    rule = table[1][current.id] if current else -1
    tree = ParseTree(NonTerminal(57, '_gen11'))
    ctx.nonterminal = "_gen11"
    tree.list = False
    if current != None and current.id in nonterminal_follow[57] and current.id not in nonterminal_first[57]:
        return tree
    if current == None:
        return tree
    if rule == 52: # $_gen11 = $alias
        ctx.rule = rules[52]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_alias(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen13(ctx):
    current = ctx.tokens.current()
    rule = table[2][current.id] if current else -1
    tree = ParseTree(NonTerminal(58, '_gen13'))
    ctx.nonterminal = "_gen13"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[58] and current.id not in nonterminal_first[58]:
        return tree
    if current == None:
        return tree
    if rule == 57: # $_gen13 = $declaration $_gen13
        ctx.rule = rules[57]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_declaration(ctx)
        tree.add(subtree)
        subtree = parse__gen13(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen20(ctx):
    current = ctx.tokens.current()
    rule = table[3][current.id] if current else -1
    tree = ParseTree(NonTerminal(59, '_gen20'))
    ctx.nonterminal = "_gen20"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[59] and current.id not in nonterminal_first[59]:
        return tree
    if current == None:
        return tree
    if rule == 102: # $_gen20 = $e $_gen21
        ctx.rule = rules[102]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_e(ctx)
        tree.add(subtree)
        subtree = parse__gen21(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen6(ctx):
    current = ctx.tokens.current()
    rule = table[4][current.id] if current else -1
    tree = ParseTree(NonTerminal(60, '_gen6'))
    ctx.nonterminal = "_gen6"
    tree.list = False
    if current != None and current.id in nonterminal_follow[60] and current.id not in nonterminal_first[60]:
        return tree
    if current == None:
        return tree
    if rule == 24: # $_gen6 = $type_e
        ctx.rule = rules[24]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen21(ctx):
    current = ctx.tokens.current()
    rule = table[5][current.id] if current else -1
    tree = ParseTree(NonTerminal(61, '_gen21'))
    ctx.nonterminal = "_gen21"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[61] and current.id not in nonterminal_first[61]:
        return tree
    if current == None:
        return tree
    if rule == 103: # $_gen21 = :comma $e $_gen21
        ctx.rule = rules[103]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 33) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_e(ctx)
        tree.add(subtree)
        subtree = parse__gen21(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_declaration(ctx):
    current = ctx.tokens.current()
    rule = table[6][current.id] if current else -1
    tree = ParseTree(NonTerminal(62, 'declaration'))
    ctx.nonterminal = "declaration"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 77: # $declaration = $type_e :identifier $_gen17 -> Declaration( type=$0, name=$1, expression=$2 )
        ctx.rule = rules[77]
        ast_parameters = OrderedDict([
            ('type', 0),
            ('name', 1),
            ('expression', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Declaration', ast_parameters)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        subtree = parse__gen17(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[62] if x >=0],
      rules[77]
    )
def parse_cmd_param_kv(ctx):
    current = ctx.tokens.current()
    rule = table[7][current.id] if current else -1
    tree = ParseTree(NonTerminal(63, 'cmd_param_kv'))
    ctx.nonterminal = "cmd_param_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 29: # $cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )
        ctx.rule = rules[29]
        ast_parameters = OrderedDict([
            ('key', 1),
            ('value', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameterAttr', ast_parameters)
        t = expect(ctx, 44) # :cmd_attr_hint
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 17) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[63] if x >=0],
      rules[29]
    )
def parse__gen9(ctx):
    current = ctx.tokens.current()
    rule = table[8][current.id] if current else -1
    tree = ParseTree(NonTerminal(64, '_gen9'))
    ctx.nonterminal = "_gen9"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[64] and current.id not in nonterminal_first[64]:
        return tree
    if current == None:
        return tree
    if rule == 40: # $_gen9 = $kv $_gen9
        ctx.rule = rules[40]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_wf_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[9][current.id] if current else -1
    tree = ParseTree(NonTerminal(65, 'wf_body_element'))
    ctx.nonterminal = "wf_body_element"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 47: # $wf_body_element = $call
        ctx.rule = rules[47]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call(ctx)
        tree.add(subtree)
        return tree
    elif rule == 48: # $wf_body_element = $declaration
        ctx.rule = rules[48]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_declaration(ctx)
        tree.add(subtree)
        return tree
    elif rule == 49: # $wf_body_element = $while_loop
        ctx.rule = rules[49]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_while_loop(ctx)
        tree.add(subtree)
        return tree
    elif rule == 50: # $wf_body_element = $if_stmt
        ctx.rule = rules[50]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_if_stmt(ctx)
        tree.add(subtree)
        return tree
    elif rule == 51: # $wf_body_element = $scatter
        ctx.rule = rules[51]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_scatter(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[65] if x >=0],
      rules[51]
    )
def parse__gen15(ctx):
    current = ctx.tokens.current()
    rule = table[10][current.id] if current else -1
    tree = ParseTree(NonTerminal(66, '_gen15'))
    ctx.nonterminal = "_gen15"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[66] and current.id not in nonterminal_first[66]:
        return tree
    if current == None:
        return tree
    if rule == 64: # $_gen15 = $mapping $_gen16
        ctx.rule = rules[64]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_mapping(ctx)
        tree.add(subtree)
        subtree = parse__gen16(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_object_kv(ctx):
    current = ctx.tokens.current()
    rule = table[11][current.id] if current else -1
    tree = ParseTree(NonTerminal(67, 'object_kv'))
    ctx.nonterminal = "object_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 79: # $object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )
        ctx.rule = rules[79]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ObjectKV', ast_parameters)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[67] if x >=0],
      rules[79]
    )
def parse_parameter_meta(ctx):
    current = ctx.tokens.current()
    rule = table[12][current.id] if current else -1
    tree = ParseTree(NonTerminal(68, 'parameter_meta'))
    ctx.nonterminal = "parameter_meta"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 38: # $parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )
        ctx.rule = rules[38]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('ParameterMeta', ast_parameters)
        t = expect(ctx, 29) # :parameter_meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[68] if x >=0],
      rules[38]
    )
def parse_postfix_quantifier(ctx):
    current = ctx.tokens.current()
    rule = table[13][current.id] if current else -1
    tree = ParseTree(NonTerminal(69, 'postfix_quantifier'))
    ctx.nonterminal = "postfix_quantifier"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 30: # $postfix_quantifier = :qmark
        ctx.rule = rules[30]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 6) # :qmark
        tree.add(t)
        return tree
    elif rule == 31: # $postfix_quantifier = :plus
        ctx.rule = rules[31]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 16) # :plus
        tree.add(t)
        return tree
    elif rule == 32: # $postfix_quantifier = :asterisk
        ctx.rule = rules[32]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 35) # :asterisk
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[69] if x >=0],
      rules[32]
    )
def parse__gen17(ctx):
    current = ctx.tokens.current()
    rule = table[14][current.id] if current else -1
    tree = ParseTree(NonTerminal(70, '_gen17'))
    ctx.nonterminal = "_gen17"
    tree.list = False
    if current != None and current.id in nonterminal_follow[70] and current.id not in nonterminal_first[70]:
        return tree
    if current == None:
        return tree
    if rule == 75: # $_gen17 = $setter
        ctx.rule = rules[75]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_setter(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen7(ctx):
    current = ctx.tokens.current()
    rule = table[15][current.id] if current else -1
    tree = ParseTree(NonTerminal(71, '_gen7'))
    ctx.nonterminal = "_gen7"
    tree.list = False
    if current != None and current.id in nonterminal_follow[71] and current.id not in nonterminal_first[71]:
        return tree
    if current == None:
        return tree
    if rule == 26: # $_gen7 = $postfix_quantifier
        ctx.rule = rules[26]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_postfix_quantifier(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen2(ctx):
    current = ctx.tokens.current()
    rule = table[16][current.id] if current else -1
    tree = ParseTree(NonTerminal(72, '_gen2'))
    ctx.nonterminal = "_gen2"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[72] and current.id not in nonterminal_first[72]:
        return tree
    if current == None:
        return tree
    if rule == 7: # $_gen2 = $sections $_gen2
        ctx.rule = rules[7]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_sections(ctx)
        tree.add(subtree)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen1(ctx):
    current = ctx.tokens.current()
    rule = table[17][current.id] if current else -1
    tree = ParseTree(NonTerminal(73, '_gen1'))
    ctx.nonterminal = "_gen1"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[73] and current.id not in nonterminal_first[73]:
        return tree
    if current == None:
        return tree
    if rule == 5: # $_gen1 = $declarations $_gen1
        ctx.rule = rules[5]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_declarations(ctx)
        tree.add(subtree)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_kv(ctx):
    current = ctx.tokens.current()
    rule = table[18][current.id] if current else -1
    tree = ParseTree(NonTerminal(74, 'kv'))
    ctx.nonterminal = "kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 43: # $kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )
        ctx.rule = rules[43]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('RuntimeAttribute', ast_parameters)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[74] if x >=0],
      rules[43]
    )
def parse__gen4(ctx):
    current = ctx.tokens.current()
    rule = table[19][current.id] if current else -1
    tree = ParseTree(NonTerminal(75, '_gen4'))
    ctx.nonterminal = "_gen4"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[75] and current.id not in nonterminal_first[75]:
        return tree
    if current == None:
        return tree
    if rule == 20: # $_gen4 = $cmd_param_kv $_gen4
        ctx.rule = rules[20]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen4(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[20][current.id] if current else -1
    tree = ParseTree(NonTerminal(76, 'call_body_element'))
    ctx.nonterminal = "call_body_element"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 62: # $call_body_element = $call_input
        ctx.rule = rules[62]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_input(ctx)
        tree.add(subtree)
        return tree
    elif rule == 63: # $call_body_element = $call_output
        ctx.rule = rules[63]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_output(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[76] if x >=0],
      rules[63]
    )
def parse_document(ctx):
    current = ctx.tokens.current()
    rule = table[21][current.id] if current else -1
    tree = ParseTree(NonTerminal(77, 'document'))
    ctx.nonterminal = "document"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 2: # $document = $_gen0 -> Document( definitions=$0 )
        ctx.rule = rules[2]
        ast_parameters = OrderedDict([
            ('definitions', 0),
        ])
        tree.astTransform = AstTransformNodeCreator('Document', ast_parameters)
        subtree = parse__gen0(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[77] if x >=0],
      rules[2]
    )
def parse_task(ctx):
    current = ctx.tokens.current()
    rule = table[22][current.id] if current else -1
    tree = ParseTree(NonTerminal(78, 'task'))
    ctx.nonterminal = "task"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 9: # $task = :task :identifier :lbrace $_gen1 $_gen2 :rbrace -> Task( name=$1, declarations=$3, sections=$4 )
        ctx.rule = rules[9]
        ast_parameters = OrderedDict([
            ('name', 1),
            ('declarations', 3),
            ('sections', 4),
        ])
        tree.astTransform = AstTransformNodeCreator('Task', ast_parameters)
        t = expect(ctx, 45) # :task
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[78] if x >=0],
      rules[9]
    )
def parse__gen16(ctx):
    current = ctx.tokens.current()
    rule = table[23][current.id] if current else -1
    tree = ParseTree(NonTerminal(79, '_gen16'))
    ctx.nonterminal = "_gen16"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[79] and current.id not in nonterminal_first[79]:
        return tree
    if current == None:
        return tree
    if rule == 65: # $_gen16 = :comma $mapping $_gen16
        ctx.rule = rules[65]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 33) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_mapping(ctx)
        tree.add(subtree)
        subtree = parse__gen16(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_scatter(ctx):
    current = ctx.tokens.current()
    rule = table[24][current.id] if current else -1
    tree = ParseTree(NonTerminal(80, 'scatter'))
    ctx.nonterminal = "scatter"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 74: # $scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen10 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )
        ctx.rule = rules[74]
        ast_parameters = OrderedDict([
            ('item', 2),
            ('collection', 4),
            ('body', 7),
        ])
        tree.astTransform = AstTransformNodeCreator('Scatter', ast_parameters)
        t = expect(ctx, 40) # :scatter
        tree.add(t)
        t = expect(ctx, 11) # :lparen
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 51) # :in
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 24) # :rparen
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[80] if x >=0],
      rules[74]
    )
def parse_call_output(ctx):
    current = ctx.tokens.current()
    rule = table[25][current.id] if current else -1
    tree = ParseTree(NonTerminal(81, 'call_output'))
    ctx.nonterminal = "call_output"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 69: # $call_output = :output :colon $_gen15 -> Outputs( map=$2 )
        ctx.rule = rules[69]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Outputs', ast_parameters)
        t = expect(ctx, 28) # :output
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[81] if x >=0],
      rules[69]
    )
def parse_call_body(ctx):
    current = ctx.tokens.current()
    rule = table[26][current.id] if current else -1
    tree = ParseTree(NonTerminal(82, 'call_body'))
    ctx.nonterminal = "call_body"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 61: # $call_body = :lbrace $_gen13 $_gen14 :rbrace -> CallBody( declarations=$1, io=$2 )
        ctx.rule = rules[61]
        ast_parameters = OrderedDict([
            ('declarations', 1),
            ('io', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('CallBody', ast_parameters)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen13(ctx)
        tree.add(subtree)
        subtree = parse__gen14(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[82] if x >=0],
      rules[61]
    )
def parse_meta(ctx):
    current = ctx.tokens.current()
    rule = table[27][current.id] if current else -1
    tree = ParseTree(NonTerminal(83, 'meta'))
    ctx.nonterminal = "meta"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 39: # $meta = :meta $map -> Meta( map=$1 )
        ctx.rule = rules[39]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('Meta', ast_parameters)
        t = expect(ctx, 7) # :meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[83] if x >=0],
      rules[39]
    )
def parse_call(ctx):
    current = ctx.tokens.current()
    rule = table[28][current.id] if current else -1
    tree = ParseTree(NonTerminal(84, 'call'))
    ctx.nonterminal = "call"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 56: # $call = :call :identifier $_gen11 $_gen12 -> Call( task=$1, alias=$2, body=$3 )
        ctx.rule = rules[56]
        ast_parameters = OrderedDict([
            ('task', 1),
            ('alias', 2),
            ('body', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Call', ast_parameters)
        t = expect(ctx, 8) # :call
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        subtree = parse__gen11(ctx)
        tree.add(subtree)
        subtree = parse__gen12(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[84] if x >=0],
      rules[56]
    )
def parse_runtime(ctx):
    current = ctx.tokens.current()
    rule = table[29][current.id] if current else -1
    tree = ParseTree(NonTerminal(85, 'runtime'))
    ctx.nonterminal = "runtime"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 37: # $runtime = :runtime $map -> Runtime( map=$1 )
        ctx.rule = rules[37]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('Runtime', ast_parameters)
        t = expect(ctx, 22) # :runtime
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[85] if x >=0],
      rules[37]
    )
def parse__gen19(ctx):
    current = ctx.tokens.current()
    rule = table[30][current.id] if current else -1
    tree = ParseTree(NonTerminal(86, '_gen19'))
    ctx.nonterminal = "_gen19"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[86] and current.id not in nonterminal_first[86]:
        return tree
    if current == None:
        return tree
    if rule == 81: # $_gen19 = :comma $type_e $_gen19
        ctx.rule = rules[81]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 33) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        subtree = parse__gen19(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_if_stmt(ctx):
    current = ctx.tokens.current()
    rule = table[31][current.id] if current else -1
    tree = ParseTree(NonTerminal(87, 'if_stmt'))
    ctx.nonterminal = "if_stmt"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 73: # $if_stmt = :if :lparen $e :rparen :lbrace $_gen10 :rbrace -> If( expression=$2, body=$5 )
        ctx.rule = rules[73]
        ast_parameters = OrderedDict([
            ('expression', 2),
            ('body', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('If', ast_parameters)
        t = expect(ctx, 20) # :if
        tree.add(t)
        t = expect(ctx, 11) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 24) # :rparen
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[87] if x >=0],
      rules[73]
    )
def parse_command_part(ctx):
    current = ctx.tokens.current()
    rule = table[32][current.id] if current else -1
    tree = ParseTree(NonTerminal(88, 'command_part'))
    ctx.nonterminal = "command_part"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 18: # $command_part = :cmd_part
        ctx.rule = rules[18]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 14) # :cmd_part
        tree.add(t)
        return tree
    elif rule == 19: # $command_part = $cmd_param
        ctx.rule = rules[19]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[88] if x >=0],
      rules[19]
    )
def parse__gen23(ctx):
    current = ctx.tokens.current()
    rule = table[33][current.id] if current else -1
    tree = ParseTree(NonTerminal(89, '_gen23'))
    ctx.nonterminal = "_gen23"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[89] and current.id not in nonterminal_first[89]:
        return tree
    if current == None:
        return tree
    if rule == 110: # $_gen23 = :comma $object_kv $_gen23
        ctx.rule = rules[110]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 33) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_object_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen23(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen5(ctx):
    current = ctx.tokens.current()
    rule = table[34][current.id] if current else -1
    tree = ParseTree(NonTerminal(90, '_gen5'))
    ctx.nonterminal = "_gen5"
    tree.list = False
    if current != None and current.id in nonterminal_follow[90] and current.id not in nonterminal_first[90]:
        return tree
    if current == None:
        return tree
    if rule == 22: # $_gen5 = :string
        ctx.rule = rules[22]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 39) # :string
        tree.add(t)
        return tree
    return tree
def parse__gen14(ctx):
    current = ctx.tokens.current()
    rule = table[35][current.id] if current else -1
    tree = ParseTree(NonTerminal(91, '_gen14'))
    ctx.nonterminal = "_gen14"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[91] and current.id not in nonterminal_first[91]:
        return tree
    if current == None:
        return tree
    if rule == 59: # $_gen14 = $call_body_element $_gen14
        ctx.rule = rules[59]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_body_element(ctx)
        tree.add(subtree)
        subtree = parse__gen14(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen0(ctx):
    current = ctx.tokens.current()
    rule = table[36][current.id] if current else -1
    tree = ParseTree(NonTerminal(92, '_gen0'))
    ctx.nonterminal = "_gen0"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[92] and current.id not in nonterminal_first[92]:
        return tree
    if current == None:
        return tree
    if rule == 0: # $_gen0 = $workflow_or_task $_gen0
        ctx.rule = rules[0]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_workflow_or_task(ctx)
        tree.add(subtree)
        subtree = parse__gen0(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_mapping(ctx):
    current = ctx.tokens.current()
    rule = table[37][current.id] if current else -1
    tree = ParseTree(NonTerminal(93, 'mapping'))
    ctx.nonterminal = "mapping"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 70: # $mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )
        ctx.rule = rules[70]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('IOMapping', ast_parameters)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 17) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[93] if x >=0],
      rules[70]
    )
def parse_command(ctx):
    current = ctx.tokens.current()
    rule = table[38][current.id] if current else -1
    tree = ParseTree(NonTerminal(94, 'command'))
    ctx.nonterminal = "command"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 17: # $command = :raw_command :raw_cmd_start $_gen3 :raw_cmd_end -> RawCommand( parts=$2 )
        ctx.rule = rules[17]
        ast_parameters = OrderedDict([
            ('parts', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('RawCommand', ast_parameters)
        t = expect(ctx, 19) # :raw_command
        tree.add(t)
        t = expect(ctx, 27) # :raw_cmd_start
        tree.add(t)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        t = expect(ctx, 38) # :raw_cmd_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[94] if x >=0],
      rules[17]
    )
def parse_cmd_param(ctx):
    current = ctx.tokens.current()
    rule = table[39][current.id] if current else -1
    tree = ParseTree(NonTerminal(95, 'cmd_param'))
    ctx.nonterminal = "cmd_param"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 28: # $cmd_param = :cmd_param_start $_gen4 $_gen5 $_gen6 :identifier $_gen7 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )
        ctx.rule = rules[28]
        ast_parameters = OrderedDict([
            ('name', 4),
            ('type', 3),
            ('prefix', 2),
            ('attributes', 1),
            ('postfix', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameter', ast_parameters)
        t = expect(ctx, 37) # :cmd_param_start
        tree.add(t)
        subtree = parse__gen4(ctx)
        tree.add(subtree)
        subtree = parse__gen5(ctx)
        tree.add(subtree)
        subtree = parse__gen6(ctx)
        tree.add(subtree)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        subtree = parse__gen7(ctx)
        tree.add(subtree)
        t = expect(ctx, 9) # :cmd_param_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[95] if x >=0],
      rules[28]
    )
def parse_workflow_or_task(ctx):
    current = ctx.tokens.current()
    rule = table[40][current.id] if current else -1
    tree = ParseTree(NonTerminal(96, 'workflow_or_task'))
    ctx.nonterminal = "workflow_or_task"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 3: # $workflow_or_task = $workflow
        ctx.rule = rules[3]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_workflow(ctx)
        tree.add(subtree)
        return tree
    elif rule == 4: # $workflow_or_task = $task
        ctx.rule = rules[4]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_task(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[96] if x >=0],
      rules[4]
    )
def parse_map(ctx):
    current = ctx.tokens.current()
    rule = table[41][current.id] if current else -1
    tree = ParseTree(NonTerminal(97, 'map'))
    ctx.nonterminal = "map"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 42: # $map = :lbrace $_gen9 :rbrace -> $1
        ctx.rule = rules[42]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[97] if x >=0],
      rules[42]
    )
def parse__gen18(ctx):
    current = ctx.tokens.current()
    rule = table[42][current.id] if current else -1
    tree = ParseTree(NonTerminal(98, '_gen18'))
    ctx.nonterminal = "_gen18"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[98] and current.id not in nonterminal_first[98]:
        return tree
    if current == None:
        return tree
    if rule == 80: # $_gen18 = $type_e $_gen19
        ctx.rule = rules[80]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        subtree = parse__gen19(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_while_loop(ctx):
    current = ctx.tokens.current()
    rule = table[43][current.id] if current else -1
    tree = ParseTree(NonTerminal(99, 'while_loop'))
    ctx.nonterminal = "while_loop"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 72: # $while_loop = :while :lparen $e :rparen :lbrace $_gen10 :rbrace -> WhileLoop( expression=$2, body=$5 )
        ctx.rule = rules[72]
        ast_parameters = OrderedDict([
            ('expression', 2),
            ('body', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('WhileLoop', ast_parameters)
        t = expect(ctx, 1) # :while
        tree.add(t)
        t = expect(ctx, 11) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 24) # :rparen
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[99] if x >=0],
      rules[72]
    )
def parse_workflow(ctx):
    current = ctx.tokens.current()
    rule = table[44][current.id] if current else -1
    tree = ParseTree(NonTerminal(100, 'workflow'))
    ctx.nonterminal = "workflow"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 46: # $workflow = :workflow :identifier :lbrace $_gen10 :rbrace -> Workflow( name=$1, body=$3 )
        ctx.rule = rules[46]
        ast_parameters = OrderedDict([
            ('name', 1),
            ('body', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Workflow', ast_parameters)
        t = expect(ctx, 50) # :workflow
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[100] if x >=0],
      rules[46]
    )
def parse__gen12(ctx):
    current = ctx.tokens.current()
    rule = table[45][current.id] if current else -1
    tree = ParseTree(NonTerminal(101, '_gen12'))
    ctx.nonterminal = "_gen12"
    tree.list = False
    if current != None and current.id in nonterminal_follow[101] and current.id not in nonterminal_first[101]:
        return tree
    if current == None:
        return tree
    if rule == 54: # $_gen12 = $call_body
        ctx.rule = rules[54]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_body(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_declarations(ctx):
    current = ctx.tokens.current()
    rule = table[46][current.id] if current else -1
    tree = ParseTree(NonTerminal(102, 'declarations'))
    ctx.nonterminal = "declarations"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[102] if x >=0],
      rules[54]
    )
def parse_outputs(ctx):
    current = ctx.tokens.current()
    rule = table[47][current.id] if current else -1
    tree = ParseTree(NonTerminal(103, 'outputs'))
    ctx.nonterminal = "outputs"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 35: # $outputs = :output :lbrace $_gen8 :rbrace -> Outputs( attributes=$2 )
        ctx.rule = rules[35]
        ast_parameters = OrderedDict([
            ('attributes', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Outputs', ast_parameters)
        t = expect(ctx, 28) # :output
        tree.add(t)
        t = expect(ctx, 48) # :lbrace
        tree.add(t)
        subtree = parse__gen8(ctx)
        tree.add(subtree)
        t = expect(ctx, 18) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[103] if x >=0],
      rules[35]
    )
def parse_output_kv(ctx):
    current = ctx.tokens.current()
    rule = table[48][current.id] if current else -1
    tree = ParseTree(NonTerminal(104, 'output_kv'))
    ctx.nonterminal = "output_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 36: # $output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )
        ctx.rule = rules[36]
        ast_parameters = OrderedDict([
            ('type', 0),
            ('var', 1),
            ('expression', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Output', ast_parameters)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        t = expect(ctx, 17) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[104] if x >=0],
      rules[36]
    )
def parse__gen8(ctx):
    current = ctx.tokens.current()
    rule = table[49][current.id] if current else -1
    tree = ParseTree(NonTerminal(105, '_gen8'))
    ctx.nonterminal = "_gen8"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[105] and current.id not in nonterminal_first[105]:
        return tree
    if current == None:
        return tree
    if rule == 33: # $_gen8 = $output_kv $_gen8
        ctx.rule = rules[33]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_output_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen8(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen10(ctx):
    current = ctx.tokens.current()
    rule = table[50][current.id] if current else -1
    tree = ParseTree(NonTerminal(106, '_gen10'))
    ctx.nonterminal = "_gen10"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[106] and current.id not in nonterminal_first[106]:
        return tree
    if current == None:
        return tree
    if rule == 44: # $_gen10 = $wf_body_element $_gen10
        ctx.rule = rules[44]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_wf_body_element(ctx)
        tree.add(subtree)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen22(ctx):
    current = ctx.tokens.current()
    rule = table[51][current.id] if current else -1
    tree = ParseTree(NonTerminal(107, '_gen22'))
    ctx.nonterminal = "_gen22"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[107] and current.id not in nonterminal_first[107]:
        return tree
    if current == None:
        return tree
    if rule == 109: # $_gen22 = $object_kv $_gen23
        ctx.rule = rules[109]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_object_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen23(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_alias(ctx):
    current = ctx.tokens.current()
    rule = table[52][current.id] if current else -1
    tree = ParseTree(NonTerminal(108, 'alias'))
    ctx.nonterminal = "alias"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 71: # $alias = :as :identifier -> $1
        ctx.rule = rules[71]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 30) # :as
        tree.add(t)
        t = expect(ctx, 52) # :identifier
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[108] if x >=0],
      rules[71]
    )
def parse__gen3(ctx):
    current = ctx.tokens.current()
    rule = table[53][current.id] if current else -1
    tree = ParseTree(NonTerminal(109, '_gen3'))
    ctx.nonterminal = "_gen3"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[109] and current.id not in nonterminal_first[109]:
        return tree
    if current == None:
        return tree
    if rule == 15: # $_gen3 = $command_part $_gen3
        ctx.rule = rules[15]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command_part(ctx)
        tree.add(subtree)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call_input(ctx):
    current = ctx.tokens.current()
    rule = table[56][current.id] if current else -1
    tree = ParseTree(NonTerminal(112, 'call_input'))
    ctx.nonterminal = "call_input"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 68: # $call_input = :input :colon $_gen15 -> Inputs( map=$2 )
        ctx.rule = rules[68]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Inputs', ast_parameters)
        t = expect(ctx, 23) # :input
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[112] if x >=0],
      rules[68]
    )
def parse_setter(ctx):
    current = ctx.tokens.current()
    rule = table[57][current.id] if current else -1
    tree = ParseTree(NonTerminal(113, 'setter'))
    ctx.nonterminal = "setter"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 78: # $setter = :equal $e -> $1
        ctx.rule = rules[78]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 17) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[113] if x >=0],
      rules[78]
    )
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
          (re.compile(r'/\*(.*?)\*/', re.DOTALL), [
              # (terminal, group, function)
          ]),
          (re.compile(r'#.*'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'task(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('task', 0, None),
          ]),
          (re.compile(r'call(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('call', 0, None),
          ]),
          (re.compile(r'workflow(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('workflow', 0, None),
          ]),
          (re.compile(r'input(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('input', 0, None),
          ]),
          (re.compile(r'output(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('output', 0, None),
          ]),
          (re.compile(r'as(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('as', 0, None),
          ]),
          (re.compile(r'if(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('if', 0, None),
          ]),
          (re.compile(r'while(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('while', 0, None),
          ]),
          (re.compile(r'runtime(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('runtime', 0, None),
          ]),
          (re.compile(r'scatter(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('scatter', 0, None),
              LexerStackPush('scatter'),
          ]),
          (re.compile(r'command\s*(?=<<<)'), [
              # (terminal, group, function)
              ('raw_command', 0, None),
              LexerStackPush('raw_command2'),
          ]),
          (re.compile(r'command\s*(?=\{)'), [
              # (terminal, group, function)
              ('raw_command', 0, None),
              LexerStackPush('raw_command'),
          ]),
          (re.compile(r'parameter_meta(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('parameter_meta', 0, None),
          ]),
          (re.compile(r'meta(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('meta', 0, None),
          ]),
          (re.compile(r'(true|false)(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('boolean', 0, None),
          ]),
          (re.compile(r'(object)\s*(\{)'), [
              # (terminal, group, function)
              ('object', 0, None),
              ('lbrace', 0, None),
          ]),
          (re.compile(r'(Array|Map|Object|Boolean|Int|Float|Uri|File|String)(?![a-zA-Z0-9_])(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('type', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_])*'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
          (re.compile(r'"([^\"]+)"'), [
              # (terminal, group, function)
              ('string', 1, None),
          ]),
          (re.compile(r'\'([^\']+)\''), [
              # (terminal, group, function)
              ('string', 1, None),
          ]),
          (re.compile(r':'), [
              # (terminal, group, function)
              ('colon', 0, None),
          ]),
          (re.compile(r','), [
              # (terminal, group, function)
              ('comma', 0, None),
          ]),
          (re.compile(r'=='), [
              # (terminal, group, function)
              ('double_equal', 0, None),
          ]),
          (re.compile(r'!='), [
              # (terminal, group, function)
              ('not_equal', 0, None),
          ]),
          (re.compile(r'='), [
              # (terminal, group, function)
              ('equal', 0, None),
          ]),
          (re.compile(r'\.'), [
              # (terminal, group, function)
              ('dot', 0, None),
          ]),
          (re.compile(r'\{'), [
              # (terminal, group, function)
              ('lbrace', 0, None),
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('rbrace', 0, None),
          ]),
          (re.compile(r'\('), [
              # (terminal, group, function)
              ('lparen', 0, None),
          ]),
          (re.compile(r'\)'), [
              # (terminal, group, function)
              ('rparen', 0, None),
          ]),
          (re.compile(r'\['), [
              # (terminal, group, function)
              ('lsquare', 0, None),
          ]),
          (re.compile(r'\]'), [
              # (terminal, group, function)
              ('rsquare', 0, None),
          ]),
          (re.compile(r'\+'), [
              # (terminal, group, function)
              ('plus', 0, None),
          ]),
          (re.compile(r'\*'), [
              # (terminal, group, function)
              ('asterisk', 0, None),
          ]),
          (re.compile(r'-'), [
              # (terminal, group, function)
              ('dash', 0, None),
          ]),
          (re.compile(r'/'), [
              # (terminal, group, function)
              ('slash', 0, None),
          ]),
          (re.compile(r'%'), [
              # (terminal, group, function)
              ('percent', 0, None),
          ]),
          (re.compile(r'<='), [
              # (terminal, group, function)
              ('lteq', 0, None),
          ]),
          (re.compile(r'<'), [
              # (terminal, group, function)
              ('lt', 0, None),
          ]),
          (re.compile(r'>='), [
              # (terminal, group, function)
              ('gteq', 0, None),
          ]),
          (re.compile(r'>'), [
              # (terminal, group, function)
              ('gt', 0, None),
          ]),
          (re.compile(r'!'), [
              # (terminal, group, function)
              ('not', 0, None),
          ]),
          (re.compile(r'-?[0-9]+\.[0-9]+'), [
              # (terminal, group, function)
              ('float', 0, None),
          ]),
          (re.compile(r'[0-9]+'), [
              # (terminal, group, function)
              ('integer', 0, None),
          ]),
        ]),
        'scatter': OrderedDict([
          (re.compile(r'\s+'), [
              # (terminal, group, function)
          ]),
          (re.compile(r'\)'), [
              # (terminal, group, function)
              ('rparen', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'\('), [
              # (terminal, group, function)
              ('lparen', 0, None),
          ]),
          (re.compile(r'\.'), [
              # (terminal, group, function)
              ('dot', 0, None),
          ]),
          (re.compile(r'\['), [
              # (terminal, group, function)
              ('lsquare', 0, None),
          ]),
          (re.compile(r'\]'), [
              # (terminal, group, function)
              ('rsquare', 0, None),
          ]),
          (re.compile(r'in(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('in', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_])*'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
        ]),
        'raw_command': OrderedDict([
          (re.compile(r'\{'), [
              # (terminal, group, function)
              ('raw_cmd_start', 0, None),
          ]),
          (re.compile(r'\}'), [
              # (terminal, group, function)
              ('raw_cmd_end', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'\$\{'), [
              # (terminal, group, function)
              ('cmd_param_start', 0, None),
              LexerStackPush('cmd_param'),
          ]),
          (re.compile(r'(.*?)(?=\$\{|\})', re.DOTALL), [
              # (terminal, group, function)
              ('cmd_part', 0, None),
          ]),
        ]),
        'raw_command2': OrderedDict([
          (re.compile(r'<<<'), [
              # (terminal, group, function)
              ('raw_cmd_start', 0, None),
          ]),
          (re.compile(r'>>>'), [
              # (terminal, group, function)
              ('raw_cmd_end', 0, None),
              LexerAction('pop'),
          ]),
          (re.compile(r'\$\{'), [
              # (terminal, group, function)
              ('cmd_param_start', 0, None),
              LexerStackPush('cmd_param'),
          ]),
          (re.compile(r'(.*?)(?=\$\{|>>>)', re.DOTALL), [
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
          (re.compile(r'\['), [
              # (terminal, group, function)
              ('lsquare', 0, None),
          ]),
          (re.compile(r'\]'), [
              # (terminal, group, function)
              ('rsquare', 0, None),
          ]),
          (re.compile(r'='), [
              # (terminal, group, function)
              ('equal', 0, None),
          ]),
          (re.compile(r'\?'), [
              # (terminal, group, function)
              ('qmark', 0, None),
          ]),
          (re.compile(r'\+'), [
              # (terminal, group, function)
              ('plus', 0, None),
          ]),
          (re.compile(r'\*'), [
              # (terminal, group, function)
              ('asterisk', 0, None),
          ]),
          (re.compile(r'[0-9]+'), [
              # (terminal, group, function)
              ('integer', 0, None),
          ]),
          (re.compile(r'(true|false)(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('boolean', 0, None),
          ]),
          (re.compile(r'(Array|Map|Object|Boolean|Int|Float|Uri|File|String)(?![a-zA-Z0-9_])(?![a-zA-Z0-9_])'), [
              # (terminal, group, function)
              ('type', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_])*(?=\s*=)'), [
              # (terminal, group, function)
              ('cmd_attr_hint', None, None),
              ('identifier', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_])*'), [
              # (terminal, group, function)
              ('identifier', 0, None),
          ]),
          (re.compile(r'"([^\"]+)"'), [
              # (terminal, group, function)
              ('string', 1, None),
          ]),
          (re.compile(r'\'([^\']+)\''), [
              # (terminal, group, function)
              ('string', 1, None),
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
