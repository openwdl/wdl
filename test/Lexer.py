import re, sys, base64, json
from collections import OrderedDict
from wdl_Parser import wdl_Parser

def token(string, lineno, colno, terminalId, lexer):
  lexer.addToken(Token(terminalId, lexer.resource, wdl_Parser.terminals[terminalId], string, lineno, colno))

class SourceCode:
  def __init__(self, resource, fp, line = 1, column = 1):
    self.__dict__.update(locals())
    self.sourceCode = fp.read()
    fp.close()

  def getResource(self):
    return self.resource

  def getString(self):
    return self.sourceCode

  def getColumn(self):
    return self.column

  def getLine(self):
    return self.line

  def __str__(self):
    return '<SourceCode file=%s>' % (self.resource)

class Token:
  def __init__(self, id, resource, terminal_str, source_string, lineno, colno):
    self.__dict__.update(locals())
  
  def getString(self):
    return self.source_string
  
  def getLine(self):
    return self.lineno
  
  def getColumn(self):
    return self.colno

  def getId(self):
    return self.id

  def getTerminalStr(self):
    return self.terminal_str

  def getResource(self):
    return self.resource

  def toAst(self):
    return self
  
  def __str__( self ):
    return json.dumps(self.json())

  def json(self):
    return OrderedDict([
      ('terminal', self.terminal_str.lower()),
      ('line', self.lineno),
      ('col', self.colno),
      ('resource', self.resource),
      ('source_string', base64.b64encode(self.source_string.encode('utf-8')).decode('utf-8'))
    ])

class Cursor:
  def __init__(self):
    self.string = ''
    self.lineno = 1
    self.colno = 1
    c = lambda x: c_Parser.terminals[x]
    self.insertSpaceAfter = {
      c('else')
    }

  def add(self, token):
    if token.lineno > self.lineno:
      self.string += ''.join('\n' for i in range(token.lineno - self.lineno))
      self.lineno = token.lineno
      self.colno = 1
    if token.colno > self.colno:
      self.string += ''.join(' ' for i in range(token.colno - self.colno))
      self.colno = token.colno
    self.string += token.source_string
    if token.fromPreprocessor or token.id in self.insertSpaceAfter:
      self.string += ' '
    self.colno += len(token.source_string)
  def __str__(self):
    return self.string

class SourceCodeWriter:
  def __init__(self, tokenList, parsetree=None, grammar=None, ast=None, theme=None, highlight=False):
    self.__dict__.update(locals())
    self.string = ''
    self.lineno = 1
    self.colno = 1
    self.ancestors = dict([(t, set()) for t in self.tokenList])
    self.parents = dict([(t, set()) for t in self.tokenList])
    self.getTokenAncestors(ast)
    self.termcolor = XTermColorMap()
    c = lambda x: c_Parser.terminals[x]
    self.insertSpaceAfter = {
      c('else')
    }

    # bah, cruft
    self.keywords = []

  def getTokenAncestors(self, ast):
    self.stack = []
    self._getTokenAncestors(ast)

  def _getTokenAncestors(self, ast):
    if not ast:
      return
    self.stack.append(ast.name)
    for (attr, obj) in ast.attributes.items():
      if isinstance(obj, Token):
        self.ancestors[obj] = self.ancestors[obj].union(set(self.stack))
        self.parents[obj] = (self.stack[-1], attr)
      elif isinstance(obj, Ast):
        self._getTokenAncestors(obj)
      elif isinstance(obj, list):
        for x in obj:
          if isinstance(x, Token):
            self.ancestors[x] = self.ancestors[x].union(set(self.stack))
            self.parents[x] = (self.stack[-1], attr)
          else:
            self._getTokenAncestors(x)
    self.stack.pop()

  def add(self, token):
    if token.lineno > self.lineno:
      self.string += ''.join('\n' for i in range(token.lineno - self.lineno))
      self.lineno = token.lineno
      self.colno = 1
    if token.colno > self.colno:
      self.string += ''.join(' ' for i in range(token.colno - self.colno))
      self.colno = token.colno

    self.string += self.doHighlight(token)

    if token.fromPreprocessor or token.id in self.insertSpaceAfter:
      self.string += ' '
    self.colno += len(token.source_string)

  def doHighlight(self, token):
    if not self.highlight:
      return token.source_string

    if token in self.parents and len(self.parents[token]):
      (parent, attr) = self.parents[token]
      if attr == 'declaration_specifiers':
        return self.termcolor.colorize(token.source_string, 0x0087ff)
      if parent == 'FuncCall' and attr == 'name':
        return self.termcolor.colorize(token.source_string, 0x8700ff)
      if parent == 'FunctionSignature' and attr == 'declarator':
        return self.termcolor.colorize(token.source_string, 0xff8700)
    if self.grammar:
      if not len(self.keywords):
        for rule in self.grammar.getRules():
          terminal = rule.isTokenAlias()
          if terminal and rule.nonterminal.string == 'keyword':
            self.keywords.append(terminal.string)
      if token.terminal_str in self.keywords:
        return self.termcolor.colorize(token.source_string, 0xffff00)
    if token.terminal_str == 'string_literal':
      return self.termcolor.colorize(token.source_string, 0xff0000)
    if token.terminal_str == 'identifier':
      return self.termcolor.colorize(token.source_string, 0x00ff00)

    return token.source_string

  def __str__(self):
    if not len(self.string):
      for token in self.tokenList:
        self.add(token)
    return self.string

class TokenList(list):
  def __init__(self, arg1=[]):
    super().__init__(arg1)
    self.isIter = False
  def __iter__(self):
    if self.isIter == False:
      self.index = 0
      isIter = True
    return self
  def __next__(self):
    try:
      rval = self[self.index]
      self.index += 1
      return rval
    except:
      raise StopIteration
  def reset(self):
    self.isIter = False
  def peek(self, whereto):
    try:
      return self[self.index + int(whereto)]
    except:
      return None
  def go(self, whereto):
    whereto = int(whereto)
    if self.index + whereto < 0 or self.index + whereto + 1 > len(self):
      raise Exception()
    self.index += whereto
    return self
  def check(self, whereto, ids):
    try:
      return self[self.index + int(whereto) - 1].id in ids
    except:
      return False
  def toString(self, parsetree=None, grammar=None, ast=None, theme=None, highlight=False):
    kwargs = locals()
    del kwargs['self']
    scw = SourceCodeWriter(self, **kwargs)
    return str(scw)
    cursor = Cursor()
    for token in self:
      cursor.add( token )
    return str(cursor)

class Lexer:
  def __iter__(self):
    return self
  
  def __next__(self):
    raise StopIteration()

class StatelessPatternMatchingLexer(Lexer):
  def __init__(self, regex):
    self.__dict__.update(locals())
  def match(self, string, wholeStringOnly=False):
    for (regex, terminalId, function) in self.regex:
      match = regex.match(string)
      if match:
        sourceString = match.group(0)
        if wholeStringOnly and sourceString != string:
          continue
        return (sourceString, terminalId, function)
    return (None, None, None)

class PatternMatchingLexer(StatelessPatternMatchingLexer):
  def __init__(self, sourceCode, regex):
    self.__dict__.update(locals())
    self.string = sourceCode.getString()
    self.resource = sourceCode.getResource()
    self.colno = sourceCode.getColumn()
    self.lineno = sourceCode.getLine()
    self.cache = []
  
  def addToken(self, token):
    self.cache.append(token)
  
  def addTokens(self, tokens):
    self.cache.extend(tokens)
  
  def hasToken(self):
    return len(self.cache) > 0
  
  def nextToken(self):
    if not self.hasToken():
      return None
    token = self.cache[0]
    self.cache = self.cache[1:]
    return token

  def advance(self, string):
    self.string = self.string[len(string):]
    newlines = len(list(filter(lambda x: x == '\n', string)))
    self.lineno += newlines
    if newlines > 0:
      self.colno = len(string.split('\n')[-1]) + 1
    else:
      self.colno += len(string)

  def peek(self, n=1):
    # returns an n-item list of tuples: (terminalId, length)
    lookahead = list()
    loc = 0
    for i in range(n):
      current = self.string[loc:]
      if not len(current):
        return lookahead
      for (regex, terminalId, function) in self.regex:
        match = regex.match(current)
        if match:
          length = len(match.group(0))
          loc += length
          lookahead.append( (terminalId,match.group(0),) )
    return lookahead

  def nextMatch(self):
    activity = True
    while activity:
      activity = False
      if not len(self.string):
        raise StopIteration()
      (string, terminalId, function) = self.match(self.string)
      if string is not None:
        activity = True
        lineno = self.lineno
        colno = self.colno
        self.advance( string )
        if function:
          function(string, lineno, colno, terminalId, self)
          return self.nextToken()
    return None

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.hasToken():
      token = self.nextToken()
      return token
    if len(self.string.strip()) <= 0:
      raise StopIteration()
    token = self.nextMatch()
    if not token:
      error = 'Invalid character on line %d, col %d' % (self.lineno, self.colno)
      raise Exception(error)
    return token

class wdlLexer(PatternMatchingLexer):
  regex = [
    ( re.compile(r'scatter-gather(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_SCATTER_GATHER, token ),
    ( re.compile(r'String(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_STRING, token ),
    ( re.compile(r'workflow(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_WORKFLOW, token ),
    ( re.compile(r'File(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_FILE, token ),
    ( re.compile(r'output(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_OUTPUT, token ),
    ( re.compile(r'step(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_STEP, token ),
    ( re.compile(r'command(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_COMMAND, token ),
    ( re.compile(r'action(?=[^a-zA-Z_]|$)'), wdl_Parser.TERMINAL_ACTION, token ),
    ( re.compile(r','), wdl_Parser.TERMINAL_COMMA, token ),
    ( re.compile(r':'), wdl_Parser.TERMINAL_COLON, token ),
    ( re.compile(r'}'), wdl_Parser.TERMINAL_RBRACE, token ),
    ( re.compile(r';'), wdl_Parser.TERMINAL_SEMI, token ),
    ( re.compile(r'{'), wdl_Parser.TERMINAL_LBRACE, token ),
    ( re.compile(r'='), wdl_Parser.TERMINAL_EQUALS, token ),
    ( re.compile(r'\('), wdl_Parser.TERMINAL_LPAREN, token ),
    ( re.compile(r'\)'), wdl_Parser.TERMINAL_RPAREN, token ),
    ( re.compile(r'"([^\\\"\n]|\\[\\"\'nrbtfav\?]|\\[0-7]{1,3}|\\x[0-9a-fA-F]+|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"'), wdl_Parser.TERMINAL_STRING_LITERAL, token ),
    ( re.compile(r'([a-zA-Z_]|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)([a-zA-Z_0-9]|\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*'), wdl_Parser.TERMINAL_IDENTIFIER, token ),
    ( re.compile(r'[ \t\n]+', 0), None, None )
  ]

  def __init__(self):
    super(wdlLexer, self).__init__(SourceCode('/dev/stdin', sys.stdin), self.regex)

if __name__ == '__main__':
  lex = wdlLexer()
  tokens = list(lex)
  print('[')
  for (i, token) in enumerate(tokens):
    print('  {}{}'.format(token, ',' if i != len(tokens) - 1 else ''))
  print(']')
