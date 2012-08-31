
package org.broadinstitute.compositetask;
public interface Parser {
  ParseTree parse(TokenStream tokens) throws SyntaxError;
  TerminalMap getTerminalMap();
}
