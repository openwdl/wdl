import java.util.Set;

class CompositeTaskForScope implements CompositeTaskScope {
  private String collection;
  private String var;
  private Set<CompositeTaskNode> nodes;
  private Ast ast;

  public CompositeTaskForScope(String collection, String var, Set<CompositeTaskNode> nodes) {
    this.ast = null;
    this.collection = collection;
    this.var = var;
    this.nodes = nodes;
  }

  public CompositeTaskForScope(Ast ast, String collection, String var, Set<CompositeTaskNode> nodes) {
    this(collection, var, nodes);
    this.ast = ast;
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
