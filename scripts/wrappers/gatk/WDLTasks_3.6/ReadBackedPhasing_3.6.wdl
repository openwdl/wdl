# --------------------------------------------------------------------------------------------
# This ReadBackedPhasing WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Annotate physical phasing information
# --------------------------------------------------------------------------------------------

task ReadBackedPhasing { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	Int ? cacheWindowSize
	Boolean ? debug
	Boolean ? enableMergePhasedSegregatingPolymorphismsToMNP
	Int ? maxGenomicDistanceForMNP
	Int ? maxPhaseSites
	Int ? min_base_quality_score
	Int ? min_mapping_quality_score
	String ? out
	Float ? phaseQualityThresh
	String ? sampleToPhase
	String variant

	command {
		java -jar ${gatk} \
			-T ReadBackedPhasing \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-cacheWindow ${default="20000" cacheWindowSize} \
			-debug ${default="false" debug} \
			-enableMergeToMNP ${default="false" enableMergePhasedSegregatingPolymorphismsToMNP} \
			-maxDistMNP ${default="1" maxGenomicDistanceForMNP} \
			-maxSites ${default="10" maxPhaseSites} \
			-mbq ${default="17" min_base_quality_score} \
			-mmq ${default="20" min_mapping_quality_score} \
			-o ${default="stdout" out} \
			-phaseThresh ${default="20.0" phaseQualityThresh} \
			${default="" "-sampleToPhase " + sampleToPhase} \
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
		cacheWindowSize: "The window size (in bases) to cache variant sites and their reads for the phasing procedure"
		debug: "If specified, print out very verbose debug information (if -l DEBUG is also specified)"
		enableMergePhasedSegregatingPolymorphismsToMNP: "Merge consecutive phased sites into MNP records"
		maxGenomicDistanceForMNP: "The maximum reference-genome distance between consecutive heterozygous sites to permit merging phased VCF records into a MNP record"
		maxPhaseSites: "The maximum number of successive heterozygous sites permitted to be used by the phasing algorithm"
		min_base_quality_score: "Minimum base quality required to consider a base for phasing"
		min_mapping_quality_score: "Minimum read mapping quality required to consider a read for phasing"
		out: "File to which variants should be written"
		phaseQualityThresh: "The minimum phasing quality score required to output phasing"
		sampleToPhase: "Only include these samples when phasing"
		variant: "Input VCF file"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
