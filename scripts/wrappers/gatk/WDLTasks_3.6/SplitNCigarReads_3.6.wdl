# --------------------------------------------------------------------------------------------
# This SplitNCigarReads WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Splits reads that contain Ns in their CIGAR string
# --------------------------------------------------------------------------------------------

task SplitNCigarReads { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] intervals
	String unsafe
	Boolean ? doNotFixOverhangs
	Int ? maxBasesInOverhang
	Int ? maxMismatchesInOverhang
	Int ? maxReadsInMemory
	String ? out

	command {
		java -jar ${gatk} \
			-T SplitNCigarReads \
			-R ${ref} \
			--input_file ${input_file} \
			--intervals ${intervals} \
			--unsafe ${unsafe} \
			-doNotFixOverhangs ${default="false" doNotFixOverhangs} \
			-maxOverhang ${default="40" maxBasesInOverhang} \
			-maxMismatches ${default="1" maxMismatchesInOverhang} \
			-maxInMemory ${default="150000" maxReadsInMemory} \
			-o ${default="stdout" out} \
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
		doNotFixOverhangs: "do not have the walker hard-clip overhanging sections of the reads"
		maxBasesInOverhang: "max number of bases allowed in the overhang"
		maxMismatchesInOverhang: "max number of mismatches allowed in the overhang"
		maxReadsInMemory: "max reads allowed to be kept in memory at a time by the BAM writer"
		out: "Write output to this BAM filename instead of STDOUT"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		unsafe: "Enable unsafe operations: nothing will be checked at runtime"
	}
}
