# Tutorial_8017.wdl #######################################################
#
# This WDL script recapitulates the workflow described in Tutorial#8017 at
# <https://software.broadinstitute.org/gatk/documentation/article?id=8017>
# titled "(How to) Map reads to a reference with alternate contigs like GRCh38".
# The tutorial provides example input data including a mini-reference that you
# must index separately. The script will finish processing in minutes.
#
###################################################################################
# You may use any reference and any number of paired FASTQ input files.
##	Input data requirements:
#	- reference FASTA, FAI index, dictionary, and five BWA indices
# 	- reference ALT index for alt-aware handling
#	- simulated paired reads in paired FASTQ format per sample each. These should be
#	  named by sample name as this sample name becomes both the RGID and RGSM.
#	  This workflow accommodates any number of samples. Provide these in
#	  [["A.read1.fq", "A.read2.fq"],["B.read1.fq", "B.read2.fq"],...] array format,
#	  and be sure to preserve the ".read#.fq" suffix.
##	Required tools:
#	- Picard v2.5.0
#	- GATK v3.6
#	- BWA v0.7.15
#	- Java JDK v1.8
###################################################################################
# The workflow scatters the processing of multiple paired FASTQ files from
# alignment to single-sample variant calling, and ends with variant calling of the
# multiple GVCFs to produce a multisample VCF.
#
# The script expects simulated reads and so omits base quality score recalibration.
# Also, the script does not accommodate intervals, e.g. via the "-L" option.
###################################################################################

# TASK DEFINITIONS ################################################################

## Align FASTQ reads with BWA-MEM
task AlignFastqWithBwaMem {
  File BWA0715
  File input_FASTQ1
  File input_FASTQ2
  String file_basename
  File ref_fasta
  File ref_index
  File ref_dict
  File ref_alt
  File ref_amb
  File ref_ann
  File ref_bwt
  File ref_pac
  File ref_sa

  command {
    ${BWA0715} mem ${ref_fasta} ${input_FASTQ1} ${input_FASTQ2} > ${file_basename}.sam
  }
  output {
    File aligned_sam = "${file_basename}.sam"
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

  command {
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
  }
  output {
    File snaut_bam = "${file_basename}_snaut.bam"
    File snaut_bai = "${file_basename}_snaut.bai"
  }
}

## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample using HaplotypeCaller
task CallSampleVariants {
  File GATK
  String file_basename
  File snaut_bam
  File snaut_bai
  File ref_fasta
  File ref_index
  File ref_dict

  command {
  java -jar ${GATK} \
    -T HaplotypeCaller \
    -R ${ref_fasta} \
    -I ${snaut_bam} \
    -o ${file_basename}.g.vcf \
	-ERC GVCF \
	--max_alternate_alleles 3 \
	--read_filter OverclippedRead \
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

workflow Tutorial_8017 {
  Array[Array[File]] input_FASTQ
  File BWA0715
  File GATK
  File PICARD
  String fastq_directory_path
  String final_vcf_name
  String min_unclipped_bases
  String unmap_contaminant_reads
  File ref_fasta
  File ref_index
  File ref_dict
  File ref_alt
  File ref_amb
  File ref_ann
  File ref_bwt
  File ref_pac
  File ref_sa

## Scatter all but first and last steps
  scatter (pair in input_FASTQ) {

	## Get file_basename
	## The script uses these variables throughout the WORKFLOW to define the
	## output file basename (file_basename) automatically from the FASTQ basename
	## so that you can provide any number of FASTQ pairs without having to manually
	## name them separately. The script also uses the basename as the RGID and RGSM.
		String sub_strip_path = fastq_directory_path
		String sub_strip_extension = "\\.read.\\.fq" + "$"

	## Align FASTQ reads with BWA-MEM
		call AlignFastqWithBwaMem {
		input:
		BWA0715 = BWA0715,
		input_FASTQ1 = pair[0],
		input_FASTQ2 = pair[1],
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict,
		ref_alt = ref_alt,
		ref_bwt = ref_bwt,
		ref_amb = ref_amb,
		ref_ann = ref_ann,
		ref_pac = ref_pac,
		ref_sa = ref_sa
		}

	## [4.1] Create unmapped uBAM
		call CreateUbam {
		input:
		PICARD = PICARD,
		aligned_sam = AlignFastqWithBwaMem.aligned_sam,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		}

	## [4.2] Add read group information to uBAM
		call AddRgToUbam {
		input:
		PICARD = PICARD,
		u_bam = CreateUbam.u_bam,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		rg_id = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		rg_sm = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, "")
		}

	## [4.3] Merge uBAM with aligned BAM
		call MergeBams {
		input:
		PICARD = PICARD,
		rg_bam = AddRgToUbam.rg_bam,
		aligned_sam = AlignFastqWithBwaMem.aligned_sam,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		min_unclipped_bases = min_unclipped_bases,
		unmap_contaminant_reads = unmap_contaminant_reads,
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}

	##[4.4] Flag duplicate inserts
		call FlagDuplicateInserts {
		input:
		PICARD = PICARD,
		merged_bam = MergeBams.merged_bam,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		}

	## [4.5] Coordinate sort, fix NM and UQ tags and index for clean BAM
		call SortFixTagsAndIndex {
		input:
		PICARD = PICARD,
		md_bam = FlagDuplicateInserts.md_bam,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
		ref_fasta = ref_fasta,
		ref_index = ref_index,
		ref_dict = ref_dict
		}

	## [4.6] Call SNP and indel variants in reference confidence (ERC) mode per sample using HaplotypeCaller
		call CallSampleVariants {
		input:
		GATK = GATK,
		snaut_bam = SortFixTagsAndIndex.snaut_bam,
		snaut_bai = SortFixTagsAndIndex.snaut_bai,
		file_basename = sub(sub(pair[0], sub_strip_path, ""), sub_strip_extension, ""),
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
