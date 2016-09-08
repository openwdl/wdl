# --------------------------------------------------------------------------------------------
# This GATKPaperGenotyper WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Simple Bayesian genotyper used in the original GATK paper
# --------------------------------------------------------------------------------------------

task GATKPaperGenotyper { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? ntVal
	Float ? log_odds_score
	String ? out

	command {
		java -jar ${gatk} \
			-T GATKPaperGenotyper \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-LOD ${default="3.0" log_odds_score} \
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
		log_odds_score: "The LOD threshold for us to call confidently a genotype"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
