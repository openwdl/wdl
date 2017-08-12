## Copyright Broad Institute, 2017
## 
## This WDL reverts a SAM or BAM file to uBAMs, one per readgroup 
##
## Requirements/expectations :
## - Pair-end sequencing data in SAM or BAM format
## - One or more read groups
##
## Outputs :
## - Set of unmapped BAMs, one per read group, with reads sorted by queryname
##
## Cromwell version support 
## - Successfully tested on v24
## - Does not work on versions < v23 due to output syntax
##
## Runtime parameters are optimized for Broad's Google Cloud Platform implementation. 
## For program versions, see docker containers. 
##
## LICENSING : 
## This script is released under the WDL source code license (BSD-3) (see LICENSE in 
## https://github.com/broadinstitute/wdl). Note however that the programs it calls may 
## be subject to different licenses. Users are responsible for checking that they are
## authorized to run all programs before running this script. Please see the docker 
## page at https://hub.docker.com/r/broadinstitute/genomes-in-the-cloud/ for detailed
## licensing information pertaining to the included programs.

# WORKFLOW DEFINITION

workflow RevertBamToUnmappedReaGroupBams { ##### TODO: check why we're including the reference
  File input_bam
  File ref_fasta
  File ref_fasta_index
  String output_dir

  # Revert inputs to unmapped
  call RevertBamToUnmappedRGBams {
    input:
      input_bam = input_bam,
      output_dir = output_dir
  }

  # Outputs that will be retained when execution is complete
  output {
    Array[File] unmapped_bams = RevertBamToUnmappedRGBams.unmapped_bams
  }
}

# TASK DEFINITIONS

# Revert a BAM to uBAMs, one per readgroup
task RevertBamToUnmappedRGBams {
  File input_bam
  String output_dir
  Float? max_discard_pct
  Int disk_size
  String mem_size
  String docker

  command {
    java ${java_opt} -jar ${jar_path} RevertSam \
      INPUT=${input_bam} \
      O=${output_dir} \
      OUTPUT_BY_READGROUP=true \
      VALIDATION_STRINGENCY=LENIENT \
      SANITIZE=TRUE \
      MAX_DISCARD_FRACTION=${max_discard_pct} \
      ATTRIBUTE_TO_CLEAR=FT \
      SORT_ORDER=queryname 
  }
  runtime {
    docker: docker
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size
  }
  output {
    Array[File] unmapped_bams = glob("*.bam")
  }
}
