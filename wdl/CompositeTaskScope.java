import java.util.Set;

interface CompositeTaskScope extends CompositeTaskNode {
  public Set<CompositeTaskNode> getNodes();
}
