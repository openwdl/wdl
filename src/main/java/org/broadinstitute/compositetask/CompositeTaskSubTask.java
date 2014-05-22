package org.broadinstitute.compositetask;

import java.util.Set;

public class CompositeTaskSubTask implements Comparable<CompositeTaskSubTask> {
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

  public int compareTo(CompositeTaskSubTask other) {
    int nameCompare = this.getTaskName().compareTo(other.getTaskName());
    int versionCompare = this.getVersion().compareTo(other.getVersion());
    if (nameCompare != 0) return nameCompare;
    else if (versionCompare != 0) return versionCompare;
    else return 0;
  }

  public String toString() {
    return "[Task: name="+this.name+", version="+this.version+"]";
  }
}
