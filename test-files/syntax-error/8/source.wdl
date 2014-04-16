composite_task CufflinksPipeline {
  step FilterBamForAlignedReads[version=8] {
    output: File("${abc}.${xyz}.bam") as filtered_bam_name,
            File("${abc}.bam") as xyz;
  }
  step Cufflinks[version=29] {
    input: input.bam=xyz;
  }
}
