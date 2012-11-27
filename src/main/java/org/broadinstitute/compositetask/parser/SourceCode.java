
package org.broadinstitute.compositetask.parser;
import java.util.List;
public interface SourceCode {
  public void advance(int amount);
  public List<String> getLines();
  public String getLine(int lineno);
  public String getString();
  public int getLine();
  public int getColumn();
  public String getResource();
}
