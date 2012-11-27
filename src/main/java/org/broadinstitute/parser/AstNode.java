
package org.broadinstitute.parser;
public interface AstNode {
  public String toString();
  public String toPrettyString();
  public String toPrettyString(int indent);
}
