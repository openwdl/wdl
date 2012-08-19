import java.util.Collection;

class CompositeTaskStep implements CompositeTaskNode {
  private CompositeTaskSubTask task;
  private String name;
  private Ast ast;

  public CompositeTaskStep(String name, CompositeTaskSubTask task) {
    this.ast = null;
    this.task = task;
    this.name = name;
  }

  public CompositeTaskStep(Ast ast, String name, CompositeTaskSubTask task) {
    this(name, task);
    this.ast = ast;
  }

  public Ast getAst() {
    return this.ast;
  }

  public String getName() {
    return this.name;
  }

  public CompositeTaskSubTask getTask() {
    return this.task;
  }

  /* TODO: Are steps only unique by name? */
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
