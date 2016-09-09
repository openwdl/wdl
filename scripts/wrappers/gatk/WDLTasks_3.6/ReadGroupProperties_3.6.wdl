# --------------------------------------------------------------------------------------------
# This ReadGroupProperties WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Collect statistics about read groups and their properties
# --------------------------------------------------------------------------------------------

task ReadGroupProperties { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Int ? max_values_for_median
	String ? out

	command {
		java -jar ${gatk} \
			-T ReadGroupProperties \
			-R ${ref} \
			--input_file ${input_file} \
			-maxElementsForMedian ${default="10000" max_values_for_median} \
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
		max_values_for_median: "Calculate median from the first maxElementsForMedian values observed"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		input_file: "Input file containing sequence data (BAM or CRAM)"
	}
}
