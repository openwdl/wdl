## Copyright Broad Institute, 2017
## 
## This WDL workflow runs GenotypeGVCFs on a set of GVCFs to joint-call multiple 
## samples, scattered across intervals.
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

# TASK DEFINITIONS

# Unzip GVCFs 
task UnzipGVCF {
    File gzipped_gvcf
    String unzipped_basename
    Int disk_size
    String mem_size

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
	    memory: mem_size 
	    disks: "local-disk " + disk_size + " HDD"
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
    String mem_size

	command {
		java -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 -Xmx8000m \
        	-jar /usr/gitc/GATK36.jar \
        	-T GenotypeGVCFs \
        	-R ${ref_fasta} \
        	--variant ${sep=' --variant ' gvcfs} \
        	-L ${interval_list} \
        	-o ${vcf_basename}.vcf.gz 
	}

	output {
		File genotyped_vcf = "${vcf_basename}.vcf.gz"
		File genotyped_index = "${vcf_basename}.vcf.gz.tbi"
	}

	runtime {
		docker: "broadinstitute/genomes-in-the-cloud:2.2.4-1469632282"
		memory: mem_size
    	cpu: "1"
    	disks: "local-disk " + disk_size + " HDD"
	}
}

# Combine multiple VCFs 
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

workflow GenotypeGVCFsScatterWf {
  	File ref_fasta
  	File ref_fasta_index
  	File ref_dict
	Array[File] input_gvcfs
	Array[File] input_gvcf_indices
	String cohort_vcf_name
    File scattered_calling_intervals_list
  
    Array[File] scattered_calling_intervals = read_lines(scattered_calling_intervals_list)

    # Unzip GVCFs in parallel
	scatter (input_gvcf in input_gvcfs) {

		# Unzip block-compressed VCFs with .gz extension because GenotypeGVCFs 
        # currently does not handle compressed files.
	    call UnzipGVCF {
		    input:
			    gzipped_gvcf = input_gvcf,
			    unzipped_basename = "temp_unzipped"
	    }
	}

	# Joint-call variants in parallel over WGS calling intervals
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
			    interval_list = subInterval
		}
	}

	# Merge per-interval VCFs into a single cohort VCF file
    call MergeVCFs {
	    input:
		    input_vcfs = GenotypeGVCFs.genotyped_vcf,
		    input_vcfs_indices = GenotypeGVCFs.genotyped_index,
		    vcf_name = cohort_vcf_name + ".vcf.gz",
		    vcf_index = cohort_vcf_name + ".vcf.gz.tbi"
    }

  	# Outputs that will be retained when execution is complete
  	output {
  		File output_merged_vcf = MergeVCFs.output_vcf
    	File output_merged_vcf_index = MergeVCFs.output_vcf_index
    }
}
