import java.util.Formatter;
import java.util.Locale;
class Terminal implements AstNode, ParseTreeNode
{
  private int id;
  private String terminal_str;
  private String source_string;
  private String resource;
  private int line;
  private int col;
  Terminal(int id, String terminal_str, String source_string, String resource, int line, int col) {
    this.id = id;
    this.terminal_str = terminal_str;
    this.source_string = source_string;
    this.resource = resource;
    this.line = line;
    this.col = col;
  }
  public int getId() {
    return this.id;
  }
  public String getTerminalStr() {
    return this.terminal_str;
  }
  public String getSourceString() {
    return this.source_string;
  }
  public String getResource() {
    return this.resource;
  }
  public int getLine() {
    return this.line;
  }
  public int getColumn() {
    return this.col;
  }
  public String toString() {
    StringBuilder sb = new StringBuilder();
    Formatter formatter = new Formatter(sb, Locale.US);
    formatter.format("{\"terminal\": \"%s\", \"line\": %d, \"col\": %d, \"resource\": \"%s\", \"source_string\": \"%s\"}", this.getTerminalStr(), this.getLine(), this.getColumn(), this.getResource(), Utility.base64_encode(this.getSourceString().getBytes()));
    return formatter.toString();
  }
  public String toPrettyString() {
    return toPrettyString(0);
  }
  public String toPrettyString(int indent) {
    String spaces = Utility.getIndentString(indent);
    return spaces + this.getTerminalStr();
  }
  public AstNode toAst() { return this; }
}
