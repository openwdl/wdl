import java.util.Set;

class CompositeTaskForLoop implements CompositeTaskScope {
  private String collection;
  private String var;
  private Set<CompositeTaskNode> nodes;

  public CompositeTaskForLoop(String collection, String var, Set<CompositeTaskNode> nodes) {
    this.collection = collection;
    this.var = var;
    this.nodes = nodes;
  }

  public Ast getAst() {
    return this.ast;
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

  public String toString() {
    return "[CompositeTaskForScope: collection=" + this.collection + ", var=" + this.var + ", # nodes=" + this.nodes.size()+ "]";
  }
}
