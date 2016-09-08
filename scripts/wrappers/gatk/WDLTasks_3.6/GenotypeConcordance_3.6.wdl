# --------------------------------------------------------------------------------------------
# This GenotypeConcordance WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Genotype concordance between two callsets
# --------------------------------------------------------------------------------------------

task GenotypeConcordance { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	String comp
	String eval
	Array[String] ? genotypeFilterExpressionComp
	Array[String] ? genotypeFilterExpressionEval
	Boolean ? ignoreFilters
	Boolean ? moltenize
	String ? out
	String ? printInterestingSites

	command {
		java -jar ${gatk} \
			-T GenotypeConcordance \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-comp ${comp} \
			-eval ${eval} \
			-gfc ${default="[]" genotypeFilterExpressionComp} \
			-gfe ${default="[]" genotypeFilterExpressionEval} \
			ignoreFilters ${default="false" ignoreFilters} \
			-moltenize ${default="false" moltenize} \
			-o ${default="stdout" out} \
			${default="" "-sites " + printInterestingSites} \
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
		comp: "The variants and genotypes to compare against"
		eval: "The variants and genotypes to evaluate"
		genotypeFilterExpressionComp: "One or more criteria to use to set COMP genotypes to no-call. These genotype-level filters are only applied to the COMP rod."
		genotypeFilterExpressionEval: "One or more criteria to use to set EVAL genotypes to no-call. These genotype-level filters are only applied to the EVAL rod."
		ignoreFilters: "Filters will be ignored"
		moltenize: "Molten rather than tabular output"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		printInterestingSites: "File to output the discordant sites and genotypes."
		intervals: "One or more genomic intervals over which to operate"
	}
}
