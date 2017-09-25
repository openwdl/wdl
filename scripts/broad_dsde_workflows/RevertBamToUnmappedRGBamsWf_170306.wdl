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

# TASK DEFINITIONS

# Split sample BAM into per-readgroup BAMs
task SplitReadsByRG {
  File input_bam
  File input_bam_index
  Int disk_size
  String mem_size

  command {
    java -Xmx4000m -jar /usr/gitc/GATK4.jar \
      SplitReads \
      -I ${input_bam} \
      -O . \
      -RG 
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size
  }
  output {
    Array[File] readgroup_bams = glob("*.bam")
  }
}

# Revert a BAM to uBAM
task RevertBamToUnmapped {
  File input_bam
  String output_basename
  Float? max_discard_pct
  Int disk_size
  String mem_size

  String output_name = "${output_basename}.bam"

  command {
    java -Xmx4000m -jar /usr/gitc/picard.jar \
    RevertSam \
    INPUT=${input_bam} \
    O=${output_name} \
    OUTPUT_BY_READGROUP=false \
    VALIDATION_STRINGENCY=LENIENT \
    SANITIZE=TRUE \
    MAX_DISCARD_FRACTION=${max_discard_pct} \
    ATTRIBUTE_TO_CLEAR=FT \
    SORT_ORDER=queryname 
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.5-1486412288"
    disks: "local-disk " + disk_size + " HDD"
    memory: mem_size
  }
  output {
    File unmapped_bam = "${output_name}"
  }
}

# WORKFLOW DEFINITION
workflow RevertBamToUnmappedRGBamsWf {
  File input_bam
  File ref_fasta
  File ref_fasta_index

  # Split input BAM by readgroup
  call SplitReadsByRG {
    input: 
      input_bam = input_bam
  }

  scatter (readgroup_bam in SplitReadsByRG.readgroup_bams) {

    String sub_strip_path = "gs://.*/"
    String sub_strip_suffix = ".bam$"

    # Revert readgroup BAMs to unmapped
    call RevertBamToUnmapped {
      input:
        input_bam = readgroup_bam,
        output_basename = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, "") + ".unmapped"
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    Array[File] unmapped_bams_output=RevertBamToUnmapped.unmapped_bam
  }
}
