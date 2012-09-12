package org.broadinstitute.compositetask;

public interface CompositeTaskColorizer {
  public String preamble();
  public String postamble();
  public String keyword(String str);
  public String string(String str);
  public String variable(String str);
  public String task(String str);
}
