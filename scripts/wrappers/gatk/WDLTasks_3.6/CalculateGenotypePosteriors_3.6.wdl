# --------------------------------------------------------------------------------------------
# This CalculateGenotypePosteriors WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Calculate genotype posterior likelihoods given panel data
# --------------------------------------------------------------------------------------------

task CalculateGenotypePosteriors { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Boolean ? defaultToAC
	Float ? deNovoPrior
	Boolean ? discoveredACpriorsOff
	Float ? globalPrior
	Boolean ? ignoreInputSamples
	Int ? numRefSamplesIfNoCall
	String ? out
	Boolean ? skipFamilyPriors
	Boolean ? skipPopulationPriors
	Array[String] ? supporting
	String variant

	command {
		java -jar ${gatk} \
			-T CalculateGenotypePosteriors \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-useAC ${default="false" defaultToAC} \
			-DNP ${default="1.0E-6" deNovoPrior} \
			-useACoff ${default="false" discoveredACpriorsOff} \
			-G ${default="0.001" globalPrior} \
			-ext ${default="false" ignoreInputSamples} \
			-nrs ${default="0" numRefSamplesIfNoCall} \
			-o ${default="stdout" out} \
			-skipFam ${default="false" skipFamilyPriors} \
			-skipPop ${default="false" skipPopulationPriors} \
			-supporting ${default="[]" supporting} \
			-V ${variant} \
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
		defaultToAC: "Use the AC field as opposed to MLEAC. Does nothing if VCF lacks MLEAC field"
		deNovoPrior: "The de novo mutation prior"
		discoveredACpriorsOff: "Do not use discovered allele count in the input callset for variants that do not appear in the external callset. "
		globalPrior: "The global Dirichlet prior parameters for the allele frequency"
		ignoreInputSamples: "Use external information only; do not inform genotype priors by the discovered allele frequency in the callset whose posteriors are being calculated. Useful for callsets containing related individuals."
		numRefSamplesIfNoCall: "The number of homozygous reference to infer were seen at a position where an other callset contains no site or genotype information"
		out: "File to which variants should be written"
		skipFamilyPriors: "Skip application of family-based priors"
		skipPopulationPriors: "Skip application of population-based priors"
		supporting: "Other callsets to use in generating genotype posteriors"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
