# --------------------------------------------------------------------------------------------
# This VariantFiltration WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Filter variant calls based on INFO and FORMAT annotations
# --------------------------------------------------------------------------------------------

task VariantFiltration { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? clusterSize
	Int ? clusterWindowSize
	Array[String] ? filterExpression
	Array[String] ? filterName
	Boolean ? filterNotInMask
	Array[String] ? genotypeFilterExpression
	Array[String] ? genotypeFilterName
	Boolean ? invalidatePreviousFilters
	Boolean ? invertFilterExpression
	Boolean ? invertGenotypeFilterExpression
	String ? mask
	Int ? maskExtension
	String ? maskName
	Boolean ? missingValuesInExpressionsShouldEvaluateAsFailing
	String ? out
	Boolean ? setFilteredGtToNocall
	String variant

	command {
		java -jar ${gatk} \
			-T VariantFiltration \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-cluster ${default="3" clusterSize} \
			-window ${default="0" clusterWindowSize} \
			-filter ${default="[]" filterExpression} \
			-filterName ${default="[]" filterName} \
			-filterNotInMask ${default="false" filterNotInMask} \
			-G_filter ${default="[]" genotypeFilterExpression} \
			-G_filterName ${default="[]" genotypeFilterName} \
			invalidatePreviousFilters ${default="false" invalidatePreviousFilters} \
			-invfilter ${default="false" invertFilterExpression} \
			-invG_filter ${default="false" invertGenotypeFilterExpression} \
			${default="" "-mask " + mask} \
			-maskExtend ${default="0" maskExtension} \
			-maskName ${default="Mask" maskName} \
			missingValuesInExpressionsShouldEvaluateAsFailing ${default="false" missingValuesInExpressionsShouldEvaluateAsFailing} \
			-o ${default="stdout" out} \
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
		clusterSize: "The number of SNPs which make up a cluster"
		clusterWindowSize: "The window size (in bases) in which to evaluate clustered SNPs"
		filterExpression: "One or more expression used with INFO fields to filter"
		filterName: "Names to use for the list of filters"
		filterNotInMask: "Filter records NOT in given input mask."
		genotypeFilterExpression: "One or more expression used with FORMAT (sample/genotype-level) fields to filter (see documentation guide for more info)"
		genotypeFilterName: "Names to use for the list of sample/genotype filters (must be a 1-to-1 mapping); this name is put in the FILTER field for variants that get filtered"
		invalidatePreviousFilters: "Remove previous filters applied to the VCF"
		invertFilterExpression: "Invert the selection criteria for --filterExpression"
		invertGenotypeFilterExpression: "Invert the selection criteria for --genotypeFilterExpression"
		mask: "Input ROD mask"
		maskExtension: "How many bases beyond records from a provided 'mask' rod should variants be filtered"
		maskName: "The text to put in the FILTER field if a 'mask' rod is provided and overlaps with a variant call"
		missingValuesInExpressionsShouldEvaluateAsFailing: "When evaluating the JEXL expressions, missing values should be considered failing the expression"
		out: "File to which variants should be written"
		setFilteredGtToNocall: "Set filtered genotypes to no-call"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
