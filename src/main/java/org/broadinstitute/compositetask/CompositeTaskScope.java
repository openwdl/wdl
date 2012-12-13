package org.broadinstitute.compositetask;

import java.util.Set;

public interface CompositeTaskScope extends CompositeTaskNode, CompositeTaskVertex {
  public Set<CompositeTaskNode> getNodes();
  public boolean contains(CompositeTaskNode node);
  public int compareTo(CompositeTaskVertex other);
}
