## Copyright Broad Institute, 2017
## 
## This WDL workflow runs GenotypeGVCFs on a set of GVCFs to joint-call multiple 
## samples, scattered across intervals. Works with GATK4 only.
##
## Requirements/expectations :
## - One or more GVCFs produced by HaplotypeCaller in GVCF mode 
##
## Outputs :
## - A VCF file and its index, with genotypes for all samples represented in the 
##   GVCF inputs.
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

workflow GenotypeGVCFs {
  	File ref_fasta
  	File ref_fasta_index
  	File ref_dict
	Array[File] input_gvcfs
	Array[File] input_gvcf_indices
	String cohort_name
    File scatter_intervals_list
  
    Array[String] scatter_intervals = read_lines(scatter_intervals_list)

	# Joint-call variants in parallel over WGS calling intervals
  	scatter (interval in scatter_intervals) {

  		# Perform joint genotyping per interval
		call CombineAndGenotypeGVCFs {
			input:
			    gvcfs = input_gvcfs,
                gvcf_indices = input_gvcf_indices,
			    vcf_basename = cohort_name,
                output_vcf = cohort_name + ".vcf.gz",
                output_vcf_index = cohort_name + ".vcf.gz.tbi",
			    ref_dict = ref_dict,
			    ref_fasta = ref_fasta,
			    ref_fasta_index = ref_fasta_index,
			    interval_list = interval
		}
	}

	# Merge per-interval VCFs into a single cohort VCF file
    call MergeIntervalVCFs {
	    input:
		    input_vcfs = GenotypeGVCFs.genotyped_vcf,
		    input_vcfs_indices = GenotypeGVCFs.genotyped_vcf_index,
		    output_vcf = cohort_name + ".vcf.gz",
		    output_vcf_index = cohort_name + ".vcf.gz.tbi"
    }

  	# Outputs that will be retained when execution is complete
  	output {
  		File output_merged_vcf = MergeVCFs.merged_vcf
    	File output_merged_vcf_index = MergeVCFs.merged_vcf_index
    }
}

# TASK DEFINITIONS

# Combine input GVCFs into a GenomicsDB then perform joint-genotyping
task CombineAndGenotypeGVCFs { 
    File ref_dict
    File ref_fasta
    File ref_fasta_index
    Array[File] gvcfs
    Array[File] gvcf_indices
    String genomics_db
    String vcf_basename
    String output_vcf 
    String output_vcf_index 
    File interval_list
    Int disk_size
    String mem_size
    String docker
    String jar_path
    String? java_opt_import
    String? java_opt_genotype

    # Here we are piping the commands because GenomicsDB is weirdly
    # dependent on file location
    command <<<

        java ${java_opt} -jar ${jar_path} ImportGenomicsDB \
            -V ${sep=' -V ' gvcfs} \
            -L ${interval_list} \
            --genomicsDBWorkspace ${genomics_db} 

        java ${java_opt} -jar ${jar_path} GenotypeGVCFs \
            -R ${ref_fasta} \
            -V gendb://${genomics_db} \
            -G StandardAnnotation \
            -newQual \
            -O ${output_vcf}
    >>>

    output {
        File genotyped_vcf = output_vcf
        File genotyped_vcf_index = output_vcf_index
    }

    runtime {
        docker: docker
        memory: mem_size
        cpu: "1"
        disks: "local-disk " + disk_size + " HDD"
    }
}

# Combine multiple VCFs ### TODO: check whether we are still using Picard for this
task MergeIntervalVCFs {
    Array [File] input_vcfs
    Array [File] input_vcfs_indices
    String output_vcf
    String output_vcf_index
    Int disk_size
    String mem_size
    String docker

    command {
        java ${java_opt} -jar ${jar_path} MergeVcfs \
        INPUT=${sep=' INPUT=' input_vcfs} \
        OUTPUT=${output_vcf}
    }

    runtime {
        docker: docker
        memory: mem_size
        disks: "local-disk " + disk_size + " HDD"
    }

    output {
        File merged_vcf = output_vcf
        File merged_vcf_index = output_vcf_index
    }
}