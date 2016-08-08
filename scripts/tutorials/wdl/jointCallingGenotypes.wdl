# The tutorial to accompany this script can be found at:
# https://software.broadinstitute.org/wdl/userguide/article?id=7614
# You can follow along with the tutorial there for a complete explanation of how to write this script.

workflow jointCallingGenotypes {

  File inputSamplesFile
  Array[Array[File]] inputSamples = read_tsv(inputSamplesFile)
  File gatk
  File refFasta
  File refIndex
  File refDict

  scatter (sample in inputSamples) {
    call HaplotypeCallerERC {
      input: GATK=gatk, 
        RefFasta=refFasta, 
        RefIndex=refIndex, 
        RefDict=refDict, 
        sampleName=sample[0],
        bamFile=sample[1], 
        bamIndex=sample[2]
    }
  }
  call GenotypeGVCFs {
    input: GATK=gatk, 
      RefFasta=refFasta, 
      RefIndex=refIndex, 
      RefDict=refDict, 
      sampleName="CEUtrio", 
      GVCFs=HaplotypeCallerERC.GVCF
  }
}

task HaplotypeCallerERC {

  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  File bamFile
  File bamIndex

  command {
    java -jar ${GATK} \
        -T HaplotypeCaller \
        -ERC GVCF \
        -R ${RefFasta} \
        -I ${bamFile} \
        -o ${sampleName}_rawLikelihoods.g.vcf
  }
  output {
    File GVCF = "${sampleName}_rawLikelihoods.g.vcf"
  }
}

task GenotypeGVCFs {

  File GATK
  File RefFasta
  File RefIndex
  File RefDict
  String sampleName
  Array[File] GVCFs

  command {
    java -jar ${GATK} \
        -T GenotypeGVCFs \
        -R ${RefFasta} \
        -V ${sep=" -V " GVCFs} \
        -o ${sampleName}_rawVariants.vcf
  }
  output {
    File rawVCF = "${sampleName}_rawVariants.vcf"
  }
}
