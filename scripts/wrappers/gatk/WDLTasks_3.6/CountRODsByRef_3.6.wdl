# --------------------------------------------------------------------------------------------
# This CountRODsByRef WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Count the number of ROD objects encountered along the reference
# --------------------------------------------------------------------------------------------

task CountRODsByRef { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Array[String] ? rod
	Boolean ? showSkipped
	Boolean ? verbose

	command {
		java -jar ${gatk} \
			-T CountRODsByRef \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-rod ${default="[]" rod} \
			-s ${default="false" showSkipped} \
			-v ${default="false" verbose} \
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
		rod: "Input VCF file(s)"
		showSkipped: "If true, this tool will print out the skipped locations"
		verbose: "If true, this tool will print out detailed information about the rods it finds and locations"
		intervals: "One or more genomic intervals over which to operate"
	}
}
