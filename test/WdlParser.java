
import java.util.*;
import java.util.HashMap;
import java.util.LinkedHashMap;
class WdlParser implements Parser {
  private TokenStream tokens;
  private HashMap<String, ExpressionParser> expressionParsers;
  /* table[nonterminal][terminal] = rule */
  private static final int[][] table = {
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, -1, -1 },
    { -1, -1, 33, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, 36, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 23, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1 },
    { -1, -1, 26, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, 40, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, 34, 37, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, 43, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1 },
    { -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 29, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1 },
    { -1, -1, 3, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, 39, -1, -1, -1, -1, 16, -1 },
    { -1, -1, -1, -1, -1, -1, 25, -1, -1, 25, -1, -1, -1, -1, -1, 22, -1, -1 },
    { -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, 14, 14, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 35, -1, -1, 35, 20, 20, -1, -1, -1, -1, 20, -1 },
    { -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, 2, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, 30, -1 },
    { -1, -1, -1, 41, 13, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1 },
  };
  public enum TerminalId {
    TERMINAL_LBRACE(0, "lbrace"),
    TERMINAL_COLON(1, "colon"),
    TERMINAL_STEP(2, "step"),
    TERMINAL_RBRACE(3, "rbrace"),
    TERMINAL_ACTION(4, "action"),
    TERMINAL_WORKFLOW(5, "workflow"),
    TERMINAL_RPAREN(6, "rparen"),
    TERMINAL_LPAREN(7, "lparen"),
    TERMINAL_SCATTER_GATHER(8, "scatter_gather"),
    TERMINAL_SEMI(9, "semi"),
    TERMINAL_STRING_LITERAL(10, "string_literal"),
    TERMINAL_IDENTIFIER(11, "identifier"),
    TERMINAL_STRING(12, "string"),
    TERMINAL_OUTPUT(13, "output"),
    TERMINAL_COMMAND(14, "command"),
    TERMINAL_COMMA(15, "comma"),
    TERMINAL_FILE(16, "file"),
    TERMINAL_EQUALS(17, "equals");
    private final int id;
    private final String string;
    TerminalId(int id, String string) {
      this.id = id;
      this.string = string;
    }
    public int id() {return id;}
    public String string() {return string;}
  }
  private class WdlTerminalMap implements TerminalMap {
    private Map<Integer, String> id_to_str;
    private Map<String, Integer> str_to_id;
    WdlTerminalMap(TerminalId[] terminals) {
      id_to_str = new HashMap<Integer, String>();
      str_to_id = new HashMap<String, Integer>();
      for( TerminalId terminal : terminals ) {
        Integer id = new Integer(terminal.id());
        String str = terminal.string();
        id_to_str.put(id, str);
        str_to_id.put(str, id);
      }
    }
    public int get(String string) { return this.str_to_id.get(string); }
    public String get(int id) { return this.id_to_str.get(id); }
    public boolean isValid(String string) { return this.str_to_id.containsKey(string); }
    public boolean isValid(int id) { return this.id_to_str.containsKey(id); }
  }
  WdlParser() {
    this.expressionParsers = new HashMap<String, ExpressionParser>();
  }
  public TerminalMap getTerminalMap() {
    return new WdlTerminalMap(TerminalId.values());
  }
  public ParseTree parse(TokenStream tokens) throws SyntaxError {
    this.tokens = tokens;
    ParseTree tree = this.parse_wdl();
    if (this.tokens.current() != null) {
      throw new SyntaxError("Finished parsing without consuming all tokens.");
    }
    return tree;
  }
  private boolean isTerminal(TerminalId terminal) {
    return (0 <= terminal.id() && terminal.id() <= 17);
  }
  private boolean isNonTerminal(TerminalId terminal) {
    return (18 <= terminal.id() && terminal.id() <= 45);
  }
  private boolean isTerminal(int terminal) {
    return (0 <= terminal && terminal <= 17);
  }
  private boolean isNonTerminal(int terminal) {
    return (18 <= terminal && terminal <= 45);
  }
  private ParseTree parse_step_action_command() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[0][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(18, "step_action_command"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 27) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("cmd", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("CommandAction", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMAND.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_STRING_LITERAL.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_workflow_body() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[1][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(19, "workflow_body"));
    tree.setList(null);
    if (current == null) {
      return tree;
    }
    if (rule == 33) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse__gen1();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_wdl_entity() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[2][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(20, "wdl_entity"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 12) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_workflow();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 36) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_workflow_step_output() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[3][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(21, "workflow_step_output"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 11) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 23) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      subtree = this.parse__gen4();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_EQUALS.id());
      tree.add(next);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_wdl() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[4][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(22, "wdl"));
    tree.setList(null);
    if (current == null) {
      return tree;
    }
    if (rule == 26) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse__gen0();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_action() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[5][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(23, "step_action"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 40) {
      tree.setAstTransformation(new AstTransformSubstitution(2));
      next = this.tokens.expect(TerminalId.TERMINAL_ACTION.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      subtree = this.parse_step_action_sub();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen1() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[6][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(24, "_gen1"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 3) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 34) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_workflow_step();
      tree.add( subtree);
      subtree = this.parse__gen1();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_workflow_step_input() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[7][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(25, "workflow_step_input"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 8) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      subtree = this.parse__gen2();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_action_scatter_gather() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[8][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(26, "step_action_scatter_gather"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 4) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("gather", 6);
      parameters.put("scatter", 4);
      parameters.put("prepare", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("ScatterGatherAction", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_SCATTER_GATHER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_workflow_step() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[9][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(27, "workflow_step"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 43) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("input", 5);
      parameters.put("step", 4);
      parameters.put("name", 1);
      parameters.put("output", 3);
      tree.setAstTransformation(new AstTransformNodeCreator("WorkflowStep", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_STEP.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      subtree = this.parse_workflow_step_output();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      subtree = this.parse_workflow_step_input();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_workflow() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[10][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(28, "workflow"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 31) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("body", 3);
      parameters.put("name", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Workflow", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_WORKFLOW.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id());
      tree.add(next);
      subtree = this.parse_workflow_body();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RBRACE.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_workflow_step_output_param() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[11][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(29, "workflow_step_output_param"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 18) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("var", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("Output", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_output() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[12][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(30, "step_output"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 6) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("parameters", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("StepOutputParameters", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_OUTPUT.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      subtree = this.parse__gen2();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_body_spec() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[13][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(31, "step_body_spec"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 15) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_output();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 19) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_action();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen5() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[14][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(32, "_gen5"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 17) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_workflow_step_output_param();
      tree.add( subtree);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen0() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[15][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(33, "_gen0"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == -1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 3) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_wdl_entity();
      tree.add( subtree);
      subtree = this.parse__gen0();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_workflow_step_input_param() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[16][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(34, "workflow_step_input_param"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 16) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("path", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("File", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_FILE.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_STRING_LITERAL.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 32) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("val", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("String", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_STRING_LITERAL.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 39) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("name", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("Variable", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen3() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[17][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(35, "_gen3"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 9 || current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 22) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_workflow_step_input_param();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_step() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[18][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(36, "step"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 21) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("body", 6);
      parameters.put("name", 1);
      parameters.put("parameters", 3);
      tree.setAstTransformation(new AstTransformNodeCreator("Step", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_STEP.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id());
      tree.add(next);
      subtree = this.parse__gen6();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id());
      tree.add(next);
      subtree = this.parse_step_body();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RBRACE.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_body() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[19][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(37, "step_body"));
    tree.setList(null);
    if (current == null) {
      return tree;
    }
    if (rule == 14) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse__gen8();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen2() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[20][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(38, "_gen2"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 9 || current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 20) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_workflow_step_input_param();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen4() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[21][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(39, "_gen4"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 42) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_workflow_step_output_param();
      tree.add( subtree);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_step_action_sub() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[22][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(40, "step_action_sub"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 2) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_action_command();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 28) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_action_scatter_gather();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_step_parameter_type() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[23][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(41, "step_parameter_type"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 24) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_STRING.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 30) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_FILE.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen8() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[24][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(42, "_gen8"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 3) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 13) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_body_spec();
      tree.add( subtree);
      subtree = this.parse__gen8();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen6() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[25][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(43, "_gen6"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 0) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_parameter();
      tree.add( subtree);
      subtree = this.parse__gen7();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen7() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[26][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(44, "_gen7"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 5) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_step_parameter();
      tree.add( subtree);
      subtree = this.parse__gen7();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_step_parameter() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[27][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(45, "step_parameter"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 11) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("type", 2);
      parameters.put("name", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("StepInputParameter", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      subtree = this.parse_step_parameter_type();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
}
