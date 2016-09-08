# --------------------------------------------------------------------------------------------
# This CallableLoci WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Collect statistics on callable, uncallable, poorly mapped, and other parts of the genome
# --------------------------------------------------------------------------------------------

task CallableLoci { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	String ? format
	Int ? maxDepth
	Float ? maxFractionOfReadsWithLowMAPQ
	String ? maxLowMAPQ
	String ? minBaseQuality
	Int ? minDepth
	Int ? minDepthForLowMAPQ
	String ? minMappingQuality
	String ? out
	File summary

	command {
		java -jar ${gatk} \
			-T CallableLoci \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-format ${default="BED" format} \
			-maxDepth ${default="-1" maxDepth} \
			-frlmq ${default="0.1" maxFractionOfReadsWithLowMAPQ} \
			-mlmq ${default="1" maxLowMAPQ} \
			-mbq ${default="20" minBaseQuality} \
			-minDepth ${default="4" minDepth} \
			-mdflmq ${default="10" minDepthForLowMAPQ} \
			-mmq ${default="10" minMappingQuality} \
			-o ${default="stdout" out} \
			-summary ${summary} \
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
		format: "Output format"
		maxDepth: "Maximum read depth before a locus is considered poorly mapped"
		maxFractionOfReadsWithLowMAPQ: "If the fraction of reads at a base with low mapping quality exceeds this value, the site may be poorly mapped"
		maxLowMAPQ: "Maximum value for MAPQ to be considered a problematic mapped read."
		minBaseQuality: "Minimum quality of bases to count towards depth."
		minDepth: "Minimum QC+ read depth before a locus is considered callable"
		minDepthForLowMAPQ: "Minimum read depth before a locus is considered a potential candidate for poorly mapped"
		minMappingQuality: "Minimum mapping quality of reads to count towards depth."
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		summary: "Name of file for output summary"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
