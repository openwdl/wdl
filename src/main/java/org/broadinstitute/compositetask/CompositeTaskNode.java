package org.broadinstitute.compositetask;

public interface CompositeTaskNode {
  public Ast getAst();
  public void setParent(CompositeTaskScope parent);
  public CompositeTaskScope getParent();
}
