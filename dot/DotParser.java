
import java.util.*;
import java.util.HashMap;
import java.util.LinkedHashMap;
class DotParser implements Parser {
  private TokenStream tokens;
  private HashMap<String, ExpressionParser> expressionParsers;
  /* table[nonterminal][terminal] = rule */
  private static final int[][] table = {
    { 30, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27 },
    { -1, 51, -1, -1, 44, 51, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, 39, -1, -1, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { 24, -1, -1, -1, -1, -1, -1, -1, 10, 24, -1, 43, -1, 26, 10, -1, 24, 9, -1, -1 },
    { -1, -1, 40, -1, -1, -1, 40, 40, -1, -1, -1, -1, -1, -1, -1, 49, -1, -1, 40, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1 },
    { -1, -1, 33, -1, -1, -1, 37, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1 },
    { 4, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1 },
    { 35, -1, -1, -1, -1, -1, -1, -1, 35, 35, -1, 35, 11, 35, 35, -1, 35, 35, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, -1, -1 },
    { 28, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, 28, -1, -1, -1 },
    { 22, -1, -1, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1 },
    { 23, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, -1, 50, -1, -1, -1, -1, -1 },
    { -1, -1, 12, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1 },
    { -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 47, -1, 42, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 0, -1, -1, -1, 5, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, -1 },
    { -1, -1, 18, -1, -1, -1, 18, 18, -1, -1, -1, -1, -1, -1, -1, 46, -1, -1, 18, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 45, -1, -1, -1, -1, 17, -1, -1, -1, -1 },
    { -1, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
    { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
  };
  public enum TerminalId {
    TERMINAL_GRAPH(0, "graph"),
    TERMINAL_RSQUARE(1, "rsquare"),
    TERMINAL_SEMI(2, "semi"),
    TERMINAL_DIGRAPH(3, "digraph"),
    TERMINAL_ASSIGN(4, "assign"),
    TERMINAL_COMMA(5, "comma"),
    TERMINAL_ARROW(6, "arrow"),
    TERMINAL_LSQUARE(7, "lsquare"),
    TERMINAL_LBRACE(8, "lbrace"),
    TERMINAL_EDGE(9, "edge"),
    TERMINAL_IDENTIFIER(10, "identifier"),
    TERMINAL_VALUE_ASSIGN_HINT(11, "value_assign_hint"),
    TERMINAL_RBRACE(12, "rbrace"),
    TERMINAL_EDGE_STMT_HINT(13, "edge_stmt_hint"),
    TERMINAL_SUBGRAPH(14, "subgraph"),
    TERMINAL_COLON(15, "colon"),
    TERMINAL_NODE(16, "node"),
    TERMINAL_NODE_STMT_HINT(17, "node_stmt_hint"),
    TERMINAL_DASHDASH(18, "dashdash"),
    TERMINAL_STRICT(19, "strict");
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
  private ParseTree parse__gen0() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[0][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(20, "_gen0"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 0 || current.getId() == 3) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 27) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_STRICT.id());
      tree.add(next);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen6() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[1][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(21, "_gen6"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 5 || current.getId() == 1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 44) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_value_assign();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen5() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[2][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(22, "_gen5"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 48) {
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
  private ParseTree parse_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[3][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(23, "stmt"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 9) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_node_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 10) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_subgraph();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 24) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 26) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_edge_stmt();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 43) {
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
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse__gen10() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[4][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(24, "_gen10"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 7 || current.getId() == 18 || current.getId() == 6 || current.getId() == 2) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 49) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_port_compass_pt();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_port_compass_pt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[5][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(25, "port_compass_pt"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 7) {
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
  private ParseTree parse__gen8() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[6][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(26, "_gen8"));
    tree.setList("mlist");
    if ( current != null ) {
      if (current.getId() == 7 || current.getId() == 2) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 37) {
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
    int rule = current != null ? this.table[7][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(27, "attr_type"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 1) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_EDGE.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 4) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_GRAPH.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 20) {
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
  private ParseTree parse__gen2() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[8][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(28, "_gen2"));
    tree.setList("tlist");
    if ( current != null ) {
      if (current.getId() == 12) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 35) {
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
  private ParseTree parse_subgraph_name() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[9][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(29, "subgraph_name"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 2) {
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
  private ParseTree parse_node_id() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[10][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(30, "node_id"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 16) {
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
  private ParseTree parse__gen4() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[11][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(31, "_gen4"));
    tree.setList("slist");
    if ( current != null ) {
      if (current.getId() == 1) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 25) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr_values();
      tree.add( subtree);
      subtree = this.parse__gen5();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_node_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[12][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(32, "node_stmt"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 32) {
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
  private ParseTree parse_attr_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[13][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(33, "attr_stmt"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 28) {
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
  private ParseTree parse_graph_type() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[14][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(34, "graph_type"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 22) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_GRAPH.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 36) {
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
  private ParseTree parse_subgraph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[15][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(35, "subgraph"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 13) {
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
  private ParseTree parse_graph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[16][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(36, "graph"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 23) {
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
  private ParseTree parse__gen11() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[17][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(37, "_gen11"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 8) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 50) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_subgraph_name();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse__gen3() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[18][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(38, "_gen3"));
    tree.setList("nlist");
    if ( current != null ) {
      if (current.getId() == 2) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 6) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_attr();
      tree.add( subtree);
      subtree = this.parse__gen3();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_edge_op() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[19][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(39, "edge_op"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 8) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_ARROW.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 29) {
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
  private ParseTree parse_edge_stmt() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[20][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(40, "edge_stmt"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 38) {
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
  private ParseTree parse__gen7() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[21][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(41, "_gen7"));
    tree.setList("mlist");
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 31) {
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
  private ParseTree parse_attr() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[22][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(42, "attr"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 3) {
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
  private ParseTree parse__gen1() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[23][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(43, "_gen1"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 8) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 42) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_node_or_subgraph() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[24][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(44, "node_or_subgraph"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 0) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_node_id();
      tree.add( subtree);
      return tree;
    }
    else if (rule == 5) {
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
  private ParseTree parse_port() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[25][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(45, "port"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 15) {
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
  private ParseTree parse_edge_rhs() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[26][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(46, "edge_rhs"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 19) {
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
  private ParseTree parse__gen9() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[27][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(47, "_gen9"));
    tree.setList(null);
    if ( current != null ) {
      if (current.getId() == 7 || current.getId() == 18 || current.getId() == 6 || current.getId() == 2) {
        return tree;
      }
    }
    if (current == null) {
      return tree;
    }
    if (rule == 46) {
      tree.setAstTransformation(new AstTransformSubstitution(0));
      subtree = this.parse_port();
      tree.add( subtree);
      return tree;
    }
    return tree;
  }
  private ParseTree parse_port_sub() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[28][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(48, "port_sub"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 17) {
      LinkedHashMap<String, Integer> parameters = new LinkedHashMap<String, Integer>();
      parameters.put("name", 1);
      tree.setAstTransformation(new AstTransformNodeCreator("Port", parameters));
      next = this.tokens.expect(TerminalId.TERMINAL_COLON.id());
      tree.add(next);
      next = this.tokens.expect(TerminalId.TERMINAL_IDENTIFIER.id());
      tree.add(next);
      return tree;
    }
    else if (rule == 45) {
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
    Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    formatter.format("Error: Unexpected symbol (%s) when parsing %s", current, stack[0].getMethodName());
    throw new SyntaxError(formatter.toString());
  }
  private ParseTree parse_attr_value_assign() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[29][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(49, "attr_value_assign"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 14) {
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
  private ParseTree parse_attr_values() throws SyntaxError {
    Terminal current = this.tokens.current();
    Terminal next;
    ParseTree subtree;
    int rule = current != null ? this.table[30][current.getId()] : -1;
    ParseTree tree = new ParseTree( new NonTerminal(50, "attr_values"));
    tree.setList(null);
    if (current == null) {
      throw new SyntaxError("Error: unexpected end of file");
    }
    if (rule == 21) {
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
}
