## Copyright Broad Institute, 2017
## 
## This WDL extracts the headers from a list of SAM/BAMs
##
## Requirements/expectations :
## - List of valid SAM or BAM files
##
## Outputs: 
## - Set of .txt files containing the header, one per input file
##
## Cromwell version support 
## - Successfully tested on v24
## - Does not work on versions < v23 due to output syntax
##
## Runtime parameters are optimized for Broad's Google Cloud Platform implementation. 
## For program versions, see docker containers. 
##
## Note that this is a really dumb way to get a SAM/BAM header when running on GCP 
## because it will require localizing the entire SAM/BAM file, which can take a while. 
## A much better way is to use gsutil like this:
##
##     gsutil cp gs://bucket/path/your.bam - | samtools view -H -
##
## And yes there's a weird trailing dash (-) there at the end; it's not a typo, leave 
## it in. 
##
## If you're running locally or on a cloud platform that doesn't require localizing 
## files then it should be fine. 
##
## LICENSING : 
## This script is released under the WDL source code license (BSD-3) (see LICENSE in 
## https://github.com/broadinstitute/wdl). Note however that the programs it calls may 
## be subject to different licenses. Users are responsible for checking that they are
## authorized to run all programs before running this script. Please see the docker 
## page at https://hub.docker.com/r/broadinstitute/genomes-in-the-cloud/ for detailed
## licensing information pertaining to the included programs.

# TASK DEFINITIONS

# Extract the header from a SAM or BAM using samtools view
task ExtractSAMHeader {
  File bam_file
  String output_name
  Int disk_size
  String mem_size

  command {
    samtools view -H ${bam_file} > ${output_name}
  }
  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.3-1469027018"
    memory: mem_size
    cpu: "1"
    disks: "local-disk " + disk_size + " HDD"
  }
  output {
    File output_header = "${output_name}"
  }
}

# WORKFLOW DEFINITION
workflow ExtractSamHeadersWf {
  Array[File] bam_list

  # Process the input files in parallel
  scatter (input_bam in bam_list) {

    String sub_strip_path = "gs://.*/"
    String sub_strip_suffix = ".bam$"

    # Extract the header to a text file
    call ExtractSAMHeader {
      input:
        bam_file = input_bam,
        output_name = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, "") + ".header.txt"
    }
  }

  # Outputs that will be retained when execution is complete
  output {
    Array[File] output_headers = ExtractSAMHeader.output_header
  }
}

