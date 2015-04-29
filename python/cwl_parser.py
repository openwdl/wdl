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
    def __init__(self, source, resource):
        self.errors = []
        self.__dict__.update(locals())
        self.lines = source.split('\n')
    def _error(self, string):
        error = SyntaxError(string)
        self.errors.append(error)
        return error
    def _get_line_col(self, line, col):
        line = self.lines[line-1]
        return "{}\n{}^".format(line, ' ' * (col-1))
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
    def no_more_tokens(self, rule, expected_terminal, last_terminal):
        error = "{resource}:{line}:{col}: error: No more tokens left to consume.  Expecting :{token}\n\n".format(
            resource=self.resource,
            line=last_terminal.line,
            col=last_terminal.col,
            token=expected_terminal
        )
        error += "{}\n\n".format(self._get_line_col(last_terminal.line, last_terminal.col))
        error += 'Rule: ' + rule
        return self._error(error)
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
    0: 'comma',
    1: 'cmd_attr_hint',
    2: 'rsquare',
    3: 'qmark',
    4: 'if',
    5: 'not',
    6: 'string',
    7: 'cmd_part',
    8: 'lbrace',
    9: 'runtime',
    10: 'output',
    11: 'dquote_string',
    12: 'raw_command',
    13: 'type_e',
    14: 'raw_cmd_end',
    15: 'call',
    16: 'meta',
    17: 'parameter_meta',
    18: 'gt',
    19: 'rbrace',
    20: 'raw_cmd_start',
    21: 'integer',
    22: 'cmd_param_end',
    23: 'workflow',
    24: 'lsquare',
    25: 'while',
    26: 'rparen',
    27: 'dash',
    28: 'double_pipe',
    29: 'slash',
    30: 'lteq',
    31: 'type',
    32: 'asterisk',
    33: 'task',
    34: 'squote_string',
    35: 'equal',
    36: 'in',
    37: 'double_ampersand',
    38: 'double_equal',
    39: 'boolean',
    40: 'cmd_param_start',
    41: 'dot',
    42: 'colon',
    43: 'object',
    44: 'scatter',
    45: 'gteq',
    46: 'lparen',
    47: 'input',
    48: 'percent',
    49: 'as',
    50: 'lt',
    51: 'not_equal',
    52: 'plus',
    53: 'e',
    54: 'identifier',
    'comma': 0,
    'cmd_attr_hint': 1,
    'rsquare': 2,
    'qmark': 3,
    'if': 4,
    'not': 5,
    'string': 6,
    'cmd_part': 7,
    'lbrace': 8,
    'runtime': 9,
    'output': 10,
    'dquote_string': 11,
    'raw_command': 12,
    'type_e': 13,
    'raw_cmd_end': 14,
    'call': 15,
    'meta': 16,
    'parameter_meta': 17,
    'gt': 18,
    'rbrace': 19,
    'raw_cmd_start': 20,
    'integer': 21,
    'cmd_param_end': 22,
    'workflow': 23,
    'lsquare': 24,
    'while': 25,
    'rparen': 26,
    'dash': 27,
    'double_pipe': 28,
    'slash': 29,
    'lteq': 30,
    'type': 31,
    'asterisk': 32,
    'task': 33,
    'squote_string': 34,
    'equal': 35,
    'in': 36,
    'double_ampersand': 37,
    'double_equal': 38,
    'boolean': 39,
    'cmd_param_start': 40,
    'dot': 41,
    'colon': 42,
    'object': 43,
    'scatter': 44,
    'gteq': 45,
    'lparen': 46,
    'input': 47,
    'percent': 48,
    'as': 49,
    'lt': 50,
    'not_equal': 51,
    'plus': 52,
    'e': 53,
    'identifier': 54,
}
# table[nonterminal][terminal] = rule
table = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 100, 100, -1, -1, -1, -1, 100, -1, -1, -1, -1, -1, -1, -1, -1, -1, 100, -1, -1, -1, -1, 103, 100, -1, -1, -1, -1, -1, -1, 100, -1, -1, -1, -1, 100, -1, -1, -1, 100, -1, -1, 100, -1, -1, -1, -1, -1, 100, 100, 100],
    [-1, -1, -1, -1, 51, -1, -1, -1, 51, -1, -1, -1, -1, 51, -1, 51, -1, -1, -1, 51, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, 50, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 77],
    [-1, -1, -1, -1, -1, -1, -1, -1, 40, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 69, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 70, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 53, -1, -1, -1, 52, -1, -1, -1, -1, 53, -1, 53, -1, -1, -1, 53, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 65, -1, -1, -1, -1, -1, -1, -1, -1, 65, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 65, -1, -1, -1, -1, -1, -1, 62],
    [-1, -1, 81, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 78, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 78, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 10, 9, -1, 8, -1, -1, -1, 12, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 54, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 72, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 68],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 56, -1, -1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 56, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [101, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 102, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 74, -1, -1, -1, -1, -1, 74, -1, -1, 74, -1, 74, -1, -1, -1, 74, -1, -1, -1, -1, -1, 74, -1, -1, -1, -1, -1, 74, -1, -1, -1, 73, -1, -1, -1, -1, -1, -1, -1, -1, 74, -1, -1, 74, -1, -1, -1, -1, -1, -1, -1],
    [63, -1, -1, -1, -1, -1, -1, -1, -1, -1, 64, -1, -1, -1, -1, -1, -1, -1, -1, 64, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 64, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 67, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, 46, -1, 45, -1, -1, -1, -1, -1, -1, -1, -1, -1, 47, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 71, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41],
    [-1, 18, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 75, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 75, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 110, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 107],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 5, 5, -1, 5, -1, -1, -1, 5, 5, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, 42, -1, -1, -1, 43, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 57, -1, -1, -1, -1, -1, -1, -1, -1, 58, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 57, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [79, -1, 80, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [108, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 109, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 59, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]
nonterminal_first = {
    55: [23, 33, -1],
    56: [47],
    57: [21, 5, 27, 6, 11, 34, 39, -1, 43, 46, 53, 52, 54],
    58: [49, -1],
    59: [54],
    60: [8],
    61: [49],
    62: [31, 13],
    63: [25],
    64: [16],
    65: [8, -1],
    66: [-1, 54],
    67: [31, 13, -1],
    68: [12, 17, 9, 10, 16],
    69: [-1, 54],
    70: [15],
    71: [23, 33, -1],
    72: [44],
    73: [32, 52, 3],
    74: [34, 21, 39, 5, 27, 43, 6, 46, 11, 52, 53, 54],
    75: [40, -1, 7],
    76: [54],
    77: [31, 13, -1],
    78: [10],
    79: [31, 13, -1],
    80: [23],
    81: [1],
    82: [0, -1],
    83: [31, 13, -1],
    84: [-1, 35],
    85: [0, -1],
    86: [40],
    87: [23, 33],
    88: [12],
    89: [31, 13],
    90: [9],
    91: [32, 52, -1, 3],
    92: [10],
    93: [10, 47],
    94: [13, 44, 4, 31, 15, 25],
    95: [4],
    96: [54],
    97: [1, -1],
    98: [31, 13],
    99: [-1, 54],
    100: [12, 17, 9, 10, -1, 16],
    101: [13, 4, 15, -1, 25, 44, 31],
    102: [17],
    103: [6, -1],
    104: [10, -1, 47],
    105: [40, 7],
    106: [35],
    107: [0, -1],
    108: [33],
    109: [0, -1],
    110: [8],
}
nonterminal_follow = {
    55: [-1],
    56: [10, 19, 47],
    57: [26],
    58: [13, 4, 15, 25, 44, 31, 8, 19],
    59: [0, 19],
    60: [12, 16, 17, 9, 10, 19],
    61: [13, 4, 15, 25, 44, 31, 8, 19],
    62: [31, 13, 19],
    63: [13, 4, 15, 25, 44, 31, 19],
    64: [12, 16, 17, 9, 10, 19],
    65: [13, 4, 15, 25, 44, 31, 19],
    66: [10, 19, 47],
    67: [2],
    68: [12, 17, 9, 10, 19, 16],
    69: [19],
    70: [13, 4, 15, 25, 44, 31, 19],
    71: [-1],
    72: [13, 4, 15, 25, 44, 31, 19],
    73: [22],
    74: [0, 1, 2, 4, 26, 27, 25, 28, 29, 6, 30, 31, 32, 10, 38, 13, 37, 15, 44, 45, 47, 48, 18, 50, 51, 52, 19, 54],
    75: [14],
    76: [0, 47, 10, 19],
    77: [10, 47],
    78: [12, 16, 17, 9, 10, 19],
    79: [54],
    80: [23, 33, -1],
    81: [6, 1],
    82: [26],
    83: [19],
    84: [13, 4, 15, 25, 44, 47, 31, 10, 19],
    85: [10, 19, 47],
    86: [14, 40, 7],
    87: [23, 33, -1],
    88: [12, 16, 17, 9, 10, 19],
    89: [0, 2, 54],
    90: [12, 16, 17, 9, 10, 19],
    91: [22],
    92: [10, 19, 47],
    93: [10, 19, 47],
    94: [13, 44, 4, 31, 15, 19, 25],
    95: [13, 4, 15, 25, 44, 31, 19],
    96: [19, 54],
    97: [6],
    98: [13, 44, 4, 31, 47, 15, 10, 19, 25],
    99: [19],
    100: [19],
    101: [19],
    102: [12, 16, 17, 9, 10, 19],
    103: [31, 13],
    104: [19],
    105: [14, 40, 7],
    106: [13, 4, 15, 25, 44, 47, 31, 10, 19],
    107: [2],
    108: [23, 33, -1],
    109: [19],
    110: [13, 4, 15, 25, 44, 31, 19],
}
rule_first = {
    0: [23, 33],
    1: [-1],
    2: [23, 33, -1],
    3: [23],
    4: [33],
    5: [12, 17, 9, 10, 16],
    6: [-1],
    7: [33],
    8: [12],
    9: [10],
    10: [9],
    11: [17],
    12: [16],
    13: [40, 7],
    14: [-1],
    15: [12],
    16: [7],
    17: [40],
    18: [1],
    19: [-1],
    20: [6],
    21: [-1],
    22: [31, 13],
    23: [-1],
    24: [32, 52, 3],
    25: [-1],
    26: [40],
    27: [1],
    28: [3],
    29: [52],
    30: [32],
    31: [31, 13],
    32: [-1],
    33: [10],
    34: [31, 13],
    35: [9],
    36: [17],
    37: [16],
    38: [54],
    39: [-1],
    40: [8],
    41: [54],
    42: [13, 44, 4, 31, 15, 25],
    43: [-1],
    44: [23],
    45: [15],
    46: [31, 13],
    47: [25],
    48: [4],
    49: [44],
    50: [49],
    51: [-1],
    52: [8],
    53: [-1],
    54: [15],
    55: [31, 13],
    56: [-1],
    57: [10, 47],
    58: [-1],
    59: [8],
    60: [47],
    61: [10],
    62: [54],
    63: [0],
    64: [-1],
    65: [-1],
    66: [47],
    67: [10],
    68: [54],
    69: [49],
    70: [25],
    71: [4],
    72: [44],
    73: [35],
    74: [-1],
    75: [31, 13],
    76: [35],
    77: [54],
    78: [31, 13],
    79: [0],
    80: [-1],
    81: [-1],
    82: [31],
    83: [31],
    84: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    85: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    86: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    87: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    88: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    89: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    90: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    91: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    92: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    93: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    94: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    95: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    96: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    97: [5],
    98: [52],
    99: [27],
    100: [53, 21, 39, 5, 27, 43, 6, 46, 11, 34, 52, 54],
    101: [0],
    102: [-1],
    103: [-1],
    104: [54],
    105: [54],
    106: [54],
    107: [54],
    108: [0],
    109: [-1],
    110: [-1],
    111: [43],
    112: [46],
    113: [6],
    114: [54],
    115: [39],
    116: [21],
    117: [11],
    118: [34],
}
nonterminal_rules = {
    55: [
        "$_gen0 = $workflow_or_task $_gen0",
        "$_gen0 = :_empty",
    ],
    56: [
        "$call_input = :input :colon $_gen14 -> Inputs( map=$2 )",
    ],
    57: [
        "$_gen19 = $e $_gen20",
        "$_gen19 = :_empty",
    ],
    58: [
        "$_gen10 = $alias",
        "$_gen10 = :_empty",
    ],
    59: [
        "$object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )",
    ],
    60: [
        "$map = :lbrace $_gen8 :rbrace -> $1",
    ],
    61: [
        "$alias = :as :identifier -> $1",
    ],
    62: [
        "$output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )",
    ],
    63: [
        "$while_loop = :while :lparen $e :rparen :lbrace $_gen9 :rbrace -> WhileLoop( expression=$2, body=$5 )",
    ],
    64: [
        "$meta = :meta $map -> Meta( map=$1 )",
    ],
    65: [
        "$_gen11 = $call_body",
        "$_gen11 = :_empty",
    ],
    66: [
        "$_gen14 = $mapping $_gen15",
        "$_gen14 = :_empty",
    ],
    67: [
        "$_gen17 = $type_e $_gen18",
        "$_gen17 = :_empty",
    ],
    68: [
        "$sections = $command",
        "$sections = $outputs",
        "$sections = $runtime",
        "$sections = $parameter_meta",
        "$sections = $meta",
    ],
    69: [
        "$_gen8 = $kv $_gen8",
        "$_gen8 = :_empty",
    ],
    70: [
        "$call = :call :identifier $_gen10 $_gen11 -> Call( task=$1, alias=$2, body=$3 )",
    ],
    71: [
        "$document = $_gen0",
    ],
    72: [
        "$scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen9 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )",
    ],
    73: [
        "$postfix_qualifier = :qmark",
        "$postfix_qualifier = :plus",
        "$postfix_qualifier = :asterisk",
    ],
    74: [
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
        "$e = :identifier <=> :lparen $_gen19 :rparen -> FunctionCall( name=$0, params=$2 )",
        "$e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )",
        "$e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )",
        "$e = :object :lbrace $_gen21 :rbrace -> ObjectLiteral( map=$2 )",
        "$e = :lparen $e :rparen -> $1",
        "$e = :string",
        "$e = :identifier",
        "$e = :boolean",
        "$e = :integer",
        "$e = :dquote_string",
        "$e = :squote_string",
    ],
    75: [
        "$_gen2 = $command_part $_gen2",
        "$_gen2 = :_empty",
    ],
    76: [
        "$mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )",
    ],
    77: [
        "$_gen12 = $declaration $_gen12",
        "$_gen12 = :_empty",
    ],
    78: [
        "$outputs = :output :lbrace $_gen7 :rbrace -> Outputs( attributes=$2 )",
    ],
    79: [
        "$_gen5 = $type_e",
        "$_gen5 = :_empty",
    ],
    80: [
        "$workflow = :workflow :identifier :lbrace $_gen9 :rbrace -> Workflow( name=$1, body=$3 )",
    ],
    81: [
        "$cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )",
    ],
    82: [
        "$_gen20 = :comma $e $_gen20",
        "$_gen20 = :_empty",
    ],
    83: [
        "$_gen7 = $output_kv $_gen7",
        "$_gen7 = :_empty",
    ],
    84: [
        "$_gen16 = $setter",
        "$_gen16 = :_empty",
    ],
    85: [
        "$_gen15 = :comma $mapping $_gen15",
        "$_gen15 = :_empty",
    ],
    86: [
        "$cmd_param = :cmd_param_start $_gen3 $_gen4 $_gen5 :identifier $_gen6 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )",
    ],
    87: [
        "$workflow_or_task = $workflow",
        "$workflow_or_task = $task",
    ],
    88: [
        "$command = :raw_command :raw_cmd_start $_gen2 :raw_cmd_end -> RawCommand( parts=$2 )",
    ],
    89: [
        "$type_e = :type <=> :lsquare $_gen17 :rsquare -> Type( name=$0, subtype=$2 )",
        "$type_e = :type",
    ],
    90: [
        "$runtime = :runtime $map -> Runtime( map=$1 )",
    ],
    91: [
        "$_gen6 = $postfix_qualifier",
        "$_gen6 = :_empty",
    ],
    92: [
        "$call_output = :output :colon $_gen14 -> Outputs( map=$2 )",
    ],
    93: [
        "$call_body_element = $call_input",
        "$call_body_element = $call_output",
    ],
    94: [
        "$wf_body_element = $call",
        "$wf_body_element = $declaration",
        "$wf_body_element = $while_loop",
        "$wf_body_element = $if_stmt",
        "$wf_body_element = $scatter",
    ],
    95: [
        "$if_stmt = :if :lparen $e :rparen :lbrace $_gen9 :rbrace -> If( expression=$2, body=$5 )",
    ],
    96: [
        "$kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )",
    ],
    97: [
        "$_gen3 = $cmd_param_kv $_gen3",
        "$_gen3 = :_empty",
    ],
    98: [
        "$declaration = $type_e :identifier $_gen16 -> Declaration( type=$0, name=$1, expression=$2 )",
    ],
    99: [
        "$_gen21 = $object_kv $_gen22",
        "$_gen21 = :_empty",
    ],
    100: [
        "$_gen1 = $sections $_gen1",
        "$_gen1 = :_empty",
    ],
    101: [
        "$_gen9 = $wf_body_element $_gen9",
        "$_gen9 = :_empty",
    ],
    102: [
        "$parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )",
    ],
    103: [
        "$_gen4 = :string",
        "$_gen4 = :_empty",
    ],
    104: [
        "$_gen13 = $call_body_element $_gen13",
        "$_gen13 = :_empty",
    ],
    105: [
        "$command_part = :cmd_part",
        "$command_part = $cmd_param",
    ],
    106: [
        "$setter = :equal $e -> $1",
    ],
    107: [
        "$_gen18 = :comma $type_e $_gen18",
        "$_gen18 = :_empty",
    ],
    108: [
        "$task = :task :identifier :lbrace $_gen1 :rbrace -> Task( name=$1, sections=$3 )",
    ],
    109: [
        "$_gen22 = :comma $object_kv $_gen22",
        "$_gen22 = :_empty",
    ],
    110: [
        "$call_body = :lbrace $_gen12 $_gen13 :rbrace -> CallBody( declarations=$1, io=$2 )",
    ],
}
rules = {
    0: "$_gen0 = $workflow_or_task $_gen0",
    1: "$_gen0 = :_empty",
    2: "$document = $_gen0",
    3: "$workflow_or_task = $workflow",
    4: "$workflow_or_task = $task",
    5: "$_gen1 = $sections $_gen1",
    6: "$_gen1 = :_empty",
    7: "$task = :task :identifier :lbrace $_gen1 :rbrace -> Task( name=$1, sections=$3 )",
    8: "$sections = $command",
    9: "$sections = $outputs",
    10: "$sections = $runtime",
    11: "$sections = $parameter_meta",
    12: "$sections = $meta",
    13: "$_gen2 = $command_part $_gen2",
    14: "$_gen2 = :_empty",
    15: "$command = :raw_command :raw_cmd_start $_gen2 :raw_cmd_end -> RawCommand( parts=$2 )",
    16: "$command_part = :cmd_part",
    17: "$command_part = $cmd_param",
    18: "$_gen3 = $cmd_param_kv $_gen3",
    19: "$_gen3 = :_empty",
    20: "$_gen4 = :string",
    21: "$_gen4 = :_empty",
    22: "$_gen5 = $type_e",
    23: "$_gen5 = :_empty",
    24: "$_gen6 = $postfix_qualifier",
    25: "$_gen6 = :_empty",
    26: "$cmd_param = :cmd_param_start $_gen3 $_gen4 $_gen5 :identifier $_gen6 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )",
    27: "$cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )",
    28: "$postfix_qualifier = :qmark",
    29: "$postfix_qualifier = :plus",
    30: "$postfix_qualifier = :asterisk",
    31: "$_gen7 = $output_kv $_gen7",
    32: "$_gen7 = :_empty",
    33: "$outputs = :output :lbrace $_gen7 :rbrace -> Outputs( attributes=$2 )",
    34: "$output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )",
    35: "$runtime = :runtime $map -> Runtime( map=$1 )",
    36: "$parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )",
    37: "$meta = :meta $map -> Meta( map=$1 )",
    38: "$_gen8 = $kv $_gen8",
    39: "$_gen8 = :_empty",
    40: "$map = :lbrace $_gen8 :rbrace -> $1",
    41: "$kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )",
    42: "$_gen9 = $wf_body_element $_gen9",
    43: "$_gen9 = :_empty",
    44: "$workflow = :workflow :identifier :lbrace $_gen9 :rbrace -> Workflow( name=$1, body=$3 )",
    45: "$wf_body_element = $call",
    46: "$wf_body_element = $declaration",
    47: "$wf_body_element = $while_loop",
    48: "$wf_body_element = $if_stmt",
    49: "$wf_body_element = $scatter",
    50: "$_gen10 = $alias",
    51: "$_gen10 = :_empty",
    52: "$_gen11 = $call_body",
    53: "$_gen11 = :_empty",
    54: "$call = :call :identifier $_gen10 $_gen11 -> Call( task=$1, alias=$2, body=$3 )",
    55: "$_gen12 = $declaration $_gen12",
    56: "$_gen12 = :_empty",
    57: "$_gen13 = $call_body_element $_gen13",
    58: "$_gen13 = :_empty",
    59: "$call_body = :lbrace $_gen12 $_gen13 :rbrace -> CallBody( declarations=$1, io=$2 )",
    60: "$call_body_element = $call_input",
    61: "$call_body_element = $call_output",
    62: "$_gen14 = $mapping $_gen15",
    63: "$_gen15 = :comma $mapping $_gen15",
    64: "$_gen15 = :_empty",
    65: "$_gen14 = :_empty",
    66: "$call_input = :input :colon $_gen14 -> Inputs( map=$2 )",
    67: "$call_output = :output :colon $_gen14 -> Outputs( map=$2 )",
    68: "$mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )",
    69: "$alias = :as :identifier -> $1",
    70: "$while_loop = :while :lparen $e :rparen :lbrace $_gen9 :rbrace -> WhileLoop( expression=$2, body=$5 )",
    71: "$if_stmt = :if :lparen $e :rparen :lbrace $_gen9 :rbrace -> If( expression=$2, body=$5 )",
    72: "$scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen9 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )",
    73: "$_gen16 = $setter",
    74: "$_gen16 = :_empty",
    75: "$declaration = $type_e :identifier $_gen16 -> Declaration( type=$0, name=$1, expression=$2 )",
    76: "$setter = :equal $e -> $1",
    77: "$object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )",
    78: "$_gen17 = $type_e $_gen18",
    79: "$_gen18 = :comma $type_e $_gen18",
    80: "$_gen18 = :_empty",
    81: "$_gen17 = :_empty",
    82: "$type_e = :type <=> :lsquare $_gen17 :rsquare -> Type( name=$0, subtype=$2 )",
    83: "$type_e = :type",
    84: "$e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )",
    85: "$e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )",
    86: "$e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )",
    87: "$e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )",
    88: "$e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )",
    89: "$e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )",
    90: "$e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )",
    91: "$e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )",
    92: "$e = $e :plus $e -> Add( lhs=$0, rhs=$2 )",
    93: "$e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )",
    94: "$e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )",
    95: "$e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )",
    96: "$e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )",
    97: "$e = :not $e -> LogicalNot( expression=$1 )",
    98: "$e = :plus $e -> UnaryPlus( expression=$1 )",
    99: "$e = :dash $e -> UnaryNegation( expression=$1 )",
    100: "$_gen19 = $e $_gen20",
    101: "$_gen20 = :comma $e $_gen20",
    102: "$_gen20 = :_empty",
    103: "$_gen19 = :_empty",
    104: "$e = :identifier <=> :lparen $_gen19 :rparen -> FunctionCall( name=$0, params=$2 )",
    105: "$e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )",
    106: "$e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )",
    107: "$_gen21 = $object_kv $_gen22",
    108: "$_gen22 = :comma $object_kv $_gen22",
    109: "$_gen22 = :_empty",
    110: "$_gen21 = :_empty",
    111: "$e = :object :lbrace $_gen21 :rbrace -> ObjectLiteral( map=$2 )",
    112: "$e = :lparen $e :rparen -> $1",
    113: "$e = :string",
    114: "$e = :identifier",
    115: "$e = :boolean",
    116: "$e = :integer",
    117: "$e = :dquote_string",
    118: "$e = :squote_string",
}
def is_terminal(id): return isinstance(id, int) and 0 <= id <= 54
def parse(src, resource='string', errors=None, start=None):
    if errors is None:
        errors = DefaultSyntaxErrorHandler(src, resource)
    tokens = lex(src, resource, errors)
    ctx = ParserContext(tokens, errors)
    tree = parse_document(ctx)
    if tokens.current() != None:
        raise ctx.errors.excess_tokens()
    return tree
def expect(ctx, terminal_id):
    current = ctx.tokens.current()
    if not current:
        raise ctx.errors.no_more_tokens(ctx.rule, terminals[terminal_id], ctx.tokens.last())
    if current.id != terminal_id:
        raise ctx.errors.unexpected_symbol(ctx.nonterminal, current, [terminals[terminal_id]], ctx.rule)
    next = ctx.tokens.advance()
    if next and not is_terminal(next.id):
        raise ctx.errors.invalid_terminal(ctx.nonterminal, next)
    return current
# START definitions for expression parser: type_e
infix_binding_power_type_e = {
    24: 1000, # $type_e = :type <=> :lsquare list($type_e, :comma) :rsquare -> Type( name=$0, subtype=$2 )
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
    tree = ParseTree(NonTerminal(89, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if not current:
        return tree
    if current.id in rule_first[82]:
        # $type_e = :type <=> :lsquare $_gen17 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[82]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 31))
    elif current.id in rule_first[83]:
        # $type_e = :type
        ctx.rule = rules[83]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 31))
    return tree
def led_type_e(left, ctx):
    tree = ParseTree(NonTerminal(89, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if current.id == 24: # :lsquare
        # $type_e = :type <=> :lsquare $_gen17 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[82]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('subtype', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Type', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 24)) # :lsquare
        tree.add(parse__gen17(ctx))
        tree.add(expect(ctx, 2)) # :rsquare
    return tree
# END definitions for expression parser: type_e
# START definitions for expression parser: e
infix_binding_power_e = {
    28: 2000, # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
    37: 3000, # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
    38: 4000, # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
    51: 4000, # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
    50: 5000, # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
    30: 5000, # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
    18: 5000, # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
    45: 5000, # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
    52: 6000, # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
    27: 6000, # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
    32: 7000, # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
    29: 7000, # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
    48: 7000, # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
    46: 9000, # $e = :identifier <=> :lparen list($e, :comma) :rparen -> FunctionCall( name=$0, params=$2 )
    24: 10000, # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
    41: 11000, # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
}
prefix_binding_power_e = {
    5: 8000, # $e = :not $e -> LogicalNot( expression=$1 )
    52: 8000, # $e = :plus $e -> UnaryPlus( expression=$1 )
    27: 8000, # $e = :dash $e -> UnaryNegation( expression=$1 )
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
    tree = ParseTree(NonTerminal(74, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if not current:
        return tree
    elif current.id in rule_first[97]:
        # $e = :not $e -> LogicalNot( expression=$1 )
        ctx.rule = rules[97]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 5))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(5)))
        tree.isPrefix = True
    elif current.id in rule_first[98]:
        # $e = :plus $e -> UnaryPlus( expression=$1 )
        ctx.rule = rules[98]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 52))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(52)))
        tree.isPrefix = True
    elif current.id in rule_first[99]:
        # $e = :dash $e -> UnaryNegation( expression=$1 )
        ctx.rule = rules[99]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 27))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(27)))
        tree.isPrefix = True
    elif current.id in rule_first[104]:
        # $e = :identifier <=> :lparen $_gen19 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[104]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 54))
    elif current.id in rule_first[105]:
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[105]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 54))
    elif current.id in rule_first[106]:
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[106]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 54))
    elif current.id in rule_first[111]:
        # $e = :object :lbrace $_gen21 :rbrace -> ObjectLiteral( map=$2 )
        ctx.rule = rules[111]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ObjectLiteral', ast_parameters)
        tree.nudMorphemeCount = 4
        tree.add(expect(ctx, 43))
        tree.add(expect(ctx, 8))
        tree.add(parse__gen21(ctx))
        tree.add(expect(ctx, 19))
    elif current.id in rule_first[112]:
        # $e = :lparen $e :rparen -> $1
        ctx.rule = rules[112]
        tree.astTransform = AstTransformSubstitution(1)
        tree.nudMorphemeCount = 3
        tree.add(expect(ctx, 46))
        tree.add(parse_e(ctx))
        tree.add(expect(ctx, 26))
    elif current.id in rule_first[113]:
        # $e = :string
        ctx.rule = rules[113]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 6))
    elif current.id in rule_first[114]:
        # $e = :identifier
        ctx.rule = rules[114]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 54))
    elif current.id in rule_first[115]:
        # $e = :boolean
        ctx.rule = rules[115]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 39))
    elif current.id in rule_first[116]:
        # $e = :integer
        ctx.rule = rules[116]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 21))
    elif current.id in rule_first[117]:
        # $e = :dquote_string
        ctx.rule = rules[117]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 11))
    elif current.id in rule_first[118]:
        # $e = :squote_string
        ctx.rule = rules[118]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 34))
    return tree
def led_e(left, ctx):
    tree = ParseTree(NonTerminal(74, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if current.id == 28: # :double_pipe
        # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
        ctx.rule = rules[84]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalOr', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 28)) # :double_pipe
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(28) - modifier))
    if current.id == 37: # :double_ampersand
        # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
        ctx.rule = rules[85]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalAnd', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 37)) # :double_ampersand
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(37) - modifier))
    if current.id == 38: # :double_equal
        # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
        ctx.rule = rules[86]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Equals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 38)) # :double_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(38) - modifier))
    if current.id == 51: # :not_equal
        # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
        ctx.rule = rules[87]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('NotEquals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 51)) # :not_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(51) - modifier))
    if current.id == 50: # :lt
        # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[88]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 50)) # :lt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(50) - modifier))
    if current.id == 30: # :lteq
        # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[89]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 30)) # :lteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(30) - modifier))
    if current.id == 18: # :gt
        # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[90]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 18)) # :gt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(18) - modifier))
    if current.id == 45: # :gteq
        # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[91]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 45)) # :gteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(45) - modifier))
    if current.id == 52: # :plus
        # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
        ctx.rule = rules[92]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Add', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 52)) # :plus
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(52) - modifier))
    if current.id == 27: # :dash
        # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
        ctx.rule = rules[93]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Subtract', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 27)) # :dash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(27) - modifier))
    if current.id == 32: # :asterisk
        # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
        ctx.rule = rules[94]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Multiply', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 32)) # :asterisk
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(32) - modifier))
    if current.id == 29: # :slash
        # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
        ctx.rule = rules[95]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Divide', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 29)) # :slash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(29) - modifier))
    if current.id == 48: # :percent
        # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
        ctx.rule = rules[96]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Remainder', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 48)) # :percent
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(48) - modifier))
    if current.id == 46: # :lparen
        # $e = :identifier <=> :lparen $_gen19 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[104]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('params', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('FunctionCall', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 46)) # :lparen
        tree.add(parse__gen19(ctx))
        tree.add(expect(ctx, 26)) # :rparen
    if current.id == 24: # :lsquare
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[105]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ArrayIndex', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 24)) # :lsquare
        modifier = 0
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(24) - modifier))
        tree.add(expect(ctx, 2)) # :rsquare
    if current.id == 41: # :dot
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[106]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('MemberAccess', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 41)) # :dot
        tree.add(expect(ctx, 54)) # :identifier
    return tree
# END definitions for expression parser: e
def parse__gen0(ctx):
    current = ctx.tokens.current()
    rule = table[0][current.id] if current else -1
    tree = ParseTree(NonTerminal(55, '_gen0'))
    ctx.nonterminal = "_gen0"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[55] and current.id not in nonterminal_first[55]:
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
def parse_call_input(ctx):
    current = ctx.tokens.current()
    rule = table[1][current.id] if current else -1
    tree = ParseTree(NonTerminal(56, 'call_input'))
    ctx.nonterminal = "call_input"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 66: # $call_input = :input :colon $_gen14 -> Inputs( map=$2 )
        ctx.rule = rules[66]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Inputs', ast_parameters)
        t = expect(ctx, 47) # :input
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse__gen14(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[56] if x >=0],
      rules[66]
    )
def parse__gen19(ctx):
    current = ctx.tokens.current()
    rule = table[2][current.id] if current else -1
    tree = ParseTree(NonTerminal(57, '_gen19'))
    ctx.nonterminal = "_gen19"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[57] and current.id not in nonterminal_first[57]:
        return tree
    if current == None:
        return tree
    if rule == 100: # $_gen19 = $e $_gen20
        ctx.rule = rules[100]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_e(ctx)
        tree.add(subtree)
        subtree = parse__gen20(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen10(ctx):
    current = ctx.tokens.current()
    rule = table[3][current.id] if current else -1
    tree = ParseTree(NonTerminal(58, '_gen10'))
    ctx.nonterminal = "_gen10"
    tree.list = False
    if current != None and current.id in nonterminal_follow[58] and current.id not in nonterminal_first[58]:
        return tree
    if current == None:
        return tree
    if rule == 50: # $_gen10 = $alias
        ctx.rule = rules[50]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_alias(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_object_kv(ctx):
    current = ctx.tokens.current()
    rule = table[4][current.id] if current else -1
    tree = ParseTree(NonTerminal(59, 'object_kv'))
    ctx.nonterminal = "object_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 77: # $object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )
        ctx.rule = rules[77]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ObjectKV', ast_parameters)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[59] if x >=0],
      rules[77]
    )
def parse_map(ctx):
    current = ctx.tokens.current()
    rule = table[5][current.id] if current else -1
    tree = ParseTree(NonTerminal(60, 'map'))
    ctx.nonterminal = "map"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 40: # $map = :lbrace $_gen8 :rbrace -> $1
        ctx.rule = rules[40]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen8(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[60] if x >=0],
      rules[40]
    )
def parse_alias(ctx):
    current = ctx.tokens.current()
    rule = table[6][current.id] if current else -1
    tree = ParseTree(NonTerminal(61, 'alias'))
    ctx.nonterminal = "alias"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 69: # $alias = :as :identifier -> $1
        ctx.rule = rules[69]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 49) # :as
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[61] if x >=0],
      rules[69]
    )
def parse_output_kv(ctx):
    current = ctx.tokens.current()
    rule = table[7][current.id] if current else -1
    tree = ParseTree(NonTerminal(62, 'output_kv'))
    ctx.nonterminal = "output_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 34: # $output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )
        ctx.rule = rules[34]
        ast_parameters = OrderedDict([
            ('type', 0),
            ('var', 1),
            ('expression', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Output', ast_parameters)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 35) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[62] if x >=0],
      rules[34]
    )
def parse_while_loop(ctx):
    current = ctx.tokens.current()
    rule = table[8][current.id] if current else -1
    tree = ParseTree(NonTerminal(63, 'while_loop'))
    ctx.nonterminal = "while_loop"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 70: # $while_loop = :while :lparen $e :rparen :lbrace $_gen9 :rbrace -> WhileLoop( expression=$2, body=$5 )
        ctx.rule = rules[70]
        ast_parameters = OrderedDict([
            ('expression', 2),
            ('body', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('WhileLoop', ast_parameters)
        t = expect(ctx, 25) # :while
        tree.add(t)
        t = expect(ctx, 46) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 26) # :rparen
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[63] if x >=0],
      rules[70]
    )
def parse_meta(ctx):
    current = ctx.tokens.current()
    rule = table[9][current.id] if current else -1
    tree = ParseTree(NonTerminal(64, 'meta'))
    ctx.nonterminal = "meta"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 37: # $meta = :meta $map -> Meta( map=$1 )
        ctx.rule = rules[37]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('Meta', ast_parameters)
        t = expect(ctx, 16) # :meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[64] if x >=0],
      rules[37]
    )
def parse__gen11(ctx):
    current = ctx.tokens.current()
    rule = table[10][current.id] if current else -1
    tree = ParseTree(NonTerminal(65, '_gen11'))
    ctx.nonterminal = "_gen11"
    tree.list = False
    if current != None and current.id in nonterminal_follow[65] and current.id not in nonterminal_first[65]:
        return tree
    if current == None:
        return tree
    if rule == 52: # $_gen11 = $call_body
        ctx.rule = rules[52]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_body(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen14(ctx):
    current = ctx.tokens.current()
    rule = table[11][current.id] if current else -1
    tree = ParseTree(NonTerminal(66, '_gen14'))
    ctx.nonterminal = "_gen14"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[66] and current.id not in nonterminal_first[66]:
        return tree
    if current == None:
        return tree
    if rule == 62: # $_gen14 = $mapping $_gen15
        ctx.rule = rules[62]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_mapping(ctx)
        tree.add(subtree)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen17(ctx):
    current = ctx.tokens.current()
    rule = table[12][current.id] if current else -1
    tree = ParseTree(NonTerminal(67, '_gen17'))
    ctx.nonterminal = "_gen17"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[67] and current.id not in nonterminal_first[67]:
        return tree
    if current == None:
        return tree
    if rule == 78: # $_gen17 = $type_e $_gen18
        ctx.rule = rules[78]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        subtree = parse__gen18(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_sections(ctx):
    current = ctx.tokens.current()
    rule = table[13][current.id] if current else -1
    tree = ParseTree(NonTerminal(68, 'sections'))
    ctx.nonterminal = "sections"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 8: # $sections = $command
        ctx.rule = rules[8]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command(ctx)
        tree.add(subtree)
        return tree
    elif rule == 9: # $sections = $outputs
        ctx.rule = rules[9]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_outputs(ctx)
        tree.add(subtree)
        return tree
    elif rule == 10: # $sections = $runtime
        ctx.rule = rules[10]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_runtime(ctx)
        tree.add(subtree)
        return tree
    elif rule == 11: # $sections = $parameter_meta
        ctx.rule = rules[11]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_parameter_meta(ctx)
        tree.add(subtree)
        return tree
    elif rule == 12: # $sections = $meta
        ctx.rule = rules[12]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_meta(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[68] if x >=0],
      rules[12]
    )
def parse__gen8(ctx):
    current = ctx.tokens.current()
    rule = table[14][current.id] if current else -1
    tree = ParseTree(NonTerminal(69, '_gen8'))
    ctx.nonterminal = "_gen8"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[69] and current.id not in nonterminal_first[69]:
        return tree
    if current == None:
        return tree
    if rule == 38: # $_gen8 = $kv $_gen8
        ctx.rule = rules[38]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen8(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call(ctx):
    current = ctx.tokens.current()
    rule = table[15][current.id] if current else -1
    tree = ParseTree(NonTerminal(70, 'call'))
    ctx.nonterminal = "call"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 54: # $call = :call :identifier $_gen10 $_gen11 -> Call( task=$1, alias=$2, body=$3 )
        ctx.rule = rules[54]
        ast_parameters = OrderedDict([
            ('task', 1),
            ('alias', 2),
            ('body', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Call', ast_parameters)
        t = expect(ctx, 15) # :call
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        subtree = parse__gen11(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[70] if x >=0],
      rules[54]
    )
def parse_document(ctx):
    current = ctx.tokens.current()
    rule = table[16][current.id] if current else -1
    tree = ParseTree(NonTerminal(71, 'document'))
    ctx.nonterminal = "document"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 2: # $document = $_gen0
        ctx.rule = rules[2]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse__gen0(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[71] if x >=0],
      rules[2]
    )
def parse_scatter(ctx):
    current = ctx.tokens.current()
    rule = table[17][current.id] if current else -1
    tree = ParseTree(NonTerminal(72, 'scatter'))
    ctx.nonterminal = "scatter"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 72: # $scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen9 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )
        ctx.rule = rules[72]
        ast_parameters = OrderedDict([
            ('item', 2),
            ('collection', 4),
            ('body', 7),
        ])
        tree.astTransform = AstTransformNodeCreator('Scatter', ast_parameters)
        t = expect(ctx, 44) # :scatter
        tree.add(t)
        t = expect(ctx, 46) # :lparen
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 36) # :in
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 26) # :rparen
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[72] if x >=0],
      rules[72]
    )
def parse_postfix_qualifier(ctx):
    current = ctx.tokens.current()
    rule = table[18][current.id] if current else -1
    tree = ParseTree(NonTerminal(73, 'postfix_qualifier'))
    ctx.nonterminal = "postfix_qualifier"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 28: # $postfix_qualifier = :qmark
        ctx.rule = rules[28]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 3) # :qmark
        tree.add(t)
        return tree
    elif rule == 29: # $postfix_qualifier = :plus
        ctx.rule = rules[29]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 52) # :plus
        tree.add(t)
        return tree
    elif rule == 30: # $postfix_qualifier = :asterisk
        ctx.rule = rules[30]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 32) # :asterisk
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[73] if x >=0],
      rules[30]
    )
def parse__gen2(ctx):
    current = ctx.tokens.current()
    rule = table[20][current.id] if current else -1
    tree = ParseTree(NonTerminal(75, '_gen2'))
    ctx.nonterminal = "_gen2"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[75] and current.id not in nonterminal_first[75]:
        return tree
    if current == None:
        return tree
    if rule == 13: # $_gen2 = $command_part $_gen2
        ctx.rule = rules[13]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_command_part(ctx)
        tree.add(subtree)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_mapping(ctx):
    current = ctx.tokens.current()
    rule = table[21][current.id] if current else -1
    tree = ParseTree(NonTerminal(76, 'mapping'))
    ctx.nonterminal = "mapping"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 68: # $mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )
        ctx.rule = rules[68]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('IOMapping', ast_parameters)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 35) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[76] if x >=0],
      rules[68]
    )
def parse__gen12(ctx):
    current = ctx.tokens.current()
    rule = table[22][current.id] if current else -1
    tree = ParseTree(NonTerminal(77, '_gen12'))
    ctx.nonterminal = "_gen12"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[77] and current.id not in nonterminal_first[77]:
        return tree
    if current == None:
        return tree
    if rule == 55: # $_gen12 = $declaration $_gen12
        ctx.rule = rules[55]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_declaration(ctx)
        tree.add(subtree)
        subtree = parse__gen12(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_outputs(ctx):
    current = ctx.tokens.current()
    rule = table[23][current.id] if current else -1
    tree = ParseTree(NonTerminal(78, 'outputs'))
    ctx.nonterminal = "outputs"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 33: # $outputs = :output :lbrace $_gen7 :rbrace -> Outputs( attributes=$2 )
        ctx.rule = rules[33]
        ast_parameters = OrderedDict([
            ('attributes', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Outputs', ast_parameters)
        t = expect(ctx, 10) # :output
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen7(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[78] if x >=0],
      rules[33]
    )
def parse__gen5(ctx):
    current = ctx.tokens.current()
    rule = table[24][current.id] if current else -1
    tree = ParseTree(NonTerminal(79, '_gen5'))
    ctx.nonterminal = "_gen5"
    tree.list = False
    if current != None and current.id in nonterminal_follow[79] and current.id not in nonterminal_first[79]:
        return tree
    if current == None:
        return tree
    if rule == 22: # $_gen5 = $type_e
        ctx.rule = rules[22]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_workflow(ctx):
    current = ctx.tokens.current()
    rule = table[25][current.id] if current else -1
    tree = ParseTree(NonTerminal(80, 'workflow'))
    ctx.nonterminal = "workflow"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 44: # $workflow = :workflow :identifier :lbrace $_gen9 :rbrace -> Workflow( name=$1, body=$3 )
        ctx.rule = rules[44]
        ast_parameters = OrderedDict([
            ('name', 1),
            ('body', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Workflow', ast_parameters)
        t = expect(ctx, 23) # :workflow
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[80] if x >=0],
      rules[44]
    )
def parse_cmd_param_kv(ctx):
    current = ctx.tokens.current()
    rule = table[26][current.id] if current else -1
    tree = ParseTree(NonTerminal(81, 'cmd_param_kv'))
    ctx.nonterminal = "cmd_param_kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 27: # $cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )
        ctx.rule = rules[27]
        ast_parameters = OrderedDict([
            ('key', 1),
            ('value', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameterAttr', ast_parameters)
        t = expect(ctx, 1) # :cmd_attr_hint
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 35) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[81] if x >=0],
      rules[27]
    )
def parse__gen20(ctx):
    current = ctx.tokens.current()
    rule = table[27][current.id] if current else -1
    tree = ParseTree(NonTerminal(82, '_gen20'))
    ctx.nonterminal = "_gen20"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[82] and current.id not in nonterminal_first[82]:
        return tree
    if current == None:
        return tree
    if rule == 101: # $_gen20 = :comma $e $_gen20
        ctx.rule = rules[101]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 0) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_e(ctx)
        tree.add(subtree)
        subtree = parse__gen20(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen7(ctx):
    current = ctx.tokens.current()
    rule = table[28][current.id] if current else -1
    tree = ParseTree(NonTerminal(83, '_gen7'))
    ctx.nonterminal = "_gen7"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[83] and current.id not in nonterminal_first[83]:
        return tree
    if current == None:
        return tree
    if rule == 31: # $_gen7 = $output_kv $_gen7
        ctx.rule = rules[31]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_output_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen7(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen16(ctx):
    current = ctx.tokens.current()
    rule = table[29][current.id] if current else -1
    tree = ParseTree(NonTerminal(84, '_gen16'))
    ctx.nonterminal = "_gen16"
    tree.list = False
    if current != None and current.id in nonterminal_follow[84] and current.id not in nonterminal_first[84]:
        return tree
    if current == None:
        return tree
    if rule == 73: # $_gen16 = $setter
        ctx.rule = rules[73]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_setter(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen15(ctx):
    current = ctx.tokens.current()
    rule = table[30][current.id] if current else -1
    tree = ParseTree(NonTerminal(85, '_gen15'))
    ctx.nonterminal = "_gen15"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[85] and current.id not in nonterminal_first[85]:
        return tree
    if current == None:
        return tree
    if rule == 63: # $_gen15 = :comma $mapping $_gen15
        ctx.rule = rules[63]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 0) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_mapping(ctx)
        tree.add(subtree)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_cmd_param(ctx):
    current = ctx.tokens.current()
    rule = table[31][current.id] if current else -1
    tree = ParseTree(NonTerminal(86, 'cmd_param'))
    ctx.nonterminal = "cmd_param"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 26: # $cmd_param = :cmd_param_start $_gen3 $_gen4 $_gen5 :identifier $_gen6 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )
        ctx.rule = rules[26]
        ast_parameters = OrderedDict([
            ('name', 4),
            ('type', 3),
            ('prefix', 2),
            ('attributes', 1),
            ('postfix', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('CommandParameter', ast_parameters)
        t = expect(ctx, 40) # :cmd_param_start
        tree.add(t)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        subtree = parse__gen4(ctx)
        tree.add(subtree)
        subtree = parse__gen5(ctx)
        tree.add(subtree)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        subtree = parse__gen6(ctx)
        tree.add(subtree)
        t = expect(ctx, 22) # :cmd_param_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[86] if x >=0],
      rules[26]
    )
def parse_workflow_or_task(ctx):
    current = ctx.tokens.current()
    rule = table[32][current.id] if current else -1
    tree = ParseTree(NonTerminal(87, 'workflow_or_task'))
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
      [terminals[x] for x in nonterminal_first[87] if x >=0],
      rules[4]
    )
def parse_command(ctx):
    current = ctx.tokens.current()
    rule = table[33][current.id] if current else -1
    tree = ParseTree(NonTerminal(88, 'command'))
    ctx.nonterminal = "command"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 15: # $command = :raw_command :raw_cmd_start $_gen2 :raw_cmd_end -> RawCommand( parts=$2 )
        ctx.rule = rules[15]
        ast_parameters = OrderedDict([
            ('parts', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('RawCommand', ast_parameters)
        t = expect(ctx, 12) # :raw_command
        tree.add(t)
        t = expect(ctx, 20) # :raw_cmd_start
        tree.add(t)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        t = expect(ctx, 14) # :raw_cmd_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[88] if x >=0],
      rules[15]
    )
def parse_runtime(ctx):
    current = ctx.tokens.current()
    rule = table[35][current.id] if current else -1
    tree = ParseTree(NonTerminal(90, 'runtime'))
    ctx.nonterminal = "runtime"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 35: # $runtime = :runtime $map -> Runtime( map=$1 )
        ctx.rule = rules[35]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('Runtime', ast_parameters)
        t = expect(ctx, 9) # :runtime
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[90] if x >=0],
      rules[35]
    )
def parse__gen6(ctx):
    current = ctx.tokens.current()
    rule = table[36][current.id] if current else -1
    tree = ParseTree(NonTerminal(91, '_gen6'))
    ctx.nonterminal = "_gen6"
    tree.list = False
    if current != None and current.id in nonterminal_follow[91] and current.id not in nonterminal_first[91]:
        return tree
    if current == None:
        return tree
    if rule == 24: # $_gen6 = $postfix_qualifier
        ctx.rule = rules[24]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_postfix_qualifier(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call_output(ctx):
    current = ctx.tokens.current()
    rule = table[37][current.id] if current else -1
    tree = ParseTree(NonTerminal(92, 'call_output'))
    ctx.nonterminal = "call_output"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 67: # $call_output = :output :colon $_gen14 -> Outputs( map=$2 )
        ctx.rule = rules[67]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Outputs', ast_parameters)
        t = expect(ctx, 10) # :output
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse__gen14(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[92] if x >=0],
      rules[67]
    )
def parse_call_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[38][current.id] if current else -1
    tree = ParseTree(NonTerminal(93, 'call_body_element'))
    ctx.nonterminal = "call_body_element"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 60: # $call_body_element = $call_input
        ctx.rule = rules[60]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_input(ctx)
        tree.add(subtree)
        return tree
    elif rule == 61: # $call_body_element = $call_output
        ctx.rule = rules[61]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_output(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[93] if x >=0],
      rules[61]
    )
def parse_wf_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[39][current.id] if current else -1
    tree = ParseTree(NonTerminal(94, 'wf_body_element'))
    ctx.nonterminal = "wf_body_element"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 45: # $wf_body_element = $call
        ctx.rule = rules[45]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call(ctx)
        tree.add(subtree)
        return tree
    elif rule == 46: # $wf_body_element = $declaration
        ctx.rule = rules[46]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_declaration(ctx)
        tree.add(subtree)
        return tree
    elif rule == 47: # $wf_body_element = $while_loop
        ctx.rule = rules[47]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_while_loop(ctx)
        tree.add(subtree)
        return tree
    elif rule == 48: # $wf_body_element = $if_stmt
        ctx.rule = rules[48]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_if_stmt(ctx)
        tree.add(subtree)
        return tree
    elif rule == 49: # $wf_body_element = $scatter
        ctx.rule = rules[49]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_scatter(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[94] if x >=0],
      rules[49]
    )
def parse_if_stmt(ctx):
    current = ctx.tokens.current()
    rule = table[40][current.id] if current else -1
    tree = ParseTree(NonTerminal(95, 'if_stmt'))
    ctx.nonterminal = "if_stmt"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 71: # $if_stmt = :if :lparen $e :rparen :lbrace $_gen9 :rbrace -> If( expression=$2, body=$5 )
        ctx.rule = rules[71]
        ast_parameters = OrderedDict([
            ('expression', 2),
            ('body', 5),
        ])
        tree.astTransform = AstTransformNodeCreator('If', ast_parameters)
        t = expect(ctx, 4) # :if
        tree.add(t)
        t = expect(ctx, 46) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 26) # :rparen
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[95] if x >=0],
      rules[71]
    )
def parse_kv(ctx):
    current = ctx.tokens.current()
    rule = table[41][current.id] if current else -1
    tree = ParseTree(NonTerminal(96, 'kv'))
    ctx.nonterminal = "kv"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 41: # $kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )
        ctx.rule = rules[41]
        ast_parameters = OrderedDict([
            ('key', 0),
            ('value', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('RuntimeAttribute', ast_parameters)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 42) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[96] if x >=0],
      rules[41]
    )
def parse__gen3(ctx):
    current = ctx.tokens.current()
    rule = table[42][current.id] if current else -1
    tree = ParseTree(NonTerminal(97, '_gen3'))
    ctx.nonterminal = "_gen3"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[97] and current.id not in nonterminal_first[97]:
        return tree
    if current == None:
        return tree
    if rule == 18: # $_gen3 = $cmd_param_kv $_gen3
        ctx.rule = rules[18]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_declaration(ctx):
    current = ctx.tokens.current()
    rule = table[43][current.id] if current else -1
    tree = ParseTree(NonTerminal(98, 'declaration'))
    ctx.nonterminal = "declaration"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 75: # $declaration = $type_e :identifier $_gen16 -> Declaration( type=$0, name=$1, expression=$2 )
        ctx.rule = rules[75]
        ast_parameters = OrderedDict([
            ('type', 0),
            ('name', 1),
            ('expression', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Declaration', ast_parameters)
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        subtree = parse__gen16(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[98] if x >=0],
      rules[75]
    )
def parse__gen21(ctx):
    current = ctx.tokens.current()
    rule = table[44][current.id] if current else -1
    tree = ParseTree(NonTerminal(99, '_gen21'))
    ctx.nonterminal = "_gen21"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[99] and current.id not in nonterminal_first[99]:
        return tree
    if current == None:
        return tree
    if rule == 107: # $_gen21 = $object_kv $_gen22
        ctx.rule = rules[107]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_object_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen22(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen1(ctx):
    current = ctx.tokens.current()
    rule = table[45][current.id] if current else -1
    tree = ParseTree(NonTerminal(100, '_gen1'))
    ctx.nonterminal = "_gen1"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[100] and current.id not in nonterminal_first[100]:
        return tree
    if current == None:
        return tree
    if rule == 5: # $_gen1 = $sections $_gen1
        ctx.rule = rules[5]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_sections(ctx)
        tree.add(subtree)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen9(ctx):
    current = ctx.tokens.current()
    rule = table[46][current.id] if current else -1
    tree = ParseTree(NonTerminal(101, '_gen9'))
    ctx.nonterminal = "_gen9"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[101] and current.id not in nonterminal_first[101]:
        return tree
    if current == None:
        return tree
    if rule == 42: # $_gen9 = $wf_body_element $_gen9
        ctx.rule = rules[42]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_wf_body_element(ctx)
        tree.add(subtree)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_parameter_meta(ctx):
    current = ctx.tokens.current()
    rule = table[47][current.id] if current else -1
    tree = ParseTree(NonTerminal(102, 'parameter_meta'))
    ctx.nonterminal = "parameter_meta"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 36: # $parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )
        ctx.rule = rules[36]
        ast_parameters = OrderedDict([
            ('map', 1),
        ])
        tree.astTransform = AstTransformNodeCreator('ParameterMeta', ast_parameters)
        t = expect(ctx, 17) # :parameter_meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[102] if x >=0],
      rules[36]
    )
def parse__gen4(ctx):
    current = ctx.tokens.current()
    rule = table[48][current.id] if current else -1
    tree = ParseTree(NonTerminal(103, '_gen4'))
    ctx.nonterminal = "_gen4"
    tree.list = False
    if current != None and current.id in nonterminal_follow[103] and current.id not in nonterminal_first[103]:
        return tree
    if current == None:
        return tree
    if rule == 20: # $_gen4 = :string
        ctx.rule = rules[20]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 6) # :string
        tree.add(t)
        return tree
    return tree
def parse__gen13(ctx):
    current = ctx.tokens.current()
    rule = table[49][current.id] if current else -1
    tree = ParseTree(NonTerminal(104, '_gen13'))
    ctx.nonterminal = "_gen13"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[104] and current.id not in nonterminal_first[104]:
        return tree
    if current == None:
        return tree
    if rule == 57: # $_gen13 = $call_body_element $_gen13
        ctx.rule = rules[57]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_call_body_element(ctx)
        tree.add(subtree)
        subtree = parse__gen13(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_command_part(ctx):
    current = ctx.tokens.current()
    rule = table[50][current.id] if current else -1
    tree = ParseTree(NonTerminal(105, 'command_part'))
    ctx.nonterminal = "command_part"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 16: # $command_part = :cmd_part
        ctx.rule = rules[16]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 7) # :cmd_part
        tree.add(t)
        return tree
    elif rule == 17: # $command_part = $cmd_param
        ctx.rule = rules[17]
        tree.astTransform = AstTransformSubstitution(0)
        subtree = parse_cmd_param(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[105] if x >=0],
      rules[17]
    )
def parse_setter(ctx):
    current = ctx.tokens.current()
    rule = table[51][current.id] if current else -1
    tree = ParseTree(NonTerminal(106, 'setter'))
    ctx.nonterminal = "setter"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 76: # $setter = :equal $e -> $1
        ctx.rule = rules[76]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 35) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[106] if x >=0],
      rules[76]
    )
def parse__gen18(ctx):
    current = ctx.tokens.current()
    rule = table[52][current.id] if current else -1
    tree = ParseTree(NonTerminal(107, '_gen18'))
    ctx.nonterminal = "_gen18"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[107] and current.id not in nonterminal_first[107]:
        return tree
    if current == None:
        return tree
    if rule == 79: # $_gen18 = :comma $type_e $_gen18
        ctx.rule = rules[79]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 0) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        subtree = parse__gen18(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_task(ctx):
    current = ctx.tokens.current()
    rule = table[53][current.id] if current else -1
    tree = ParseTree(NonTerminal(108, 'task'))
    ctx.nonterminal = "task"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 7: # $task = :task :identifier :lbrace $_gen1 :rbrace -> Task( name=$1, sections=$3 )
        ctx.rule = rules[7]
        ast_parameters = OrderedDict([
            ('name', 1),
            ('sections', 3),
        ])
        tree.astTransform = AstTransformNodeCreator('Task', ast_parameters)
        t = expect(ctx, 33) # :task
        tree.add(t)
        t = expect(ctx, 54) # :identifier
        tree.add(t)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[108] if x >=0],
      rules[7]
    )
def parse__gen22(ctx):
    current = ctx.tokens.current()
    rule = table[54][current.id] if current else -1
    tree = ParseTree(NonTerminal(109, '_gen22'))
    ctx.nonterminal = "_gen22"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[109] and current.id not in nonterminal_first[109]:
        return tree
    if current == None:
        return tree
    if rule == 108: # $_gen22 = :comma $object_kv $_gen22
        ctx.rule = rules[108]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 0) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_object_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen22(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call_body(ctx):
    current = ctx.tokens.current()
    rule = table[55][current.id] if current else -1
    tree = ParseTree(NonTerminal(110, 'call_body'))
    ctx.nonterminal = "call_body"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 59: # $call_body = :lbrace $_gen12 $_gen13 :rbrace -> CallBody( declarations=$1, io=$2 )
        ctx.rule = rules[59]
        ast_parameters = OrderedDict([
            ('declarations', 1),
            ('io', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('CallBody', ast_parameters)
        t = expect(ctx, 8) # :lbrace
        tree.add(t)
        subtree = parse__gen12(ctx)
        tree.add(subtree)
        subtree = parse__gen13(ctx)
        tree.add(subtree)
        t = expect(ctx, 19) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[110] if x >=0],
      rules[59]
    )
# Lexer Code #
# START USER CODE
# END USER CODE
def emit(ctx, terminal, source_string, line, col):
    if terminal:
        ctx.tokens.append(Terminal(terminals[terminal], terminal, source_string, ctx.resource, line, col))
def default_action(ctx, terminal, source_string, line, col):
    emit(ctx, terminal, source_string, line, col)
def init(ctx):
    return {}
def destroy(ctx, user_ctx):
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
          (re.compile(r'task(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('task', 0, None),
          ]),
          (re.compile(r'call(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('call', 0, None),
          ]),
          (re.compile(r'workflow(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('workflow', 0, None),
          ]),
          (re.compile(r'input(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('input', 0, None),
          ]),
          (re.compile(r'output(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('output', 0, None),
          ]),
          (re.compile(r'as(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('as', 0, None),
          ]),
          (re.compile(r'if(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('if', 0, None),
          ]),
          (re.compile(r'while(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('while', 0, None),
          ]),
          (re.compile(r'runtime(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('runtime', 0, None),
          ]),
          (re.compile(r'scatter(?![a-zA-Z0-9_-])'), [
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
          (re.compile(r'parameter_meta(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('parameter_meta', 0, None),
          ]),
          (re.compile(r'meta(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('meta', 0, None),
          ]),
          (re.compile(r'(true|false)(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('boolean', 0, None),
          ]),
          (re.compile(r'(object)\s*(\{)'), [
              # (terminal, group, function)
              ('object', 0, None),
              ('lbrace', 0, None),
          ]),
          (re.compile(r'(array|map|object|boolean|int|float|uri|file|string|raw_string)(?![a-zA-Z0-9_-])(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('type', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_-])*'), [
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
          (re.compile(r'in(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('in', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_-])*'), [
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
          (re.compile(r'\${'), [
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
          (re.compile(r'\${'), [
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
          (re.compile(r'(true|false)(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('boolean', 0, None),
          ]),
          (re.compile(r'(array|map|object|boolean|int|float|uri|file|string|raw_string)(?![a-zA-Z0-9_-])(?![a-zA-Z0-9_-])'), [
              # (terminal, group, function)
              ('type', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_-])*(?=\s*=)'), [
              # (terminal, group, function)
              ('cmd_attr_hint', None, None),
              ('identifier', 0, None),
          ]),
          (re.compile(r'[a-zA-Z]([a-zA-Z0-9_-])*'), [
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
            errors = DefaultSyntaxErrorHandler(string, resource)
        ctx = LexerContext(string, resource, errors, None)
        user_context = init(ctx)
        ctx.user_context = user_context
        while len(ctx.string):
            matched = self._next(ctx, debug)
            if matched == False:
                raise ctx.errors.unrecognized_token(string, ctx.line, ctx.col)
        destroy(ctx, ctx.user_context)
        return ctx.tokens
def lex(source, resource, errors=None, debug=False):
    return TokenStream(HermesLexer().lex(source, resource, errors, debug))
