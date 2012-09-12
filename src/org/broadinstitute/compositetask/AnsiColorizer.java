package org.broadinstitute.compositetask;

public class AnsiColorizer implements CompositeTaskColorizer {
  public AnsiColorizer() {
    
  }

  public String preamble() {
    return "";
  }

  public String postamble() {
    return "";
  }

  public String keyword(String str) {
    return "\033[38;5;109m" + str + "\033[0m";
  }

  public String string(String str) {
    return "\033[38;5;222m" + str + "\033[0m";
  }

  public String variable(String str) {
    return "\033[38;5;143m" + str + "\033[0m";
  }
}
