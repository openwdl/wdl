import java.util.Set;

class CompositeTaskSubTask {
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

  public String toString() {
    return "[Task: name="+this.name+", version="+this.version+"]";
  }
}
