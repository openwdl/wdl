# --------------------------------------------------------------------------------------------
# This AnalyzeCovariates WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Create plots to visualize base recalibration results
# --------------------------------------------------------------------------------------------

task AnalyzeCovariates { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	File ? BQSR
	File ? afterReportFile
	File ? beforeReportFile
	Boolean ? ignoreLastModificationTimes
	File ? intermediateCsvFile
	File ? plotsReportFile

	command {
		java -jar ${gatk} \
			-T AnalyzeCovariates \
			-R ${ref} \
			${default="" "--BQSR " + BQSR} \
			${default="" "-after " + afterReportFile} \
			${default="" "-before " + beforeReportFile} \
			-ignoreLMT ${default="false" ignoreLastModificationTimes} \
			${default="" "-csv " + intermediateCsvFile} \
			${default="" "-plots " + plotsReportFile} \
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
		afterReportFile: "file containing the BQSR second-pass report file"
		beforeReportFile: "file containing the BQSR first-pass report file"
		ignoreLastModificationTimes: "do not emit warning messages related to suspicious last modification time order of inputs"
		intermediateCsvFile: "location of the csv intermediate file"
		plotsReportFile: "location of the output report"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
