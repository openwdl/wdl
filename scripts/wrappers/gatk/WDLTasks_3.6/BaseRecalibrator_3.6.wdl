# --------------------------------------------------------------------------------------------
# This BaseRecalibrator WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Detect systematic errors in base quality scores
# --------------------------------------------------------------------------------------------

task BaseRecalibrator { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	File ? BQSR
	Int ? nctVal
	String ? binary_tag_name
	Float ? bqsrBAQGapOpenPenalty
	String ? covariate
	String ? deletions_default_quality
	Int ? indels_context_size
	String ? insertions_default_quality
	Array[String] ? knownSites
	Boolean ? list
	String ? low_quality_tail
	Boolean ? lowMemoryMode
	Int ? maximum_cycle_value
	Int ? mismatches_context_size
	String ? mismatches_default_quality
	Boolean ? no_standard_covs
	File out
	Int ? quantizing_levels
	Boolean ? run_without_dbsnp_potentially_ruining_quality
	String ? solid_nocall_strategy
	String ? solid_recal_mode
	Boolean ? sort_by_all_columns

	command {
		java -jar ${gatk} \
			-T BaseRecalibrator \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "--BQSR " + BQSR} \
			${default="" "-nct" + nctVal} \
			${default="" "-bintag " + binary_tag_name} \
			-bqsrBAQGOP ${default="40.0" bqsrBAQGapOpenPenalty} \
			${default="" "-cov " + covariate} \
			-ddq ${default="45" deletions_default_quality} \
			-ics ${default="3" indels_context_size} \
			-idq ${default="45" insertions_default_quality} \
			-knownSites ${default="[]" knownSites} \
			-ls ${default="false" list} \
			-lqt ${default="2" low_quality_tail} \
			-lowMemoryMode ${default="false" lowMemoryMode} \
			-maxCycle ${default="500" maximum_cycle_value} \
			-mcs ${default="2" mismatches_context_size} \
			-mdq ${default="-1" mismatches_default_quality} \
			-noStandard ${default="false" no_standard_covs} \
			-o ${out} \
			-ql ${default="16" quantizing_levels} \
			-run_without_dbsnp_potentially_ruining_quality ${default="false" run_without_dbsnp_potentially_ruining_quality} \
			-solid_nocall_strategy ${default="THROW_EXCEPTION" solid_nocall_strategy} \
			-sMode ${default="SET_Q_ZERO" solid_recal_mode} \
			-sortAllCols ${default="false" sort_by_all_columns} \
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
		binary_tag_name: "the binary tag covariate name if using it"
		bqsrBAQGapOpenPenalty: "BQSR BAQ gap open penalty (Phred Scaled).  Default value is 40.  30 is perhaps better for whole genome call sets"
		covariate: "One or more covariates to be used in the recalibration. Can be specified multiple times"
		deletions_default_quality: "default quality for the base deletions covariate"
		indels_context_size: "Size of the k-mer context to be used for base insertions and deletions"
		insertions_default_quality: "default quality for the base insertions covariate"
		knownSites: "A database of known polymorphic sites"
		list: "List the available covariates and exit"
		low_quality_tail: "minimum quality for the bases in the tail of the reads to be considered"
		lowMemoryMode: "Reduce memory usage in multi-threaded code at the expense of threading efficiency"
		maximum_cycle_value: "The maximum cycle value permitted for the Cycle covariate"
		mismatches_context_size: "Size of the k-mer context to be used for base mismatches"
		mismatches_default_quality: "default quality for the base mismatches covariate"
		no_standard_covs: "Do not use the standard set of covariates, but rather just the ones listed using the -cov argument"
		out: "The output recalibration table file to create"
		quantizing_levels: "number of distinct quality scores in the quantized output"
		run_without_dbsnp_potentially_ruining_quality: "If specified, allows the recalibrator to be used without a dbsnp rod. Very unsafe and for expert users only."
		solid_nocall_strategy: "Defines the behavior of the recalibrator when it encounters no calls in the color space. Options = THROW_EXCEPTION, LEAVE_READ_UNRECALIBRATED, or PURGE_READ"
		solid_recal_mode: "How should we recalibrate solid bases in which the reference was inserted? Options = DO_NOTHING, SET_Q_ZERO, SET_Q_ZERO_BASE_N, or REMOVE_REF_BIAS"
		sort_by_all_columns: "Sort the rows in the tables of reports"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
