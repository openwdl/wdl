import java.util.ArrayList;
import java.util.List;

class WdlSyntaxErrorFormatter implements SyntaxErrorFormatter {
  private TerminalMap map;
  public void setTerminalMap(TerminalMap map) {
    this.map = map;
  }
  public String unexpected_eof(String method, List<Integer> expected) {
    return "Error: unexpected end of file";
  }
  public String excess_tokens(String method, Terminal terminal) {
    return "Finished parsing without consuming all tokens.";
  }
  public String unexpected_symbol(String method, Terminal actual, List<Integer> expected) {
    ArrayList<String> expected_terminals = new ArrayList<String>();
    for ( Integer e : expected ) {
      expected_terminals.add(this.map.get(e.intValue()));
    }
    return "Unexpected symbol when parsing " + method + ".  Expected " + Utility.join(expected_terminals, ", ") + ", got " + actual.getTerminalStr() + ".";
  }
  public String no_more_tokens(String method, int expecting) {
    return "No more tokens.  Expecting " + this.map.get(expecting);
  }
  public String invalid_terminal(String method, Terminal invalid) {
    return "Invalid symbol ID: "+invalid.getId()+" ("+invalid.getTerminalStr()+")";
  }
}
