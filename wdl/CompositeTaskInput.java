class CompositeTaskInput {
  private CompositeTaskNode node;
  private String parameter;

  public CompositeTaskInput(CompositeTaskNode node) {
    this.node = node;
    this.parameter = null;
  }

  public CompositeTaskInput(CompositeTaskNode node, String parameter) {
    this(node);
    this.parameter = parameter;
  }

  public CompositeTaskNode getNode() {
    return this.node;
  }

  public String getParameter() {
    return this.parameter;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskInput other) {
    return false;
  }

  public String toString() {
    return "[Input node="+this.node+", param="+this.parameter+"]";
  }
}
