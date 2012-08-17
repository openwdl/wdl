import java.util.Set;

class CompositeTaskForScope implements CompositeTaskScope {
  private String collection;
  private String var;
  private Set<CompositeTaskNode> nodes;

  public CompositeTaskForScope(String collection, String var, Set<CompositeTaskNode> nodes) {
    this.collection = collection;
    this.var = var;
    this.nodes = nodes;
  }

  public String getCollectionName() {
    return this.collection;
  }

  public String getVarName() {
    return this.var;
  }

  public Set<CompositeTaskNode> getNodes() {
    return this.nodes;
  }
}
