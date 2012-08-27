import java.util.Set;

class CompositeTaskStepInput {
  private String parameter;
  private CompositeTaskVariable variable;

  public CompositeTaskStepInput(String parameter, CompositeTaskVariable variable) {
    this.parameter = parameter;
    this.variable = variable;
  }

  public CompositeTaskStepInput(Ast ast) {
  }

  public Ast getAst() {
    return null;
  }

  public String getParameter() {
    return this.parameter;
  }

  public CompositeTaskVariable getVariable() {
    return this.variable;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskStepInput other) {
    return false;
  }

  public String toString() {
    return "[StepInput: parameter=" + this.parameter + "]";
  }
}
