# --------------------------------------------------------------------------------------------
# This MuTect2 WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Call somatic SNPs and indels via local re-assembly of haplotypes
# --------------------------------------------------------------------------------------------

task MuTect2 { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Boolean input_filetumor
	Boolean ? input_filenormal
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
	Boolean ? artifact_detection_mode
	String ? bamOutput
	String ? bamWriterType
	Float ? bandPassSigma
	Array[String] ? comp
	Boolean ? consensus
	File ? contamination_fraction_per_sample_file
	Float ? contamination_fraction_to_filter
	Array[String] ? cosmic
	String ? dbsnp
	Float ? dbsnp_normal_lod
	Boolean ? debug
	String ? debug_read_name
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
	String ? group
	Float ? heterozygosity
	Float ? indel_heterozygosity
	Float ? initial_normal_lod
	Float ? initial_tumor_lod
	Array[Float] ? input_prior
	Array[Int] ? kmerSize
	Boolean ? m2debug
	Float ? max_alt_allele_in_normal_fraction
	Int ? max_alt_alleles_in_normal_count
	Int ? max_alt_alleles_in_normal_qscore_sum
	Int ? max_alternate_alleles
	Int ? max_num_PL_values
	Int ? maxNumHaplotypesInPopulation
	String ? min_base_quality_score
	Int ? minDanglingBranchLength
	Int ? minPruning
	Float ? normal_lod
	Array[String] ? normal_panel
	Int ? numPruningSamples
	String ? out
	String ? output_mode
	Int ? phredScaledGlobalReadMismappingRate
	Int ? sample_ploidy
	Float ? standard_min_confidence_threshold_for_calling
	Float ? standard_min_confidence_threshold_for_emitting
	Float ? tumor_lod
	Boolean ? useFilteredReadsForAnnotations

	command {
		java -jar ${gatk} \
			-T MuTect2 \
			-R ${ref} \
			--input_file:tumor ${input_filetumor} \
			${default="" "--input_file:normal " + input_filenormal} \
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
			-A ${default="[DepthPerAlleleBySample, BaseQualitySumPerAlleleBySample, TandemRepeatAnnotator, OxoGReadCounts]" annotation} \
			artifact_detection_mode ${default="false" artifact_detection_mode} \
			${default="" "-bamout " + bamOutput} \
			-bamWriterType ${default="CALLED_HAPLOTYPES" bamWriterType} \
			${default="" "-bandPassSigma " + bandPassSigma} \
			-comp ${default="[]" comp} \
			-consensus ${default="false" consensus} \
			${default="" "-contaminationFile " + contamination_fraction_per_sample_file} \
			-contamination ${default="0.0" contamination_fraction_to_filter} \
			-cosmic ${default="[]" cosmic} \
			${default="" "-D " + dbsnp} \
			dbsnp_normal_lod ${default="5.5" dbsnp_normal_lod} \
			-debug ${default="false" debug} \
			${default="" "debug_read_name " + debug_read_name} \
			-disableOptimizations ${default="false" disableOptimizations} \
			-doNotRunPhysicalPhasing ${default="false" doNotRunPhysicalPhasing} \
			-dontIncreaseKmerSizesForCycles ${default="false" dontIncreaseKmerSizesForCycles} \
			-dontTrimActiveRegions ${default="false" dontTrimActiveRegions} \
			-dontUseSoftClippedBases ${default="false" dontUseSoftClippedBases} \
			-edr ${default="false" emitDroppedReads} \
			-ERC ${default="NONE" emitRefConfidence} \
			-XA ${default="[SpanningDeletions]" excludeAnnotation} \
			-forceActive ${default="false" forceActive} \
			-gcpHMM ${default="10" gcpHMM} \
			-gt_mode ${default="DISCOVERY" genotyping_mode} \
			${default="" "-graph " + graphOutput} \
			-G ${default="[]" group} \
			-hets ${default="0.001" heterozygosity} \
			-indelHeterozygosity ${default="1.25E-4" indel_heterozygosity} \
			initial_normal_lod ${default="0.5" initial_normal_lod} \
			initial_tumor_lod ${default="4.0" initial_tumor_lod} \
			-inputPrior ${default="[]" input_prior} \
			-kmerSize ${default="[10, 25]" kmerSize} \
			-m2debug ${default="false" m2debug} \
			max_alt_allele_in_normal_fraction ${default="0.03" max_alt_allele_in_normal_fraction} \
			max_alt_alleles_in_normal_count ${default="1" max_alt_alleles_in_normal_count} \
			max_alt_alleles_in_normal_qscore_sum ${default="20" max_alt_alleles_in_normal_qscore_sum} \
			-maxAltAlleles ${default="6" max_alternate_alleles} \
			-maxNumPLValues ${default="100" max_num_PL_values} \
			-maxNumHaplotypesInPopulation ${default="128" maxNumHaplotypesInPopulation} \
			-mbq ${default="10" min_base_quality_score} \
			-minDanglingBranchLength ${default="4" minDanglingBranchLength} \
			-minPruning ${default="2" minPruning} \
			normal_lod ${default="2.2" normal_lod} \
			-PON ${default="[]" normal_panel} \
			-numPruningSamples ${default="1" numPruningSamples} \
			-o ${default="stdout" out} \
			-out_mode ${default="EMIT_VARIANTS_ONLY" output_mode} \
			-globalMAPQ ${default="45" phredScaledGlobalReadMismappingRate} \
			-ploidy ${default="2" sample_ploidy} \
			-stand_call_conf ${default="30.0" standard_min_confidence_threshold_for_calling} \
			-stand_emit_conf ${default="30.0" standard_min_confidence_threshold_for_emitting} \
			tumor_lod ${default="6.3" tumor_lod} \
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
		artifact_detection_mode: "Enable artifact detection for creating panels of normals"
		bamOutput: "File to which assembled haplotypes should be written"
		bamWriterType: "Which haplotypes should be written to the BAM"
		bandPassSigma: "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default"
		comp: "comparison VCF file"
		consensus: "1000G consensus mode"
		contamination_fraction_per_sample_file: "Tab-separated File containing fraction of contamination in sequencing data (per sample) to aggressively remove. Format should be <SampleID><TAB><Contamination> (Contamination is double) per line; No header."
		contamination_fraction_to_filter: "Fraction of contamination in sequencing data (for all samples) to aggressively remove"
		cosmic: "VCF file of COSMIC sites"
		dbsnp: "dbSNP file"
		dbsnp_normal_lod: "LOD threshold for calling normal non-variant at dbsnp sites"
		debug: "Print out very verbose debug information about each triggering active region"
		debug_read_name: "trace this read name through the calling process"
		disableOptimizations: "Don't skip calculations in ActiveRegions with no variants"
		doNotRunPhysicalPhasing: "Disable physical phasing"
		dontIncreaseKmerSizesForCycles: "Disable iterating over kmer sizes when graph cycles are detected"
		dontTrimActiveRegions: "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping"
		dontUseSoftClippedBases: "If specified, we will not analyze soft clipped bases in the reads"
		emitDroppedReads: "Emit reads that are dropped for filtering, trimming, realignment failure"
		emitRefConfidence: "Mode for emitting reference confidence scores"
		excludeAnnotation: "One or more specific annotations to exclude"
		forceActive: "If provided, all bases will be tagged as active"
		gcpHMM: "Flat gap continuation penalty for use in the Pair HMM"
		genotyping_mode: "Specifies how to determine the alternate alleles to use for genotyping"
		graphOutput: "Write debug assembly graph information to this file"
		group: "One or more classes/groups of annotations to apply to variant calls"
		heterozygosity: "Heterozygosity value used to compute prior likelihoods for any locus"
		indel_heterozygosity: "Heterozygosity for indel calling"
		initial_normal_lod: "Initial LOD threshold for calling normal variant"
		initial_tumor_lod: "Initial LOD threshold for calling tumor variant"
		input_prior: "Input prior for calls"
		kmerSize: "Kmer size to use in the read threading assembler"
		m2debug: "Print out very verbose M2 debug information"
		max_alt_allele_in_normal_fraction: "Threshold for maximum alternate allele fraction in normal"
		max_alt_alleles_in_normal_count: "Threshold for maximum alternate allele counts in normal"
		max_alt_alleles_in_normal_qscore_sum: "Threshold for maximum alternate allele quality score sum in normal"
		max_alternate_alleles: "Maximum number of alternate alleles to genotype"
		max_num_PL_values: "Maximum number of PL values to output"
		maxNumHaplotypesInPopulation: "Maximum number of haplotypes to consider for your population"
		min_base_quality_score: "Minimum base quality required to consider a base for calling"
		minDanglingBranchLength: "Minimum length of a dangling branch to attempt recovery"
		minPruning: "Minimum support to not prune paths in the graph"
		normal_lod: "LOD threshold for calling normal non-germline"
		normal_panel: "VCF file of sites observed in normal"
		numPruningSamples: "Number of samples that must pass the minPruning threshold"
		out: "File to which variants should be written"
		output_mode: "Specifies which type of calls we should output"
		phredScaledGlobalReadMismappingRate: "The global assumed mismapping rate for reads"
		sample_ploidy: "Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy)."
		standard_min_confidence_threshold_for_calling: "The minimum phred-scaled confidence threshold at which variants should be called"
		standard_min_confidence_threshold_for_emitting: "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)"
		tumor_lod: "LOD threshold for calling tumor variant"
		useFilteredReadsForAnnotations: "Use the contamination-filtered read maps for the purposes of annotating variants"
		input_filetumor: "Output version information"
		input_filenormal: "Output version information"
		intervals: "One or more genomic intervals over which to operate"
		BQSR: "Input covariates table file for on-the-fly base quality score recalibration"
	}
}
