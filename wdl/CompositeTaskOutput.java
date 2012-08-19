class CompositeTaskOutput {
  private CompositeTaskNode node;
  private String type;
  private String path;
  
  public CompositeTaskOutput(CompositeTaskNode node, String type, String path) {
    this.node = node;
    this.type = type;
    this.path = path;
  }

  public CompositeTaskNode getNode() {
    return this.node;
  }

  public String getType() {
    return this.type;
  }

  public String getPath() {
    return this.path;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskOutput other) {
    return false;
  }

  public String toString() {
    return "[Output node="+this.node+", path="+this.path+"]";
  }
}
