class CompositeTaskEdge {
  private CompositeTaskOutput start;
  private CompositeTaskInput end;
  private String variable;

  public CompositeTaskEdge(CompositeTaskOutput start, CompositeTaskInput end, String variable) {
    this.start = start;
    this.end = end;
    this.variable = variable;
  }

  public CompositeTaskOutput getStart() {
    return this.start;
  }

  public CompositeTaskInput getEnd() {
    return this.end;
  }

  public String getVariable() {
    return this.variable;
  }

  /* TODO: How will these methods be implemented? */
  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskEdge other) {
    return false;
  }

  public String toString() {
    return "[Edge\n  from="+this.start+",\n  to="+this.end+",\n  var="+this.variable+"\n]";
  }
}
