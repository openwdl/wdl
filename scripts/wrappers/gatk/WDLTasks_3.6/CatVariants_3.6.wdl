# --------------------------------------------------------------------------------------------
# This CatVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Concatenate VCF files of non-overlapping genome intervals, all with the same set of samples
# --------------------------------------------------------------------------------------------

task CatVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Boolean ? assumeSorted
	Boolean ? help
	String ? log_to_file
	String ? logging_level
	File outputFile
	File reference
	Array[File] variant
	Int ? variant_index_parameter
	String ? variant_index_type
	Boolean ? version

	command {
		java -jar ${gatk} \
			-T CatVariants \
			-R ${ref} \
			-assumeSorted ${default="false" assumeSorted} \
			-h ${default="false" help} \
			${default="" "-log " + log_to_file} \
			-l ${default="INFO" logging_level} \
			-out ${outputFile} \
			-R ${reference} \
			-V ${variant} \
			variant_index_parameter ${default="-1" variant_index_parameter} \
			variant_index_type ${default="DYNAMIC_SEEK" variant_index_type} \
			-version ${default="false" version} \
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
		assumeSorted: "assumeSorted should be true if the input files are already sorted (based on the position of the variants)"
		help: "Generate the help message"
		log_to_file: "Set the logging location"
		logging_level: "Set the minimum level of logging"
		outputFile: "output file"
		reference: "genome reference file <name>.fasta"
		variant: "Input VCF file/s"
		variant_index_parameter: "the parameter (bin width or features per bin) to pass to the VCF/BCF IndexCreator"
		variant_index_type: "which type of IndexCreator to use for VCF/BCF indices"
		version: "Output version information"
	}
}
