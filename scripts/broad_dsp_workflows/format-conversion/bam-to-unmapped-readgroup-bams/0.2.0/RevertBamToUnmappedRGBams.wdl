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
## - Successfully tested on v27
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
workflow BamToUnmappedRGBamsWf {

  File ref_fasta
  File ref_fasta_index

  File input_bam

  String picard_path
  String picard_docker

  Int preemptible_tries

  # Revert input to unmapped
  call RevertBamToUnmappedRGBams {
    input:
      input_bam = input_bam,
      picard_path = picard_path,
      docker_image = picard_docker
  }

  scatter (unmapped_bam in RevertBamToUnmappedRGBams.unmapped_bams) {

    # Get the basename, i.e. strip the filepath and the extension
    String bam_basename = basename(unmapped_bam, ".bam")

    # Sort the BAM records
    call SortBamByQueryname {
      input:
        input_bam = unmapped_bam,
        sorted_bam_name = bam_basename + ".unmapped.bam",
        picard_path = picard_path,
        docker_image = picard_docker,
        preemptible_tries = preemptible_tries
    }

    # ValidateSamFile
    call ValidateSamFile {
      input:
        input_bam = SortBamByQueryname.sorted_bam,
        report_filename = bam_basename + ".unmapped.validation_report",
        picard_path = picard_path,
        docker_image = picard_docker,
        preemptible_tries = preemptible_tries
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    Array[File] sortsam_out = SortBamByQueryname.sorted_bam
    Array[File] validatesam_out = ValidateSamFile.report
  }
}

# TASK DEFINITIONS

# Revert a BAM to uBAMs, one per readgroup
task RevertBamToUnmappedRGBams {
  File input_bam
  String output_dir

  Int disk_size
  String mem_size

  String docker_image
  String picard_path
  String java_opt

  command {
    java ${java_opt} -jar ${picard_path}picard.jar \
      RevertSam \
      INPUT=${input_bam} \
      O=${output_dir} \
      OUTPUT_BY_READGROUP=true \
      VALIDATION_STRINGENCY=LENIENT \
      ATTRIBUTE_TO_CLEAR=FT \
      ATTRIBUTE_TO_CLEAR=CO \
      SORT_ORDER=coordinate
  }
  runtime {
    docker: docker_image
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size 
  }
  output {
    Array[File] unmapped_bams = glob("*.bam")
  }
}

# Sort the BAM records by queryname
task SortBamByQueryname {
  File input_bam
  String sorted_bam_name

  Int preemptible_tries
  Int disk_size
  String mem_size

  String docker_image
  String picard_path
  String java_opt

  command {
    java ${java_opt} -jar ${picard_path}picard.jar \
      SortSam \
      INPUT=${input_bam} \
      OUTPUT=${sorted_bam_name} \
      SORT_ORDER=queryname \
      MAX_RECORDS_IN_RAM=1000000
  }
  runtime {
    docker: docker_image
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size 
    preemptible: preemptible_tries
  }
  output {
    File sorted_bam = "${sorted_bam_name}"
  }
}

# Check that the BAM format is technically valid
task ValidateSamFile {
  File input_bam
  String report_filename

  Int preemptible_tries
  Int disk_size
  String mem_size

  String docker_image
  String picard_path
  String java_opt

  command {
    java ${java_opt} -jar ${picard_path}picard.jar \
      ValidateSamFile \
      INPUT=${input_bam} \
      OUTPUT=${report_filename} \
      MODE=VERBOSE \
      IS_BISULFITE_SEQUENCED=false 
  }
  runtime {
    docker: docker_image
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size 
    preemptible: preemptible_tries 
  }
  output {
    File report = "${report_filename}"
  }
}
