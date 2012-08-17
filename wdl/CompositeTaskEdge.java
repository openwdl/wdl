class CompositeTaskEdge {
  private CompositeTaskOutput start;
  private CompositeTaskInput end;

  public CompositeTaskEdge(CompositeTaskOutput start, CompositeTaskInput end) {
    this.start = start;
    this.end = end;
  }

  public CompositeTaskOutput getStart() {
    return this.start;
  }

  public CompositeTaskInput getEnd() {
    return this.end;
  }

  /* TODO: How will these methods be implemented? */
  public int hashCode() {

  }

  public boolean equals(CompositeTaskEdge other) {

  }
}
