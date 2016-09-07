## Copyright Broad Institute, 2016
## 
## This WDL validates a list of BAMs in SUMMARY mode
##
## Requirements/expectations :
## - List of BAM files to validate
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

# Extract the header from a BAM using samtools
task ValidateBAM {
  File bam_file
  String output_basename

  command {
    java -Xmx3000m -jar /usr/gitc/picard.jar \
      ValidateSamFile \
      I=${bam_file} \
      OUTPUT=${output_basename}.txt \
      MODE=SUMMARY 
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.3-1469027018"
    memory: "1 GB"
    cpu: "1"
    disks: "local-disk " + 200 + " HDD"
  }
  output {
    File output_bam = "${output_basename}.txt"
  }
}

# WORKFLOW DEFINITION
workflow ValidateBAMs {
  Array[File] bam_list

  # Convert multiple pairs of input fastqs in parallel
  scatter (input_bam in bam_list) {

    String sub_strip_path = "gs://.*/"
    String sub_strip_suffix = ".bam$"

    # Convert pair of FASTQs to uBAM
    call ValidateBAM {
      input:
        bam_file = input_bam,
        output_basename = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, "") + ".validation"
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    ValidateBAM.*
  }
}

