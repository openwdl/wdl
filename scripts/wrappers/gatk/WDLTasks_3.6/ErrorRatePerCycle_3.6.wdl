# --------------------------------------------------------------------------------------------
# This ErrorRatePerCycle WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Compute the read error rate per position
# --------------------------------------------------------------------------------------------

task ErrorRatePerCycle { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? min_base_quality_score
	Int ? min_mapping_quality_score
	String ? out

	command {
		java -jar ${gatk} \
			-T ErrorRatePerCycle \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-mbq ${default="0" min_base_quality_score} \
			-mmq ${default="20" min_mapping_quality_score} \
			-o ${default="stdout" out} \
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
		min_base_quality_score: "Minimum base quality required to consider a base for calling"
		min_mapping_quality_score: "Minimum read mapping quality required to consider a read for calling"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
