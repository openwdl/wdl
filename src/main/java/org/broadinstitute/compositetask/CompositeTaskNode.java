package org.broadinstitute.compositetask;

import org.broadinstitute.compositetask.parser.Ast;

public interface CompositeTaskNode {
  public Ast getAst();
  public void setParent(CompositeTaskScope parent);
  public CompositeTaskScope getParent();
}
