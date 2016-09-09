# --------------------------------------------------------------------------------------------
# This ApplyRecalibration WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Apply a score cutoff to filter variants based on a recalibration table
# --------------------------------------------------------------------------------------------

task ApplyRecalibration { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	Boolean ? excludeFiltered
	Boolean ? ignore_all_filters
	String ? ignore_filter
	Array[String] task_input
	Float ? lodCutoff
	String ? mode
	String ? out
	String recal_file
	File ? tranches_file
	Float ? ts_filter_level
	Boolean ? useAlleleSpecificAnnotations

	command {
		java -jar ${gatk} \
			-T ApplyRecalibration \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-ef ${default="false" excludeFiltered} \
			-ignoreAllFilters ${default="false" ignore_all_filters} \
			${default="" "-ignoreFilter " + ignore_filter} \
			-input ${task_input} \
			${default="" "-lodCutoff " + lodCutoff} \
			-mode ${default="SNP" mode} \
			-o ${default="stdout" out} \
			-recalFile ${recal_file} \
			${default="" "-tranchesFile " + tranches_file} \
			${default="" "-ts_filter_level " + ts_filter_level} \
			-AS ${default="false" useAlleleSpecificAnnotations} \
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
		excludeFiltered: "Don't output filtered loci after applying the recalibration"
		ignore_all_filters: "If specified, the variant recalibrator will ignore all input filters. Useful to rerun the VQSR from a filtered output file."
		ignore_filter: "If specified, the recalibration will be applied to variants marked as filtered by the specified filter name in the input VCF file"
		task_input: "The raw input variants to be recalibrated"
		lodCutoff: "The VQSLOD score below which to start filtering"
		mode: "Recalibration mode to employ: 1.) SNP for recalibrating only SNPs (emitting indels untouched in the output VCF); 2.) INDEL for indels; and 3.) BOTH for recalibrating both SNPs and indels simultaneously."
		out: "The output filtered and recalibrated VCF file in which each variant is annotated with its VQSLOD value"
		recal_file: "The input recal file used by ApplyRecalibration"
		tranches_file: "The input tranches file describing where to cut the data"
		ts_filter_level: "The truth sensitivity level at which to start filtering"
		useAlleleSpecificAnnotations: "If specified, the tool will attempt to apply a filter to each allele based on the input tranches and allele-specific .recal file."
		intervals: "One or more genomic intervals over which to operate"
	}
}
