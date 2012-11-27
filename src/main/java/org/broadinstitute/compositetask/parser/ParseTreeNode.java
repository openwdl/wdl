
package org.broadinstitute.compositetask.parser;
public interface ParseTreeNode {
  public AstNode toAst();
  public String toString();
  public String toPrettyString();
  public String toPrettyString(int indent);
}
