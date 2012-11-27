
package org.broadinstitute.parser;
import java.util.ArrayList;
import java.util.List;
import java.util.Formatter;
import java.util.Locale;
public class TokenStream extends ArrayList<Terminal> {
  private int index;
  private TerminalMap terminals;
  private SyntaxErrorFormatter syntaxErrorFormatter;
  public TokenStream(List<Terminal> terminals) {
    super(terminals);
    reset();
  }
  public TokenStream() {
    reset();
  }
  public void setTerminalMap(TerminalMap terminals) {
    this.terminals = terminals;
  }
  public void setSyntaxErrorFormatter(SyntaxErrorFormatter syntaxErrorFormatter) {
    this.syntaxErrorFormatter = syntaxErrorFormatter;
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
  public Terminal last() {
    return this.get(this.size() - 1);
  }
  public Terminal expect(TerminalIdentifier expecting, String nonterminal, String rule) throws SyntaxError {
    Terminal current = current();
    if (current == null) {
      throw new SyntaxError(syntaxErrorFormatter.no_more_tokens(nonterminal, expecting, last()));
    }
    if (current.getId() != expecting.id()) {
      ArrayList<TerminalIdentifier> expectedList = new ArrayList<TerminalIdentifier>();
      expectedList.add(expecting);
      throw new SyntaxError(syntaxErrorFormatter.unexpected_symbol(nonterminal, current, expectedList, rule));
    }
    Terminal next = advance();
    if ( next != null && !this.terminals.isValid(next.getId()) ) {
      throw new SyntaxError(syntaxErrorFormatter.invalid_terminal(nonterminal, next));
    }
    return current;
  }
}
