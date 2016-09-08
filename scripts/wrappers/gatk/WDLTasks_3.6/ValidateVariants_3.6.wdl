# --------------------------------------------------------------------------------------------
# This ValidateVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Validate a VCF file with an extra strict set of criteria
# --------------------------------------------------------------------------------------------

task ValidateVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	String ? dbsnp
	Boolean ? doNotValidateFilteredRecords
	Boolean ? validateGVCF
	Array[String] ? validationTypeToExclude
	String variant
	Boolean ? warnOnErrors

	command {
		java -jar ${gatk} \
			-T ValidateVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-D " + dbsnp} \
			-doNotValidateFilteredRecords ${default="false" doNotValidateFilteredRecords} \
			-gvcf ${default="false" validateGVCF} \
			-Xtype ${default="[]" validationTypeToExclude} \
			-V ${variant} \
			-warnOnErrors ${default="false" warnOnErrors} \
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
		dbsnp: "dbSNP file"
		doNotValidateFilteredRecords: "skip validation on filtered records"
		validateGVCF: "Validate this file as a GVCF"
		validationTypeToExclude: "which validation type to exclude from a full strict validation"
		variant: "Input VCF file"
		warnOnErrors: "just emit warnings on errors instead of terminating the run at the first instance"
		intervals: "One or more genomic intervals over which to operate"
	}
}
