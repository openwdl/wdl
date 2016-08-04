# Tutorial_8017_toSE.wdl ##########################################################
#
# This WDL script recapitulates one of the workflows outlined in Tutorial#8017 at
# <https://software.broadinstitute.org/gatk/documentation/article?id=8017>.
# The tutorial provides example input data including a mini-reference
# that finishes processing in a few minutes.
#
# Until the HaplotypeCaller feature to disable the BadMateFilter is available, this
# script provides a blunt workaround.
#
# Requires Gawk, a cousin of AWK that parses bitwise flags.
###################################################################################

## Strip 0x1 PAIRED flag from reads to circumvent HaplotypeCaller's BadMateFilter
## Note this task produces a SAM that does NOT VALIDATE with ValidateSamFile.
task PairedToSingleEnd {
  File snaut_bam
  File samtools
  String file_basename

  command <<<
    ${samtools} view -h ${snaut_bam} | \
    gawk '{printf "%s\t", $1; if(and($2,0x1)){t=$2-0x1}else{t=$2};
     printf "%s\t" , t; for (i=3; i<NF; i++){printf "%s\t", $i} ;
     printf "%s\n",$NF}'| ${samtools} view -Sb - > ${file_basename}_se.bam
     ${samtools} index ${file_basename}_se.bam ${file_basename}_se.bai
  >>>
  output {
    File se_bam = "${file_basename}_se.bam"
    File se_bai = "${file_basename}_se.bai"
  }
}

## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample
## using HaplotypeCaller
task CallSampleVariants {
  File GATK
  String file_basename
  File se_bai
  File se_bam
  File ref_fasta
  File ref_index
  File ref_dict

  command {
  java -jar ${GATK} \
    -T HaplotypeCaller \
    -R ${ref_fasta} \
    -I ${se_bam} \
    -o ${file_basename}.g.vcf \
	-ERC GVCF \
	--emitDroppedReads \
	-bamout ${file_basename}_hc.bam
  }
  output {
    File sample_gvcfs = "${file_basename}.g.vcf"
    File sample_gvcf_indices = "${file_basename}.g.vcf.idx"
    File bamout = "${file_basename}_hc.bam"
  }
}

## [4.7] Call genotypes on all samples
task CallCohortVariants {
  File GATK
  Array [File] sample_gvcfs
  Array [File] sample_gvcf_indices
  File ref_fasta
  File ref_index
  File ref_dict
  String final_vcf_name

  command {
  java -jar ${GATK} \
    -T GenotypeGVCFs \
    -R ${ref_fasta} \
    -o ${final_vcf_name}.vcf \
    --variant ${sep=' --variant ' sample_gvcfs}
  }
  output {
    File cohort_vcf = "${final_vcf_name}.vcf"
    File cohort_vcf_index = "${final_vcf_name}.vcf.idx"
  }
}

# WORKFLOW DEFINITION ########################################################

workflow Tutorial_8017_toSE {
  Array[Array[File]] snaut_bam
  File samtools
  File GATK
  String bam_directory_path
  String final_vcf_name
  File ref_fasta
  File ref_index
  File ref_dict

## Scatter all but last step
  scatter (bam in snaut_bam) {

	## Get file_basename
		String sub_strip_path = bam_directory_path
		String sub_strip_extension = "\\.bam" + "$"

	## Strip 0x1 PAIRED flag from reads to circumvent HaplotypeCaller's BadMateFilter
		call PairedToSingleEnd {
		input:
		snaut_bam = bam[0],
		samtools = samtools,
		file_basename = sub(sub(bam[0], sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample using HaplotypeCaller
		call CallSampleVariants {
		input:
		GATK = GATK,
		se_bai = PairedToSingleEnd.se_bai,
		se_bam = PairedToSingleEnd.se_bam,
		file_basename = sub(sub(bam[0], sub_strip_path, ""), sub_strip_extension, ""),
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}
	  }

## [4.7] Call genotypes on samples
call CallCohortVariants {
  input:
  GATK = GATK,
  sample_gvcfs = CallSampleVariants.sample_gvcfs,
  sample_gvcf_indices = CallSampleVariants.sample_gvcf_indices,
  ref_fasta = ref_fasta,
  ref_index = ref_index,
  ref_dict = ref_dict,
  final_vcf_name = final_vcf_name
  }
}
