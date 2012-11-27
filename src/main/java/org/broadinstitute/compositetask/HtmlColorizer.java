package org.broadinstitute.compositetask;

public class HtmlColorizer implements CompositeTaskColorizer {
  public String preamble() {
    return "";
  }

  public String postamble() {
    return "";
  }

  public String keyword(String str) {
    return "<span class=\"ct-keyword\">" + str + "</span>";
  }

  public String string(String str) {
    return "<span class=\"ct-string\">" + str + "</span>";
  }

  public String variable(String str) {
    return "<span class=\"ct-variable\">" + str + "</span>";
  }

  public String task(String str) {
    return "<span class=\"ct-task\">" + str + "</span>";
  }
}
