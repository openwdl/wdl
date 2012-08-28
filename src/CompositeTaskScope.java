import java.util.Set;

interface CompositeTaskScope extends CompositeTaskNode, CompositeTaskVertex {
  public Set<CompositeTaskNode> getNodes();
  public boolean contains(CompositeTaskNode node);
}
