
import java.util.*;
import java.util.HashMap;
import java.util.LinkedHashMap;
class WdlParser implements Parser {
  private TokenStream tokens;
  private HashMap<String, ExpressionParser> expressionParsers;
  private SyntaxErrorFormatter syntaxErrorFormatter;
  private Map<String, TerminalId[]> first;
  private Map<String, TerminalId[]> follow;
  /* table[nonterminal][terminal] = rule */
  private static final int[][] table = {
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1, -1 },
    { 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, -1, 28, -1, -1, -1, -1 },
    { 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 44, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 19, -1, 19, -1, -1, -1, -1, 40, -1, -1, -1, -1, -1, -1, -1 },
    { -1, 2, -1, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, 26, -1, -1 },
    { 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 43, -1, -1, -1, -1, -1 },
    { -1, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 23, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, 4 },
    { -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, 0, -1, 0, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 45, -1, 25, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, 8, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
  };
  public enum TerminalId {
    TERMINAL_STEP(0, "step"),
    TERMINAL_STRING(1, "string"),
    TERMINAL_LPAREN(2, "lparen"),
    TERMINAL_LSQUARE(3, "lsquare"),
    TERMINAL_IN(4, "in"),
    TERMINAL_RPAREN(5, "rparen"),
    TERMINAL_LBRACE(6, "lbrace"),
    TERMINAL_INPUT(7, "input"),
    TERMINAL_NUMBER(8, "number"),
    TERMINAL_OUTPUT(9, "output"),
    TERMINAL_FILE(10, "file"),
    TERMINAL_AS(11, "as"),
    TERMINAL_DOT(12, "dot"),
    TERMINAL_SEMI(13, "semi"),
    TERMINAL_RBRACE(14, "rbrace"),
    TERMINAL_COMMA(15, "comma"),
    TERMINAL_COMPOSITE_TASK(16, "composite_task"),
    TERMINAL_FOR(17, "for"),
    TERMINAL_ASSIGN(18, "assign"),
    TERMINAL_IDENTIFIER(19, "identifier"),
    TERMINAL_COLON(20, "colon"),
    TERMINAL_RSQUARE(21, "rsquare");
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
  WdlParser(SyntaxErrorFormatter syntaxErrorFormatter) {
    this.syntaxErrorFormatter = syntaxErrorFormatter; 
    this.expressionParsers = new HashMap<String, ExpressionParser>();
    this.first = new HashMap<String, TerminalId[]>();
    this.follow = new HashMap<String, TerminalId[]>();
    ArrayList<TerminalId> list;
    this.first.put("step_input", new TerminalId[] {  });
    this.first.put("_gen1", new TerminalId[] {  });
    this.first.put("composite_task_entity", new TerminalId[] {  });
    this.first.put("step_output_list", new TerminalId[] {  });
    this.first.put("step_name", new TerminalId[] {  });
    this.first.put("task_attr", new TerminalId[] {  });
    this.first.put("_gen4", new TerminalId[] {  });
    this.first.put("task_attr_value", new TerminalId[] {  });
    this.first.put("_gen3", new TerminalId[] {  });
    this.first.put("_gen7", new TerminalId[] {  });
    this.first.put("_gen2", new TerminalId[] {  });
    this.first.put("wdl", new TerminalId[] {  });
    this.first.put("task_attrs", new TerminalId[] {  });
    this.first.put("variable", new TerminalId[] {  });
    this.first.put("step_output", new TerminalId[] {  });
    this.first.put("step_attr", new TerminalId[] {  });
    this.first.put("_gen9", new TerminalId[] {  });
    this.first.put("_gen6", new TerminalId[] {  });
    this.first.put("_gen5", new TerminalId[] {  });
    this.first.put("step", new TerminalId[] {  });
    this.first.put("wdl_entity", new TerminalId[] {  });
    this.first.put("composite_task", new TerminalId[] {  });
    this.first.put("_gen11", new TerminalId[] {  });
    this.first.put("_gen0", new TerminalId[] {  });
    this.first.put("step_input_list", new TerminalId[] {  });
    this.first.put("_gen8", new TerminalId[] {  });
    this.first.put("task_identifier", new TerminalId[] {  });
    this.first.put("for_loop", new TerminalId[] {  });
    this.first.put("_gen10", new TerminalId[] {  });
    this.first.put("variable_member", new TerminalId[] {  });
    this.follow.put("step_input", new TerminalId[] {  });
    this.follow.put("_gen1", new TerminalId[] {  });
    this.follow.put("composite_task_entity", new TerminalId[] {  });
    this.follow.put("step_output_list", new TerminalId[] {  });
    this.follow.put("step_name", new TerminalId[] {  });
    this.follow.put("task_attr", new TerminalId[] {  });
    this.follow.put("_gen4", new TerminalId[] {  });
    this.follow.put("task_attr_value", new TerminalId[] {  });
    this.follow.put("_gen3", new TerminalId[] {  });
    this.follow.put("_gen7", new TerminalId[] {  });
    this.follow.put("_gen2", new TerminalId[] {  });
    this.follow.put("wdl", new TerminalId[] {  });
    this.follow.put("task_attrs", new TerminalId[] {  });
    this.follow.put("variable", new TerminalId[] {  });
    this.follow.put("step_output", new TerminalId[] {  });
    this.follow.put("step_attr", new TerminalId[] {  });
    this.follow.put("_gen9", new TerminalId[] {  });
    this.follow.put("_gen6", new TerminalId[] {  });
    this.follow.put("_gen5", new TerminalId[] {  });
    this.follow.put("step", new TerminalId[] {  });
    this.follow.put("wdl_entity", new TerminalId[] {  });
    this.follow.put("composite_task", new TerminalId[] {  });
    this.follow.put("_gen11", new TerminalId[] {  });
    this.follow.put("_gen0", new TerminalId[] {  });
    this.follow.put("step_input_list", new TerminalId[] {  });
    this.follow.put("_gen8", new TerminalId[] {  });
    this.follow.put("task_identifier", new TerminalId[] {  });
    this.follow.put("for_loop", new TerminalId[] {  });
    this.follow.put("_gen10", new TerminalId[] {  });
    this.follow.put("variable_member", new TerminalId[] {  });
  }
  public TerminalMap getTerminalMap() {
    return new WdlTerminalMap(TerminalId.values());
  }
  public ParseTree parse(TokenStream tokens) throws SyntaxError {
    this.tokens = tokens;
    ParseTree tree = this.parse_wdl();
    if (this.tokens.current() != null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.excess_tokens(stack[1].getMethodName(), this.tokens.current()));
    }
    return tree;
  }
  private boolean isTerminal(TerminalId terminal) {
    return (0 <= terminal.id() && terminal.id() <= 21);
  }
  private boolean isNonTerminal(TerminalId terminal) {
    return (22 <= terminal.id() && terminal.id() <= 51);
  }
  private boolean isTerminal(int terminal) {
    return (0 <= terminal && terminal <= 21);
  }
  private boolean isNonTerminal(int terminal) {
    return (22 <= terminal && terminal <= 51);
  }
  private ParseTree parse_step_input() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[0][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(22, "step_input"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 29) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("parameter", 0);
      parameters.put("value", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("StepInput", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_ASSIGN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse_variable();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_input", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen1() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[1][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(23, "_gen1"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 14) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 28) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_composite_task_entity();
      tree.add( subtree);
      subtree = this.parse__gen1();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_composite_task_entity() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[2][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(24, "composite_task_entity"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 9) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 34) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_for_loop();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("composite_task_entity", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_step_output_list() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[3][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(25, "step_output_list"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 27) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("outputs", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("StepOutputList", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_OUTPUT.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen9();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_output_list", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_step_name() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[4][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(26, "step_name"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 18) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_AS.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_name", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_task_attr() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[5][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(27, "task_attr"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 44) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("value", 2);
      parameters.put("key", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("TaskAttribute", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_ASSIGN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse_task_attr_value();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("task_attr", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen4() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[6][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(28, "_gen4"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 14) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 19) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_attr();
      tree.add( subtree);
      subtree = this.parse__gen4();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_task_attr_value() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[7][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(29, "task_attr_value"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 2) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_STRING.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    else if (rule == 37) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    else if (rule == 39) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_NUMBER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("task_attr_value", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen3() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[8][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(30, "_gen3"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 6) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 6) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_name();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen7() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[9][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(31, "_gen7"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 13) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 26) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_input();
      tree.add( subtree);
      subtree = this.parse__gen8();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen2() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[10][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(32, "_gen2"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 14) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 12) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step();
      tree.add( subtree);
      subtree = this.parse__gen2();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_wdl() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[11][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(33, "wdl"));
    tree.setList(null);
    if (current == null) {
      return tree;
    }
    if (rule == 43) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse__gen0();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("wdl", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_task_attrs() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[12][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(34, "task_attrs"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 36) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_LSQUARE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen6();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RSQUARE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("task_attrs", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_variable() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[13][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(35, "variable"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 13) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("member", 1);
      parameters.put("name", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("Variable", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen11();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("variable", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_step_output() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[14][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(36, "step_output"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 41) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("as", 5);
      parameters.put("file", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("StepFileOutput", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_FILE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_STRING.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_AS.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse_variable();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_output", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_step_attr() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[15][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(37, "step_attr"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 23) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_input_list();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 31) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_output_list();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_attr", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen9() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[16][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(38, "_gen9"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 13) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 11) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_step_output();
      tree.add( subtree);
      subtree = this.parse__gen10();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen6() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[17][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(39, "_gen6"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 21) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 1) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_task_attr();
      tree.add( subtree);
      subtree = this.parse__gen6();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen5() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[18][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(40, "_gen5"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 11) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 32) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_task_attrs();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_step() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[19][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(41, "step"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 22) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("body", 4);
      parameters.put("task", 1);
      parameters.put("name", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("Step", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_STEP.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse_task_identifier();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen4();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_wdl_entity() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[20][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(42, "wdl_entity"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 3) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_composite_task();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("wdl_entity", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_composite_task() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[21][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(43, "composite_task"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 17) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("body", 3);
      parameters.put("name", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("CompositeTask", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_COMPOSITE_TASK.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen1();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("composite_task", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen11() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[22][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(44, "_gen11"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 15 || current.getId() == 13) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 42) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_variable_member();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen0() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[23][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(45, "_gen0"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == -1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 24) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_wdl_entity();
      tree.add( subtree);
      subtree = this.parse__gen0();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_step_input_list() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[24][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(46, "step_input_list"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 10) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("inputs", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("StepInputList", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_INPUT.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen7();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("step_input_list", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen8() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[25][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(47, "_gen8"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 13) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 25) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id(), this.syntaxErrorFormatter);
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_step_input();
      tree.add( subtree);
      subtree = this.parse__gen8();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_task_identifier() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[26][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(48, "task_identifier"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 7) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("attributes", 1);
      parameters.put("name", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("Task", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("task_identifier", current, new ArrayList<Integer>()));
  }
  private ParseTree parse_for_loop() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[27][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(49, "for_loop"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 14) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("body", 7);
      parameters.put("item", 2);
      parameters.put("collection", 4);
      tree.setAstTransformation(new AstTransformNodeCreator("ForLoop", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_FOR.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LPAREN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_RPAREN.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      subtree = this.parse__gen2();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RBRACE.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("for_loop", current, new ArrayList<Integer>()));
  }
  private ParseTree parse__gen10() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[28][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(50, "_gen10"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 13) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 8) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id(), this.syntaxErrorFormatter);
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_step_output();
      tree.add( subtree);
      subtree = this.parse__gen10();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_variable_member() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[29][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(51, "variable_member"));
    tree.setList(null);
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(this.syntaxErrorFormatter.unexpected_eof(stack[1].getMethodName(), null));
    }
    if (rule == 33) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_DOT.id(), this.syntaxErrorFormatter);
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id(), this.syntaxErrorFormatter);
      tree.add(next);
      return tree;
    }
    throw new SyntaxError(this.syntaxErrorFormatter.unexpected_symbol("variable_member", current, new ArrayList<Integer>()));
  }
}
