
package org.broadinstitute.compositetask;
import java.util.List;
public interface SyntaxErrorFormatter {
  /* Called when the parser runs out of tokens but isn't finished parsing. */
  String unexpected_eof(String method, List<TerminalIdentifier> expected, List<String> nt_rules);
  /* Called when the parser finished parsing but there are still tokens left in the stream. */
  String excess_tokens(String method, Terminal terminal);
  /* Called when the parser is expecting one token and gets another. */
  String unexpected_symbol(String method, Terminal actual, List<TerminalIdentifier> expected, String rule);
  /* Called when the parser is expecing a tokens but there are no more tokens. */
  String no_more_tokens(String method, TerminalIdentifier expecting, Terminal last);
  /* Invalid terminal is found in the token stream. */
  String invalid_terminal(String method, Terminal invalid);
}
