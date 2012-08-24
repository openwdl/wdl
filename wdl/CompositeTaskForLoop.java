import java.util.Set;

class CompositeTaskForLoop implements CompositeTaskScope {
  private CompositeTaskVariable collection;
  private CompositeTaskVariable var;
  private Set<CompositeTaskNode> nodes;

  public CompositeTaskForLoop(CompositeTaskVariable collection, CompositeTaskVariable var, Set<CompositeTaskNode> nodes) {
    this.collection = collection;
    this.var = var;
    this.nodes = nodes;
  }

  public Ast getAst() {
    return null;
  }

  public CompositeTaskVariable getCollectionName() {
    return this.collection;
  }

  public CompositeTaskVariable getVarName() {
    return this.var;
  }

  public Set<CompositeTaskNode> getNodes() {
    return this.nodes;
  }

  public String toString() {
    return "[CompositeTaskForScope: collection=" + this.collection + ", var=" + this.var + ", # nodes=" + this.nodes.size()+ "]";
  }
}
