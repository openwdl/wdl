# --------------------------------------------------------------------------------------------
# This DepthOfCoverage WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Assess sequence coverage by a wide array of metrics, partitioned by sample, read group, or library
# --------------------------------------------------------------------------------------------

task DepthOfCoverage { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? ntVal
	File ? calculateCoverageOverGenes
	String ? countType
	Boolean ? ignoreDeletionSites
	Boolean ? includeDeletions
	Boolean ? includeRefNSites
	String ? maxBaseQuality
	Int ? maxMappingQuality
	String ? minBaseQuality
	Int ? minMappingQuality
	Int ? nBins
	Boolean ? omitDepthOutputAtEachBase
	Boolean ? omitIntervalStatistics
	Boolean ? omitLocusTable
	Boolean ? omitPerSampleStats
	String ? out
	String ? outputFormat
	String ? partitionType
	Boolean ? printBaseCounts
	Boolean ? printBinEndpointsAndExit
	Int ? start
	Int ? stop
	String ? summaryCoverageThreshold

	command {
		java -jar ${gatk} \
			-T DepthOfCoverage \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			${default="" "-geneList " + calculateCoverageOverGenes} \
			countType ${default="COUNT_READS" countType} \
			ignoreDeletionSites ${default="false" ignoreDeletionSites} \
			-dels ${default="false" includeDeletions} \
			includeRefNSites ${default="false" includeRefNSites} \
			maxBaseQuality ${default="127" maxBaseQuality} \
			maxMappingQuality ${default="2147483647" maxMappingQuality} \
			-mbq ${default="-1" minBaseQuality} \
			-mmq ${default="-1" minMappingQuality} \
			nBins ${default="499" nBins} \
			-omitBaseOutput ${default="false" omitDepthOutputAtEachBase} \
			-omitIntervals ${default="false" omitIntervalStatistics} \
			-omitLocusTable ${default="false" omitLocusTable} \
			-omitSampleSummary ${default="false" omitPerSampleStats} \
			-o ${default="None" out} \
			outputFormat ${default="rtable" outputFormat} \
			-pt ${default="[sample]" partitionType} \
			-baseCounts ${default="false" printBaseCounts} \
			printBinEndpointsAndExit ${default="false" printBinEndpointsAndExit} \
			start ${default="1" start} \
			stop ${default="500" stop} \
			-ct ${default="[15]" summaryCoverageThreshold} \
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
		calculateCoverageOverGenes: "Calculate coverage statistics over this list of genes"
		countType: "How should overlapping reads from the same fragment be handled?"
		ignoreDeletionSites: "Ignore sites consisting only of deletions"
		includeDeletions: "Include information on deletions"
		includeRefNSites: "Include sites where the reference is N"
		maxBaseQuality: "Maximum quality of bases to count towards depth"
		maxMappingQuality: "Maximum mapping quality of reads to count towards depth"
		minBaseQuality: "Minimum quality of bases to count towards depth"
		minMappingQuality: "Minimum mapping quality of reads to count towards depth"
		nBins: "Number of bins to use for granular binning"
		omitDepthOutputAtEachBase: "Do not output depth of coverage at each base"
		omitIntervalStatistics: "Do not calculate per-interval statistics"
		omitLocusTable: "Do not calculate per-sample per-depth counts of loci"
		omitPerSampleStats: "Do not output the summary files per-sample"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		outputFormat: "The format of the output file"
		partitionType: "Partition type for depth of coverage"
		printBaseCounts: "Add base counts to per-locus output"
		printBinEndpointsAndExit: "Print the bin values and exit immediately"
		start: "Starting (left endpoint) for granular binning"
		stop: "Ending (right endpoint) for granular binning"
		summaryCoverageThreshold: "Coverage threshold (in percent) for summarizing statistics"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
