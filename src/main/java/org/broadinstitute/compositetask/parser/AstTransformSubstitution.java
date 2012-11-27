
package org.broadinstitute.compositetask.parser;
public class AstTransformSubstitution implements AstTransform {
  private int index;
  AstTransformSubstitution(int index) {
    this.index = index;
  }
  public int getIndex() {
    return this.index;
  }
  public String toString() {
    return "AstSubstitution: $" + Integer.toString(this.index);
  }
}
