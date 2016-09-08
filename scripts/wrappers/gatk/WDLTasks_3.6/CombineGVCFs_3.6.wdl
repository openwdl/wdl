# --------------------------------------------------------------------------------------------
# This CombineGVCFs WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Combine per-sample gVCF files produced by HaplotypeCaller into a multi-sample gVCF file
# --------------------------------------------------------------------------------------------

task CombineGVCFs { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Array[String] ? annotation
	Int ? breakBandsAtMultiplesOf
	Boolean ? convertToBasePairResolution
	String ? dbsnp
	String ? group
	String ? out
	Array[String] variant

	command {
		java -jar ${gatk} \
			-T CombineGVCFs \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-A ${default="[AS_RMSMappingQuality]" annotation} \
			-breakBandsAtMultiplesOf ${default="0" breakBandsAtMultiplesOf} \
			-bpResolution ${default="false" convertToBasePairResolution} \
			${default="" "-D " + dbsnp} \
			-G ${default="[StandardAnnotation]" group} \
			-o ${default="stdout" out} \
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
		annotation: "One or more specific annotations to recompute.  The single value 'none' removes the default annotations"
		breakBandsAtMultiplesOf: "If > 0, reference bands will be broken up at genomic positions that are multiples of this number"
		convertToBasePairResolution: "If specified, convert banded gVCFs to all-sites gVCFs"
		dbsnp: "dbSNP file"
		group: "One or more classes/groups of annotations to apply to variant calls"
		out: "File to which the combined gVCF should be written"
		variant: "One or more input gVCF files"
		intervals: "One or more genomic intervals over which to operate"
	}
}
