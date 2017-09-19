### 2017-09-19

Reorganized workflows into functional categories with explicit versioning using directories.

- data-processing
  - pre-processing-for-variant-discovery
- format-conversion
  - bam-to-unmapped-readgroup-bams
  - paired-fastq-to-unmapped-bam
  - readgroup-bams-to-paired-fastqs
- quality-control
  - validate-bams
- germline-short-variant-discovery
  - genotype-gvcfs
  - haplotypecaller-gvcf-per-sample
  - joint-discovery-end-to-end
  - variant-recalibration
- uncategorized
  - extract-sam-headers


### 2017-08-23 
 
- NEW: HaplotypeCallerGvcf_GATK3.wdl
  - + b37.wgs.inputs.json
- NEW: PreProcessingForVariantDiscovery_GATK4.wdl 
  - + hg38.wgs.inputs.json 
  - + b37.wgs.inputs.json
- ARCHIVE: HaplotypeCallerGvcfScatterWf_170204.wdl + inputs.json
- ARCHIVE: GenericPreProcessingToGVCF_170420.wdl + inputs.json
- ARCHIVE: GenericPreProcessing_170421.wdl + inputs.json
- RENAME: broad_dsde_workflows -> broad_dsp_workflows
- NEW: Added this CHANGELOG to record changes to contents of this directory