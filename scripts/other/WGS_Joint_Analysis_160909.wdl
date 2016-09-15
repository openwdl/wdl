## Copyright Broad Institute, 2016
## 
## This WDL pipeline implements joint analysis (joint genotyping, variant filtering 
## and genotype refinement) according to the GATK Best Practices (June 2016) for 
## germline SNP and Indel discovery in human whole-genome sequencing (WGS) data.
##
## DEV NOTE: STILL NEED TO ADD GENOTYPE REFINEMENT
##
## Requirements/expectations :
## - GVCFs produced by HaplotypeCaller in GVCF mode from WGS data 
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

# Unzip GVCFs because GenotypeGVCFs is picky
task UnzipGVCF {
    File gzipped_gvcf
    String unzipped_basename
    File ref_dict
    Int disk_size
    Int preemptible_tries

    # HACK ALERT! Using .gvcf extension here to force IndexFeatureFile to make the right 
    # kind of index, but afterward we need to change to .g.vcf which is the correct 
    # for GVCFs.
    command <<<
	gunzip -c ${gzipped_gvcf} > ${unzipped_basename}.gvcf
    java -Xmx2g -jar /usr/gitc/GATK4.jar IndexFeatureFile -F ${unzipped_basename}.gvcf
    mv ${unzipped_basename}.gvcf ${unzipped_basename}.g.vcf
    mv ${unzipped_basename}.gvcf.idx ${unzipped_basename}.g.vcf.idx
    >>>

	runtime {
	    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
	    memory: "3 GB"
	    disks: "local-disk " + disk_size + " HDD"
	    preemptible: preemptible_tries
	}

    output {
	    File unzipped_gvcf = "${unzipped_basename}.g.vcf"
	    File gvcf_index = "${unzipped_basename}.g.vcf.idx"
    }
}

# Perform joint-genotyping
task GenotypeGVCFs { 
	Array[File] gvcfs
    Array[File] gvcf_indices
    String vcf_basename
    File ref_dict
    File ref_fasta
    File ref_fasta_index
  	File interval_list
    Int disk_size
    Int preemptible_tries

	command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
        	-T GenotypeGVCFs \
        	-R ${ref_fasta} \
        	--variant ${sep=' --variant ' gvcfs} \
        	-L ${interval_list} \
        	-o ${vcf_basename}.gz 
	}

	output {
		File genotyped_vcf = "${vcf_basename}.gz"
		File genotyped_index = "${vcf_basename}.gz.tbi"
	}

	runtime {
		docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
		memory: "10 GB"
    	cpu: "1"
    	disks: "local-disk " + disk_size + " HDD"
    	preemptible: preemptible_tries
	}
}

# Combine multiple VCFs from scattered GenotypeGVCFs runs
task MergeVCFs {
    File ref_dict
    Array [File] input_vcfs
    Array [File] input_vcfs_indices
    String cohort_vcf_name
    Int disk_size
    Int preemptible_tries

    command {
	    java -Xmx2g -jar /usr/gitc/picard.jar \
	    MergeVcfs \
	    INPUT=${sep=' INPUT=' input_vcfs} \
	    OUTPUT=${cohort_vcf_name}.vcf.gz
    }

  	runtime {
	    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
	    memory: "3 GB"
	    disks: "local-disk " + disk_size + " HDD"
	    preemptible: preemptible_tries
	}

    output {
	    File output_vcf = "${cohort_vcf_name}.vcf.gz"
	    File output_vcf_index = "${cohort_vcf_name}.vcf.gz.tbi"
    }
}

workflow JointAnalysis {
  	String cohort_vcf_name
  	File ref_fasta
  	File ref_fasta_index
  	File ref_dict
	Array[File] input_gvcfs
	Array[File] input_gvcf_indices
	Array[File] scattered_calling_intervals
    String cohort_vcf_name
    Int preemptible_tries
    Int small_disk

    # Unzip GVCFs 
	scatter (input_gvcf in input_gvcfs) {

	    call UnzipGVCF {
		    input:
			    gzipped_gvcf = input_gvcf,
			    unzipped_basename = "temp_unzipped",
			    ref_dict = ref_dict,
			    disk_size = small_disk,
			    preemptible_tries = preemptible_tries
	    }
	}

	# Joint-genotype variants in parallel over WGS calling intervals
  	scatter (subInterval in scattered_calling_intervals) {

  		# Perform joint genotyping per interval
		call GenotypeGVCFs {
			input:
			    gvcfs = UnzipGVCF.unzipped_gvcf,
			    gvcf_indices = UnzipGVCF.gvcf_index,
			    vcf_basename = cohort_vcf_name,
			    ref_dict = ref_dict,
			    ref_fasta = ref_fasta,
			    ref_fasta_index = ref_fasta_index,
			    interval_list = subInterval,
			    disk_size = small_disk,
			    preemptible_tries = preemptible_tries
		}
	}

	# Merge per-interval VCFs into a single cohort VCF file
    call MergeVCFs {
	    input:
		    ref_dict = ref_dict,
		    input_vcfs = GenotypeGVCFs.genotyped_vcf,
		    input_vcfs_indices = GenotypeGVCFs.genotyped_index,
		    cohort_vcf_name = cohort_vcf_name,
		    disk_size = small_disk,
		    preemptible_tries = preemptible_tries
    }

    ### ADD GENOTYPE REFINEMENT HERE

  	# Outputs that will be retained when execution is complete
  	output {
 		MergeVCFs.*
    }
}

