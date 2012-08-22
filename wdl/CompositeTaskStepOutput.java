import java.util.Set;

class CompositeTaskStepOutput {
  private String type;
  private String path;
  private CompositeTaskVariable variable;

  public CompositeTaskStepOutput(String type, String path, CompositeTaskVariable variable) {
    this.parameter = parameter;
    this.variable = variable;
  }

  public CompositeTaskStepOutput(Ast ast) {
  }

  public Ast getAst() {
    return null;
  }

  public String getPath() {
    return this.path;
  }

  public String getType() {
    return this.type;
  }

  public CompositeTaskVariable getVariable() {
    return this.variable;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskStepOutput other) {
    return false;
  }

  public String toString() {
    return "[StepOutput: name=" + this.name + "]";
  }
}
