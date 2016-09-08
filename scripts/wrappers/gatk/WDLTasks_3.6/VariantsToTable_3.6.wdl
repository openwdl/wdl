# --------------------------------------------------------------------------------------------
# This VariantsToTable WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Extract specific fields from a VCF file to a tab-delimited table
# --------------------------------------------------------------------------------------------

task VariantsToTable { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Boolean ? allowMissingData
	Array[String] ? fields
	Array[String] ? genotypeFields
	Int ? maxRecords
	Boolean ? moltenize
	String ? out
	Boolean ? showFiltered
	Boolean ? splitMultiAllelic
	Array[String] variant

	command {
		java -jar ${gatk} \
			-T VariantsToTable \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-AMD ${default="false" allowMissingData} \
			-F ${default="[]" fields} \
			-GF ${default="[]" genotypeFields} \
			-M ${default="-1" maxRecords} \
			-moltenize ${default="false" moltenize} \
			-o ${default="stdout" out} \
			-raw ${default="false" showFiltered} \
			-SMA ${default="false" splitMultiAllelic} \
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
		allowMissingData: "If provided, we will not require every record to contain every field"
		fields: "The name of each field to capture for output in the table"
		genotypeFields: "The name of each genotype field to capture for output in the table"
		maxRecords: "If provided, we will emit at most maxRecord records to the table"
		moltenize: "If provided, we will produce molten output"
		out: "File to which results should be written"
		showFiltered: "If provided, field values from filtered records will be included in the output"
		splitMultiAllelic: "If provided, we will split multi-allelic records into multiple lines of output"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
