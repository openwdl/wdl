# --------------------------------------------------------------------------------------------
# This VariantRecalibrator WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Build a recalibration model to score variant quality for filtering purposes
# --------------------------------------------------------------------------------------------

task VariantRecalibrator { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	Int ? ntVal
	Array[String] ? aggregate
	Float ? badLodCutoff
	Float ? dirichlet
	Boolean ? ignore_all_filters
	Array[String] ? ignore_filter
	Array[String] task_input
	Int ? max_attempts
	Int ? maxGaussians
	Int ? maxIterations
	Int ? maxNegativeGaussians
	Int ? maxNumTrainingData
	Int ? minNumBadVariants
	String mode
	String ? model_file
	Int ? MQCapForLogitJitterTransform
	Int ? numKMeans
	Boolean ? output_model
	Float ? priorCounts
	String recal_file
	Array[String] resource
	File ? rscript_file
	Float ? shrinkage
	Float ? stdThreshold
	Float ? target_titv
	File tranches_file
	Boolean ? trustAllPolymorphic
	Array[Float] ? TStranche
	Array[String] use_annotation
	Boolean ? useAlleleSpecificAnnotations

	command {
		java -jar ${gatk} \
			-T VariantRecalibrator \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			${default="" "-nt" + ntVal} \
			${default="" "-aggregate " + aggregate} \
			-badLodCutoff ${default="-5.0" badLodCutoff} \
			-dirichlet ${default="0.001" dirichlet} \
			-ignoreAllFilters ${default="false" ignore_all_filters} \
			-ignoreFilter ${default="[]" ignore_filter} \
			-input ${task_input} \
			-max_attempts ${default="1" max_attempts} \
			-mG ${default="8" maxGaussians} \
			-mI ${default="150" maxIterations} \
			-mNG ${default="2" maxNegativeGaussians} \
			-maxNumTrainingData ${default="2500000" maxNumTrainingData} \
			-minNumBad ${default="1000" minNumBadVariants} \
			-mode ${mode} \
			-modelFile ${default="stdout" model_file} \
			-MQCap ${default="0" MQCapForLogitJitterTransform} \
			-nKM ${default="100" numKMeans} \
			-outputModel ${default="false" output_model} \
			-priorCounts ${default="20.0" priorCounts} \
			-recalFile ${recal_file} \
			-resource ${resource} \
			${default="" "-rscriptFile " + rscript_file} \
			-shrinkage ${default="1.0" shrinkage} \
			-std ${default="10.0" stdThreshold} \
			-titv ${default="2.15" target_titv} \
			-tranchesFile ${tranches_file} \
			-allPoly ${default="false" trustAllPolymorphic} \
			-tranche ${default="[100.0, 99.9, 99.0, 90.0]" TStranche} \
			-an ${use_annotation} \
			-AS ${default="false" useAlleleSpecificAnnotations} \
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
		aggregate: "Additional raw input variants to be used in building the model"
		badLodCutoff: "LOD score cutoff for selecting bad variants"
		dirichlet: "The dirichlet parameter in the variational Bayes algorithm."
		ignore_all_filters: "If specified, the variant recalibrator will ignore all input filters. Useful to rerun the VQSR from a filtered output file."
		ignore_filter: "If specified, the variant recalibrator will also use variants marked as filtered by the specified filter name in the input VCF file"
		task_input: "One or more VCFs of raw input variants to be recalibrated"
		max_attempts: "Number of attempts to build a model before failing"
		maxGaussians: "Max number of Gaussians for the positive model"
		maxIterations: "Maximum number of VBEM iterations"
		maxNegativeGaussians: "Max number of Gaussians for the negative model"
		maxNumTrainingData: "Maximum number of training data"
		minNumBadVariants: "Minimum number of bad variants"
		mode: "Recalibration mode to employ"
		model_file: "A GATKReport containing the positive and negative model fits"
		MQCapForLogitJitterTransform: "Apply logit transform and jitter to MQ values"
		numKMeans: "Number of k-means iterations"
		output_model: "If specified, the variant recalibrator will output the VQSR model fit to the file specified by -modelFile or to stdout"
		priorCounts: "The number of prior counts to use in the variational Bayes algorithm."
		recal_file: "The output recal file used by ApplyRecalibration"
		resource: "A list of sites for which to apply a prior probability of being correct but which aren't used by the algorithm (training and truth sets are required to run)"
		rscript_file: "The output rscript file generated by the VQSR to aid in visualization of the input data and learned model"
		shrinkage: "The shrinkage parameter in the variational Bayes algorithm."
		stdThreshold: "Annotation value divergence threshold (number of standard deviations from the means) "
		target_titv: "The expected novel Ti/Tv ratio to use when calculating FDR tranches and for display on the optimization curve output figures. (approx 2.15 for whole genome experiments). ONLY USED FOR PLOTTING PURPOSES!"
		tranches_file: "The output tranches file used by ApplyRecalibration"
		trustAllPolymorphic: "Trust that all the input training sets' unfiltered records contain only polymorphic sites to drastically speed up the computation."
		TStranche: "The levels of truth sensitivity at which to slice the data. (in percent, that is 1.0 for 1 percent)"
		use_annotation: "The names of the annotations which should used for calculations"
		useAlleleSpecificAnnotations: "If specified, the variant recalibrator will attempt to use the allele-specific versions of the specified annotations."
		intervals: "One or more genomic intervals over which to operate"
	}
}
