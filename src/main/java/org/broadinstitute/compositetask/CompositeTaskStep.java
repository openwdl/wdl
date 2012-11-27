package org.broadinstitute.compositetask;

import java.util.Set;

import org.broadinstitute.parser.Ast;

public class CompositeTaskStep implements CompositeTaskNode, CompositeTaskVertex {
  private CompositeTaskSubTask task;
  private String name;
  private Set<CompositeTaskStepInput> inputs;
  private Set<CompositeTaskStepOutput> outputs;
  private CompositeTaskScope parent;

  public CompositeTaskStep(String name, CompositeTaskSubTask task, Set<CompositeTaskStepInput> inputs, Set<CompositeTaskStepOutput> outputs) {
    this.task = task;
    this.name = name;
    this.inputs = inputs;
    this.outputs = outputs;
    this.parent = null;
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

  public Set<CompositeTaskStepOutput> getOutputs() {
    return this.outputs;
  }

  public Set<CompositeTaskStepInput> getInputs() {
    return this.inputs;
  }

  public void setParent(CompositeTaskScope parent) {
    this.parent = parent;
  }

  public CompositeTaskScope getParent() {
    return this.parent;
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
