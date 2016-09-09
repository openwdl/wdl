# --------------------------------------------------------------------------------------------
# This VariantsToBinaryPed WDL task was generated on 09/09/16 for use with GATK version 3.6
# For more information on using this wrapper, please see the WDL repository at 
# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md
# Task Summary: Convert VCF to binary pedigree file
# --------------------------------------------------------------------------------------------

task VariantsToBinaryPed { 
	File gatk
	File ref
	File refIndex
	File refDict
	String ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string
	Array[String] ? intervals
	String bed
	String bim
	Boolean ? checkAlternateAlleles
	String ? dbsnp
	String fam
	Boolean ? majorAlleleFirst
	File metaData
	Int minGenotypeQuality
	String ? outputMode
	String variant

	command {
		java -jar ${gatk} \
			-T VariantsToBinaryPed \
			-R ${ref} \
			${default="" "--intervals " + intervals} \
			-bed ${bed} \
			-bim ${bim} \
			checkAlternateAlleles ${default="false" checkAlternateAlleles} \
			${default="" "-D " + dbsnp} \
			-fam ${fam} \
			majorAlleleFirst ${default="false" majorAlleleFirst} \
			-m ${metaData} \
			-mgq ${minGenotypeQuality} \
			-mode ${default="INDIVIDUAL_MAJOR" outputMode} \
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
		bed: "output bed file"
		bim: "output map file"
		checkAlternateAlleles: "Checks that alternate alleles actually appear in samples, erroring out if they do not"
		dbsnp: "dbSNP file"
		fam: "output fam file"
		majorAlleleFirst: "Sets the major allele to be 'reference' for the bim file, rather than the ref allele"
		metaData: "Sample metadata file"
		minGenotypeQuality: "If genotype quality is lower than this value, output NO_CALL"
		outputMode: "The output file mode (SNP major or individual major)"
		variant: "Input VCF file"
		intervals: "One or more genomic intervals over which to operate"
	}
}
