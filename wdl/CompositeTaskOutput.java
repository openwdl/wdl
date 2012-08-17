class CompositeTaskOutput {
  private CompositeTaskNode node;
  private String type;
  private String path;
  private String name;
  
  public CompositeTaskOutput(CompositeTaskNode node, String type, String path, String name) {
    this.node = node;
    this.type = type;
    this.path = path;
    this.name = name;
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

  public String getName() {
    return this.name;
  }

  public int hashCode() {

  }

  public boolean equals(CompositeTaskOutput other) {
    
  }
}
