# --------------------------------------------------------------------------------------------
# This QualifyMissingIntervals WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Collect quality metrics for a set of intervals
# --------------------------------------------------------------------------------------------

task QualifyMissingIntervals { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? nctVal
	String ? baitsfile
	Int ? coveragethreshold
	Float ? gcthreshold
	String ? intervalsizethreshold
	String ? mappingthreshold
	String ? out
	String ? qualthreshold
	String targetsfile

	command {
		java -jar ${gatk} \
			-T QualifyMissingIntervals \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "-nct" + nctVal} \
			${default="" "-baits " + baitsfile} \
			-cov ${default="20" coveragethreshold} \
			-gc ${default="0.3" gcthreshold} \
			-size ${default="10" intervalsizethreshold} \
			-mmq ${default="20" mappingthreshold} \
			-o ${default="stdout" out} \
			-mbq ${default="20" qualthreshold} \
			-targets ${targetsfile} \
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
		baitsfile: "Undocumented option"
		coveragethreshold: "minimum coverage to be considered sequenceable"
		gcthreshold: "upper and lower bound for an interval to be considered high/low GC content"
		intervalsizethreshold: "minimum interval length to be considered"
		mappingthreshold: "minimum mapping quality for it to be considered usable"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		qualthreshold: "minimum base quality for it to be considered usable"
		targetsfile: "Undocumented option"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
