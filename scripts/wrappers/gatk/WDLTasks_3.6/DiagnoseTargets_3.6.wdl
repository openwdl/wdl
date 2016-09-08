# --------------------------------------------------------------------------------------------
# This DiagnoseTargets WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Analyze coverage distribution and validate read mates per interval and per sample
# --------------------------------------------------------------------------------------------

task DiagnoseTargets { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Float ? bad_mate_status_threshold
	Float ? coverage_status_threshold
	Float ? excessive_coverage_status_threshold
	Int ? maximum_coverage
	Int ? maximum_insert_size
	Int ? minimum_base_quality
	Int ? minimum_coverage
	Int ? minimum_mapping_quality
	String ? missing_intervals
	String ? out
	Float ? quality_status_threshold
	Float ? voting_status_threshold

	command {
		java -jar ${gatk} \
			-T DiagnoseTargets \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-stBM ${default="0.5" bad_mate_status_threshold} \
			-stC ${default="0.2" coverage_status_threshold} \
			-stXC ${default="0.2" excessive_coverage_status_threshold} \
			-max ${default="1073741823" maximum_coverage} \
			-ins ${default="500" maximum_insert_size} \
			-BQ ${default="20" minimum_base_quality} \
			-min ${default="5" minimum_coverage} \
			-MQ ${default="20" minimum_mapping_quality} \
			${default="" "-missing " + missing_intervals} \
			-o ${default="stdout" out} \
			-stQ ${default="0.5" quality_status_threshold} \
			-stV ${default="0.5" voting_status_threshold} \
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
		bad_mate_status_threshold: "The proportion of the loci needed for calling BAD_MATE"
		coverage_status_threshold: "The proportion of the loci needed for calling LOW_COVERAGE and COVERAGE_GAPS"
		excessive_coverage_status_threshold: "The proportion of the loci needed for calling EXCESSIVE_COVERAGE"
		maximum_coverage: "The maximum allowable coverage, used for calling EXCESSIVE_COVERAGE"
		maximum_insert_size: "The maximum allowed distance between a read and its mate"
		minimum_base_quality: "The minimum Base Quality that is considered for calls"
		minimum_coverage: "The minimum allowable coverage, used for calling LOW_COVERAGE"
		minimum_mapping_quality: "The minimum read mapping quality considered for calls"
		missing_intervals: "Produces a file with the intervals that don't pass filters"
		out: "File to which interval statistics should be written"
		quality_status_threshold: "The proportion of the loci needed for calling POOR_QUALITY"
		voting_status_threshold: "The needed proportion of samples containing a call for the interval to adopt the call "
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
