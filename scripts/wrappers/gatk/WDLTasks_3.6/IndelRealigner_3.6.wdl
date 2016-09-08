# --------------------------------------------------------------------------------------------
# This IndelRealigner WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Perform local realignment of reads around indels
# --------------------------------------------------------------------------------------------

task IndelRealigner { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	String ? consensusDeterminationModel
	Float ? entropyThreshold
	Array[String] ? knownAlleles
	Float ? LODThresholdForCleaning
	Int ? maxConsensuses
	Int ? maxIsizeForMovement
	Int ? maxPositionalMoveAllowed
	Int ? maxReadsForConsensuses
	Int ? maxReadsForRealignment
	Int ? maxReadsInMemory
	Boolean ? noOriginalAlignmentTags
	String ? nWayOut
	String ? out
	String targetIntervals

	command {
		java -jar ${gatk} \
			-T IndelRealigner \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-model ${default="USE_READS" consensusDeterminationModel} \
			-entropy ${default="0.15" entropyThreshold} \
			-known ${default="[]" knownAlleles} \
			-LOD ${default="5.0" LODThresholdForCleaning} \
			-maxConsensuses ${default="30" maxConsensuses} \
			-maxIsize ${default="3000" maxIsizeForMovement} \
			-maxPosMove ${default="200" maxPositionalMoveAllowed} \
			-greedy ${default="120" maxReadsForConsensuses} \
			-maxReads ${default="20000" maxReadsForRealignment} \
			-maxInMemory ${default="150000" maxReadsInMemory} \
			-noTags ${default="false" noOriginalAlignmentTags} \
			${default="" "-nWayOut " + nWayOut} \
			${default="" "-o " + out} \
			-targetIntervals ${targetIntervals} \
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
		consensusDeterminationModel: "Determines how to compute the possible alternate consenses"
		entropyThreshold: "Percentage of mismatches at a locus to be considered having high entropy (0.0 < entropy <= 1.0)"
		knownAlleles: "Input VCF file(s) with known indels"
		LODThresholdForCleaning: "LOD threshold above which the cleaner will clean"
		maxConsensuses: "Max alternate consensuses to try (necessary to improve performance in deep coverage)"
		maxIsizeForMovement: "maximum insert size of read pairs that we attempt to realign"
		maxPositionalMoveAllowed: "Maximum positional move in basepairs that a read can be adjusted during realignment"
		maxReadsForConsensuses: "Max reads used for finding the alternate consensuses (necessary to improve performance in deep coverage)"
		maxReadsForRealignment: "Max reads allowed at an interval for realignment"
		maxReadsInMemory: "max reads allowed to be kept in memory at a time by the SAMFileWriter"
		noOriginalAlignmentTags: "Don't output the original cigar or alignment start tags for each realigned read in the output bam"
		nWayOut: "Generate one output file for each input (-I) bam file (not compatible with -output)"
		out: "Output bam"
		targetIntervals: "Intervals file output from RealignerTargetCreator"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
