
package org.broadinstitute.compositetask.parser;
import java.util.ArrayList;
public class AstList extends ArrayList<AstNode> implements AstNode {
  public String toString() {
    return "[" + Utility.join(this, ", ") + "]";
  }
  public String toPrettyString() {
    return toPrettyString(0);
  }
  public String toPrettyString(int indent) {
    String spaces = Utility.getIndentString(indent);
    if (this.size() == 0) {
      return spaces + "[]";
    }
    ArrayList<String> elements = new ArrayList<String>();
    for ( AstNode node : this ) {
      elements.add(node.toPrettyString(indent + 2));
    }
    return spaces + "[\n" + Utility.join(elements, ",\n") + "\n" + spaces + "]";
  }
}
