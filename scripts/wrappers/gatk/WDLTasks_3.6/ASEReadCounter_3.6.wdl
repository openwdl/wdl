# --------------------------------------------------------------------------------------------
# This ASEReadCounter WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Calculate read counts per allele for allele-specific expression analysis
# --------------------------------------------------------------------------------------------

task ASEReadCounter { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	String unsafe
	String ? countOverlapReadsType
	String ? minBaseQuality
	Int ? minDepthOfNonFilteredBase
	Int ? minMappingQuality
	String ? out
	String ? outputFormat
	String sitesVCFFile

	command {
		java -jar ${gatk} \
			-T ASEReadCounter \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			--unsafe ${unsafe} \
			-overlap ${default="COUNT_FRAGMENTS_REQUIRE_SAME_BASE" countOverlapReadsType} \
			-mbq ${default="0" minBaseQuality} \
			-minDepth ${default="-1" minDepthOfNonFilteredBase} \
			-mmq ${default="0" minMappingQuality} \
			-o ${default="stdout" out} \
			outputFormat ${default="RTABLE" outputFormat} \
			-sites ${sitesVCFFile} \
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
		countOverlapReadsType: "Handling of overlapping reads from the same fragment"
		minBaseQuality: "Minimum base quality"
		minDepthOfNonFilteredBase: "Minimum number of bases that pass filters"
		minMappingQuality: "Minimum read mapping quality"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		outputFormat: "Format of the output file, can be CSV, TABLE, RTABLE"
		sitesVCFFile: "Undocumented option"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		unsafe: "Enable unsafe operations: nothing will be checked at runtime"
	}
}
