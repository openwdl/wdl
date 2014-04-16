composite_task CufflinksPipeline {
  step FilterBamForAlignedReads[version=8] {
    output: File("${filtered_bam_name}.bam") as filtered_bam_name;
  }
  step Cufflinks[version=29] {
    input: input.bam=filtered_bam_name;
  }
}
