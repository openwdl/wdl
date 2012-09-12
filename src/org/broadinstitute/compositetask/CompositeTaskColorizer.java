package org.broadinstitute.compositetask;

public interface CompositeTaskColorizer {
  String preamble();
  String postamble();
  String keyword(String str);
  String string(String str);
  String variable(String str);
}
