
package org.broadinstitute.parser;
public interface ExpressionParser extends Parser {
  ParseTree parse(TokenStream tokens, int rbp) throws SyntaxError;
}
