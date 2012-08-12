interface Parser {
  ParseTree parse(TokenStream tokens) throws SyntaxError;
  TerminalMap getTerminalMap();
}
