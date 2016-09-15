## Copyright Broad Institute, 2016
## 
## This WDL pipeline implements VQSR filtering according to the GATK Best Practices 
## (June 2016) for germline SNP and Indel discovery in human whole-genome sequencing 
## (WGS) data.
##
## Requirements/expectations :
## - Cohort VCF produced by GenotypeGVCFs from WGS data 
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

# Build VQSR model
task BuildVQSRModel {
    File ref_dict
    File ref_fasta 
    File ref_fasta_index
    File cohort_vcf
    File cohort_vcf_index
    String output_basename
    String mode
    Array[String] annotations
    Array[Float] tranches
	Array[String] resources
	Array[File] resource_files
	Array[File] resource_indices
    Int disk_size
    Int preemptible_tries

    command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
			-T VariantRecalibrator \
			-R ${ref_fasta} \
			-input ${cohort_vcf} \
	        -resource:${sep=' -resource:' resources} \
	        -an ${sep=' -an ' annotations} \
	        -mode ${mode} \
	        -tranche ${sep=' -tranche ' tranches} \
	        -recalFile ${output_basename}.${mode}.recal \
	        -tranchesFile ${output_basename}.${mode}.tranches \
	        -rscriptFile ${output_basename}.${mode}.plots.R
    }

	runtime {
	    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
	    memory: "2 GB"
	    disks: "local-disk " + disk_size + " HDD"
	    preemptible: preemptible_tries
	}

    output {
	    File recal_file = "${output_basename}.${mode}.recal"
	    File recal_file_index = "${output_basename}.${mode}.recal.idx"
	    File tranches_file = "${output_basename}.${mode}.tranches"
	    File rscript_file = "${output_basename}.${mode}.plots.R"
    }
}

# Apply recalibration
task ApplyRecalibrationFilter {
    File ref_dict
    File ref_fasta 
    File ref_fasta_index
    File cohort_vcf
    File cohort_vcf_index
    File recal_file
    File recal_file_index
    String output_basename
    String mode
    File tranches_file
    Float filter_level
    Int disk_size
    Int preemptible_tries

    command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
			-T ApplyRecalibration \
			-R ${ref_fasta} \
			-input ${cohort_vcf} \
	        -mode ${mode} \
	        --ts_filter_level ${filter_level} \
	        -recalFile ${recal_file} \
	        -tranchesFile ${tranches_file} \
	        -o ${output_basename}.vcf.gz
    }

	runtime {
	    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
	    memory: "2 GB"
	    disks: "local-disk " + disk_size + " HDD"
	    preemptible: preemptible_tries
	}

    output {
	    File recalibrated_vcf = "${output_basename}.vcf.gz"
	    File recalibrated_vcf_index = "${output_basename}.vcf.gz.tbi"
    }
}

workflow JustVQSR {
  	File ref_fasta
  	File ref_fasta_index
  	File ref_dict
	File input_vcf
	File input_vcf_index
	Array[String] SNP_annotations
	Array[String] INDEL_annotations
	Array[Float] SNP_tranches
	Array[Float] INDEL_tranches
	Array[String] SNP_resources
	Array[String] INDEL_resources
	Array[File] resource_files
	Array[File] resource_indices
    String cohort_vcf_name
    Float SNP_filter_level
    Float INDEL_filter_level
    Int preemptible_tries
    Int small_disk

    # Build SNP model 
    call BuildVQSRModel as BuildVQSRModelForSNPs {
	    input:
		  	ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = input_vcf,
    		cohort_vcf_index = input_vcf_index,
    		output_basename = cohort_vcf_name,
    		annotations = SNP_annotations,
    		mode = "SNP",
    		tranches = SNP_tranches,
    		resources = SNP_resources,
			resource_files = resource_files,
			resource_indices = resource_indices,
		    disk_size = small_disk,
		    preemptible_tries = preemptible_tries
    }

    # Build INDEL model 
    call BuildVQSRModel as BuildVQSRModelForINDELs {
	    input:
		  	ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = input_vcf,
    		cohort_vcf_index = input_vcf_index,
    		output_basename = cohort_vcf_name,
    		annotations = INDEL_annotations,
    		mode = "INDEL",
    		tranches = INDEL_tranches,
    		resources = INDEL_resources,
			resource_files = resource_files,
			resource_indices = resource_indices,
		    disk_size = small_disk,
		    preemptible_tries = preemptible_tries
    }

    # Apply SNP filter
    call ApplyRecalibrationFilter as ApplyRecalibrationFilterForSNPs {
    	input:
    		ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = input_vcf,
    		cohort_vcf_index = input_vcf_index,
    		output_basename = cohort_vcf_name + ".recalibrated.SNP",
    		mode = "SNP",
		    recal_file = BuildVQSRModelForSNPs.recal_file,
		    recal_file_index = BuildVQSRModelForSNPs.recal_file_index,
		    tranches_file = BuildVQSRModelForSNPs.tranches_file,
		    filter_level = SNP_filter_level,
		    disk_size = small_disk,
		    preemptible_tries = preemptible_tries
    }

    # Apply INDEL filter
    call ApplyRecalibrationFilter as ApplyRecalibrationFilterForINDELs {
    	input:
    		ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = ApplyRecalibrationFilterForSNPs.recalibrated_vcf,
    		cohort_vcf_index = ApplyRecalibrationFilterForSNPs.recalibrated_vcf_index,
    		output_basename = cohort_vcf_name + ".recalibrated.SNP.INDEL",
    		mode = "INDEL",
		    recal_file = BuildVQSRModelForINDELs.recal_file,
		    recal_file_index = BuildVQSRModelForINDELs.recal_file_index,
		    tranches_file = BuildVQSRModelForINDELs.tranches_file,
		    filter_level = INDEL_filter_level,
		    disk_size = small_disk,
		    preemptible_tries = preemptible_tries
    }

  	# Outputs that will be retained when execution is complete
  	output {
 		BuildVQSRModelForSNPs.*
 		BuildVQSRModelForINDELs.*
 		ApplyRecalibrationFilterForSNPs.*
 		ApplyRecalibrationFilterForINDELs.*
    }
}

