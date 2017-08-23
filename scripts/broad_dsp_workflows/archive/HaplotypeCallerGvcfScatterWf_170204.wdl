## Copyright Broad Institute, 2017
## 
## This WDL workflow runs HaplotypeCaller in GVCF mode on a single sample, scattered 
## across intervals.
##
## Requirements/expectations :
## - One analysis-ready BAM file for a single sample (as identified in RG:SM)
## - Set of variant calling intervals lists for the scatter, provided in a file
##
## Outputs :
## - One GVCF file and its index
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

# HaplotypeCaller per-sample in GVCF mode
task HaplotypeCaller {
  File input_bam
  File input_bam_index
  String gvcf_name
  String gvcf_index
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  File interval_list
  Int? interval_padding
  Int disk_size
  String mem_size

  command {
    java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx800m \
      -jar /usr/gitc/GATK36.jar \
      -T HaplotypeCaller \
      -R ${ref_fasta} \
      -I ${input_bam} \
      -o ${gvcf_name} \
      -L ${interval_list} \
      -ip ${default=100 interval_padding} \
      -ERC GVCF 
  }

  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
    cpu: "1"
    memory: mem_size 
    disks: "local-disk " + disk_size + " HDD"
  }

  output {
    File output_gvcf = "${gvcf_name}"
    File output_gvcf_index = "${gvcf_index}"
  }
}

# Merge GVCFs generated per-interval for the same sample
task MergeVCFs {
  Array [File] input_vcfs
  Array [File] input_vcfs_indices
  String vcf_name
  String vcf_index
  Int disk_size
  String mem_size

  command {
    java -Xmx2g -jar /usr/gitc/picard.jar \
    MergeVcfs \
    INPUT=${sep=' INPUT=' input_vcfs} \
    OUTPUT=${vcf_name}
  }

  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
    memory: mem_size
    disks: "local-disk " + disk_size + " HDD"
}

  output {
    File output_vcf = "${vcf_name}"
    File output_vcf_index = "${vcf_index}"
  }
}

# WORKFLOW DEFINITION 
workflow HaplotypeCallerGvcfScatterWf {
  File input_bam
  File input_bam_index
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  File scattered_calling_intervals_list
  
  Array[File] scattered_calling_intervals = read_lines(scattered_calling_intervals_list)

  String sub_strip_path = "gs://.*/"
  String sub_strip_suffix = ".bam$"

  String sample_basename = sub(sub(input_bam, sub_strip_path, ""), sub_strip_suffix, "")
  
  String gvcf_name = sample_basename + ".g.vcf.gz"
  String gvcf_index = sample_basename + ".g.vcf.gz.tbi"

  # Call variants in parallel over grouped calling intervals
  scatter (interval_file in scattered_calling_intervals) {

    # Generate GVCF by interval
    call HaplotypeCaller {
      input:
        input_bam = input_bam,
        input_bam_index = input_bam_index,
        interval_list = interval_file,
        gvcf_name = gvcf_name,
        gvcf_index = gvcf_index,
        ref_dict = ref_dict,
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index
    }
  }

  # Merge per-interval GVCFs
  call MergeVCFs {
    input:
      input_vcfs = HaplotypeCaller.output_gvcf,
      input_vcfs_indices = HaplotypeCaller.output_gvcf_index,
      vcf_name = gvcf_name,
      vcf_index = gvcf_index
  }

  # Outputs that will be retained when execution is complete
  output {
    File output_merged_gvcf = MergeVCFs.output_vcf
    File output_merged_gvcf_index = MergeVCFs.output_vcf_index
  }
}