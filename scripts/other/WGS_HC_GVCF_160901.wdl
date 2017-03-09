## Copyright Broad Institute, 2016
## 
## This WDL pipeline implements HaplotypeCaller GVCF calling according to the 
## GATK Best Practices (June 2016) for germline SNP and Indel discovery in human 
## whole-genome sequencing (WGS) data.
##
## Requirements/expectations :
## - Analysis-ready BAM produced according to Best Practices 
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
    File bam_index
    String sample_basename
    File ref_dict
    File ref_fasta
    File ref_fasta_index
    File intervals_file
    Int disk_size
    Int preemptible_tries

  command {
    java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx800m \
      -jar /usr/gitc/GATK36.jar \
      -T HaplotypeCaller \
      -R ${ref_fasta} \
      -o ${sample_basename}.g.vcf.gz \
      -I ${input_bam} \
      -L ${intervals_file} \
      -ERC GVCF 
  }

  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.3-1469027018"
    memory: "10 GB"
    cpu: "1"
    disks: "local-disk " + disk_size + " HDD"
    preemptible: preemptible_tries
  }

  output {
    File output_gvcf = "${sample_basename}.g.vcf.gz"
    File output_gvcf_index = "${sample_basename}.g.vcf.gz.tbi"
  }
}

task MergeVCFs {
  File ref_dict
  Array [File] input_vcfs
  Array [File] input_vcfs_indices
  String vcf_basename
  Int disk_size
  Int preemptible_tries

  command {
    java -Xmx2g -jar /usr/gitc/picard.jar \
    MergeVcfs \
    INPUT=${sep=' INPUT=' input_vcfs} \
    OUTPUT=${vcf_basename}.g.vcf.gz
  }

  runtime {
    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
    memory: "3 GB"
    disks: "local-disk " + disk_size + " HDD"
    preemptible: preemptible_tries
}

  output {
    File output_vcf = "${vcf_basename}.g.vcf.gz"
    File output_vcf_index = "${vcf_basename}.g.vcf.gz.tbi"
  }
}

# WORKFLOW DEFINITION 
workflow ScatterHaplotypeCaller {
  File input_bam
  File input_bam_index
  File ref_dict
  File ref_fasta
  File ref_fasta_index
  String sample_basename
  Array[File] scattered_intervals
  Int agg_preemptible_tries
  Int agg_small_disk

  # Call variants in parallel over grouped calling intervals
  scatter (interval_file in scattered_intervals) {

    # Generate GVCF by interval
    call HaplotypeCaller {
      input:
        input_bam = input_bam,
        bam_index = input_bam_index,
        intervals_file = interval_file,
        sample_basename = sample_basename,
        ref_dict = ref_dict,
        ref_fasta = ref_fasta,
        ref_fasta_index = ref_fasta_index,
        disk_size = agg_small_disk,
        preemptible_tries = agg_preemptible_tries
    }
  }

  # Merge per-interval GVCFs
  call MergeVCFs {
    input:
    ref_dict = ref_dict,
      input_vcfs = HaplotypeCaller.output_gvcf,
      input_vcfs_indices = HaplotypeCaller.output_gvcf_index,
      vcf_basename = sample_basename,
      disk_size = agg_small_disk,
      preemptible_tries = agg_preemptible_tries
  }

  # Outputs that will be retained when execution is complete
  output {
    MergeVCFs.*
  }
}