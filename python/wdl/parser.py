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
    0: 'integer',
    1: 'type',
    2: 'parameter_meta',
    3: 'rparen',
    4: 'dash',
    5: 'percent',
    6: 'identifier',
    7: 'e',
    8: 'lparen',
    9: 'double_ampersand',
    10: 'lsquare',
    11: 'type_e',
    12: 'asterisk',
    13: 'task',
    14: 'raw_cmd_end',
    15: 'equal',
    16: 'in',
    17: 'not_equal',
    18: 'boolean',
    19: 'lbrace',
    20: 'raw_command',
    21: 'squote_string',
    22: 'lt',
    23: 'rbrace',
    24: 'colon',
    25: 'call',
    26: 'output',
    27: 'rsquare',
    28: 'lteq',
    29: 'if',
    30: 'scatter',
    31: 'as',
    32: 'runtime',
    33: 'string',
    34: 'cmd_part',
    35: 'dot',
    36: 'double_pipe',
    37: 'meta',
    38: 'not',
    39: 'workflow',
    40: 'raw_cmd_start',
    41: 'cmd_attr_hint',
    42: 'slash',
    43: 'comma',
    44: 'gt',
    45: 'cmd_param_start',
    46: 'object',
    47: 'dquote_string',
    48: 'input',
    49: 'cmd_param_end',
    50: 'gteq',
    51: 'qmark',
    52: 'double_equal',
    53: 'while',
    54: 'plus',
    'integer': 0,
    'type': 1,
    'parameter_meta': 2,
    'rparen': 3,
    'dash': 4,
    'percent': 5,
    'identifier': 6,
    'e': 7,
    'lparen': 8,
    'double_ampersand': 9,
    'lsquare': 10,
    'type_e': 11,
    'asterisk': 12,
    'task': 13,
    'raw_cmd_end': 14,
    'equal': 15,
    'in': 16,
    'not_equal': 17,
    'boolean': 18,
    'lbrace': 19,
    'raw_command': 20,
    'squote_string': 21,
    'lt': 22,
    'rbrace': 23,
    'colon': 24,
    'call': 25,
    'output': 26,
    'rsquare': 27,
    'lteq': 28,
    'if': 29,
    'scatter': 30,
    'as': 31,
    'runtime': 32,
    'string': 33,
    'cmd_part': 34,
    'dot': 35,
    'double_pipe': 36,
    'meta': 37,
    'not': 38,
    'workflow': 39,
    'raw_cmd_start': 40,
    'cmd_attr_hint': 41,
    'slash': 42,
    'comma': 43,
    'gt': 44,
    'cmd_param_start': 45,
    'object': 46,
    'dquote_string': 47,
    'input': 48,
    'cmd_param_end': 49,
    'gteq': 50,
    'qmark': 51,
    'double_equal': 52,
    'while': 53,
    'plus': 54,
}
# table[nonterminal][terminal] = rule
table = [
    [-1, -1, -1, 104, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 103, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, 26, -1, -1, 26],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, -1, -1, 66, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 65, -1, -1, -1, -1, 66, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 56, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 45, -1, 44, -1, -1, -1, 44, 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 44, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 73, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, -1, -1, 54, -1, -1, -1, 55, -1, 55, -1, -1, -1, 55, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 69, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 60, -1, -1, 59, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 59, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 70, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 77, -1, -1, -1, -1, -1, -1, -1, -1, -1, 77, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 68, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 71, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 111, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 110, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 53, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, 53, -1, 53, -1, -1, -1, 53, 53, 52, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1],
    [-1, 24, -1, -1, -1, -1, 25, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 72, -1],
    [-1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 40, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 79, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 64, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 67, -1, -1, 67, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 67, -1, -1, -1, -1, -1, -1],
    [-1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 47, -1, -1, -1, 50, 51, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 82, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 81, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 43, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [102, -1, -1, 105, 102, -1, 102, 102, 102, -1, -1, -1, -1, -1, -1, -1, -1, -1, 102, -1, -1, 102, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 102, -1, -1, -1, -1, 102, -1, -1, -1, -1, -1, -1, -1, 102, 102, -1, -1, -1, -1, -1, -1, 102],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 74, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, 31],
    [-1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, 8, -1, -1, 7, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 80, -1, -1, -1, -1, -1, -1, -1, -1, -1, 80, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 83, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 109, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 112, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 63, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 58, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 58, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 78, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, 76, -1, -1, -1, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1, 75, -1, -1, -1, -1, -1, -1, -1, 76, -1, 76, 76, -1, -1, 76, 76, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1, -1, 76, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]
nonterminal_first = {
    55: [43, -1],
    56: [39, 13, -1],
    57: [54, 51, 12, -1],
    58: [43, -1],
    59: [25],
    60: [11, 30, 1, -1, 25, 53, 29],
    61: [29],
    62: [19, -1],
    63: [19],
    64: [26],
    65: [48, 26, -1],
    66: [20],
    67: [37],
    68: [6],
    69: [-1],
    70: [11, 1],
    71: [48],
    72: [45, 34],
    73: [2],
    74: [33, -1],
    75: [31],
    76: [32],
    77: [11, 1],
    78: [13, 39],
    79: [41],
    80: [19],
    81: [43, -1],
    82: [31, -1],
    83: [11, 1, -1],
    84: [53],
    85: [11, 1, -1],
    86: [39, 13, -1],
    87: [6, -1],
    88: [6],
    89: [6, -1],
    90: [11, 30, 1, 25, 53, 29],
    91: [43, -1],
    92: [13],
    93: [37, 32, 26, 20, 2],
    94: [39],
    95: [45],
    96: [6],
    97: [4, 33, 6, 7, -1, 8, 38, 18, 46, 47, 21, 0, 54],
    98: [26],
    99: [30],
    100: [],
    101: [51, 12, 54],
    102: [2, -1, 37, 32, 26, 20],
    103: [11, 1],
    104: [11, 1, -1],
    105: [6, -1],
    106: [48, 26],
    107: [45, 34, -1],
    108: [11, 1, -1],
    109: [15],
    110: [15, -1],
    111: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    112: [41, -1],
}
nonterminal_follow = {
    55: [3],
    56: [-1],
    57: [49],
    58: [48, 26, 23],
    59: [11, 30, 1, 23, 25, 53, 29],
    60: [23],
    61: [11, 30, 1, 23, 25, 53, 29],
    62: [11, 30, 1, 23, 25, 53, 29],
    63: [11, 30, 1, 23, 25, 53, 29],
    64: [48, 26, 23],
    65: [23],
    66: [2, 32, 20, 23, 37, 26],
    67: [2, 32, 20, 23, 37, 26],
    68: [48, 23, 43, 26],
    69: [37, 32, 26, 2, 20],
    70: [11, 30, 48, 1, 23, 25, 26, 53, 29],
    71: [48, 26, 23],
    72: [45, 34, 14],
    73: [2, 32, 20, 23, 37, 26],
    74: [11, 1],
    75: [11, 30, 1, 19, 23, 25, 53, 29],
    76: [2, 32, 20, 23, 37, 26],
    77: [43, 6, 27],
    78: [-1, 13, 39],
    79: [41, 33],
    80: [2, 32, 20, 23, 37, 26],
    81: [23],
    82: [11, 30, 1, 19, 23, 25, 53, 29],
    83: [6],
    84: [11, 30, 1, 23, 25, 53, 29],
    85: [23],
    86: [-1],
    87: [23],
    88: [43, 23],
    89: [48, 26, 23],
    90: [11, 30, 1, 23, 25, 53, 29],
    91: [27],
    92: [-1, 13, 39],
    93: [23, 2, 37, 32, 26, 20],
    94: [-1, 13, 39],
    95: [45, 34, 14],
    96: [23, 6],
    97: [3],
    98: [2, 32, 20, 23, 37, 26],
    99: [11, 30, 1, 23, 25, 53, 29],
    100: [37, 32, 26, 2, 20],
    101: [49],
    102: [23],
    103: [11, 1, 23],
    104: [27],
    105: [23],
    106: [48, 26, 23],
    107: [14],
    108: [48, 26],
    109: [11, 30, 1, 48, 23, 25, 26, 53, 29],
    110: [11, 30, 1, 48, 23, 25, 26, 53, 29],
    111: [30, 53, 29, 1, 3, 4, 5, 33, 36, 6, 9, 41, 11, 42, 12, 17, 43, 44, 22, 48, 50, 23, 25, 52, 26, 28, 27, 54],
    112: [33],
}
rule_first = {
    0: [13, 39],
    1: [-1],
    2: [-1, 13, 39],
    3: [39],
    4: [13],
    5: [],
    6: [-1],
    7: [37, 32, 26, 20, 2],
    8: [-1],
    9: [13],
    10: [20],
    11: [26],
    12: [32],
    13: [2],
    14: [37],
    15: [45, 34],
    16: [-1],
    17: [20],
    18: [34],
    19: [45],
    20: [41],
    21: [-1],
    22: [33],
    23: [-1],
    24: [11, 1],
    25: [-1],
    26: [51, 12, 54],
    27: [-1],
    28: [45],
    29: [41],
    30: [51],
    31: [54],
    32: [12],
    33: [11, 1],
    34: [-1],
    35: [26],
    36: [11, 1],
    37: [32],
    38: [2],
    39: [37],
    40: [6],
    41: [-1],
    42: [19],
    43: [6],
    44: [11, 30, 1, 25, 53, 29],
    45: [-1],
    46: [39],
    47: [25],
    48: [11, 1],
    49: [53],
    50: [29],
    51: [30],
    52: [31],
    53: [-1],
    54: [19],
    55: [-1],
    56: [25],
    57: [11, 1],
    58: [-1],
    59: [48, 26],
    60: [-1],
    61: [19],
    62: [48],
    63: [26],
    64: [6],
    65: [43],
    66: [-1],
    67: [-1],
    68: [48],
    69: [26],
    70: [6],
    71: [31],
    72: [53],
    73: [29],
    74: [30],
    75: [15],
    76: [-1],
    77: [11, 1],
    78: [15],
    79: [6],
    80: [11, 1],
    81: [43],
    82: [-1],
    83: [-1],
    84: [1],
    85: [1],
    86: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    87: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    88: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    89: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    90: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    91: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    92: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    93: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    94: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    95: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    96: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    97: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    98: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    99: [38],
    100: [54],
    101: [4],
    102: [18, 4, 33, 46, 47, 21, 6, 7, 8, 38, 0, 54],
    103: [43],
    104: [-1],
    105: [-1],
    106: [6],
    107: [6],
    108: [6],
    109: [6],
    110: [43],
    111: [-1],
    112: [-1],
    113: [46],
    114: [8],
    115: [33],
    116: [6],
    117: [18],
    118: [0],
    119: [47],
    120: [21],
}
nonterminal_rules = {
    55: [
        "$_gen21 = :comma $e $_gen21",
        "$_gen21 = :_empty",
    ],
    56: [
        "$document = $_gen0 -> Document( definitions=$0 )",
    ],
    57: [
        "$_gen7 = $postfix_quantifier",
        "$_gen7 = :_empty",
    ],
    58: [
        "$_gen16 = :comma $mapping $_gen16",
        "$_gen16 = :_empty",
    ],
    59: [
        "$call = :call :identifier $_gen11 $_gen12 -> Call( task=$1, alias=$2, body=$3 )",
    ],
    60: [
        "$_gen10 = $wf_body_element $_gen10",
        "$_gen10 = :_empty",
    ],
    61: [
        "$if_stmt = :if :lparen $e :rparen :lbrace $_gen10 :rbrace -> If( expression=$2, body=$5 )",
    ],
    62: [
        "$_gen12 = $call_body",
        "$_gen12 = :_empty",
    ],
    63: [
        "$call_body = :lbrace $_gen13 $_gen14 :rbrace -> CallBody( declarations=$1, io=$2 )",
    ],
    64: [
        "$call_output = :output :colon $_gen15 -> Outputs( map=$2 )",
    ],
    65: [
        "$_gen14 = $call_body_element $_gen14",
        "$_gen14 = :_empty",
    ],
    66: [
        "$command = :raw_command :raw_cmd_start $_gen3 :raw_cmd_end -> RawCommand( parts=$2 )",
    ],
    67: [
        "$meta = :meta $map -> Meta( map=$1 )",
    ],
    68: [
        "$mapping = :identifier :equal $e -> IOMapping( key=$0, value=$2 )",
    ],
    69: [
        "$_gen1 = $declarations $_gen1",
        "$_gen1 = :_empty",
    ],
    70: [
        "$declaration = $type_e :identifier $_gen17 -> Declaration( type=$0, name=$1, expression=$2 )",
    ],
    71: [
        "$call_input = :input :colon $_gen15 -> Inputs( map=$2 )",
    ],
    72: [
        "$command_part = :cmd_part",
        "$command_part = $cmd_param",
    ],
    73: [
        "$parameter_meta = :parameter_meta $map -> ParameterMeta( map=$1 )",
    ],
    74: [
        "$_gen5 = :string",
        "$_gen5 = :_empty",
    ],
    75: [
        "$alias = :as :identifier -> $1",
    ],
    76: [
        "$runtime = :runtime $map -> Runtime( map=$1 )",
    ],
    77: [
        "$type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )",
        "$type_e = :type",
    ],
    78: [
        "$workflow_or_task = $workflow",
        "$workflow_or_task = $task",
    ],
    79: [
        "$cmd_param_kv = :cmd_attr_hint :identifier :equal $e -> CommandParameterAttr( key=$1, value=$3 )",
    ],
    80: [
        "$map = :lbrace $_gen9 :rbrace -> $1",
    ],
    81: [
        "$_gen23 = :comma $object_kv $_gen23",
        "$_gen23 = :_empty",
    ],
    82: [
        "$_gen11 = $alias",
        "$_gen11 = :_empty",
    ],
    83: [
        "$_gen6 = $type_e",
        "$_gen6 = :_empty",
    ],
    84: [
        "$while_loop = :while :lparen $e :rparen :lbrace $_gen10 :rbrace -> WhileLoop( expression=$2, body=$5 )",
    ],
    85: [
        "$_gen8 = $output_kv $_gen8",
        "$_gen8 = :_empty",
    ],
    86: [
        "$_gen0 = $workflow_or_task $_gen0",
        "$_gen0 = :_empty",
    ],
    87: [
        "$_gen9 = $kv $_gen9",
        "$_gen9 = :_empty",
    ],
    88: [
        "$object_kv = :identifier :colon $e -> ObjectKV( key=$0, value=$2 )",
    ],
    89: [
        "$_gen15 = $mapping $_gen16",
        "$_gen15 = :_empty",
    ],
    90: [
        "$wf_body_element = $call",
        "$wf_body_element = $declaration",
        "$wf_body_element = $while_loop",
        "$wf_body_element = $if_stmt",
        "$wf_body_element = $scatter",
    ],
    91: [
        "$_gen19 = :comma $type_e $_gen19",
        "$_gen19 = :_empty",
    ],
    92: [
        "$task = :task :identifier :lbrace $_gen1 $_gen2 :rbrace -> Task( name=$1, declarations=$3, sections=$4 )",
    ],
    93: [
        "$sections = $command",
        "$sections = $outputs",
        "$sections = $runtime",
        "$sections = $parameter_meta",
        "$sections = $meta",
    ],
    94: [
        "$workflow = :workflow :identifier :lbrace $_gen10 :rbrace -> Workflow( name=$1, body=$3 )",
    ],
    95: [
        "$cmd_param = :cmd_param_start $_gen4 $_gen5 $_gen6 :identifier $_gen7 :cmd_param_end -> CommandParameter( name=$4, type=$3, prefix=$2, attributes=$1, postfix=$5 )",
    ],
    96: [
        "$kv = :identifier :colon $e -> RuntimeAttribute( key=$0, value=$2 )",
    ],
    97: [
        "$_gen20 = $e $_gen21",
        "$_gen20 = :_empty",
    ],
    98: [
        "$outputs = :output :lbrace $_gen8 :rbrace -> Outputs( attributes=$2 )",
    ],
    99: [
        "$scatter = :scatter :lparen :identifier :in $e :rparen :lbrace $_gen10 :rbrace -> Scatter( item=$2, collection=$4, body=$7 )",
    ],
    100: [
    ],
    101: [
        "$postfix_quantifier = :qmark",
        "$postfix_quantifier = :plus",
        "$postfix_quantifier = :asterisk",
    ],
    102: [
        "$_gen2 = $sections $_gen2",
        "$_gen2 = :_empty",
    ],
    103: [
        "$output_kv = $type_e :identifier :equal $e -> Output( type=$0, var=$1, expression=$3 )",
    ],
    104: [
        "$_gen18 = $type_e $_gen19",
        "$_gen18 = :_empty",
    ],
    105: [
        "$_gen22 = $object_kv $_gen23",
        "$_gen22 = :_empty",
    ],
    106: [
        "$call_body_element = $call_input",
        "$call_body_element = $call_output",
    ],
    107: [
        "$_gen3 = $command_part $_gen3",
        "$_gen3 = :_empty",
    ],
    108: [
        "$_gen13 = $declaration $_gen13",
        "$_gen13 = :_empty",
    ],
    109: [
        "$setter = :equal $e -> $1",
    ],
    110: [
        "$_gen17 = $setter",
        "$_gen17 = :_empty",
    ],
    111: [
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
        "$e = :dquote_string",
        "$e = :squote_string",
    ],
    112: [
        "$_gen4 = $cmd_param_kv $_gen4",
        "$_gen4 = :_empty",
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
    119: "$e = :dquote_string",
    120: "$e = :squote_string",
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
    10: 1000, # $type_e = :type <=> :lsquare list($type_e, :comma) :rsquare -> Type( name=$0, subtype=$2 )
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
    tree = ParseTree(NonTerminal(77, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if not current:
        return tree
    if current.id in rule_first[84]:
        # $type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[84]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 1))
    elif current.id in rule_first[85]:
        # $type_e = :type
        ctx.rule = rules[85]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 1))
    return tree
def led_type_e(left, ctx):
    tree = ParseTree(NonTerminal(77, 'type_e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "type_e"
    if current.id == 10: # :lsquare
        # $type_e = :type <=> :lsquare $_gen18 :rsquare -> Type( name=$0, subtype=$2 )
        ctx.rule = rules[84]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('subtype', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Type', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 10)) # :lsquare
        tree.add(parse__gen18(ctx))
        tree.add(expect(ctx, 27)) # :rsquare
    return tree
# END definitions for expression parser: type_e
# START definitions for expression parser: e
infix_binding_power_e = {
    36: 2000, # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
    9: 3000, # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
    52: 4000, # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
    17: 4000, # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
    22: 5000, # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
    28: 5000, # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
    44: 5000, # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
    50: 5000, # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
    54: 6000, # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
    4: 6000, # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
    12: 7000, # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
    42: 7000, # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
    5: 7000, # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
    8: 9000, # $e = :identifier <=> :lparen list($e, :comma) :rparen -> FunctionCall( name=$0, params=$2 )
    10: 10000, # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
    35: 11000, # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
}
prefix_binding_power_e = {
    38: 8000, # $e = :not $e -> LogicalNot( expression=$1 )
    54: 8000, # $e = :plus $e -> UnaryPlus( expression=$1 )
    4: 8000, # $e = :dash $e -> UnaryNegation( expression=$1 )
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
    tree = ParseTree(NonTerminal(111, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if not current:
        return tree
    elif current.id in rule_first[99]:
        # $e = :not $e -> LogicalNot( expression=$1 )
        ctx.rule = rules[99]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 38))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(38)))
        tree.isPrefix = True
    elif current.id in rule_first[100]:
        # $e = :plus $e -> UnaryPlus( expression=$1 )
        ctx.rule = rules[100]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 54))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(54)))
        tree.isPrefix = True
    elif current.id in rule_first[101]:
        # $e = :dash $e -> UnaryNegation( expression=$1 )
        ctx.rule = rules[101]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 2
        tree.add(expect(ctx, 4))
        tree.add(parse_e_internal(ctx, get_prefix_binding_power_e(4)))
        tree.isPrefix = True
    elif current.id in rule_first[106]:
        # $e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[106]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 6))
    elif current.id in rule_first[107]:
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[107]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 6))
    elif current.id in rule_first[108]:
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[108]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 6))
    elif current.id in rule_first[113]:
        # $e = :object :lbrace $_gen22 :rbrace -> ObjectLiteral( map=$2 )
        ctx.rule = rules[113]
        ast_parameters = OrderedDict([
            ('map', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ObjectLiteral', ast_parameters)
        tree.nudMorphemeCount = 4
        tree.add(expect(ctx, 46))
        tree.add(expect(ctx, 19))
        tree.add(parse__gen22(ctx))
        tree.add(expect(ctx, 23))
    elif current.id in rule_first[114]:
        # $e = :lparen $e :rparen -> $1
        ctx.rule = rules[114]
        tree.astTransform = AstTransformSubstitution(1)
        tree.nudMorphemeCount = 3
        tree.add(expect(ctx, 8))
        tree.add(parse_e(ctx))
        tree.add(expect(ctx, 3))
    elif current.id in rule_first[115]:
        # $e = :string
        ctx.rule = rules[115]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 33))
    elif current.id in rule_first[116]:
        # $e = :identifier
        ctx.rule = rules[116]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 6))
    elif current.id in rule_first[117]:
        # $e = :boolean
        ctx.rule = rules[117]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 18))
    elif current.id in rule_first[118]:
        # $e = :integer
        ctx.rule = rules[118]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 0))
    elif current.id in rule_first[119]:
        # $e = :dquote_string
        ctx.rule = rules[119]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 47))
    elif current.id in rule_first[120]:
        # $e = :squote_string
        ctx.rule = rules[120]
        tree.astTransform = AstTransformSubstitution(0)
        tree.nudMorphemeCount = 1
        tree.add(expect(ctx, 21))
    return tree
def led_e(left, ctx):
    tree = ParseTree(NonTerminal(111, 'e'))
    current = ctx.tokens.current()
    ctx.nonterminal = "e"
    if current.id == 36: # :double_pipe
        # $e = $e :double_pipe $e -> LogicalOr( lhs=$0, rhs=$2 )
        ctx.rule = rules[86]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalOr', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 36)) # :double_pipe
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(36) - modifier))
    if current.id == 9: # :double_ampersand
        # $e = $e :double_ampersand $e -> LogicalAnd( lhs=$0, rhs=$2 )
        ctx.rule = rules[87]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LogicalAnd', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 9)) # :double_ampersand
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(9) - modifier))
    if current.id == 52: # :double_equal
        # $e = $e :double_equal $e -> Equals( lhs=$0, rhs=$2 )
        ctx.rule = rules[88]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Equals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 52)) # :double_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(52) - modifier))
    if current.id == 17: # :not_equal
        # $e = $e :not_equal $e -> NotEquals( lhs=$0, rhs=$2 )
        ctx.rule = rules[89]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('NotEquals', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 17)) # :not_equal
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(17) - modifier))
    if current.id == 22: # :lt
        # $e = $e :lt $e -> LessThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[90]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 22)) # :lt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(22) - modifier))
    if current.id == 28: # :lteq
        # $e = $e :lteq $e -> LessThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[91]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('LessThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 28)) # :lteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(28) - modifier))
    if current.id == 44: # :gt
        # $e = $e :gt $e -> GreaterThan( lhs=$0, rhs=$2 )
        ctx.rule = rules[92]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThan', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 44)) # :gt
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(44) - modifier))
    if current.id == 50: # :gteq
        # $e = $e :gteq $e -> GreaterThanOrEqual( lhs=$0, rhs=$2 )
        ctx.rule = rules[93]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('GreaterThanOrEqual', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 50)) # :gteq
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(50) - modifier))
    if current.id == 54: # :plus
        # $e = $e :plus $e -> Add( lhs=$0, rhs=$2 )
        ctx.rule = rules[94]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Add', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 54)) # :plus
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(54) - modifier))
    if current.id == 4: # :dash
        # $e = $e :dash $e -> Subtract( lhs=$0, rhs=$2 )
        ctx.rule = rules[95]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Subtract', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 4)) # :dash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(4) - modifier))
    if current.id == 12: # :asterisk
        # $e = $e :asterisk $e -> Multiply( lhs=$0, rhs=$2 )
        ctx.rule = rules[96]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Multiply', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 12)) # :asterisk
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(12) - modifier))
    if current.id == 42: # :slash
        # $e = $e :slash $e -> Divide( lhs=$0, rhs=$2 )
        ctx.rule = rules[97]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Divide', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 42)) # :slash
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(42) - modifier))
    if current.id == 5: # :percent
        # $e = $e :percent $e -> Remainder( lhs=$0, rhs=$2 )
        ctx.rule = rules[98]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('Remainder', ast_parameters)
        tree.isExprNud = True
        tree.add(left)
        tree.add(expect(ctx, 5)) # :percent
        modifier = 0
        tree.isInfix = True
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(5) - modifier))
    if current.id == 8: # :lparen
        # $e = :identifier <=> :lparen $_gen20 :rparen -> FunctionCall( name=$0, params=$2 )
        ctx.rule = rules[106]
        ast_parameters = OrderedDict([
            ('name', 0),
            ('params', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('FunctionCall', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 8)) # :lparen
        tree.add(parse__gen20(ctx))
        tree.add(expect(ctx, 3)) # :rparen
    if current.id == 10: # :lsquare
        # $e = :identifier <=> :lsquare $e :rsquare -> ArrayIndex( lhs=$0, rhs=$2 )
        ctx.rule = rules[107]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('ArrayIndex', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 10)) # :lsquare
        modifier = 0
        tree.add(parse_e_internal(ctx, get_infix_binding_power_e(10) - modifier))
        tree.add(expect(ctx, 27)) # :rsquare
    if current.id == 35: # :dot
        # $e = :identifier <=> :dot :identifier -> MemberAccess( lhs=$0, rhs=$2 )
        ctx.rule = rules[108]
        ast_parameters = OrderedDict([
            ('lhs', 0),
            ('rhs', 2),
        ])
        tree.astTransform = AstTransformNodeCreator('MemberAccess', ast_parameters)
        tree.add(left)
        tree.add(expect(ctx, 35)) # :dot
        tree.add(expect(ctx, 6)) # :identifier
    return tree
# END definitions for expression parser: e
def parse__gen21(ctx):
    current = ctx.tokens.current()
    rule = table[0][current.id] if current else -1
    tree = ParseTree(NonTerminal(55, '_gen21'))
    ctx.nonterminal = "_gen21"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[55] and current.id not in nonterminal_first[55]:
        return tree
    if current == None:
        return tree
    if rule == 103: # $_gen21 = :comma $e $_gen21
        ctx.rule = rules[103]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 43) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_e(ctx)
        tree.add(subtree)
        subtree = parse__gen21(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_document(ctx):
    current = ctx.tokens.current()
    rule = table[1][current.id] if current else -1
    tree = ParseTree(NonTerminal(56, 'document'))
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
      [terminals[x] for x in nonterminal_first[56] if x >=0],
      rules[2]
    )
def parse__gen7(ctx):
    current = ctx.tokens.current()
    rule = table[2][current.id] if current else -1
    tree = ParseTree(NonTerminal(57, '_gen7'))
    ctx.nonterminal = "_gen7"
    tree.list = False
    if current != None and current.id in nonterminal_follow[57] and current.id not in nonterminal_first[57]:
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
def parse__gen16(ctx):
    current = ctx.tokens.current()
    rule = table[3][current.id] if current else -1
    tree = ParseTree(NonTerminal(58, '_gen16'))
    ctx.nonterminal = "_gen16"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[58] and current.id not in nonterminal_first[58]:
        return tree
    if current == None:
        return tree
    if rule == 65: # $_gen16 = :comma $mapping $_gen16
        ctx.rule = rules[65]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 43) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_mapping(ctx)
        tree.add(subtree)
        subtree = parse__gen16(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_call(ctx):
    current = ctx.tokens.current()
    rule = table[4][current.id] if current else -1
    tree = ParseTree(NonTerminal(59, 'call'))
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
        t = expect(ctx, 25) # :call
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        subtree = parse__gen11(ctx)
        tree.add(subtree)
        subtree = parse__gen12(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[59] if x >=0],
      rules[56]
    )
def parse__gen10(ctx):
    current = ctx.tokens.current()
    rule = table[5][current.id] if current else -1
    tree = ParseTree(NonTerminal(60, '_gen10'))
    ctx.nonterminal = "_gen10"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[60] and current.id not in nonterminal_first[60]:
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
def parse_if_stmt(ctx):
    current = ctx.tokens.current()
    rule = table[6][current.id] if current else -1
    tree = ParseTree(NonTerminal(61, 'if_stmt'))
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
        t = expect(ctx, 29) # :if
        tree.add(t)
        t = expect(ctx, 8) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 3) # :rparen
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[61] if x >=0],
      rules[73]
    )
def parse__gen12(ctx):
    current = ctx.tokens.current()
    rule = table[7][current.id] if current else -1
    tree = ParseTree(NonTerminal(62, '_gen12'))
    ctx.nonterminal = "_gen12"
    tree.list = False
    if current != None and current.id in nonterminal_follow[62] and current.id not in nonterminal_first[62]:
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
def parse_call_body(ctx):
    current = ctx.tokens.current()
    rule = table[8][current.id] if current else -1
    tree = ParseTree(NonTerminal(63, 'call_body'))
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
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen13(ctx)
        tree.add(subtree)
        subtree = parse__gen14(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[63] if x >=0],
      rules[61]
    )
def parse_call_output(ctx):
    current = ctx.tokens.current()
    rule = table[9][current.id] if current else -1
    tree = ParseTree(NonTerminal(64, 'call_output'))
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
        t = expect(ctx, 26) # :output
        tree.add(t)
        t = expect(ctx, 24) # :colon
        tree.add(t)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[64] if x >=0],
      rules[69]
    )
def parse__gen14(ctx):
    current = ctx.tokens.current()
    rule = table[10][current.id] if current else -1
    tree = ParseTree(NonTerminal(65, '_gen14'))
    ctx.nonterminal = "_gen14"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[65] and current.id not in nonterminal_first[65]:
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
def parse_command(ctx):
    current = ctx.tokens.current()
    rule = table[11][current.id] if current else -1
    tree = ParseTree(NonTerminal(66, 'command'))
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
        t = expect(ctx, 20) # :raw_command
        tree.add(t)
        t = expect(ctx, 40) # :raw_cmd_start
        tree.add(t)
        subtree = parse__gen3(ctx)
        tree.add(subtree)
        t = expect(ctx, 14) # :raw_cmd_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[66] if x >=0],
      rules[17]
    )
def parse_meta(ctx):
    current = ctx.tokens.current()
    rule = table[12][current.id] if current else -1
    tree = ParseTree(NonTerminal(67, 'meta'))
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
        t = expect(ctx, 37) # :meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[67] if x >=0],
      rules[39]
    )
def parse_mapping(ctx):
    current = ctx.tokens.current()
    rule = table[13][current.id] if current else -1
    tree = ParseTree(NonTerminal(68, 'mapping'))
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
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 15) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[68] if x >=0],
      rules[70]
    )
def parse__gen1(ctx):
    current = ctx.tokens.current()
    rule = table[14][current.id] if current else -1
    tree = ParseTree(NonTerminal(69, '_gen1'))
    ctx.nonterminal = "_gen1"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[69] and current.id not in nonterminal_first[69]:
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
def parse_declaration(ctx):
    current = ctx.tokens.current()
    rule = table[15][current.id] if current else -1
    tree = ParseTree(NonTerminal(70, 'declaration'))
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
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        subtree = parse__gen17(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[70] if x >=0],
      rules[77]
    )
def parse_call_input(ctx):
    current = ctx.tokens.current()
    rule = table[16][current.id] if current else -1
    tree = ParseTree(NonTerminal(71, 'call_input'))
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
        t = expect(ctx, 48) # :input
        tree.add(t)
        t = expect(ctx, 24) # :colon
        tree.add(t)
        subtree = parse__gen15(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[71] if x >=0],
      rules[68]
    )
def parse_command_part(ctx):
    current = ctx.tokens.current()
    rule = table[17][current.id] if current else -1
    tree = ParseTree(NonTerminal(72, 'command_part'))
    ctx.nonterminal = "command_part"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 18: # $command_part = :cmd_part
        ctx.rule = rules[18]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 34) # :cmd_part
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
      [terminals[x] for x in nonterminal_first[72] if x >=0],
      rules[19]
    )
def parse_parameter_meta(ctx):
    current = ctx.tokens.current()
    rule = table[18][current.id] if current else -1
    tree = ParseTree(NonTerminal(73, 'parameter_meta'))
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
        t = expect(ctx, 2) # :parameter_meta
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[73] if x >=0],
      rules[38]
    )
def parse__gen5(ctx):
    current = ctx.tokens.current()
    rule = table[19][current.id] if current else -1
    tree = ParseTree(NonTerminal(74, '_gen5'))
    ctx.nonterminal = "_gen5"
    tree.list = False
    if current != None and current.id in nonterminal_follow[74] and current.id not in nonterminal_first[74]:
        return tree
    if current == None:
        return tree
    if rule == 22: # $_gen5 = :string
        ctx.rule = rules[22]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 33) # :string
        tree.add(t)
        return tree
    return tree
def parse_alias(ctx):
    current = ctx.tokens.current()
    rule = table[20][current.id] if current else -1
    tree = ParseTree(NonTerminal(75, 'alias'))
    ctx.nonterminal = "alias"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 71: # $alias = :as :identifier -> $1
        ctx.rule = rules[71]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 31) # :as
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[75] if x >=0],
      rules[71]
    )
def parse_runtime(ctx):
    current = ctx.tokens.current()
    rule = table[21][current.id] if current else -1
    tree = ParseTree(NonTerminal(76, 'runtime'))
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
        t = expect(ctx, 32) # :runtime
        tree.add(t)
        subtree = parse_map(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[76] if x >=0],
      rules[37]
    )
def parse_workflow_or_task(ctx):
    current = ctx.tokens.current()
    rule = table[23][current.id] if current else -1
    tree = ParseTree(NonTerminal(78, 'workflow_or_task'))
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
      [terminals[x] for x in nonterminal_first[78] if x >=0],
      rules[4]
    )
def parse_cmd_param_kv(ctx):
    current = ctx.tokens.current()
    rule = table[24][current.id] if current else -1
    tree = ParseTree(NonTerminal(79, 'cmd_param_kv'))
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
        t = expect(ctx, 41) # :cmd_attr_hint
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 15) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[79] if x >=0],
      rules[29]
    )
def parse_map(ctx):
    current = ctx.tokens.current()
    rule = table[25][current.id] if current else -1
    tree = ParseTree(NonTerminal(80, 'map'))
    ctx.nonterminal = "map"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 42: # $map = :lbrace $_gen9 :rbrace -> $1
        ctx.rule = rules[42]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen9(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[80] if x >=0],
      rules[42]
    )
def parse__gen23(ctx):
    current = ctx.tokens.current()
    rule = table[26][current.id] if current else -1
    tree = ParseTree(NonTerminal(81, '_gen23'))
    ctx.nonterminal = "_gen23"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[81] and current.id not in nonterminal_first[81]:
        return tree
    if current == None:
        return tree
    if rule == 110: # $_gen23 = :comma $object_kv $_gen23
        ctx.rule = rules[110]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 43) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_object_kv(ctx)
        tree.add(subtree)
        subtree = parse__gen23(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse__gen11(ctx):
    current = ctx.tokens.current()
    rule = table[27][current.id] if current else -1
    tree = ParseTree(NonTerminal(82, '_gen11'))
    ctx.nonterminal = "_gen11"
    tree.list = False
    if current != None and current.id in nonterminal_follow[82] and current.id not in nonterminal_first[82]:
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
def parse__gen6(ctx):
    current = ctx.tokens.current()
    rule = table[28][current.id] if current else -1
    tree = ParseTree(NonTerminal(83, '_gen6'))
    ctx.nonterminal = "_gen6"
    tree.list = False
    if current != None and current.id in nonterminal_follow[83] and current.id not in nonterminal_first[83]:
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
def parse_while_loop(ctx):
    current = ctx.tokens.current()
    rule = table[29][current.id] if current else -1
    tree = ParseTree(NonTerminal(84, 'while_loop'))
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
        t = expect(ctx, 53) # :while
        tree.add(t)
        t = expect(ctx, 8) # :lparen
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 3) # :rparen
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[84] if x >=0],
      rules[72]
    )
def parse__gen8(ctx):
    current = ctx.tokens.current()
    rule = table[30][current.id] if current else -1
    tree = ParseTree(NonTerminal(85, '_gen8'))
    ctx.nonterminal = "_gen8"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[85] and current.id not in nonterminal_first[85]:
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
def parse__gen0(ctx):
    current = ctx.tokens.current()
    rule = table[31][current.id] if current else -1
    tree = ParseTree(NonTerminal(86, '_gen0'))
    ctx.nonterminal = "_gen0"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[86] and current.id not in nonterminal_first[86]:
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
def parse__gen9(ctx):
    current = ctx.tokens.current()
    rule = table[32][current.id] if current else -1
    tree = ParseTree(NonTerminal(87, '_gen9'))
    ctx.nonterminal = "_gen9"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[87] and current.id not in nonterminal_first[87]:
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
def parse_object_kv(ctx):
    current = ctx.tokens.current()
    rule = table[33][current.id] if current else -1
    tree = ParseTree(NonTerminal(88, 'object_kv'))
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
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 24) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[88] if x >=0],
      rules[79]
    )
def parse__gen15(ctx):
    current = ctx.tokens.current()
    rule = table[34][current.id] if current else -1
    tree = ParseTree(NonTerminal(89, '_gen15'))
    ctx.nonterminal = "_gen15"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[89] and current.id not in nonterminal_first[89]:
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
def parse_wf_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[35][current.id] if current else -1
    tree = ParseTree(NonTerminal(90, 'wf_body_element'))
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
      [terminals[x] for x in nonterminal_first[90] if x >=0],
      rules[51]
    )
def parse__gen19(ctx):
    current = ctx.tokens.current()
    rule = table[36][current.id] if current else -1
    tree = ParseTree(NonTerminal(91, '_gen19'))
    ctx.nonterminal = "_gen19"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[91] and current.id not in nonterminal_first[91]:
        return tree
    if current == None:
        return tree
    if rule == 81: # $_gen19 = :comma $type_e $_gen19
        ctx.rule = rules[81]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 43) # :comma
        tree.add(t)
        tree.listSeparator = t
        subtree = parse_type_e(ctx)
        tree.add(subtree)
        subtree = parse__gen19(ctx)
        tree.add(subtree)
        return tree
    return tree
def parse_task(ctx):
    current = ctx.tokens.current()
    rule = table[37][current.id] if current else -1
    tree = ParseTree(NonTerminal(92, 'task'))
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
        t = expect(ctx, 13) # :task
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen1(ctx)
        tree.add(subtree)
        subtree = parse__gen2(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[92] if x >=0],
      rules[9]
    )
def parse_sections(ctx):
    current = ctx.tokens.current()
    rule = table[38][current.id] if current else -1
    tree = ParseTree(NonTerminal(93, 'sections'))
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
      [terminals[x] for x in nonterminal_first[93] if x >=0],
      rules[14]
    )
def parse_workflow(ctx):
    current = ctx.tokens.current()
    rule = table[39][current.id] if current else -1
    tree = ParseTree(NonTerminal(94, 'workflow'))
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
        t = expect(ctx, 39) # :workflow
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[94] if x >=0],
      rules[46]
    )
def parse_cmd_param(ctx):
    current = ctx.tokens.current()
    rule = table[40][current.id] if current else -1
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
        t = expect(ctx, 45) # :cmd_param_start
        tree.add(t)
        subtree = parse__gen4(ctx)
        tree.add(subtree)
        subtree = parse__gen5(ctx)
        tree.add(subtree)
        subtree = parse__gen6(ctx)
        tree.add(subtree)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        subtree = parse__gen7(ctx)
        tree.add(subtree)
        t = expect(ctx, 49) # :cmd_param_end
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[95] if x >=0],
      rules[28]
    )
def parse_kv(ctx):
    current = ctx.tokens.current()
    rule = table[41][current.id] if current else -1
    tree = ParseTree(NonTerminal(96, 'kv'))
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
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 24) # :colon
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[96] if x >=0],
      rules[43]
    )
def parse__gen20(ctx):
    current = ctx.tokens.current()
    rule = table[42][current.id] if current else -1
    tree = ParseTree(NonTerminal(97, '_gen20'))
    ctx.nonterminal = "_gen20"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[97] and current.id not in nonterminal_first[97]:
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
def parse_outputs(ctx):
    current = ctx.tokens.current()
    rule = table[43][current.id] if current else -1
    tree = ParseTree(NonTerminal(98, 'outputs'))
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
        t = expect(ctx, 26) # :output
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen8(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[98] if x >=0],
      rules[35]
    )
def parse_scatter(ctx):
    current = ctx.tokens.current()
    rule = table[44][current.id] if current else -1
    tree = ParseTree(NonTerminal(99, 'scatter'))
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
        t = expect(ctx, 30) # :scatter
        tree.add(t)
        t = expect(ctx, 8) # :lparen
        tree.add(t)
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 16) # :in
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        t = expect(ctx, 3) # :rparen
        tree.add(t)
        t = expect(ctx, 19) # :lbrace
        tree.add(t)
        subtree = parse__gen10(ctx)
        tree.add(subtree)
        t = expect(ctx, 23) # :rbrace
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[99] if x >=0],
      rules[74]
    )
def parse_declarations(ctx):
    current = ctx.tokens.current()
    rule = table[45][current.id] if current else -1
    tree = ParseTree(NonTerminal(100, 'declarations'))
    ctx.nonterminal = "declarations"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[100] if x >=0],
      rules[74]
    )
def parse_postfix_quantifier(ctx):
    current = ctx.tokens.current()
    rule = table[46][current.id] if current else -1
    tree = ParseTree(NonTerminal(101, 'postfix_quantifier'))
    ctx.nonterminal = "postfix_quantifier"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 30: # $postfix_quantifier = :qmark
        ctx.rule = rules[30]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 51) # :qmark
        tree.add(t)
        return tree
    elif rule == 31: # $postfix_quantifier = :plus
        ctx.rule = rules[31]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 54) # :plus
        tree.add(t)
        return tree
    elif rule == 32: # $postfix_quantifier = :asterisk
        ctx.rule = rules[32]
        tree.astTransform = AstTransformSubstitution(0)
        t = expect(ctx, 12) # :asterisk
        tree.add(t)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[101] if x >=0],
      rules[32]
    )
def parse__gen2(ctx):
    current = ctx.tokens.current()
    rule = table[47][current.id] if current else -1
    tree = ParseTree(NonTerminal(102, '_gen2'))
    ctx.nonterminal = "_gen2"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[102] and current.id not in nonterminal_first[102]:
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
def parse_output_kv(ctx):
    current = ctx.tokens.current()
    rule = table[48][current.id] if current else -1
    tree = ParseTree(NonTerminal(103, 'output_kv'))
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
        t = expect(ctx, 6) # :identifier
        tree.add(t)
        t = expect(ctx, 15) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[103] if x >=0],
      rules[36]
    )
def parse__gen18(ctx):
    current = ctx.tokens.current()
    rule = table[49][current.id] if current else -1
    tree = ParseTree(NonTerminal(104, '_gen18'))
    ctx.nonterminal = "_gen18"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[104] and current.id not in nonterminal_first[104]:
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
def parse__gen22(ctx):
    current = ctx.tokens.current()
    rule = table[50][current.id] if current else -1
    tree = ParseTree(NonTerminal(105, '_gen22'))
    ctx.nonterminal = "_gen22"
    tree.list = 'slist'
    if current != None and current.id in nonterminal_follow[105] and current.id not in nonterminal_first[105]:
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
def parse_call_body_element(ctx):
    current = ctx.tokens.current()
    rule = table[51][current.id] if current else -1
    tree = ParseTree(NonTerminal(106, 'call_body_element'))
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
      [terminals[x] for x in nonterminal_first[106] if x >=0],
      rules[63]
    )
def parse__gen3(ctx):
    current = ctx.tokens.current()
    rule = table[52][current.id] if current else -1
    tree = ParseTree(NonTerminal(107, '_gen3'))
    ctx.nonterminal = "_gen3"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[107] and current.id not in nonterminal_first[107]:
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
def parse__gen13(ctx):
    current = ctx.tokens.current()
    rule = table[53][current.id] if current else -1
    tree = ParseTree(NonTerminal(108, '_gen13'))
    ctx.nonterminal = "_gen13"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[108] and current.id not in nonterminal_first[108]:
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
def parse_setter(ctx):
    current = ctx.tokens.current()
    rule = table[54][current.id] if current else -1
    tree = ParseTree(NonTerminal(109, 'setter'))
    ctx.nonterminal = "setter"
    tree.list = False
    if current == None:
        raise ctx.errors.unexpected_eof()
    if rule == 78: # $setter = :equal $e -> $1
        ctx.rule = rules[78]
        tree.astTransform = AstTransformSubstitution(1)
        t = expect(ctx, 15) # :equal
        tree.add(t)
        subtree = parse_e(ctx)
        tree.add(subtree)
        return tree
    raise ctx.errors.unexpected_symbol(
      ctx.nonterminal,
      ctx.tokens.current(),
      [terminals[x] for x in nonterminal_first[109] if x >=0],
      rules[78]
    )
def parse__gen17(ctx):
    current = ctx.tokens.current()
    rule = table[55][current.id] if current else -1
    tree = ParseTree(NonTerminal(110, '_gen17'))
    ctx.nonterminal = "_gen17"
    tree.list = False
    if current != None and current.id in nonterminal_follow[110] and current.id not in nonterminal_first[110]:
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
def parse__gen4(ctx):
    current = ctx.tokens.current()
    rule = table[57][current.id] if current else -1
    tree = ParseTree(NonTerminal(112, '_gen4'))
    ctx.nonterminal = "_gen4"
    tree.list = 'nlist'
    if current != None and current.id in nonterminal_follow[112] and current.id not in nonterminal_first[112]:
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
          (re.compile(r'(array|map|object|boolean|int|float|uri|file|string)(?![a-zA-Z0-9_])(?![a-zA-Z0-9_])'), [
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
          (re.compile(r'(array|map|object|boolean|int|float|uri|file|string)(?![a-zA-Z0-9_])(?![a-zA-Z0-9_])'), [
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
