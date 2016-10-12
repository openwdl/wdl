# The tutorial to accompany this script can be found at:
# https://software.broadinstitute.org/wdl/userguide/article?id=7334
# You can follow along with the tutorial there for a complete explanation of how to write this script.

workflow SimpleVariantDiscovery {
  File gatk
  File refFasta
  File refIndex
  File refDict
  String name
  call haplotypeCaller {
    input: 
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict
  }
  call select as selectSNPs {
    input:  
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      type="SNP",
      rawVCF=haplotypeCaller.rawVCF
  }
  call hardFilterSNP {
    input: 
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      rawSNPs=selectSNPs.rawSubset
  }
  call select as selectIndels {
    input: 
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      type="INDEL", 
      rawVCF=haplotypeCaller.rawVCF
  }
  call hardFilterIndel {
    input: 
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      rawIndels=selectIndels.rawSubset
  }
  call combine {
    input: 
      sampleName=name, 
      RefFasta=refFasta, 
      GATK=gatk, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      filteredSNPs=hardFilterSNP.filteredSNPs, 
      filteredIndels=hardFilterIndel.filteredIndels
  }
}

#This task calls GATK's tool, HaplotypeCaller in normal mode. This tool takes a pre-processed 
#bam file and discovers variant sites. These raw variant calls are then written to a vcf file.
task haplotypeCaller {
  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  File inputBAM
  File bamIndex
  command {
    java -jar ${GATK} \
      -T HaplotypeCaller \
      -R ${RefFasta} \
      -I ${inputBAM} \
      -o ${sampleName}.raw.indels.snps.vcf
  }
  output {
    File rawVCF = "${sampleName}.raw.indels.snps.vcf"
  }
}

#This task calls GATK's tool, SelectVariants, in order to separate indel calls from SNPs in
#the raw variant vcf produced by HaplotypeCaller. The type can be set to "INDEL"
#or "SNP".
task select {
  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  String type
  File rawVCF
  command {
    java -jar ${GATK} \
      -T SelectVariants \
      -R ${RefFasta} \
      -V ${rawVCF} \
      -selectType ${type} \
      -o ${sampleName}_raw.${type}.vcf
  }
  output {
    File rawSubset = "${sampleName}_raw.${type}.vcf"
  }
}

#This task calls GATK's tool, VariantFiltration. It applies certain recommended filtering 
#thresholds to the SNP-only vcf. VariantFiltration filters out any variant that is "TRUE" 
#for any part of the filterExpression (i.e. if a variant has a QD of 1.3, it would be 
#filtered out). The variant calls remain in the file, but they are tagged as not passing.
#GATK tools downstream in the pipeline will ignore filtered calls by default
task hardFilterSNP {
  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  File rawSNPs
  command {
    java -jar ${GATK} \
      -T VariantFiltration \
      -R ${RefFasta} \
      -V ${rawSNPs} \
      --filterExpression "FS > 60.0" \
      --filterName "snp_filter" \
      -o ${sampleName}.filtered.snps.vcf
  }
  output {
    File filteredSNPs = "${sampleName}.filtered.snps.vcf"
  }
}

#As above, this task calls GATK's tool, VariantFiltration. However, this one applied filters
#meant for indels only.
task hardFilterIndel {
  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  File rawIndels
  command {
    java -jar ${GATK} \
      -T VariantFiltration \
      -R ${RefFasta} \
      -V ${rawIndels} \
      --filterExpression "FS > 200.0" \
      --filterName "indel_filter" \
      -o ${sampleName}.filtered.indels.vcf
  }
  output {
    File filteredIndels = "${sampleName}.filtered.indels.vcf"
  }
}

#This task calls GATK's tool, CombineVariants. It will merge the separate SNP- and Indel-only 
#vcfs into one file.
task combine {
  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  File filteredSNPs
  File filteredIndels
  command {
    java -jar ${GATK} \
      -T CombineVariants \
      -R ${RefFasta} \
      -V ${filteredSNPs} \
      -V ${filteredIndels} \
      --genotypemergeoption UNSORTED \
      -o ${sampleName}.filtered.snps.indels.vcf
  }
  output {
    File filteredVCF = "${sampleName}.filtered.snps.indels.vcf"
  }
}
