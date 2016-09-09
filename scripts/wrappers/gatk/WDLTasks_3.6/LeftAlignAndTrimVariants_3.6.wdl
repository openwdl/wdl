# --------------------------------------------------------------------------------------------
# This LeftAlignAndTrimVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Left-align indels in a variant callset
# --------------------------------------------------------------------------------------------

task LeftAlignAndTrimVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Boolean ? dontTrimAlleles
	Boolean ? keepOriginalAC
	String ? out
	Boolean ? splitMultiallelics
	String variant

	command {
		java -jar ${gatk} \
			-T LeftAlignAndTrimVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-notrim ${default="false" dontTrimAlleles} \
			-keepOriginalAC ${default="false" keepOriginalAC} \
			-o ${default="stdout" out} \
			-split ${default="false" splitMultiallelics} \
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
		dontTrimAlleles: "Do not Trim alleles to remove bases common to all of them"
		keepOriginalAC: "Store the original AC, AF, and AN values after subsetting"
		out: "File to which variants should be written"
		splitMultiallelics: "Split multiallelic records and left-align individual alleles"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
