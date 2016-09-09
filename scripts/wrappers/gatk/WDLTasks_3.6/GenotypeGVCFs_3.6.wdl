# --------------------------------------------------------------------------------------------
# This GenotypeGVCFs WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Perform joint genotyping on gVCF files produced by HaplotypeCaller
# --------------------------------------------------------------------------------------------

task GenotypeGVCFs { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	Boolean ? annotateNDA
	Array[String] ? annotation
	String ? dbsnp
	Array[String] ? group
	Float ? heterozygosity
	Boolean ? includeNonVariantSites
	Float ? indel_heterozygosity
	Array[Float] ? input_prior
	Int ? max_alternate_alleles
	Int ? max_num_PL_values
	String ? out
	Int ? sample_ploidy
	Float ? standard_min_confidence_threshold_for_calling
	Float ? standard_min_confidence_threshold_for_emitting
	Array[String] variant

	command {
		java -jar ${gatk} \
			-T GenotypeGVCFs \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			-nda ${default="false" annotateNDA} \
			-A ${default="[]" annotation} \
			${default="" "-D " + dbsnp} \
			-G ${default="[StandardAnnotation]" group} \
			-hets ${default="0.001" heterozygosity} \
			-allSites ${default="false" includeNonVariantSites} \
			-indelHeterozygosity ${default="1.25E-4" indel_heterozygosity} \
			-inputPrior ${default="[]" input_prior} \
			-maxAltAlleles ${default="6" max_alternate_alleles} \
			-maxNumPLValues ${default="100" max_num_PL_values} \
			-o ${default="stdout" out} \
			-ploidy ${default="2" sample_ploidy} \
			-stand_call_conf ${default="30.0" standard_min_confidence_threshold_for_calling} \
			-stand_emit_conf ${default="30.0" standard_min_confidence_threshold_for_emitting} \
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
		annotateNDA: "If provided, we will annotate records with the number of alternate alleles that were discovered (but not necessarily genotyped) at a given site"
		annotation: "One or more specific annotations to recompute.  The single value 'none' removes the default annotations"
		dbsnp: "dbSNP file"
		group: "One or more classes/groups of annotations to apply to variant calls"
		heterozygosity: "Heterozygosity value used to compute prior likelihoods for any locus"
		includeNonVariantSites: "Include loci found to be non-variant after genotyping"
		indel_heterozygosity: "Heterozygosity for indel calling"
		input_prior: "Input prior for calls"
		max_alternate_alleles: "Maximum number of alternate alleles to genotype"
		max_num_PL_values: "Maximum number of PL values to output"
		out: "File to which variants should be written"
		sample_ploidy: "Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy)."
		standard_min_confidence_threshold_for_calling: "The minimum phred-scaled confidence threshold at which variants should be called"
		standard_min_confidence_threshold_for_emitting: "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)"
		variant: "One or more input gVCF files"
		intervals: "One or more genomic intervals over which to operate"
	}
}
