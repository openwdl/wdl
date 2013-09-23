package org.broadinstitute.compositetask;

import java.util.Set;

import org.broadinstitute.parser.Ast;

public class CompositeTaskStepOutput {
  private String type;
  private String method;
  private String path;
  private CompositeTaskVariable variable;

  public CompositeTaskStepOutput(String type, String method, String path, CompositeTaskVariable variable) {
    this.type = type;
    this.method = method;
    this.path = path;
    this.variable = variable;
  }

  public Ast getAst() {
    return null;
  }

  public String getPath() {
    return this.path.replaceAll("^\"|\"$", "");
  }

  public String getMethod() {
    return this.method;
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
    return "[StepOutput: path=" + this.path + "]";
  }
}
