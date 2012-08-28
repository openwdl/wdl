import java.util.Set;

class CompositeTaskForLoop implements CompositeTaskScope {
  private CompositeTaskVariable collection;
  private CompositeTaskVariable var;
  private Set<CompositeTaskNode> nodes;
  private CompositeTaskScope parent;

  public CompositeTaskForLoop(CompositeTaskVariable collection, CompositeTaskVariable var, Set<CompositeTaskNode> nodes) {
    this.collection = collection;
    this.var = var;
    this.nodes = nodes;
    this.parent = null;
  }

  public Ast getAst() {
    return null;
  }

  public CompositeTaskVariable getCollection() {
    return this.collection;
  }

  public CompositeTaskVariable getVariable() {
    return this.var;
  }

  public Set<CompositeTaskNode> getNodes() {
    return this.nodes;
  }

  public void setParent(CompositeTaskScope parent) {
    this.parent = parent;
  }

  public CompositeTaskScope getParent() {
    return this.parent;
  }

  public boolean contains(CompositeTaskNode node) {
    for ( CompositeTaskNode sub_node : this.nodes ) {
      if ( node.equals(sub_node) ) {
        return true;
      }

      if ( sub_node instanceof CompositeTaskScope ) {
        CompositeTaskScope scope = (CompositeTaskScope) sub_node;
        if ( scope.contains(node) ) {
          return true;
        }
      }
    }
    return false;
  }

  public String toString() {
    return "[CompositeTaskForScope: collection=" + this.collection + ", var=" + this.var + ", # nodes=" + this.nodes.size()+ "]";
  }
}
