import java.util.ArrayList;
import java.util.List;

class WdlSyntaxErrorFormatter implements SyntaxErrorFormatter {
  private SourceCode code;
  public void setSourceCode(SourceCode code) {
    this.code = code;
  }

  public String unexpected_eof(String method, List<TerminalIdentifier> expected, List<String> nt_rules) {
    ArrayList<String> expected_terminals = new ArrayList<String>();
    if ( expected != null && expected.size() > 0 ) {
      for ( TerminalIdentifier e : expected ) {
        expected_terminals.add(e.string());
      }
    }
    return "Unexpected end of file when parsing " + method + "\n\nExpecting one of: " + Utility.join(expected_terminals, ", ") + "\nPossible rules:\n" + Utility.join(nt_rules, "\n");
  }

  public String excess_tokens(String method, Terminal terminal) {
    String msg = "Finished parsing without consuming all tokens";
    msg += "\nLocation: " + terminal.getResource() + " @ line " + terminal.getLine() + ", column " + terminal.getColumn();
    return msg;
  }

  public String unexpected_symbol(String method, Terminal actual, List<TerminalIdentifier> expected, String rule) {
    String msg = "Unexpected symbol " + actual.getTerminalStr();

    if ( expected != null && expected.size() > 0 ) {
      ArrayList<String> expected_terminals = new ArrayList<String>();
      for ( TerminalIdentifier e : expected ) {
        expected_terminals.add(e.string());
      }
      msg += ".  Expecting " + Utility.join(expected_terminals, ", ") + ".";
    }

    msg += "\nRule: " + rule;
    msg += "\nLocation: " + actual.getResource() + " @ line " + actual.getLine() + ", column " + actual.getColumn() + ":\n\n";
    msg += code.getLine(actual.getLine()) + "\n";
    msg += Utility.getIndentString(actual.getColumn()-1) + "^\n";
    return msg;
  }

  public String no_more_tokens(String method, TerminalIdentifier expecting, Terminal last) {
    String lastLine = this.code.getLine(last.getLine());
    return "No more tokens when parsing " + method + "\nExpecting: " + expecting.string() + "\nLocation: " + last.getResource() + " @ line " + last.getLine() + ", column " + last.getColumn() + ":\n\n" + lastLine + "\n" + Utility.getIndentString(last.getColumn()-1) + "^\n";
  }

  public String invalid_terminal(String method, Terminal invalid) {
    return "Invalid symbol ID: "+invalid.getId()+" ("+invalid.getTerminalStr()+")";
  }

  public String missing_version(Terminal task_name) {
    return "Version information missing for task " + task_name.getSourceString() + "\nLocation: " + task_name.getResource() + " @ line " + task_name.getLine() + ", column " + task_name.getColumn() + ":\n\n" + this.code.getLine(task_name.getLine()) + "\n" + Utility.getIndentString(task_name.getColumn()-1) + "^\n";
  }

}
