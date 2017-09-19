### Content overview

This directory contains WDL workflows developed at the Broad Institute and supported by the Data Sciences Platform team (which develops GATK, much of Picard, Cromwell/WDL and Workbench/FireCloud). These workflows are NOT run in production at Broad; for production pipeline workflows, see the `broad_pipelines` directory. 

The workflows are organized by functional domain and specific use case, and are [semantically versioned](http://semver.org/) using numbered directories. Here's a concrete example:

- germline-short-variant-discovery
  - haplotypecaller-gvcf-per-sample
    - 0.1.0
      - HaplotypeCallerGvcfScatterWf_170204.wdl
      - HaplotypeCallerGvcfScatterWf_170204.inputs.json
    - 0.2.0
      - HaplotypeCallerGvcf_GATK3.wdl
      - HaplotypeCallerGvcf_GATK3.b37.wgs.inputs.json

Note that the names of the workflows and files may change from one version to the next due to evolving features and naming standards. Where available we include version notes; see also the header of the WDL files for important notes about requirements and limitations.

Each WDL  script is accompanied by a JSON file of example inputs bearing the same  name, with the `.inputs.json` extension instead of `.wdl`. Unless otherwise specified, all WDL scripts can be run with the generic options file `generic.options.json`. 

### Important limitations

These scripts are provided "as-is", without any guarantees as to performance 
or results. It is the responsibility of the user to test these scripts 
fully before running them in production.

Many parameters and implementation decisions are optimized for our use of 
the Google Cloud Platform. In some cases the scripts may need to be 
modified in order to be run optimally and/or successfully on a different platform. 


