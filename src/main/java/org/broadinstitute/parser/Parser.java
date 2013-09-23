
package org.broadinstitute.parser;
public interface Parser {
  ParseTree parse(TokenStream tokens) throws SyntaxError;
  TerminalMap getTerminalMap();
}
