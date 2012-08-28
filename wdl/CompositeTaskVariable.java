import java.util.Set;

class CompositeTaskVariable implements CompositeTaskVertex {
  private String name;
  private String member;

  public CompositeTaskVariable(String name, String member) {
    this.name = name;
    this.member = member;
  }

  public CompositeTaskVariable(String name) {
    this.name = name;
  }

  public Ast getAst() {
    return null;
  }

  public String getName() {
    return this.name;
  }

  public String getMember() {
    return this.member;
  }

  public int hashCode() {
    return 0;
  }

  public boolean equals(CompositeTaskVariable other) {
    if ( other.getName().equals(this.name) ) {
      if ( other.getMember() == null && this.member == null ) {
        return true;
      }

      if ( other.getMember() != null && other.getMember().equals(this.member) ) {
        return true;
      }
    }
    return false;
  }

  public String toString() {
    return "[Variable: name=" + this.name + "]";
  }
}
