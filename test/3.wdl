workflow SomeAnalysisWorkflow {
  step PreprocessNormal: (normal_pp_bam) = PreprocessBam( File("normal.bam"), "xyz" );
  step PreprocessTumor: (tumor_pp_bam) = PreprocessBam( File("tumor.bam"), "abc" );
  step DoAnalysis: (analysis_file, str) = DoAnalysis(normal_pp_bam, tumor_pp_bam);
  step GenerateReport: GenerateReport();
}

step PreprocessBam(input_bam:File, option:String) {
  output: File("preprocessed.bam");
  action: command("python ${libdir}preprocess.py ${input_bam} --with-option=${option}");
}

step DoAnalysis(normal_bam:File, tumor_bam:File) {
  output: File("dir/analysis.txt"), "static string";
  action: command("python ${libdir}script.py ${normal_bam} ${tumor_bam}");
}

step GenerateReport() {
  action: command("Rscript ${libdir}report.R");
}

step ScatterGatherStep() {
  action: scatter-gather(prepare, scatter, gather);
}
