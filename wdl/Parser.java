interface Parser {
  ParseTree parse(TokenStream tokens, SyntaxErrorFormatter formatter) throws SyntaxError;
  TerminalMap getTerminalMap();
}
