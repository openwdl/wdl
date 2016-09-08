# --------------------------------------------------------------------------------------------
# This SelectVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Select a subset of variants from a larger callset
# --------------------------------------------------------------------------------------------

task SelectVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	String ? concordance
	String ? discordance
	String ? exclude_sample_expressions
	String ? exclude_sample_file
	String ? exclude_sample_name
	Boolean ? excludeFiltered
	File ? excludeIDs
	Boolean ? excludeNonVariants
	Boolean ? forceValidOutput
	Boolean ? invertMendelianViolation
	Boolean ? invertselect
	File ? keepIDs
	Boolean ? keepOriginalAC
	Boolean ? keepOriginalDP
	Int ? maxFilteredGenotypes
	Float ? maxFractionFilteredGenotypes
	Int ? maxIndelSize
	Float ? maxNOCALLfraction
	Int ? maxNOCALLnumber
	Boolean ? mendelianViolation
	Float ? mendelianViolationQualThreshold
	Int ? minFilteredGenotypes
	Float ? minFractionFilteredGenotypes
	Int ? minIndelSize
	String ? out
	Boolean ? preserveAlleles
	Float ? remove_fraction_genotypes
	Boolean ? removeUnusedAlternates
	String ? restrictAllelesTo
	String ? sample_expressions
	String ? sample_file
	String ? sample_name
	Float ? select_random_fraction
	Array[String] ? selectexpressions
	Array[String] ? selectTypeToExclude
	Array[String] ? selectTypeToInclude
	Boolean ? setFilteredGtToNocall
	String variant

	command {
		java -jar ${gatk} \
			-T SelectVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			${default="" "-conc " + concordance} \
			${default="" "-disc " + discordance} \
			-xl_se ${default="[]" exclude_sample_expressions} \
			-xl_sf ${default="[]" exclude_sample_file} \
			-xl_sn ${default="[]" exclude_sample_name} \
			-ef ${default="false" excludeFiltered} \
			${default="" "-xlIDs " + excludeIDs} \
			-env ${default="false" excludeNonVariants} \
			forceValidOutput ${default="false" forceValidOutput} \
			-invMv ${default="false" invertMendelianViolation} \
			-invertSelect ${default="false" invertselect} \
			${default="" "-IDs " + keepIDs} \
			-keepOriginalAC ${default="false" keepOriginalAC} \
			-keepOriginalDP ${default="false" keepOriginalDP} \
			maxFilteredGenotypes ${default="2147483647" maxFilteredGenotypes} \
			maxFractionFilteredGenotypes ${default="1.0" maxFractionFilteredGenotypes} \
			maxIndelSize ${default="2147483647" maxIndelSize} \
			maxNOCALLfraction ${default="1.0" maxNOCALLfraction} \
			maxNOCALLnumber ${default="2147483647" maxNOCALLnumber} \
			-mv ${default="false" mendelianViolation} \
			-mvq ${default="0.0" mendelianViolationQualThreshold} \
			minFilteredGenotypes ${default="0" minFilteredGenotypes} \
			minFractionFilteredGenotypes ${default="0.0" minFractionFilteredGenotypes} \
			minIndelSize ${default="0" minIndelSize} \
			-o ${default="stdout" out} \
			-noTrim ${default="false" preserveAlleles} \
			-fractionGenotypes ${default="0.0" remove_fraction_genotypes} \
			-trimAlternates ${default="false" removeUnusedAlternates} \
			-restrictAllelesTo ${default="ALL" restrictAllelesTo} \
			${default="" "-se " + sample_expressions} \
			${default="" "-sf " + sample_file} \
			-sn ${default="[]" sample_name} \
			-fraction ${default="0.0" select_random_fraction} \
			-select ${default="[]" selectexpressions} \
			-xlSelectType ${default="[]" selectTypeToExclude} \
			-selectType ${default="[]" selectTypeToInclude} \
			setFilteredGtToNocall ${default="false" setFilteredGtToNocall} \
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
		concordance: "Output variants also called in this comparison track"
		discordance: "Output variants not called in this comparison track"
		exclude_sample_expressions: "List of sample expressions to exclude"
		exclude_sample_file: "List of samples to exclude"
		exclude_sample_name: "Exclude genotypes from this sample"
		excludeFiltered: "Don't include filtered sites"
		excludeIDs: "List of variant IDs to select"
		excludeNonVariants: "Don't include non-variant sites"
		forceValidOutput: "Forces output VCF to be compliant to up-to-date version"
		invertMendelianViolation: "Output non-mendelian violation sites only"
		invertselect: "Invert the selection criteria for -select"
		keepIDs: "List of variant IDs to select"
		keepOriginalAC: "Store the original AC, AF, and AN values after subsetting"
		keepOriginalDP: "Store the original DP value after subsetting"
		maxFilteredGenotypes: "Maximum number of samples filtered at the genotype level"
		maxFractionFilteredGenotypes: "Maximum fraction of samples filtered at the genotype level"
		maxIndelSize: "Maximum size of indels to include"
		maxNOCALLfraction: "Maximum fraction of samples with no-call genotypes"
		maxNOCALLnumber: "Maximum number of samples with no-call genotypes"
		mendelianViolation: "Output mendelian violation sites only"
		mendelianViolationQualThreshold: "Minimum GQ score for each trio member to accept a site as a violation"
		minFilteredGenotypes: "Minimum number of samples filtered at the genotype level"
		minFractionFilteredGenotypes: "Maximum fraction of samples filtered at the genotype level"
		minIndelSize: "Minimum size of indels to include"
		out: "File to which variants should be written"
		preserveAlleles: "Preserve original alleles, do not trim"
		remove_fraction_genotypes: "Select a fraction of genotypes at random from the input and sets them to no-call"
		removeUnusedAlternates: "Remove alternate alleles not present in any genotypes"
		restrictAllelesTo: "Select only variants of a particular allelicity"
		sample_expressions: "Regular expression to select multiple samples"
		sample_file: "File containing a list of samples to include"
		sample_name: "Include genotypes from this sample"
		select_random_fraction: "Select a fraction of variants at random from the input"
		selectexpressions: "One or more criteria to use when selecting the data"
		selectTypeToExclude: "Do not select certain type of variants from the input file"
		selectTypeToInclude: "Select only a certain type of variants from the input file"
		setFilteredGtToNocall: "Set filtered genotypes to no-call"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
