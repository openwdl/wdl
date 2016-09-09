# --------------------------------------------------------------------------------------------
# This RealignerTargetCreator WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Define intervals to target for local realignment
# --------------------------------------------------------------------------------------------

task RealignerTargetCreator { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? ntVal
	Array[String] ? known
	Int ? maxIntervalSize
	Int ? minReadsAtLocus
	Float ? mismatchFraction
	File ? out
	Int ? windowSize

	command {
		java -jar ${gatk} \
			-T RealignerTargetCreator \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-known ${default="[]" known} \
			-maxInterval ${default="500" maxIntervalSize} \
			-minReads ${default="4" minReadsAtLocus} \
			-mismatch ${default="0.0" mismatchFraction} \
			${default="" "-o " + out} \
			-window ${default="10" windowSize} \
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
		known: "Input VCF file with known indels"
		maxIntervalSize: "maximum interval size; any intervals larger than this value will be dropped"
		minReadsAtLocus: "minimum reads at a locus to enable using the entropy calculation"
		mismatchFraction: "fraction of base qualities needing to mismatch for a position to have high entropy"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		windowSize: "window size for calculating entropy or SNP clusters"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
