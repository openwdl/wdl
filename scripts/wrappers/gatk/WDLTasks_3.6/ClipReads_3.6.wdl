# --------------------------------------------------------------------------------------------
# This ClipReads WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Read clipping based on quality, position or sequence matching
# --------------------------------------------------------------------------------------------

task ClipReads { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	String ? clipRepresentation
	String ? clipSequence
	String ? clipSequencesFile
	String ? cyclesToTrim
	String ? out
	String ? outputStatistics
	Int ? qTrimmingThreshold

	command {
		java -jar ${gatk} \
			-T ClipReads \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			-CR ${default="WRITE_NS" clipRepresentation} \
			${default="" "-X " + clipSequence} \
			${default="" "-XF " + clipSequencesFile} \
			${default="" "-CT " + cyclesToTrim} \
			-o ${default="stdout" out} \
			${default="" "-os " + outputStatistics} \
			-QT ${default="-1" qTrimmingThreshold} \
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
		clipRepresentation: "How should we actually clip the bases?"
		clipSequence: "Remove sequences within reads matching this sequence"
		clipSequencesFile: "Remove sequences within reads matching the sequences in this FASTA file"
		cyclesToTrim: "String indicating machine cycles to clip from the reads"
		out: "Write BAM output here"
		outputStatistics: "File to output statistics"
		qTrimmingThreshold: "If provided, the Q-score clipper will be applied"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
	}
}
