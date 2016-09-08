# --------------------------------------------------------------------------------------------
# This DiffObjects WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: A generic engine for comparing tree-structured objects
# --------------------------------------------------------------------------------------------

task DiffObjects { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Boolean ? doPairwise
	Int ? iterations
	File master
	Int ? maxCount1Diffs
	Int ? maxDiffs
	Int ? maxObjectsToRead
	Int ? maxRawDiffsToSummarize
	Int ? minCountForDiff
	String ? out
	Boolean ? showItemizedDifferences
	File test

	command {
		java -jar ${gatk} \
			-T DiffObjects \
			-R ${ref} \
			-doPairwise ${default="false" doPairwise} \
			iterations ${default="1" iterations} \
			-m ${master} \
			-M1 ${default="0" maxCount1Diffs} \
			-M ${default="0" maxDiffs} \
			-motr ${default="-1" maxObjectsToRead} \
			-maxRawDiffsToSummarize ${default="-1" maxRawDiffsToSummarize} \
			-MCFD ${default="1" minCountForDiff} \
			-o ${default="stdout" out} \
			-SID ${default="false" showItemizedDifferences} \
			-t ${test} \
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
		doPairwise: "If provided, we will compute the minimum pairwise differences to summary, which can be extremely expensive"
		iterations: "Number of iterations to perform, should be 1 unless you are doing memory testing"
		master: "Master file: expected results"
		maxCount1Diffs: "Max. number of diffs occuring exactly once in the file to process"
		maxDiffs: "Max. number of diffs to process"
		maxObjectsToRead: "Max. number of objects to read from the files.  -1 [default] means unlimited"
		maxRawDiffsToSummarize: "Max. number of differences to include in the summary.  -1 [default] means unlimited"
		minCountForDiff: "Min number of observations for a records to display"
		out: "File to which results should be written"
		showItemizedDifferences: "Should we enumerate all differences between the files?"
		test: "Test file: new results to compare to the master file"
	}
}
