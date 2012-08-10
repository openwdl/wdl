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
  public Terminal expect(int expecting, SyntaxErrorFormatter syntaxErrorFormatter) throws SyntaxError {
    Terminal current = current();
    if (current == null) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(syntaxErrorFormatter.no_more_tokens(stack[2].getMethodName(), expecting));
    }
    if (current.getId() != expecting) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      ArrayList<Integer> expectedList = new ArrayList<Integer>();
      expectedList.add(expecting);
      throw new SyntaxError(syntaxErrorFormatter.unexpected_symbol(stack[2].getMethodName(), current, expectedList));
    }
    Terminal next = advance();
    if ( next != null && !this.terminals.isValid(next.getId()) ) {
      StackTraceElement[] stack = Thread.currentThread().getStackTrace();
      throw new SyntaxError(syntaxErrorFormatter.invalid_terminal(stack[2].getMethodName(), next));
    }
    return current;
  }
}
