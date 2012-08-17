import java.util.Collection;

class CompositeTaskStep implements CompositeTaskNode {
  private CompositeTaskSubTask task;
  private String name;

  public CompositeTaskStep(CompositeTaskSubTask task) {
    this.task = task;
    this.name = task.getTaskName();
  }

  public CompositeTaskStep(String name, CompositeTaskSubTask task) {
    this.task = task;
    this.name = name;
  }

  public String getName() {
    return this.name;
  }

  public CompositeTaskSubTask getTask() {
    return this.task;
  }

  /* TODO: Are steps only unique by name? */
  public int hashCode() {

  }

  public boolean equals(CompositeTaskStep other) {

  }
}
