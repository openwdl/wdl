workflow helloHaplotypeCaller {
  call haplotypeCaller
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
