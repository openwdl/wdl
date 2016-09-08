# --------------------------------------------------------------------------------------------
# This ValidationSiteSelector WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Randomly select variant records according to specified options
# --------------------------------------------------------------------------------------------

task ValidationSiteSelector { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	String ? frequencySelectionMode
	Boolean ? ignoreGenotypes
	Boolean ? ignorePolymorphicStatus
	Boolean ? includeFilteredSites
	Int numValidationSites
	String ? out
	String ? sample_expressions
	String ? sample_file
	String ? sample_name
	String ? sampleMode
	Float ? samplePNonref
	Array[String] ? selectTypeToInclude
	Array[String] variant

	command {
		java -jar ${gatk} \
			-T ValidationSiteSelector \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-freqMode ${default="KEEP_AF_SPECTRUM" frequencySelectionMode} \
			-ignoreGenotypes ${default="false" ignoreGenotypes} \
			-ignorePolymorphicStatus ${default="false" ignorePolymorphicStatus} \
			-ifs ${default="false" includeFilteredSites} \
			-numSites ${numValidationSites} \
			-o ${default="stdout" out} \
			${default="" "-se " + sample_expressions} \
			${default="" "-sf " + sample_file} \
			-sn ${default="[]" sample_name} \
			-sampleMode ${default="NONE" sampleMode} \
			-samplePNonref ${default="0.99" samplePNonref} \
			-selectType ${default="[]" selectTypeToInclude} \
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
		frequencySelectionMode: "Allele Frequency selection mode"
		ignoreGenotypes: "If true, will ignore genotypes in VCF, will take AC,AF from annotations and will make no sample selection"
		ignorePolymorphicStatus: "If true, will ignore polymorphic status in VCF, and will take VCF record directly without pre-selection"
		includeFilteredSites: "If true, will include filtered sites in set to choose variants from"
		numValidationSites: "Number of output validation sites"
		out: "File to which variants should be written"
		sample_expressions: "Regular expression to select many samples from the ROD tracks provided. Can be specified multiple times"
		sample_file: "File containing a list of samples (one per line) to include. Can be specified multiple times"
		sample_name: "Include genotypes from this sample. Can be specified multiple times"
		sampleMode: "Sample selection mode"
		samplePNonref: "GL-based selection mode only: the probability that a site is non-reference in the samples for which to include the site"
		selectTypeToInclude: "Select only a certain type of variants from the input file. Valid types are INDEL, SNP, MIXED, MNP, SYMBOLIC, NO_VARIATION. Can be specified multiple times"
		variant: "Input VCF file, can be specified multiple times"
		intervals: "One or more genomic intervals over which to operate"
	}
}
