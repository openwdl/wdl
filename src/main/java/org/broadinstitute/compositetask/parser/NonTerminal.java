
package org.broadinstitute.compositetask.parser;
public class NonTerminal {
  private int id;
  private String string;
  NonTerminal(int id, String string) {
    this.id = id;
    this.string = string;
  }
  public int getId() {
    return this.id;
  }
  public String getString() {
    return this.string;
  }
  public String toString() {
    return this.string;
  }
}
