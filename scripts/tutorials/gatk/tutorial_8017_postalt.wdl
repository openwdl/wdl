# Tutorial_8017_postalt.wdl ################################################
#
# This WDL script recapitulates one of the workflows outlined in Tutorial#8017 at
# <https://software.broadinstitute.org/gatk/documentation/article?id=8017>.
# The tutorial provides example input data including a mini-reference
# that finishes processing in a few minutes.
#
# Until the HaplotypeCaller feature to disable the BadMateFilter is available, this
# script provides a blunt workaround.
#
# Requires Gawk, a cousin of AWK that parses bitwise flags, and the javascript
# interpreter k8 as well as the bwa-postalt.js script.
###################################################################################

## K8 postalt.js process query-grouped aligned SAM
task PostAltProcess {
  File K8
  File POSTALT
  File ref_alt
  File aligned_sam
  String file_basename

  command {
    ${K8} ${POSTALT} ${ref_alt} ${aligned_sam} > ${file_basename}_postalt.sam
  }
  output {
    File postalt_sam = "${file_basename}_postalt.sam"
  }
}

## [4.1] Create unmapped uBAM
task CreateUbam {
  File PICARD
  File aligned_sam
  String file_basename

  command {
	java -jar ${PICARD} RevertSam \
	  I=${aligned_sam} \
	  O=${file_basename}_u.bam \
	  ATTRIBUTE_TO_CLEAR=XS \
	  ATTRIBUTE_TO_CLEAR=XA
  }
  output {
    File u_bam = "${file_basename}_u.bam"
  }
}

## [4.2] Add read group information to uBAM
task AddRgToUbam {
  File PICARD
  File u_bam
  String file_basename
  String rg_id
  String rg_sm

  command {
    java -jar ${PICARD} AddOrReplaceReadGroups \
      I=${u_bam} \
      O=${file_basename}_rg.bam \
      RGID=${rg_id} \
      RGSM=${rg_sm} \
      RGLB=wgsim \
      RGPU=shlee \
      RGPL=illumina
  }
  output {
    File rg_bam = "${file_basename}_rg.bam"
  }
}

## [4.3] Merge uBAM with aligned BAM
task MergeBams {
  File PICARD
  String file_basename
  File rg_bam
  File aligned_sam
  String unmap_contaminant_reads
  String min_unclipped_bases
  File ref_fasta
  File ref_index
  File ref_dict

  command {
	java -jar ${PICARD} MergeBamAlignment \
	  ALIGNED=${aligned_sam} \
	  UNMAPPED=${rg_bam} \
	  O=${file_basename}_m.bam \
	  R=${ref_fasta} \
	  SORT_ORDER=unsorted \
	  CLIP_ADAPTERS=false \
	  ADD_MATE_CIGAR=true \
	  MAX_INSERTIONS_OR_DELETIONS=-1 \
	  PRIMARY_ALIGNMENT_STRATEGY=MostDistant \
	  UNMAP_CONTAMINANT_READS=${unmap_contaminant_reads} \
	  MIN_UNCLIPPED_BASES=${min_unclipped_bases} \
	  ATTRIBUTES_TO_RETAIN=XS \
	  ATTRIBUTES_TO_RETAIN=XA
  }
  output {
    File merged_bam = "${file_basename}_m.bam"
  }
}

## [4.4] Flag duplicate reads
task FlagDuplicateInserts {
  File PICARD
  File merged_bam
  String file_basename

  command {
	java -jar ${PICARD} MarkDuplicates \
	  INPUT=${merged_bam} \
	  OUTPUT=${file_basename}_md.bam \
	  METRICS_FILE=${file_basename}_md.bam.txt \
	  OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500 \
	  ASSUME_SORT_ORDER=queryname
  }
  output {
    File md_bam = "${file_basename}_md.bam"
    File md_metrics = "${file_basename}_md.bam.txt"
  }
}

## [4.5] Coordinate sort, fix NM and UQ tags and index for clean BAM
task SortFixTagsAndIndex {
  File PICARD
  File md_bam
  String file_basename
  File ref_fasta
  File ref_index
  File ref_dict

  command <<<
    set -o pipefail
    java -jar ${PICARD} SortSam \
      INPUT=${md_bam} \
      OUTPUT=/dev/stdout \
      SORT_ORDER=coordinate | \
      java -jar ${PICARD} SetNmAndUqTags \
      INPUT=/dev/stdin \
      OUTPUT=${file_basename}_snaut.bam \
      CREATE_INDEX=true \
      R=${ref_fasta}
  >>>
  output {
    File snaut_bam = "${file_basename}_snaut.bam"
    File snaut_bai = "${file_basename}_snaut.bai"
  }
}

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

## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample using HaplotypeCaller
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

workflow Tutorial_8017_postalt {
  Array[File] aligned_sam
  File K8
  File POSTALT
  File samtools
  File GATK
  File PICARD
  String sam_directory_path
  String final_vcf_name
  String min_unclipped_bases
  String unmap_contaminant_reads
  File ref_fasta
  File ref_index
  File ref_dict
  File ref_alt

## Scatter all but last step
  scatter (sam in aligned_sam) {

	## Get file_basename
		String sub_strip_path = sam_directory_path
		String sub_strip_extension = "\\.sam" + "$"

	## K8 postalt.js process query-grouped aligned SAM
		call PostAltProcess {
		input:
		K8 = K8,
		POSTALT = POSTALT,
		ref_alt = ref_alt,
		aligned_sam = sam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.1] Create unmapped uBAM
		call CreateUbam {
		input:
		PICARD = PICARD,
		aligned_sam = sam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		}

	## [4.2] Add read group information to uBAM
		call AddRgToUbam {
		input:
		PICARD = PICARD,
		u_bam = CreateUbam.u_bam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		rg_id = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		rg_sm = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.3] Merge uBAM with aligned BAM
		call MergeBams {
		input:
		PICARD = PICARD,
		rg_bam = AddRgToUbam.rg_bam,
		aligned_sam = PostAltProcess.postalt_sam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		min_unclipped_bases = min_unclipped_bases,
		unmap_contaminant_reads = unmap_contaminant_reads,
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}

	## [4.4] Flag duplicate inserts
		call FlagDuplicateInserts {
		input:
		PICARD = PICARD,
		merged_bam = MergeBams.merged_bam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.5] Coordinate sort, fix NM and UQ tags and index for clean BAM
		call SortFixTagsAndIndex {
		input:
		PICARD = PICARD,
		md_bam = FlagDuplicateInserts.md_bam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}

	## Strip 0x1 PAIRED flag from reads to circumvent HaplotypeCaller's BadMateFilter
		call PairedToSingleEnd {
		input:
		snaut_bam = SortFixTagsAndIndex.snaut_bam,
		samtools = samtools,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample using HaplotypeCaller
		call CallSampleVariants {
		input:
		GATK = GATK,
		se_bai = PairedToSingleEnd.se_bai,
		se_bam = PairedToSingleEnd.se_bam,
		file_basename = sub(sub(sam, sub_strip_path, ""), sub_strip_extension, ""),
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}
	  }

## [4.7] Call genotypes on three samples
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
