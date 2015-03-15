task bwa-mem {
  command {
    bwa mem \
    ${prefix='-t ' cpus?} \
    ${prefix='-I ' sep=',' type=array[int] min_std_max_min} \
    ${prefix='-m ' type=int minimum_seed_length} \
    ${type=uri reference} \
    ${type=array[uri] sep=' ' reads}
  }
  outputs {
    "output.bam" -> bam
    "${bam}.bai" -> bai
  }
  runtime {
    docker: "broadinstitute/bwa-mem:latest"
    memory: "5GB"
  }
}
