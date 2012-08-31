
package org.broadinstitute.compositetask;
interface AstNode {
  public String toString();
  public String toPrettyString();
  public String toPrettyString(int indent);
}
