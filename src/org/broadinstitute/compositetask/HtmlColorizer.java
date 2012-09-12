package org.broadinstitute.compositetask;

public class HtmlColorizer implements CompositeTaskColorizer {
  private ColorTheme theme;

  public HtmlColorizer(ColorTheme theme) {
    this.theme = theme;
  }

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
}
