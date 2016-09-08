# --------------------------------------------------------------------------------------------
# This PrintReads WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Write out sequence read data (for filtering, merging, subsetting etc)
# --------------------------------------------------------------------------------------------

task PrintReads { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	File ? BQSR
	Int ? nctVal
	Int ? number
	String ? out
	String ? platform
	String ? readGroup
	String ? sample_file
	String ? sample_name
	Boolean ? simplify

	command {
		java -jar ${gatk} \
			-T PrintReads \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "--BQSR " + BQSR} \
			${default="" "-nct" + nctVal} \
			-n ${default="-1" number} \
			-o ${default="stdout" out} \
			${default="" "-platform " + platform} \
			${default="" "-readGroup " + readGroup} \
			-sf ${default="[]" sample_file} \
			-sn ${default="[]" sample_name} \
			-s ${default="false" simplify} \
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
		number: "Print the first n reads from the file, discarding the rest"
		out: "Write output to this BAM filename instead of STDOUT"
		platform: "Exclude all reads with this platform from the output"
		readGroup: "Exclude all reads with this read group from the output"
		sample_file: "File containing a list of samples (one per line). Can be specified multiple times"
		sample_name: "Sample name to be included in the analysis. Can be specified multiple times."
		simplify: "Simplify all reads"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
