class WdlSourceCodeFormatter {
  private WdlSourceColorizer colorizer;
  private WdlSourceCodeNormalizer normalizer;

  WdlSourceReformatter(WdlSourceColorizer colorizer, WdlSourceCodeNormalizer normalizer) {
    this.colorizer = colorizer;
    this.normalizer = normalizer;
  }

  WdlSourceReformatter(WdlSourceColorizer colorizer) {
    this.colorizer = colorizer;
  }

  WdlSourceReformatter(WdlSourceCodeNormalizer normalizer) {
    this.normalizer = normalizer;
  }

  public String compile(CompositeTask task) {

  }
}
