# --------------------------------------------------------------------------------------------
# This CountIntervals WDL task was generated on 10/04/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Count contiguous regions in an interval list
# --------------------------------------------------------------------------------------------

task CountIntervals { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Array[String] ? check
	Int ? numOverlaps
	String ? out

	command {
		java -jar ${gatk} \
			-T CountIntervals \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-check ${default="[]" check} \
			-no ${default="2" numOverlaps} \
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
		check: "Any number of RODs"
		numOverlaps: "Count all occurrences of X or more overlapping intervals; defaults to 2"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		intervals: "One or more genomic intervals over which to operate"
	}
}

workflow CountIntervalsWf { 
	call CountIntervals
}
