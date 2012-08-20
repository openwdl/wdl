import java.util.Set;

class CompositeTaskBaseScope implements CompositeTaskScope {
  private Set<CompositeTaskNode> nodes;
  private Ast ast;

  CompositeTaskBaseScope(Ast ast, Set<CompositeTaskNode> nodes) {
    this.ast = ast;
    this.nodes = nodes;
  }

  public Set<CompositeTaskNode> getNodes() {
    return this.nodes;
  }

  public Ast getAst() {
    return this.ast;
  }
}
