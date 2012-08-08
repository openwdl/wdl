
import java.util.*;
import java.util.HashMap;
import java.util.LinkedHashMap;
class DotParser implements Parser {
  private TokenStream tokens;
  private HashMap<String, ExpressionParser> expressionParsers;
  /* table[nonterminal][terminal] = rule */
  private static final int[][] table = {
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 48, 35, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, 17, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 37, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1 },
    { -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, 41, 41, -1, -1, -1, -1, -1, -1 },
    { 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, -1 },
    { 44, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, 6, -1, 44, -1 },
    { -1, -1, 36, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1, 27, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, -1, 39, -1, -1, -1, -1, 50 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 43, -1, -1, -1, -1, -1, -1, -1, -1 },
    { 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, 5, -1, -1, -1 },
    { -1, 31, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, 30, 30, -1, -1, -1, -1, -1, -1 },
    { -1, 33, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, 45, 16, 45, -1, 16, 40, -1, -1, -1, -1, -1, -1, 16, -1, 21, -1, 32, -1, -1 },
    { 42, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, 42, -1, 42, -1 },
    { -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, 51, -1, -1, 51, -1, -1, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, -1, -1 },
    { -1, 38, -1, 38, -1, -1, -1, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, 28, 28, 28, -1, 28, 28, -1, -1, -1, 47, -1, -1, 28, -1, 28, -1, 28, -1, -1 },
    { 49, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, 49, -1, -1, -1, -1, 49, -1, 49, -1 },
    { -1, 24, -1, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25 },
    { -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 8, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
  };
  public enum TerminalId {
    TERMINAL_DASHDASH(0, "dashdash"),
    TERMINAL_LBRACE(1, "lbrace"),
    TERMINAL_NODE(2, "node"),
    TERMINAL_SUBGRAPH(3, "subgraph"),
    TERMINAL_COLON(4, "colon"),
    TERMINAL_EDGE(5, "edge"),
    TERMINAL_NODE_STMT_HINT(6, "node_stmt_hint"),
    TERMINAL_STRICT(7, "strict"),
    TERMINAL_RSQUARE(8, "rsquare"),
    TERMINAL_IDENTIFIER(9, "identifier"),
    TERMINAL_RBRACE(10, "rbrace"),
    TERMINAL_LSQUARE(11, "lsquare"),
    TERMINAL_DIGRAPH(12, "digraph"),
    TERMINAL_GRAPH(13, "graph"),
    TERMINAL_COMMA(14, "comma"),
    TERMINAL_EDGE_STMT_HINT(15, "edge_stmt_hint"),
    TERMINAL_SEMI(16, "semi"),
    TERMINAL_VALUE_ASSIGN_HINT(17, "value_assign_hint"),
    TERMINAL_ARROW(18, "arrow"),
    TERMINAL_ASSIGN(19, "assign");
    private final int id;
    private final String string;
    TerminalId(int id, String string) {
      this.id = id;
      this.string = string;
    }
    public int id() {return id;}
    public String string() {return string;}
  }
  private class DotTerminalMap implements TerminalMap {
    private Map<Integer, String> id_to_str;
    private Map<String, Integer> str_to_id;
    DotTerminalMap(TerminalId[] terminals) {
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
  DotParser() {
    this.expressionParsers = new HashMap<String, ExpressionParser>();
  }
  public TerminalMap getTerminalMap() {
    return new DotTerminalMap(TerminalId.values());
  }
  public ParseTree parse(TokenStream tokens) throws SyntaxError {
    this.tokens = tokens;
    ParseTree tree = this.parse_graph();
    if (this.tokens.current() != null) {
      throw new SyntaxError("Finished parsing without consuming all tokens.");
    }
    return tree;
  }
  private boolean isTerminal(TerminalId terminal) {
    return (0 <= terminal.id() && terminal.id() <= 19);
  }
  private boolean isNonTerminal(TerminalId terminal) {
    return (20 <= terminal.id() && terminal.id() <= 50);
  }
  private boolean isTerminal(int terminal) {
    return (0 <= terminal && terminal <= 19);
  }
  private boolean isNonTerminal(int terminal) {
    return (20 <= terminal && terminal <= 50);
  }
  private ParseTree parse_graph_type() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[0][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(20, "graph_type"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_graph_type(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 35) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_GRAPH.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 48) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_DIGRAPH.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_port_sub() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[1][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(21, "port_sub"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_port_sub(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 12) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("name", 0);
      parameters.put("compass_point", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Port", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      subtree = this.parse__gen10();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 17) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("name", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Port", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_attr_values() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[2][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(22, "attr_values"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_attr_values(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 22) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("value", 1);
      parameters.put("key", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("AttributeValue", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      subtree = this.parse__gen6();
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
    int rule = current != null ? this.table[3][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(23, "_gen5"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen5(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 8) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 20) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_COMMA.id());
      tree.add(next);
      tree.setListSeparator(next);
      subtree = this.parse_attr_values();
      tree.add( subtree);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_edge_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[4][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(24, "edge_stmt"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_edge_stmt(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 9) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("node", 1);
      parameters.put("attributes", 3);
      parameters.put("edges", 2);
      tree.setAstTransformation(new AstTransformNodeCreator("Edg", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_EDGE_STMT_HINT.id());
      tree.add(next);
      subtree = this.parse_node_or_subgraph();
      tree.add( subtree);
      subtree = this.parse__gen7();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_port_compass_pt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[5][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(25, "port_compass_pt"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_port_compass_pt(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 3) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_graph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[6][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(26, "graph"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_graph(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 41) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("strict", 0);
      parameters.put("type", 1);
      parameters.put("name", 2);
      parameters.put("statements", 4);
      tree.setAstTransformation(new AstTransformNodeCreator("Graph", parameters));
      subtree = this.parse__gen0();
      tree.add( subtree);
      subtree = this.parse_graph_type();
      tree.add( subtree);
      subtree = this.parse__gen1();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id());
      tree.add(next);
      subtree = this.parse__gen2();
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
  private ParseTree parse_edge_rhs() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[7][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(27, "edge_rhs"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_edge_rhs(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 14) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("node", 1);
      parameters.put("edge_type", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("EdgeDeclaration", parameters));
      subtree = this.parse_edge_op();
      tree.add( subtree);
      subtree = this.parse_node_or_subgraph();
      tree.add( subtree);
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
    int rule = current != null ? this.table[8][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(28, "_gen8"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen8(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("mlist");
    if ( current != null ) {
      if (current.getId() == 11 || current.getId() == 16) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 44) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_edge_rhs();
      tree.add( subtree);
      subtree = this.parse__gen8();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_attr_type() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[9][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(29, "attr_type"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_attr_type(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 10) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_EDGE.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 27) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_GRAPH.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 36) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_NODE.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_node_id() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[10][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(30, "node_id"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_node_id(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 34) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("name", 0);
      parameters.put("port", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("NodeId", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      subtree = this.parse__gen9();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen6() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[11][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(31, "_gen6"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen6(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 14 || current.getId() == 8) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 50) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_value_assign();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_attr() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[12][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(32, "attr"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_attr(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 43) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_LSQUARE.id());
      tree.add(next);
      subtree = this.parse__gen4();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_RSQUARE.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen7() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[13][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(33, "_gen7"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen7(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("mlist");
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 1) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_edge_rhs();
      tree.add( subtree);
      subtree = this.parse__gen8();
      tree.add( subtree);
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
    int rule = current != null ? this.table[14][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(34, "_gen3"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen3(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 16) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 15) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen1() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[15][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(35, "_gen1"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen1(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 11) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_edge_op() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[16][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(36, "edge_op"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_edge_op(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 2) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_ARROW.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 26) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_DASHDASH.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen0() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[17][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(37, "_gen0"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen0(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 13 || current.getId() == 12) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 18) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_STRICT.id());
      tree.add(next);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_subgraph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[18][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(38, "subgraph"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_subgraph(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 33) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("statements", 2);
      parameters.put("name", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("SubGraph", parameters));
      subtree = this.parse__gen11();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_LBRACE.id());
      tree.add(next);
      subtree = this.parse__gen2();
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
  private ParseTree parse_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[19][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(39, "stmt"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_stmt(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 16) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 21) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_edge_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 32) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("value", 3);
      parameters.put("key", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Assign", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_VALUE_ASSIGN_HINT.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_ASSIGN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 40) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_node_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 45) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_subgraph();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen9() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[20][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(40, "_gen9"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen9(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 0 || current.getId() == 16 || current.getId() == 18 || current.getId() == 11) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 7) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_port();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_subgraph_name() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[21][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(41, "subgraph_name"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_subgraph_name(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 4) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_SUBGRAPH.id());
      tree.add(next);
      subtree = this.parse__gen1();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_attr_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[22][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(42, "attr_stmt"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_attr_stmt(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 51) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("values", 1);
      parameters.put("type", 0);
      tree.setAstTransformation(new AstTransformNodeCreator("Attribute", parameters));
      subtree = this.parse_attr_type();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_node_or_subgraph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[23][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(43, "node_or_subgraph"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_node_or_subgraph(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 23) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_node_id();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 38) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_subgraph();
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
    int rule = current != null ? this.table[24][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(44, "_gen2"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen2(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("tlist");
    if ( current != null ) {
      if (current.getId() == 10) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 28) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_stmt();
      tree.add( subtree);
      next = this.tokens.expect(TerminalId.TERMINAL_SEMI.id());
      tree.add(next);
      subtree = this.parse__gen2();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen10() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[25][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(45, "_gen10"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen10(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 0 || current.getId() == 16 || current.getId() == 18 || current.getId() == 11) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 13) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_port_compass_pt();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen11() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[26][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(46, "_gen11"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen11(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 29) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_subgraph_name();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_attr_value_assign() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[27][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(47, "attr_value_assign"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_attr_value_assign(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 25) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_ASSIGN.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_port() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[28][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(48, "port"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_port(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 19) {
      tree.setAstTransformation(new AstTransformSubstitution(1));
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      subtree = this.parse_port_sub();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_node_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[29][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(49, "node_stmt"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse_node_stmt(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 46) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("attributes", 2);
      parameters.put("id", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Node", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_NODE_STMT_HINT.id());
      tree.add(next);
      subtree = this.parse_node_id();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen4() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[30][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(50, "_gen4"));
    StackTraceElement[] trace = Thread.currentThread().getStackTrace();
    System.out.println(Utility.getIndentString(trace.length-4) + "parse__gen4(): rule="+rule+", current="+current.getTerminalStr() + "["+current.getId()+"] ("+current.getLine() + ", " + current.getColumn() + ")");
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 8) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 0) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_values();
      tree.add( subtree);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
}
