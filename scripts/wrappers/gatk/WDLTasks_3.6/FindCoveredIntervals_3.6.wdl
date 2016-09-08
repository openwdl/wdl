# --------------------------------------------------------------------------------------------
# This FindCoveredIntervals WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Outputs a list of intervals that are covered to or above a given threshold
# --------------------------------------------------------------------------------------------

task FindCoveredIntervals { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Float ? activeProbabilityThreshold
	Int ? activeRegionExtension
	Array[String] ? activeRegionIn
	Int ? activeRegionMaxSize
	String ? activeRegionOut
	String ? activityProfileOut
	Float ? bandPassSigma
	Int ? coverage_threshold
	Boolean ? forceActive
	Int ? minBaseQuality
	Int ? minMappingQuality
	String ? out
	Boolean ? uncovered

	command {
		java -jar ${gatk} \
			-T FindCoveredIntervals \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-ActProbThresh ${default="0.002" activeProbabilityThreshold} \
			${default="" "-activeRegionExtension " + activeRegionExtension} \
			${default="" "-AR " + activeRegionIn} \
			${default="" "-activeRegionMaxSize " + activeRegionMaxSize} \
			${default="" "-ARO " + activeRegionOut} \
			${default="" "-APO " + activityProfileOut} \
			${default="" "-bandPassSigma " + bandPassSigma} \
			-cov ${default="20" coverage_threshold} \
			-forceActive ${default="false" forceActive} \
			-minBQ ${default="0" minBaseQuality} \
			-minMQ ${default="0" minMappingQuality} \
			-o ${default="stdout" out} \
			-u ${default="false" uncovered} \
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
		activeProbabilityThreshold: "Threshold for the probability of a profile state being active."
		activeRegionExtension: "The active region extension; if not provided defaults to Walker annotated default"
		activeRegionIn: "Use this interval list file as the active regions to process"
		activeRegionMaxSize: "The active region maximum size; if not provided defaults to Walker annotated default"
		activeRegionOut: "Output the active region to this IGV formatted file"
		activityProfileOut: "Output the raw activity profile results in IGV format"
		bandPassSigma: "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default"
		coverage_threshold: "The minimum allowable coverage to be considered covered"
		forceActive: "If provided, all bases will be tagged as active"
		minBaseQuality: "The minimum allowable base quality score to be counted for coverage"
		minMappingQuality: "The minimum allowable mapping quality score to be counted for coverage"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		uncovered: "output intervals that fail the coverage threshold instead"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
