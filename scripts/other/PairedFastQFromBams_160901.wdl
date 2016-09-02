## Copyright Broad Institute, 2016
## 
## This WDL converts a list of BAMs to pairs of FASTQs
##
## Requirements/expectations :
## - List of valid BAM files
## - Max one readgroup per BAM files. If there are more, the distinctions will be lost.
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
task PairedFastQFromBam {
  File bam_file
  String fastq_1
  String fastq_2
  String unpaired

  command {
    java -Xmx3000m -jar /usr/gitc/picard.jar \
      SamToFastq \
      I=${bam_file} \
      FASTQ=${fastq_1} \
      SECOND_END_FASTQ=${fastq_2} \
      UNPAIRED_FASTQ=${unpaired} \
      INCLUDE_NON_PRIMARY_ALIGNMENTS=true \
      INCLUDE_NON_PF_READS=true \
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.3-1469027018"
    memory: "3500 MB"
    cpu: "1"
    disks: "local-disk " + 200 + " HDD"
  }
}

# WORKFLOW DEFINITION
workflow PairedFastQFromBams {
  Array[File] bam_list

  # Convert multiple pairs of input fastqs in parallel
  scatter (input_bam in bam_list) {

    String sub_strip_path = "gs://.*/"
    String sub_strip_suffix = ".bam$"
    String output_basename = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, "")

    # Convert pair of FASTQs to uBAM
    call PairedFastQFromBam {
      input:
        bam_file = input_bam,
        fastq_1 = output_basename + "_1.fastq",
        fastq_2 = output_basename + "_2.fastq",
        unpaired = output_basename + "_up.fastq"
    }
  }
}

