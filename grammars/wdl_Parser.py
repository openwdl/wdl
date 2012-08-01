import sys, inspect
from ParserCommon import *
def whoami():
  return inspect.stack()[1][3]
def whosdaddy():
  return inspect.stack()[2][3]
def parse( iterator, entry ):
  p = wdl_Parser()
  return p.parse(iterator, entry)
class wdl_Parser:
  # Quark - finite string set maps one string to exactly one int, and vice versa
  terminals = {
    0: 'comma',
    1: 'string_literal',
    2: 'scatter_gather',
    3: 'string',
    4: 'workflow',
    5: 'file',
    6: 'identifier',
    7: 'output',
    8: 'colon',
    9: 'rbrace',
    10: 'semi',
    11: 'step',
    12: 'lbrace',
    13: 'equals',
    14: 'lparen',
    15: 'command',
    16: 'action',
    17: 'rparen',
    'comma': 0,
    'string_literal': 1,
    'scatter_gather': 2,
    'string': 3,
    'workflow': 4,
    'file': 5,
    'identifier': 6,
    'output': 7,
    'colon': 8,
    'rbrace': 9,
    'semi': 10,
    'step': 11,
    'lbrace': 12,
    'equals': 13,
    'lparen': 14,
    'command': 15,
    'action': 16,
    'rparen': 17,
  }
  # Quark - finite string set maps one string to exactly one int, and vice versa
  nonterminals = {
    18: 'step_body',
    19: 'workflow',
    20: 'step',
    21: 'step_body_spec',
    22: '_gen2',
    23: '_gen4',
    24: 'step_action_sub',
    25: 'step_action_scatter_gather',
    26: 'step_parameter_type',
    27: '_gen6',
    28: '_gen5',
    29: '_gen3',
    30: '_gen7',
    31: 'step_action_command',
    32: '_gen8',
    33: 'workflow_body',
    34: '_gen0',
    35: 'workflow_step_output',
    36: 'step_parameter',
    37: 'workflow_step_input',
    38: 'wdl',
    39: 'workflow_step_input_param',
    40: 'workflow_step_output_param',
    41: 'workflow_step',
    42: '_gen1',
    43: 'step_action',
    44: 'wdl_entity',
    45: 'step_output',
    'step_body': 18,
    'workflow': 19,
    'step': 20,
    'step_body_spec': 21,
    '_gen2': 22,
    '_gen4': 23,
    'step_action_sub': 24,
    'step_action_scatter_gather': 25,
    'step_parameter_type': 26,
    '_gen6': 27,
    '_gen5': 28,
    '_gen3': 29,
    '_gen7': 30,
    'step_action_command': 31,
    '_gen8': 32,
    'workflow_body': 33,
    '_gen0': 34,
    'workflow_step_output': 35,
    'step_parameter': 36,
    'workflow_step_input': 37,
    'wdl': 38,
    'workflow_step_input_param': 39,
    'workflow_step_output_param': 40,
    'workflow_step': 41,
    '_gen1': 42,
    'step_action': 43,
    'wdl_entity': 44,
    'step_output': 45,
  }
  # table[nonterminal][terminal] = rule
  table = [
    [-1, -1, -1, -1, -1, -1, -1, 3, -1, 3, -1, -1, -1, -1, -1, -1, 3, -1],
    [-1, -1, -1, -1, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 40, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1],
    [-1, 6, -1, -1, -1, 6, 6, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, 39],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21],
    [-1, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1, -1],
    [-1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 18, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20],
    [33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25],
    [9, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, 10],
    [35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 24, -1, 43, -1, -1, -1, -1, -1, -1, 24, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, 31, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 23, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1],
    [-1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1],
    [-1, 4, -1, -1, -1, 38, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, 2, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1],
    [-1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  ]
  TERMINAL_COMMA = 0
  TERMINAL_STRING_LITERAL = 1
  TERMINAL_SCATTER_GATHER = 2
  TERMINAL_STRING = 3
  TERMINAL_WORKFLOW = 4
  TERMINAL_FILE = 5
  TERMINAL_IDENTIFIER = 6
  TERMINAL_OUTPUT = 7
  TERMINAL_COLON = 8
  TERMINAL_RBRACE = 9
  TERMINAL_SEMI = 10
  TERMINAL_STEP = 11
  TERMINAL_LBRACE = 12
  TERMINAL_EQUALS = 13
  TERMINAL_LPAREN = 14
  TERMINAL_COMMAND = 15
  TERMINAL_ACTION = 16
  TERMINAL_RPAREN = 17
  def __init__(self, tokens=None):
    self.__dict__.update(locals())
    self.expressionParsers = dict()
  def isTerminal(self, id):
    return 0 <= id <= 17
  def isNonTerminal(self, id):
    return 18 <= id <= 45
  def parse(self, tokens):
    self.tokens = tokens
    self.start = 'WDL'
    tree = self.parse_wdl()
    if self.tokens.current() != None:
      raise SyntaxError( 'Finished parsing without consuming all tokens.' )
    return tree
  def expect(self, terminalId):
    currentToken = self.tokens.current()
    if not currentToken:
      raise SyntaxError( 'No more tokens.  Expecting %s' % (self.terminals[terminalId]) )
    if currentToken.getId() != terminalId:
      raise SyntaxError( 'Unexpected symbol when parsing %s.  Expected %s, got %s.' %(whosdaddy(), self.terminals[terminalId], currentToken if currentToken else 'None') )
    nextToken = self.tokens.advance()
    if nextToken and not self.isTerminal(nextToken.getId()):
      raise SyntaxError( 'Invalid symbol ID: %d (%s)' % (nextToken.getId(), nextToken) )
    return currentToken
  def parse_step_body(self):
    current = self.tokens.current()
    rule = self.table[0][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(18, self.nonterminals[18]))
    tree.list = False
    if current == None:
      return tree
    if rule == 3:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse__gen8()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_workflow(self):
    current = self.tokens.current()
    rule = self.table[1][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(19, self.nonterminals[19]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 41:
      tree.astTransform = AstTransformNodeCreator('Workflow', {'body': 3, 'name': 1})
      t = self.expect(4) # workflow
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(12) # lbrace
      tree.add(t)
      subtree = self.parse_workflow_body()
      tree.add( subtree )
      t = self.expect(9) # rbrace
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_step(self):
    current = self.tokens.current()
    rule = self.table[2][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(20, self.nonterminals[20]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 40:
      tree.astTransform = AstTransformNodeCreator('Step', {'body': 6, 'name': 1, 'parameters': 3})
      t = self.expect(11) # step
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(14) # lparen
      tree.add(t)
      subtree = self.parse__gen6()
      tree.add( subtree )
      t = self.expect(17) # rparen
      tree.add(t)
      t = self.expect(12) # lbrace
      tree.add(t)
      subtree = self.parse_step_body()
      tree.add( subtree )
      t = self.expect(9) # rbrace
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_step_body_spec(self):
    current = self.tokens.current()
    rule = self.table[3][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(21, self.nonterminals[21]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 7:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_action()
      tree.add( subtree )
      return tree
    elif rule == 17:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_output()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse__gen2(self):
    current = self.tokens.current()
    rule = self.table[4][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(22, self.nonterminals[22]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17, 10]):
      return tree
    if current == None:
      return tree
    if rule == 6:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_workflow_step_input_param()
      tree.add( subtree )
      subtree = self.parse__gen3()
      tree.add( subtree )
      return tree
    return tree
  def parse__gen4(self):
    current = self.tokens.current()
    rule = self.table[5][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(23, self.nonterminals[23]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17]):
      return tree
    if current == None:
      return tree
    if rule == 1:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_workflow_step_output_param()
      tree.add( subtree )
      subtree = self.parse__gen5()
      tree.add( subtree )
      return tree
    return tree
  def parse_step_action_sub(self):
    current = self.tokens.current()
    rule = self.table[6][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(24, self.nonterminals[24]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 29:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_action_command()
      tree.add( subtree )
      return tree
    elif rule == 42:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_action_scatter_gather()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_step_action_scatter_gather(self):
    current = self.tokens.current()
    rule = self.table[7][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(25, self.nonterminals[25]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 36:
      tree.astTransform = AstTransformNodeCreator('ScatterGatherAction', {'gather': 6, 'scatter': 4, 'prepare': 2})
      t = self.expect(2) # scatter_gather
      tree.add(t)
      t = self.expect(14) # lparen
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(0) # comma
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(0) # comma
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(17) # rparen
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_step_parameter_type(self):
    current = self.tokens.current()
    rule = self.table[8][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(26, self.nonterminals[26]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 18:
      tree.astTransform = AstTransformSubstitution(0)
      t = self.expect(3) # string
      tree.add(t)
      return tree
    elif rule == 27:
      tree.astTransform = AstTransformSubstitution(0)
      t = self.expect(5) # file
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse__gen6(self):
    current = self.tokens.current()
    rule = self.table[9][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(27, self.nonterminals[27]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17]):
      return tree
    if current == None:
      return tree
    if rule == 32:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_parameter()
      tree.add( subtree )
      subtree = self.parse__gen7()
      tree.add( subtree )
      return tree
    return tree
  def parse__gen5(self):
    current = self.tokens.current()
    rule = self.table[10][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(28, self.nonterminals[28]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17]):
      return tree
    if current == None:
      return tree
    if rule == 33:
      tree.astTransform = AstTransformSubstitution(0)
      t = self.expect(0) # comma
      tree.add(t)
      tree.listSeparator = t
      subtree = self.parse_workflow_step_output_param()
      tree.add( subtree )
      subtree = self.parse__gen5()
      tree.add( subtree )
      return tree
    return tree
  def parse__gen3(self):
    current = self.tokens.current()
    rule = self.table[11][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(29, self.nonterminals[29]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17, 10]):
      return tree
    if current == None:
      return tree
    if rule == 9:
      tree.astTransform = AstTransformSubstitution(0)
      t = self.expect(0) # comma
      tree.add(t)
      tree.listSeparator = t
      subtree = self.parse_workflow_step_input_param()
      tree.add( subtree )
      subtree = self.parse__gen3()
      tree.add( subtree )
      return tree
    return tree
  def parse__gen7(self):
    current = self.tokens.current()
    rule = self.table[12][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(30, self.nonterminals[30]))
    tree.list = 'slist'
    if current != None and (current.getId() in [17]):
      return tree
    if current == None:
      return tree
    if rule == 35:
      tree.astTransform = AstTransformSubstitution(0)
      t = self.expect(0) # comma
      tree.add(t)
      tree.listSeparator = t
      subtree = self.parse_step_parameter()
      tree.add( subtree )
      subtree = self.parse__gen7()
      tree.add( subtree )
      return tree
    return tree
  def parse_step_action_command(self):
    current = self.tokens.current()
    rule = self.table[13][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(31, self.nonterminals[31]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 5:
      tree.astTransform = AstTransformNodeCreator('CommandAction', {'cmd': 2})
      t = self.expect(15) # command
      tree.add(t)
      t = self.expect(14) # lparen
      tree.add(t)
      t = self.expect(1) # string_literal
      tree.add(t)
      t = self.expect(17) # rparen
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse__gen8(self):
    current = self.tokens.current()
    rule = self.table[14][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(32, self.nonterminals[32]))
    tree.list = 'nlist'
    if current != None and (current.getId() in [9]):
      return tree
    if current == None:
      return tree
    if rule == 24:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step_body_spec()
      tree.add( subtree )
      subtree = self.parse__gen8()
      tree.add( subtree )
      return tree
    return tree
  def parse_workflow_body(self):
    current = self.tokens.current()
    rule = self.table[15][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(33, self.nonterminals[33]))
    tree.list = False
    if current == None:
      return tree
    if rule == 31:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse__gen1()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse__gen0(self):
    current = self.tokens.current()
    rule = self.table[16][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(34, self.nonterminals[34]))
    tree.list = 'nlist'
    if current != None and (current.getId() in [-1]):
      return tree
    if current == None:
      return tree
    if rule == 23:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_wdl_entity()
      tree.add( subtree )
      subtree = self.parse__gen0()
      tree.add( subtree )
      return tree
    return tree
  def parse_workflow_step_output(self):
    current = self.tokens.current()
    rule = self.table[17][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(35, self.nonterminals[35]))
    tree.list = False
    if current != None and (current.getId() in [6]):
      return tree
    if current == None:
      return tree
    if rule == 11:
      tree.astTransform = AstTransformSubstitution(1)
      t = self.expect(14) # lparen
      tree.add(t)
      subtree = self.parse__gen4()
      tree.add( subtree )
      t = self.expect(17) # rparen
      tree.add(t)
      t = self.expect(13) # equals
      tree.add(t)
      return tree
    return tree
  def parse_step_parameter(self):
    current = self.tokens.current()
    rule = self.table[18][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(36, self.nonterminals[36]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 12:
      tree.astTransform = AstTransformNodeCreator('StepInputParameter', {'type': 2, 'name': 0})
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(8) # colon
      tree.add(t)
      subtree = self.parse_step_parameter_type()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_workflow_step_input(self):
    current = self.tokens.current()
    rule = self.table[19][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(37, self.nonterminals[37]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 14:
      tree.astTransform = AstTransformSubstitution(1)
      t = self.expect(14) # lparen
      tree.add(t)
      subtree = self.parse__gen2()
      tree.add( subtree )
      t = self.expect(17) # rparen
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_wdl(self):
    current = self.tokens.current()
    rule = self.table[20][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(38, self.nonterminals[38]))
    tree.list = False
    if current == None:
      return tree
    if rule == 34:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse__gen0()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_workflow_step_input_param(self):
    current = self.tokens.current()
    rule = self.table[21][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(39, self.nonterminals[39]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 4:
      tree.astTransform = AstTransformNodeCreator('String', {'val': 0})
      t = self.expect(1) # string_literal
      tree.add(t)
      return tree
    elif rule == 15:
      tree.astTransform = AstTransformNodeCreator('Variable', {'name': 0})
      t = self.expect(6) # identifier
      tree.add(t)
      return tree
    elif rule == 38:
      tree.astTransform = AstTransformNodeCreator('File', {'path': 2})
      t = self.expect(5) # file
      tree.add(t)
      t = self.expect(14) # lparen
      tree.add(t)
      t = self.expect(1) # string_literal
      tree.add(t)
      t = self.expect(17) # rparen
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_workflow_step_output_param(self):
    current = self.tokens.current()
    rule = self.table[22][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(40, self.nonterminals[40]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 26:
      tree.astTransform = AstTransformNodeCreator('Output', {'var': 0})
      t = self.expect(6) # identifier
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_workflow_step(self):
    current = self.tokens.current()
    rule = self.table[23][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(41, self.nonterminals[41]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 8:
      tree.astTransform = AstTransformNodeCreator('WorkflowStep', {'input': 5, 'step': 4, 'name': 1, 'output': 3})
      t = self.expect(11) # step
      tree.add(t)
      t = self.expect(6) # identifier
      tree.add(t)
      t = self.expect(8) # colon
      tree.add(t)
      subtree = self.parse_workflow_step_output()
      tree.add( subtree )
      t = self.expect(6) # identifier
      tree.add(t)
      subtree = self.parse_workflow_step_input()
      tree.add( subtree )
      t = self.expect(10) # semi
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse__gen1(self):
    current = self.tokens.current()
    rule = self.table[24][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(42, self.nonterminals[42]))
    tree.list = 'nlist'
    if current != None and (current.getId() in [9]):
      return tree
    if current == None:
      return tree
    if rule == 2:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_workflow_step()
      tree.add( subtree )
      subtree = self.parse__gen1()
      tree.add( subtree )
      return tree
    return tree
  def parse_step_action(self):
    current = self.tokens.current()
    rule = self.table[25][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(43, self.nonterminals[43]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 30:
      tree.astTransform = AstTransformSubstitution(2)
      t = self.expect(16) # action
      tree.add(t)
      t = self.expect(8) # colon
      tree.add(t)
      subtree = self.parse_step_action_sub()
      tree.add( subtree )
      t = self.expect(10) # semi
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_wdl_entity(self):
    current = self.tokens.current()
    rule = self.table[26][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(44, self.nonterminals[44]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 0:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_step()
      tree.add( subtree )
      return tree
    elif rule == 16:
      tree.astTransform = AstTransformSubstitution(0)
      subtree = self.parse_workflow()
      tree.add( subtree )
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
  def parse_step_output(self):
    current = self.tokens.current()
    rule = self.table[27][current.getId()] if current else -1
    tree = ParseTree( NonTerminal(45, self.nonterminals[45]))
    tree.list = False
    if current == None:
      raise SyntaxError('Error: unexpected end of file')
    if rule == 19:
      tree.astTransform = AstTransformNodeCreator('StepOutputParameters', {'parameters': 2})
      t = self.expect(7) # output
      tree.add(t)
      t = self.expect(8) # colon
      tree.add(t)
      subtree = self.parse__gen2()
      tree.add( subtree )
      t = self.expect(10) # semi
      tree.add(t)
      return tree
    raise SyntaxError('Error: Unexpected symbol (%s) when parsing %s' % (current, whoami()))
