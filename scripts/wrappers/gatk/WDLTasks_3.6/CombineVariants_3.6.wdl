# --------------------------------------------------------------------------------------------
# This CombineVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Combine variant records from different sources
# --------------------------------------------------------------------------------------------

task CombineVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	Boolean ? assumeIdenticalSamples
	Boolean ? excludeNonVariants
	Boolean ? filteredAreUncalled
	String ? filteredrecordsmergetype
	String ? genotypemergeoption
	Boolean ? mergeInfoWithMaxAC
	Boolean ? minimalVCF
	Int ? minimumN
	String ? out
	Boolean ? printComplexMerges
	String ? rod_priority_list
	String ? setKey
	Boolean ? suppressCommandLineHeader
	Array[String] variant

	command {
		java -jar ${gatk} \
			-T CombineVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-assumeIdenticalSamples ${default="false" assumeIdenticalSamples} \
			-env ${default="false" excludeNonVariants} \
			-filteredAreUncalled ${default="false" filteredAreUncalled} \
			-filteredRecordsMergeType ${default="KEEP_IF_ANY_UNFILTERED" filteredrecordsmergetype} \
			${default="" "-genotypeMergeOptions " + genotypemergeoption} \
			-mergeInfoWithMaxAC ${default="false" mergeInfoWithMaxAC} \
			-minimalVCF ${default="false" minimalVCF} \
			-minN ${default="1" minimumN} \
			-o ${default="stdout" out} \
			-printComplexMerges ${default="false" printComplexMerges} \
			${default="" "-priority " + rod_priority_list} \
			-setKey ${default="set" setKey} \
			-suppressCommandLineHeader ${default="false" suppressCommandLineHeader} \
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
		assumeIdenticalSamples: "Assume input VCFs have identical sample sets and disjoint calls"
		excludeNonVariants: "Exclude sites where no variation is present after merging"
		filteredAreUncalled: "Treat filtered variants as uncalled"
		filteredrecordsmergetype: "Determines how we should handle records seen at the same site in the VCF, but with different FILTER fields"
		genotypemergeoption: "Determines how we should merge genotype records for samples shared across the ROD files"
		mergeInfoWithMaxAC: "Use the INFO content of the record with the highest AC"
		minimalVCF: "Emit a sites-only file"
		minimumN: "Minimum number of input files the site must be observed in to be included"
		out: "File to which variants should be written"
		printComplexMerges: "Emit interesting sites requiring complex compatibility merging to file"
		rod_priority_list: "Ordered list specifying priority for merging"
		setKey: "Key name for the set attribute"
		suppressCommandLineHeader: "Do not output the command line to the header"
		variant: "VCF files to merge together"
		intervals: "One or more genomic intervals over which to operate"
	}
}
