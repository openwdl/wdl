class WdlSourceCodeFormatter {
  private WdlTerminalColorizer colorizer;
  private WdlSourceCodeNormalizer normalizer;

  WdlSourceCodeFormatter(WdlTerminalColorizer colorizer, WdlSourceCodeNormalizer normalizer) {
    this.colorizer = colorizer;
    this.normalizer = normalizer;
  }

  WdlSourceCodeFormatter(WdlTerminalColorizer colorizer) {
    this.colorizer = colorizer;
  }

  WdlSourceCodeFormatter(WdlSourceCodeNormalizer normalizer) {
    this.normalizer = normalizer;
  }

  public String compile(CompositeTask task) {

  }
}
