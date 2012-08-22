import java.util.Set;

class CompositeTaskVariable {
  private String name;
  private String member;

  public CompositeTaskVariable(String name, String member) {
    this.name = name;
    this.member = member;
  }

  public CompositeTaskVariable(String name) {
    this.name = name;
  }

  public CompositeTaskVariable(Ast ast) {
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
    return false;
  }

  public String toString() {
    return "[Variable: name=" + this.name + "]";
  }
}
