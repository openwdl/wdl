# --------------------------------------------------------------------------------------------
# This PhaseByTransmission WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Compute the most likely genotype combination and phasing for trios and parent/child pairs
# --------------------------------------------------------------------------------------------

task PhaseByTransmission { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Float ? DeNovoPrior
	Boolean ? FatherAlleleFirst
	String ? MendelianViolationsFile
	String ? out
	String variant

	command {
		java -jar ${gatk} \
			-T PhaseByTransmission \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-prior ${default="1.0E-8" DeNovoPrior} \
			-fatherAlleleFirst ${default="false" FatherAlleleFirst} \
			${default="" "-mvf " + MendelianViolationsFile} \
			-o ${default="stdout" out} \
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
		DeNovoPrior: "Prior for de novo mutations. Default: 1e-8"
		FatherAlleleFirst: "Ouputs the father allele as the first allele in phased child genotype. i.e. father|mother rather than mother|father."
		MendelianViolationsFile: "File to output the mendelian violation details."
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		variant: "Input VCF file"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
