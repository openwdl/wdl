# --------------------------------------------------------------------------------------------
# This ContEst WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Estimate cross-sample contamination
# --------------------------------------------------------------------------------------------

task ContEst { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Boolean input_fileeval
	Boolean ? input_filegenotype
	Array[String] ? intervals
	String ? base_report
	Float ? beta_threshold
	String ? genotype_mode
	String ? genotypes
	String ? lane_level_contamination
	String ? likelihood_file
	Int ? min_mapq
	Int ? min_qscore
	Int ? minimum_base_count
	String ? out
	String popfile
	String ? population
	Float ? precision
	String ? sample_name
	Float ? trim_fraction
	Boolean ? verify_sample

	command {
		java -jar ${gatk} \
			-T ContEst \
			-R ${ref} \
			--input_file:eval ${input_fileeval} \
			${default="" "--input_file:genotype " + input_filegenotype} \
			${default="" "--intervals " + intervals} \
			${default="" "-br " + base_report} \
			beta_threshold ${default="0.95" beta_threshold} \
			-gm ${default="HARD_THRESHOLD" genotype_mode} \
			${default="" "-genotypes " + genotypes} \
			${default="" "-llc " + lane_level_contamination} \
			${default="" "-lf " + likelihood_file} \
			min_mapq ${default="20" min_mapq} \
			min_qscore ${default="20" min_qscore} \
			-mbc ${default="500" minimum_base_count} \
			-o ${default="stdout" out} \
			-pf ${popfile} \
			-population ${default="CEU" population} \
			-pc ${default="0.1" precision} \
			-sn ${default="unknown" sample_name} \
			trim_fraction ${default="0.01" trim_fraction} \
			-vs ${default="false" verify_sample} \
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
		base_report: "Where to write a full report about the loci we processed"
		beta_threshold: "threshold for p(f>=0.5) to trim"
		genotype_mode: "which approach should we take to getting the genotypes (only in array-free mode)"
		genotypes: "the genotype information for our sample"
		lane_level_contamination: "set to META (default), SAMPLE or READGROUP to produce per-bam, per-sample or per-lane estimates"
		likelihood_file: "write the likelihood values to the specified location"
		min_mapq: "threshold for minimum mapping quality score"
		min_qscore: "threshold for minimum base quality score"
		minimum_base_count: "what minimum number of bases do we need to see to call contamination in a lane / sample?"
		out: "An output file created by the walker.  Will overwrite contents if file exists"
		popfile: "the variant file containing information about the population allele frequencies"
		population: "evaluate contamination for just a single contamination population"
		precision: "the degree of precision to which the contamination tool should estimate (e.g. the bin size)"
		sample_name: "The sample name; used to extract the correct genotypes from mutli-sample truth vcfs"
		trim_fraction: "at most, what fraction of sites should be trimmed based on BETA_THRESHOLD"
		verify_sample: "should we verify that the sample name is in the genotypes file?"
		input_fileeval: "Output version information"
		input_filegenotype: "Output version information"
		intervals: "One or more genomic intervals over which to operate"
	}
}
