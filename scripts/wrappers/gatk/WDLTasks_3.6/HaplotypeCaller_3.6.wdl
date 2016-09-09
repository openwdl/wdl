# --------------------------------------------------------------------------------------------
# This HaplotypeCaller WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Call germline SNPs and indels via local re-assembly of haplotypes
# --------------------------------------------------------------------------------------------

task HaplotypeCaller { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] input_file
	Array[String] ? intervals
	File ? BQSR
	Int ? nctVal
	Float ? activeProbabilityThreshold
	Int ? activeRegionExtension
	Array[String] ? activeRegionIn
	Int ? activeRegionMaxSize
	String ? activeRegionOut
	String ? activityProfileOut
	String ? alleles
	Boolean ? allowNonUniqueKmersInRef
	Boolean ? allSitePLs
	Boolean ? annotateNDA
	Array[String] ? annotation
	String ? bamOutput
	String ? bamWriterType
	Float ? bandPassSigma
	Array[String] ? comp
	Boolean ? consensus
	File ? contamination_fraction_per_sample_file
	Float ? contamination_fraction_to_filter
	String ? dbsnp
	Boolean ? debug
	Boolean ? disableOptimizations
	Boolean ? doNotRunPhysicalPhasing
	Boolean ? dontIncreaseKmerSizesForCycles
	Boolean ? dontTrimActiveRegions
	Boolean ? dontUseSoftClippedBases
	Boolean ? emitDroppedReads
	String ? emitRefConfidence
	Array[String] ? excludeAnnotation
	Boolean ? forceActive
	Int ? gcpHMM
	String ? genotyping_mode
	String ? graphOutput
	Array[String] ? group
	Array[Int] ? GVCFGQBands
	Float ? heterozygosity
	Float ? indel_heterozygosity
	Int ? indelSizeToEliminateInRefModel
	Array[Float] ? input_prior
	Array[Int] ? kmerSize
	Int ? max_alternate_alleles
	Int ? max_num_PL_values
	Int ? maxNumHaplotypesInPopulation
	Int ? maxReadsInRegionPerSample
	String ? min_base_quality_score
	Int ? minDanglingBranchLength
	Int ? minPruning
	Int ? minReadsPerAlignmentStart
	Int ? numPruningSamples
	String ? out
	String ? output_mode
	String ? pcr_indel_model
	Int ? phredScaledGlobalReadMismappingRate
	String ? sample_name
	Int ? sample_ploidy
	Float ? standard_min_confidence_threshold_for_calling
	Float ? standard_min_confidence_threshold_for_emitting
	Boolean ? useAllelesTrigger
	Boolean ? useFilteredReadsForAnnotations

	command {
		java -jar ${gatk} \
			-T HaplotypeCaller \
			-R ${ref} \
			--input_file ${input_file} \
			${default="" "--intervals " + intervals} \
			${default="" "--BQSR " + BQSR} \
			${default="" "-nct" + nctVal} \
			-ActProbThresh ${default="0.002" activeProbabilityThreshold} \
			${default="" "-activeRegionExtension " + activeRegionExtension} \
			${default="" "-AR " + activeRegionIn} \
			${default="" "-activeRegionMaxSize " + activeRegionMaxSize} \
			${default="" "-ARO " + activeRegionOut} \
			${default="" "-APO " + activityProfileOut} \
			${default="" "-alleles " + alleles} \
			-allowNonUniqueKmersInRef ${default="false" allowNonUniqueKmersInRef} \
			-allSitePLs ${default="false" allSitePLs} \
			-nda ${default="false" annotateNDA} \
			-A ${default="[]" annotation} \
			${default="" "-bamout " + bamOutput} \
			-bamWriterType ${default="CALLED_HAPLOTYPES" bamWriterType} \
			${default="" "-bandPassSigma " + bandPassSigma} \
			-comp ${default="[]" comp} \
			-consensus ${default="false" consensus} \
			${default="" "-contaminationFile " + contamination_fraction_per_sample_file} \
			-contamination ${default="0.0" contamination_fraction_to_filter} \
			${default="" "-D " + dbsnp} \
			-debug ${default="false" debug} \
			-disableOptimizations ${default="false" disableOptimizations} \
			-doNotRunPhysicalPhasing ${default="false" doNotRunPhysicalPhasing} \
			-dontIncreaseKmerSizesForCycles ${default="false" dontIncreaseKmerSizesForCycles} \
			-dontTrimActiveRegions ${default="false" dontTrimActiveRegions} \
			-dontUseSoftClippedBases ${default="false" dontUseSoftClippedBases} \
			-edr ${default="false" emitDroppedReads} \
			-ERC ${default="false" emitRefConfidence} \
			-XA ${default="[]" excludeAnnotation} \
			-forceActive ${default="false" forceActive} \
			-gcpHMM ${default="10" gcpHMM} \
			-gt_mode ${default="DISCOVERY" genotyping_mode} \
			${default="" "-graph " + graphOutput} \
			-G ${default="[StandardAnnotation, StandardHCAnnotation]" group} \
			-GQB ${default="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]" GVCFGQBands} \
			-hets ${default="0.001" heterozygosity} \
			-indelHeterozygosity ${default="1.25E-4" indel_heterozygosity} \
			-ERCIS ${default="10" indelSizeToEliminateInRefModel} \
			-inputPrior ${default="[]" input_prior} \
			-kmerSize ${default="[10, 25]" kmerSize} \
			-maxAltAlleles ${default="6" max_alternate_alleles} \
			-maxNumPLValues ${default="100" max_num_PL_values} \
			-maxNumHaplotypesInPopulation ${default="128" maxNumHaplotypesInPopulation} \
			-maxReadsInRegionPerSample ${default="10000" maxReadsInRegionPerSample} \
			-mbq ${default="10" min_base_quality_score} \
			-minDanglingBranchLength ${default="4" minDanglingBranchLength} \
			-minPruning ${default="2" minPruning} \
			-minReadsPerAlignStart ${default="10" minReadsPerAlignmentStart} \
			-numPruningSamples ${default="1" numPruningSamples} \
			-o ${default="stdout" out} \
			-out_mode ${default="EMIT_VARIANTS_ONLY" output_mode} \
			-pcrModel ${default="CONSERVATIVE" pcr_indel_model} \
			-globalMAPQ ${default="45" phredScaledGlobalReadMismappingRate} \
			${default="" "-sn " + sample_name} \
			-ploidy ${default="2" sample_ploidy} \
			-stand_call_conf ${default="30.0" standard_min_confidence_threshold_for_calling} \
			-stand_emit_conf ${default="30.0" standard_min_confidence_threshold_for_emitting} \
			-allelesTrigger ${default="false" useAllelesTrigger} \
			-useFilteredReadsForAnnotations ${default="false" useFilteredReadsForAnnotations} \
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
		alleles: "The set of alleles at which to genotype when --genotyping_mode is GENOTYPE_GIVEN_ALLELES"
		allowNonUniqueKmersInRef: "Allow graphs that have non-unique kmers in the reference"
		allSitePLs: "Annotate all sites with PLs"
		annotateNDA: "If provided, we will annotate records with the number of alternate alleles that were discovered (but not necessarily genotyped) at a given site"
		annotation: "One or more specific annotations to apply to variant calls"
		bamOutput: "File to which assembled haplotypes should be written"
		bamWriterType: "Which haplotypes should be written to the BAM"
		bandPassSigma: "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default"
		comp: "Comparison VCF file"
		consensus: "1000G consensus mode"
		contamination_fraction_per_sample_file: "Tab-separated File containing fraction of contamination in sequencing data (per sample) to aggressively remove. Format should be <SampleID><TAB><Contamination> (Contamination is double) per line; No header."
		contamination_fraction_to_filter: "Fraction of contamination in sequencing data (for all samples) to aggressively remove"
		dbsnp: "dbSNP file"
		debug: "Print out very verbose debug information about each triggering active region"
		disableOptimizations: "Don't skip calculations in ActiveRegions with no variants"
		doNotRunPhysicalPhasing: "Disable physical phasing"
		dontIncreaseKmerSizesForCycles: "Disable iterating over kmer sizes when graph cycles are detected"
		dontTrimActiveRegions: "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping"
		dontUseSoftClippedBases: "Do not analyze soft clipped bases in the reads"
		emitDroppedReads: "Emit reads that are dropped for filtering, trimming, realignment failure"
		emitRefConfidence: "Mode for emitting reference confidence scores"
		excludeAnnotation: "One or more specific annotations to exclude"
		forceActive: "If provided, all bases will be tagged as active"
		gcpHMM: "Flat gap continuation penalty for use in the Pair HMM"
		genotyping_mode: "Specifies how to determine the alternate alleles to use for genotyping"
		graphOutput: "Write debug assembly graph information to this file"
		group: "One or more classes/groups of annotations to apply to variant calls"
		GVCFGQBands: "GQ thresholds for reference confidence bands"
		heterozygosity: "Heterozygosity value used to compute prior likelihoods for any locus"
		indel_heterozygosity: "Heterozygosity for indel calling"
		indelSizeToEliminateInRefModel: "The size of an indel to check for in the reference model"
		input_prior: "Input prior for calls"
		kmerSize: "Kmer size to use in the read threading assembler"
		max_alternate_alleles: "Maximum number of alternate alleles to genotype"
		max_num_PL_values: "Maximum number of PL values to output"
		maxNumHaplotypesInPopulation: "Maximum number of haplotypes to consider for your population"
		maxReadsInRegionPerSample: "Maximum reads in an active region"
		min_base_quality_score: "Minimum base quality required to consider a base for calling"
		minDanglingBranchLength: "Minimum length of a dangling branch to attempt recovery"
		minPruning: "Minimum support to not prune paths in the graph"
		minReadsPerAlignmentStart: "Minimum number of reads sharing the same alignment start for each genomic location in an active region"
		numPruningSamples: "Number of samples that must pass the minPruning threshold"
		out: "File to which variants should be written"
		output_mode: "Specifies which type of calls we should output"
		pcr_indel_model: "The PCR indel model to use"
		phredScaledGlobalReadMismappingRate: "The global assumed mismapping rate for reads"
		sample_name: "Name of single sample to use from a multi-sample bam"
		sample_ploidy: "Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy)."
		standard_min_confidence_threshold_for_calling: "The minimum phred-scaled confidence threshold at which variants should be called"
		standard_min_confidence_threshold_for_emitting: "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)"
		useAllelesTrigger: "Use additional trigger on variants found in an external alleles file"
		useFilteredReadsForAnnotations: "Use the contamination-filtered read maps for the purposes of annotating variants"
		input_file: "Input file containing sequence data (BAM or CRAM)"
		intervals: "One or more genomic intervals over which to operate"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
