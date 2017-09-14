## Content overview

This directory contains the following WDL scripts used in production at
the Broad Institute. Old versions are stored in the `archive` directory.
Versions are distinguished by a datestamp (format: YYMMDD). Each WDL 
script is accompanied by a JSON file of example inputs bearing the same 
name, with the `.inputs.json` extension instead of `.wdl`, as well as a 
JSON file of example options with the `.options.json` extension. 

## Important limitations

These scripts are provided "as-is", without any guarantees as to performance 
or results. It is the responsibility of the user to test these scripts 
fully before running them in production.

Many parameters and implementation decisions are optimized for our use cases and for running on the Google Cloud Platform. In some cases the scripts may need to be modified in order to be run optimally on different data and/or different platforms. Wherever possible, we provide alternative versions of these pipelines that were rendered more generic, platform-agnostic and/or stripped down (e.g. without the numerous QC steps); they can be found in the `broad_dsp_workflows` directory. 

## Inventory of scripts

### `GOTC_PairedEndSingleSampleWf_<datestamp>.wdl`
This WDL pipeline implements data pre-processing and initial variant
calling (GVCF generation) according to the GATK Best Practices for 
germline SNP and Indel discovery in human whole-genome sequencing (WGS) 
data. Formerly named `GOTC_PublicPairedSingleSampleWf_<datestamp>.wdl`. 
bucket. See accompanying `*.md` file for important caveats and implementation notes.