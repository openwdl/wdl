# --------------------------------------------------------------------------------------------
# This VariantEval WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: General-purpose tool for variant evaluation (% in dbSNP, genotype concordance, Ti/Tv ratios, and a lot more)
# --------------------------------------------------------------------------------------------

task VariantEval { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	File ? ancestralAlignments
	Array[String] ? comp
	String ? dbsnp
	Boolean ? doNotUseAllStandardModules
	Boolean ? doNotUseAllStandardStratifications
	Array[String] eval
	String ? evalModule
	String ? goldStandard
	Boolean ? keepAC0
	String ? known_names
	String ? knownCNVs
	Boolean ? list
	Float ? mendelianViolationQualThreshold
	Boolean ? mergeEvals
	Float ? minPhaseQuality
	String ? out
	Boolean ? requireStrictAlleleMatch
	String ? sample
	Int ? samplePloidy
	Array[String] ? select_exps
	Array[String] ? select_names
	String ? stratificationModule
	String ? stratIntervals

	command {
		java -jar ${gatk} \
			-T VariantEval \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			${default="" "-aa " + ancestralAlignments} \
			-comp ${default="[]" comp} \
			${default="" "-D " + dbsnp} \
			-noEV ${default="false" doNotUseAllStandardModules} \
			-noST ${default="false" doNotUseAllStandardStratifications} \
			-eval ${eval} \
			-EV ${default="[]" evalModule} \
			${default="" "-gold " + goldStandard} \
			-keepAC0 ${default="false" keepAC0} \
			-knownName ${default="[]" known_names} \
			${default="" "-knownCNVs " + knownCNVs} \
			-ls ${default="false" list} \
			-mvq ${default="50.0" mendelianViolationQualThreshold} \
			-mergeEvals ${default="false" mergeEvals} \
			-mpq ${default="10.0" minPhaseQuality} \
			-o ${default="stdout" out} \
			-strict ${default="false" requireStrictAlleleMatch} \
			${default="" "-sn " + sample} \
			-ploidy ${default="2" samplePloidy} \
			-select ${default="[]" select_exps} \
			-selectName ${default="[]" select_names} \
			-ST ${default="[]" stratificationModule} \
			${default="" "-stratIntervals " + stratIntervals} \
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
		ancestralAlignments: "Fasta file with ancestral alleles"
		comp: "Input comparison file(s)"
		dbsnp: "dbSNP file"
		doNotUseAllStandardModules: "Do not use the standard modules by default (instead, only those that are specified with the -EV option)"
		doNotUseAllStandardStratifications: "Do not use the standard stratification modules by default (instead, only those that are specified with the -S option)"
		eval: "Input evaluation file(s)"
		evalModule: "One or more specific eval modules to apply to the eval track(s) (in addition to the standard modules, unless -noEV is specified)"
		goldStandard: "Evaluations that count calls at sites of true variation (e.g., indel calls) will use this argument as their gold standard for comparison"
		keepAC0: "If provided, modules that track polymorphic sites will not require that a site have AC > 0 when the input eval has genotypes"
		known_names: "Name of ROD bindings containing variant sites that should be treated as known when splitting eval rods into known and novel subsets"
		knownCNVs: "File containing tribble-readable features describing a known list of copy number variants"
		list: "List the available eval modules and exit"
		mendelianViolationQualThreshold: "Minimum genotype QUAL score for each trio member required to accept a site as a violation. Default is 50."
		mergeEvals: "If provided, all -eval tracks will be merged into a single eval track"
		minPhaseQuality: "Minimum phasing quality"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		requireStrictAlleleMatch: "If provided only comp and eval tracks with exactly matching reference and alternate alleles will be counted as overlapping"
		sample: "Derive eval and comp contexts using only these sample genotypes, when genotypes are available in the original context"
		samplePloidy: "Per-sample ploidy (number of chromosomes per sample)"
		select_exps: "One or more stratifications to use when evaluating the data"
		select_names: "Names to use for the list of stratifications (must be a 1-to-1 mapping)"
		stratificationModule: "One or more specific stratification modules to apply to the eval track(s) (in addition to the standard stratifications, unless -noS is specified)"
		stratIntervals: "File containing tribble-readable features for the IntervalStratificiation"
		intervals: "One or more genomic intervals over which to operate"
	}
}
