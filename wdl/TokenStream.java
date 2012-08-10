import java.util.ArrayList;
import java.util.Formatter;
import java.util.Locale;
class TokenStream extends ArrayList<Terminal> {
  private int index;
  private TerminalMap terminals;
  TokenStream(TerminalMap terminals) {
    this.terminals = terminals;
    reset();
  }
  public void reset() {
    this.index = 0;
  }
  public Terminal advance() {
    this.index += 1;
    return this.current();
  }
  public Terminal current() {
    try {
      return this.get(this.index);
    } catch (IndexOutOfBoundsException e) {
      return null;
    }
  }
  public Terminal expect(int expecting) throws SyntaxError {
    Terminal current = current();
    if (current == null) {
      throw new SyntaxError( "No more tokens.  Expecting " + this.terminals.get(expecting) );
    }
    if (current.getId() != expecting) {
      Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      formatter.format("Unexpected symbol when parsing %s.  Expected %s, got %s.", stack[2].getMethodName(), this.terminals.get(expecting), current != null ? current : "<end of stream>");
      throw new SyntaxError(formatter.toString());
    }
    Terminal next = advance();
    if ( next != null && !this.terminals.isValid(next.getId()) ) {
      Formatter formatter = new Formatter(new StringBuilder(), Locale.US);
      formatter.format("Invalid symbol ID: %d (%s)", next.getId(), next.getTerminalStr());
      throw new SyntaxError(formatter.toString());
    }
    return current;
  }
}
