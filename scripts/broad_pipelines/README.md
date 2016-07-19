This directory contains the following WDL scripts used in production at
the Broad Institute. Old versions are stored in the `archive` directory.
Versions are distinguished with a datestamp (format: YYMMDD). Each WDL 
script is accompanied by a JSON file of example inputs bearing the same 
name, with the `.json` extension instead of `.wdl`. 

####`PublicPairedSingleSampleWf-<datestamp>.wdl`
This WDL pipeline implements data pre-processing and initial variant
calling (GVCF generation) according to the GATK Best Practices for 
germline SNP and Indel discovery in human whole-genome sequencing (WGS) 
data.

