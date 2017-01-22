## Copyright Broad Institute, 2017
## 
## This WDL reverts a set of single-readgroup BAMs to paired FASTQs
##
## Requirements/expectations:
## - List of valid BAM files
## - Max one readgroup per BAM files. If there are more, the distinctions will be lost!
##
## Outputs: 
## - Sets of two FASTQ files of paired reads (*_1 and *_2) plus one FASTQ file of 
## unpaired reads (*_unp) per input file. 
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

# TASK DEFINITIONS

# Run SamToFASTQ to revert the bam
task RevertBAMToPairedFASTQ {
  File bam_file
  String output_basename
  Int disk_size
  String mem_size

  command {
    java -Xmx3000m -jar /usr/gitc/picard.jar \
      SamToFastq \
      I=${bam_file} \
      FASTQ=${output_basename}_1.fastq \
      SECOND_END_FASTQ=${output_basename}_2.fastq \
      UNPAIRED_FASTQ=${output_basename}_unp.fastq \
      INCLUDE_NON_PRIMARY_ALIGNMENTS=true \
      INCLUDE_NON_PF_READS=true 
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.3-1469027018"
    memory: mem_size
    cpu: "1"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    Array[File] output_fastqs = glob("*.fastq")
  }
}

# WORKFLOW DEFINITION
workflow RevertRGBamsToPairedFastQsWf {
  Array[File] bam_list

  # Process input files in parallel
  scatter (input_bam in bam_list) {

    String sub_strip_path = "gs://.*/"
    String sub_strip_suffix = ".bam$"

    # Revert inputs to paired FASTQ 
    call RevertBAMToPairedFASTQ {
      input:
        bam_file = input_bam,
        output_basename = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, ""),
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    Array[Array[File]] output_fastqs_globs=RevertBAMToPairedFASTQ.output_fastqs
  }
}

