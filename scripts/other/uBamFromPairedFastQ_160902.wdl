## Copyright Broad Institute, 2016
## 
## This WDL converts FASTQ to uBAM and adds read group information using FastqToSam
##
## Requirements/expectations :
## - Whole-genome pair-end sequencing data in FASTQ format (one file per orientation)
## - One or more read groups, one per pair of FASTQ files 
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

# Merge original input uBAM file with BWA-aligned BAM file
task FastqToSam {
  # pair-specific
  File fastq_1
  File fastq_2
  String readgroup_name
  String sample_name
  String library_name
  String platform_unit
  String run_date
  String platform_name
  String sequencing_center

  command {
    java -Xmx3000m -jar /usr/gitc/picard.jar \
      FastqToSam \
      FASTQ=${fastq_1} \
      FASTQ2=${fastq_2} \
      OUTPUT=${readgroup_name}.bam \
      READ_GROUP_NAME=${readgroup_name} \
      SAMPLE_NAME=${sample_name} \
      LIBRARY_NAME=${library_name} \
      PLATFORM_UNIT=${platform_unit} \
      RUN_DATE=${run_date} \
      PLATFORM=${platform_name} \
      SEQUENCING_CENTER=${sequencing_center} 
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
    memory: "10 GB"
    cpu: "1"
    disks: "local-disk " + 400 + " HDD"
  }
  output {
    File output_bam = "${readgroup_name}.bam"
  }
}

# WORKFLOW DEFINITION
workflow uBamFromPairedFastQ {
  Array[String] readgroup_list
  Map[String, Array[File]] fastq_pairs
  Map[String, Array[String]] metadata

  # Convert multiple pairs of input fastqs in parallel
  scatter (readgroup in readgroup_list) {

    # Convert pair of FASTQs to uBAM
    call FastqToSam {
      input:
        # pair-specific
        fastq_1 = fastq_pairs[readgroup][0],
        fastq_2 = fastq_pairs[readgroup][1],
        readgroup_name = readgroup,
        sample_name = metadata[readgroup][0],
        library_name = metadata[readgroup][1],
        platform_unit = metadata[readgroup][2],
        run_date = metadata[readgroup][3],
        platform_name = metadata[readgroup][4],
        sequencing_center = metadata[readgroup][5]
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    FastqToSam.*
  }
}

