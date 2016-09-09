# --------------------------------------------------------------------------------------------
# This VariantAnnotator WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Annotate variant calls with context information
# --------------------------------------------------------------------------------------------

task VariantAnnotator { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? input_file
	Array[String] ? intervals
	Int ? ntVal
	Boolean ? alwaysAppendDbsnpId
	Array[String] ? annotation
	Array[String] ? comp
	String ? dbsnp
	Array[String] ? excludeAnnotation
	String ? expression
	Array[String] ? group
	Boolean ? list
	Float ? MendelViolationGenotypeQualityThreshold
	String ? out
	Array[String] ? resource
	Boolean ? resourceAlleleConcordance
	String ? snpEffFile
	Boolean ? useAllAnnotations
	String variant

	command {
		java -jar ${gatk} \
			-T VariantAnnotator \
			-R ${ref} \
			${default="" "--input_file " + input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-alwaysAppendDbsnpId ${default="false" alwaysAppendDbsnpId} \
			-A ${default="[]" annotation} \
			-comp ${default="[]" comp} \
			${default="" "-D " + dbsnp} \
			-XA ${default="[]" excludeAnnotation} \
			-E ${default="{}" expression} \
			-G ${default="[]" group} \
			-ls ${default="false" list} \
			-mvq ${default="0.0" MendelViolationGenotypeQualityThreshold} \
			-o ${default="stdout" out} \
			-resource ${default="[]" resource} \
			-rac ${default="false" resourceAlleleConcordance} \
			${default="" "-snpEffFile " + snpEffFile} \
			-all ${default="false" useAllAnnotations} \
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
		alwaysAppendDbsnpId: "Add dbSNP ID even if one is already present"
		annotation: "One or more specific annotations to apply to variant calls"
		comp: "Comparison VCF file"
		dbsnp: "dbSNP file"
		excludeAnnotation: "One or more specific annotations to exclude"
		expression: "One or more specific expressions to apply to variant calls"
		group: "One or more classes/groups of annotations to apply to variant calls"
		list: "List the available annotations and exit"
		MendelViolationGenotypeQualityThreshold: "GQ threshold for annotating MV ratio"
		out: "File to which variants should be written"
		resource: "External resource VCF file"
		resourceAlleleConcordance: "Check for allele concordances when using an external resource VCF file"
		snpEffFile: "SnpEff file from which to get annotations"
		useAllAnnotations: "Use all possible annotations (not for the faint of heart)"
		variant: "Input VCF file"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
