# --------------------------------------------------------------------------------------------
# This RandomlySplitVariants WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Randomly split variants into different sets
# --------------------------------------------------------------------------------------------

task RandomlySplitVariants { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Float ? fractionToOut1
	Int ? numOfOutputVCFFiles
	String ? out1
	File ? out2
	String ? prefixForAllOutputFileNames
	Boolean ? splitToManyFiles
	String variant

	command {
		java -jar ${gatk} \
			-T RandomlySplitVariants \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-fraction ${default="0.5" fractionToOut1} \
			-N ${default="-1" numOfOutputVCFFiles} \
			-o1 ${default="stdout" out1} \
			${default="" "-o2 " + out2} \
			${default="" "-baseOutputName " + prefixForAllOutputFileNames} \
			-splitToMany ${default="false" splitToManyFiles} \
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
		fractionToOut1: "Fraction of records to be placed in out1 (must be 0 >= fraction <= 1); all other records are placed in out2"
		numOfOutputVCFFiles: "number of output VCF files. Only works with SplitToMany = true"
		out1: "File #1 to which variants should be written"
		out2: "File #2 to which variants should be written"
		prefixForAllOutputFileNames: "the name of the output VCF file will be: <baseOutputName>.split.<number>.vcf. Required with SplitToMany option"
		splitToManyFiles: "split (with uniform distribution) to more than 2 files. numOfFiles and baseOutputName parameters are required"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
