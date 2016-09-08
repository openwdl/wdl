# --------------------------------------------------------------------------------------------
# This UnifiedGenotyper WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Call SNPs and indels on a per-locus basis
# --------------------------------------------------------------------------------------------

task UnifiedGenotyper { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	File ? BQSR
	Int ? nctVal
	Int ? ntVal
	String ? alleles
	Boolean ? allSitePLs
	Boolean ? annotateNDA
	Array[String] ? annotation
	Array[String] ? comp
	Boolean ? computeSLOD
	File ? contamination_fraction_per_sample_file
	Float ? contamination_fraction_to_filter
	String ? dbsnp
	Array[String] ? excludeAnnotation
	String ? genotype_likelihoods_model
	String ? genotyping_mode
	String ? group
	Float ? heterozygosity
	Float ? indel_heterozygosity
	String ? indelGapContinuationPenalty
	String ? indelGapOpenPenalty
	Array[Float] ? input_prior
	Int ? max_alternate_alleles
	Float ? max_deletion_fraction
	Int ? max_num_PL_values
	Int ? min_base_quality_score
	Int ? min_indel_count_for_genotyping
	Float ? min_indel_fraction_per_sample
	String ? onlyEmitSamples
	String ? out
	String ? output_mode
	String ? pair_hmm_implementation
	Float ? pcr_error_rate
	Int ? sample_ploidy
	Float ? standard_min_confidence_threshold_for_calling
	Float ? standard_min_confidence_threshold_for_emitting

	command {
		java -jar ${gatk} \
			-T UnifiedGenotyper \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "--BQSR " + BQSR} \
			${default="" "-nct" + nctVal} \
			${default="" "-nt" + ntVal} \
			${default="" "-alleles " + alleles} \
			-allSitePLs ${default="false" allSitePLs} \
			-nda ${default="false" annotateNDA} \
			-A ${default="[]" annotation} \
			-comp ${default="[]" comp} \
			-slod ${default="false" computeSLOD} \
			${default="" "-contaminationFile " + contamination_fraction_per_sample_file} \
			-contamination ${default="0.0" contamination_fraction_to_filter} \
			${default="" "-D " + dbsnp} \
			-XA ${default="[]" excludeAnnotation} \
			-glm ${default="SNP" genotype_likelihoods_model} \
			-gt_mode ${default="DISCOVERY" genotyping_mode} \
			-G ${default="[Standard, StandardUG]" group} \
			-hets ${default="0.001" heterozygosity} \
			-indelHeterozygosity ${default="1.25E-4" indel_heterozygosity} \
			-indelGCP ${default="10" indelGapContinuationPenalty} \
			-indelGOP ${default="45" indelGapOpenPenalty} \
			-inputPrior ${default="[]" input_prior} \
			-maxAltAlleles ${default="6" max_alternate_alleles} \
			-deletions ${default="0.05" max_deletion_fraction} \
			-maxNumPLValues ${default="100" max_num_PL_values} \
			-mbq ${default="17" min_base_quality_score} \
			-minIndelCnt ${default="5" min_indel_count_for_genotyping} \
			-minIndelFrac ${default="0.25" min_indel_fraction_per_sample} \
			-onlyEmitSamples ${default="[]" onlyEmitSamples} \
			-o ${default="stdout" out} \
			-out_mode ${default="EMIT_VARIANTS_ONLY" output_mode} \
			-pairHMM ${default="LOGLESS_CACHING" pair_hmm_implementation} \
			-pcr_error ${default="1.0E-4" pcr_error_rate} \
			-ploidy ${default="2" sample_ploidy} \
			-stand_call_conf ${default="30.0" standard_min_confidence_threshold_for_calling} \
			-stand_emit_conf ${default="30.0" standard_min_confidence_threshold_for_emitting} \
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
		alleles: "The set of alleles at which to genotype when --genotyping_mode is GENOTYPE_GIVEN_ALLELES"
		allSitePLs: "Annotate all sites with PLs"
		annotateNDA: "If provided, we will annotate records with the number of alternate alleles that were discovered (but not necessarily genotyped) at a given site"
		annotation: "One or more specific annotations to apply to variant calls"
		comp: "Comparison VCF file"
		computeSLOD: "If provided, we will calculate the SLOD (SB annotation)"
		contamination_fraction_per_sample_file: "Tab-separated File containing fraction of contamination in sequencing data (per sample) to aggressively remove. Format should be <SampleID><TAB><Contamination> (Contamination is double) per line; No header."
		contamination_fraction_to_filter: "Fraction of contamination in sequencing data (for all samples) to aggressively remove"
		dbsnp: "dbSNP file"
		excludeAnnotation: "One or more specific annotations to exclude"
		genotype_likelihoods_model: "Genotype likelihoods calculation model to employ -- SNP is the default option, while INDEL is also available for calling indels and BOTH is available for calling both together"
		genotyping_mode: "Specifies how to determine the alternate alleles to use for genotyping"
		group: "One or more classes/groups of annotations to apply to variant calls.  The single value 'none' removes the default group"
		heterozygosity: "Heterozygosity value used to compute prior likelihoods for any locus"
		indel_heterozygosity: "Heterozygosity for indel calling"
		indelGapContinuationPenalty: "Indel gap continuation penalty, as Phred-scaled probability.  I.e., 30 => 10^-30/10"
		indelGapOpenPenalty: "Indel gap open penalty, as Phred-scaled probability.  I.e., 30 => 10^-30/10"
		input_prior: "Input prior for calls"
		max_alternate_alleles: "Maximum number of alternate alleles to genotype"
		max_deletion_fraction: "Maximum fraction of reads with deletions spanning this locus for it to be callable"
		max_num_PL_values: "Maximum number of PL values to output"
		min_base_quality_score: "Minimum base quality required to consider a base for calling"
		min_indel_count_for_genotyping: "Minimum number of consensus indels required to trigger genotyping run"
		min_indel_fraction_per_sample: "Minimum fraction of all reads at a locus that must contain an indel (of any allele) for that sample to contribute to the indel count for alleles"
		onlyEmitSamples: "If provided, only these samples will be emitted into the VCF, regardless of which samples are present in the BAM file"
		out: "File to which variants should be written"
		output_mode: "Specifies which type of calls we should output"
		pair_hmm_implementation: "The PairHMM implementation to use for -glm INDEL genotype likelihood calculations"
		pcr_error_rate: "The PCR error rate to be used for computing fragment-based likelihoods"
		sample_ploidy: "Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy)."
		standard_min_confidence_threshold_for_calling: "The minimum phred-scaled confidence threshold at which variants should be called"
		standard_min_confidence_threshold_for_emitting: "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
