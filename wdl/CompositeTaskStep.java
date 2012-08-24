import java.util.Set;

class CompositeTaskStep implements CompositeTaskNode, CompositeTaskVertex {
  private CompositeTaskSubTask task;
  private String name;
  private Set<CompositeTaskStepInput> inputs;
  private Set<CompositeTaskStepOutput> outputs;

  public CompositeTaskStep(String name, CompositeTaskSubTask task, Set<CompositeTaskStepInput> inputs, Set<CompositeTaskStepOutput> outputs) {
    this.task = task;
    this.name = name;
    this.inputs = inputs;
    this.outputs = outputs;
  }

  public Ast getAst() {
    return null;
  }

  public String getName() {
    return this.name;
  }

  public CompositeTaskSubTask getTask() {
    return this.task;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskStep other) {
    return false;
  }

  public String toString() {
    return "[Step: name=" + this.name + "]";
  }
}
