### Content overview

This directory contains the following WDL scripts used in production at
the Broad Institute. Old versions are stored in the `archive` directory.
Versions are distinguished with a datestamp (format: YYMMDD). Each WDL 
script is accompanied by a JSON file of example inputs bearing the same 
name, with the `.inputs.json` extension instead of `.wdl`, as well as a 
JSON file of example options with the `.options.json` extension. 

### Important limitations

These scripts are provided "as-is", without any guarantees as to performance 
or results. It is the responsibility of the user to test these scripts 
fully before running them in production.

Many parameters and implementation decisions are optimized for our use of 
the Google Cloud Platform. In some cases (such as dynamic filename modifications 
and extension swapping using the sub() function) the scripts may need to be 
modified in order to be run successfully on a different platform. 

### Inventory of scripts

#### `PublicPairedSingleSampleWf-<datestamp>.wdl`
This WDL pipeline implements data pre-processing and initial variant
calling (GVCF generation) according to the GATK Best Practices for 
germline SNP and Indel discovery in human whole-genome sequencing (WGS) 
data.

