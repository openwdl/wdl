# --------------------------------------------------------------------------------------------
# This SimulateReadsForVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Generate simulated reads for variants
# --------------------------------------------------------------------------------------------

task SimulateReadsForVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? errorRate
	String out
	Int ? readDepth
	Int ? readLength
	String ? readSamplingMode
	String ? rgPlatform
	String variant

	command {
		java -jar ${gatk} \
			-T SimulateReadsForVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-ER ${default="20" errorRate} \
			-o ${out} \
			-DP ${default="20" readDepth} \
			-RL ${default="101" readLength} \
			-RSM ${default="CONSTANT" readSamplingMode} \
			-RGPL ${default="ILLUMINA" rgPlatform} \
			-V ${variant} \
			${default="\n" userString} 
	}

	output {
		#To track additional outputs from your task, please manually add them below
		String taskOut = "${out}"
	}

	runtime {
		docker: "broadinstitute/genomes-in-the-cloud:2.2.2-1466113830"
	}

	parameter_meta {
		gatk: "Executable jar for the GenomeAnalysisTK"
		ref: "fasta file of reference genome"
		refIndex: "Index file of reference genome"
		refDict: "dict file of reference genome"
		userString: "An optional parameter which allows the user to specify additions to the command line at run time"
		errorRate: "Base error rate (Phred-scaled)"
		out: "Reads corresponding to variants"
		readDepth: "Read depth to generate"
		readLength: "Read lengths (bp)"
		readSamplingMode: "Sampling mode"
		rgPlatform: "Sequencing platform"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
