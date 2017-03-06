## Copyright Broad Institute, 2017
## 
## This WDL workflow runs VQSR filtering on a VCF.
##
## Requirements/expectations :
## - VCF produced by HaplotypeCaller or GenotypeGVCFs
## - Bare minimum 1 WGS sample or 30 Exome samples. Gene panels are not supported.
##
## Outputs :
## - A VCF file to which VQSR filtering has been applied (all sites are retained; 
## filtered sites are so annotated in the FILTER field).
##
## Note about VQSR wiring :
## The SNP and INDEL models are built in parallel, but then the corresponding 
## recalibrations are applied in series. Because the INDEL model is generally ready 
## first (because there are fewer indels than SNPs) we set INDEL recalibration to 
## be applied first to the input VCF, while the SNP model is still being built. By 
## the time the SNP model is available, the indel-recalibrated file is available to 
## serve as input to apply the SNP recalibration. If we did it the other way around, 
## we would have to wait until the SNP recal file was available despite the INDEL 
## recal file being there already, then apply SNP recalibration, then apply INDEL 
## recalibration. This would lead to a longer wall clock time for complete workflow 
## execution. Wiring the INDEL recalibration to be applied first solves the problem.
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

# Build VQSR model
task BuildVQSRModel {
    File ref_dict
    File ref_fasta 
    File ref_fasta_index
    File cohort_vcf
    File cohort_vcf_index
    File interval_list
    String output_basename
    String mode
    Array[String] annotations
    Array[Float] tranches
	Array[String] resources
	Array[File] resource_files
	Array[File] resource_indices
    Int disk_size
    String mem_size

    command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
			-T VariantRecalibrator \
			-R ${ref_fasta} \
			-input ${cohort_vcf} \
            -L ${interval_list} \
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
	    memory: mem_size
	    disks: "local-disk " + disk_size + " HDD"
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
    File interval_list
    String output_basename
    String mode
    File tranches_file
    Float filter_level
    Int disk_size
    String mem_size

    command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
			-T ApplyRecalibration \
			-R ${ref_fasta} \
			-input ${cohort_vcf} \
            -L ${interval_list} \
	        -mode ${mode} \
	        --ts_filter_level ${filter_level} \
	        -recalFile ${recal_file} \
	        -tranchesFile ${tranches_file} \
	        -o ${output_basename}.vcf.gz
    }

	runtime {
	    docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
	    memory: mem_size
	    disks: "local-disk " + disk_size + " HDD"
	}

    output {
	    File recalibrated_vcf = "${output_basename}.vcf.gz"
	    File recalibrated_vcf_index = "${output_basename}.vcf.gz.tbi"
    }
}

workflow VariantRecalibrationWf {
  	File ref_fasta
  	File ref_fasta_index
  	File ref_dict
	File input_vcf
	File input_vcf_index
    File calling_intervals_list
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

    # Build SNP model 
    call BuildVQSRModel as BuildVQSRModelForSNPs {
	    input:
		  	ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = input_vcf,
    		cohort_vcf_index = input_vcf_index,
            interval_list = calling_intervals_list,
    		output_basename = cohort_vcf_name,
    		annotations = SNP_annotations,
    		mode = "SNP",
    		tranches = SNP_tranches,
    		resources = SNP_resources,
			resource_files = resource_files,
			resource_indices = resource_indices
    }

    # Build INDEL model 
    call BuildVQSRModel as BuildVQSRModelForINDELs {
	    input:
		  	ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
		    cohort_vcf = input_vcf,
    		cohort_vcf_index = input_vcf_index,
            interval_list = calling_intervals_list,
    		output_basename = cohort_vcf_name,
    		annotations = INDEL_annotations,
    		mode = "INDEL",
    		tranches = INDEL_tranches,
    		resources = INDEL_resources,
			resource_files = resource_files,
			resource_indices = resource_indices
    }

    # Apply INDEL filter (first because INDEL model is usually done sooner)
    call ApplyRecalibrationFilter as ApplyRecalibrationFilterForINDELs {
        input:
            ref_dict = ref_dict,
            ref_fasta = ref_fasta,
            ref_fasta_index = ref_fasta_index,
            cohort_vcf = input_vcf,
            cohort_vcf_index = input_vcf_index,
            interval_list = calling_intervals_list,
            output_basename = cohort_vcf_name + ".recal.INDEL",
            mode = "INDEL",
            recal_file = BuildVQSRModelForINDELs.recal_file,
            recal_file_index = BuildVQSRModelForINDELs.recal_file_index,
            tranches_file = BuildVQSRModelForINDELs.tranches_file,
            filter_level = INDEL_filter_level
    }

    # Apply SNP filter
    call ApplyRecalibrationFilter as ApplyRecalibrationFilterForSNPs {
    	input:
    		ref_dict = ref_dict,
			ref_fasta = ref_fasta,
			ref_fasta_index = ref_fasta_index,
            cohort_vcf = ApplyRecalibrationFilterForINDELs.recalibrated_vcf,
            cohort_vcf_index = ApplyRecalibrationFilterForINDELs.recalibrated_vcf_index,
            interval_list = calling_intervals_list,
    		output_basename = cohort_vcf_name + ".recal.INDEL.SNP",
    		mode = "SNP",
		    recal_file = BuildVQSRModelForSNPs.recal_file,
		    recal_file_index = BuildVQSRModelForSNPs.recal_file_index,
		    tranches_file = BuildVQSRModelForSNPs.tranches_file,
		    filter_level = SNP_filter_level
    }

  	# Outputs that will be retained when execution is complete
  	output {
  		File snp_tranches = BuildVQSRModelForSNPs.tranches_file
  		File indel_tranches = BuildVQSRModelForINDELs.tranches_file
 		File fully_filtered_vcf = ApplyRecalibrationFilterForINDELs.recalibrated_vcf
 		File fully_filtered_vcf_idx = ApplyRecalibrationFilterForINDELs.recalibrated_vcf_index
    }
}