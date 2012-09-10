package org.broadinstitute.compositetask;

import java.util.Set;

public class CompositeTaskSubTask {
  private String name;
  private String version;

  public CompositeTaskSubTask(String name, String version) {
    this.name = name;
    this.version = version;
  }

  public String getTaskName() {
    return this.name;
  }

  public String getVersion() {
    return this.version;
  }

  public Set<String> getInputs() {
    /* TODO: implement */
    return null;
  }

  public boolean equals(CompositeTaskSubTask other) {
    if (other.getTaskName().equals(this.name) && other.getVersion().equals(this.version)) {
      return true;
    }
    return false;
  }

  public String toString() {
    return "[Task: name="+this.name+", version="+this.version+"]";
  }
}
