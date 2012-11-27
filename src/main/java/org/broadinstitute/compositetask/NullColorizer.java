package org.broadinstitute.compositetask;

public class NullColorizer implements CompositeTaskColorizer {
  public String preamble() {
    return "";
  }

  public String postamble() {
    return "";
  }

  public String keyword(String str) {
    return str;
  }

  public String string(String str) {
    return str;
  }

  public String variable(String str) {
    return str;
  }

  public String task(String str) {
    return str;
  }
}
