import java.util.List;
interface SyntaxErrorFormatter {
  /* Called when the parser runs out of tokens but isn't finished parsing. */
  String unexpected_eof(String method, List<Integer> expected);
  /* Called when the parser finished parsing but there are still tokens left in the stream. */
  String excess_tokens(String method, Terminal terminal);
  /* Called when the parser is expecting one token and gets another. */
  String unexpected_symbol(String method, Terminal actual, List<Integer> expected);
  /* Called when the parser is expecing a tokens but there are no more tokens. */
  String no_more_tokens(String method, int expecting);
  /* Invalid terminal is found in the token stream. */
  String invalid_terminal(String method, Terminal invalid);
}
