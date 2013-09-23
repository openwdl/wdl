package org.broadinstitute.compositetask;

import java.awt.Color;

import org.broadinstitute.parser.Terminal;

public interface ColorTheme {
  Color getColor(Terminal terminal);
}
