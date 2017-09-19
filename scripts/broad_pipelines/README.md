## Content overview

This directory contains WDL workflows used in production at the Broad Institute. The workflows are organized by functional domain and specific use case, and are [semantically versioned](http://semver.org/) using numbered directories. Here's a concrete example:

- germline-short-variant-discovery
  - gvcf-generation-per-sample
    - (...)
    - 0.2.0
      - PublicPairedSingleSampleWf_170412.wdl
      - PublicPairedSingleSampleWf_170412.inputs.json
      - PublicPairedSingleSampleWf_170412.options.json
      - PublicPairedSingleSampleWf_170412.md
    - 1.0.0
      - GOTC_PairedEndSingleSampleWf.wdl
      - GOTC_PairedEndSingleSampleWf.inputs.json
      - GOTC_PairedEndSingleSampleWf.options.json
      - GOTC_PairedEndSingleSampleWf.md

Note that the names of the workflows and files may change from one version to the next due to evolving features and naming standards. Where available we include version notes (see `.md` file); see also the header of the WDL files for important notes about requirements and limitations.

Each WDL script is accompanied by a JSON file of example inputs bearing the same name, with the `.inputs.json` extension instead of `.wdl`, as well as a JSON file of example options with the `.options.json` extension. 

## Important limitations

These scripts are provided "as-is", without any guarantees as to performance 
or results. It is the responsibility of the user to test these scripts 
fully before running them in production.

Many parameters and implementation decisions are optimized for our use cases and for running on the Google Cloud Platform. In some cases the scripts may need to be modified in order to be run optimally on different data and/or different platforms. Wherever possible, we provide alternative versions of these pipelines that were rendered more generic, platform-agnostic and/or stripped down (e.g. without the numerous QC steps); they can be found in the `broad_dsp_workflows` directory. 