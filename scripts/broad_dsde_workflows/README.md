### Content overview

This directory contains WDL scripts developed at the Broad Institute and supported by the DSDE group (which develops GATK, Picard and Cromwell/WDL among other things). These scripts are NOT run in production at Broad; for production pipeline scripts, see the `broad_pipelines` directory. 

Each WDL  script is accompanied by a JSON file of example inputs bearing the same  name, with the `.inputs.json` extension instead of `.wdl`. Unless otherwise specified, all WDL scripts can be run with the generic options file `generic.options.json`. 

### Important limitations

These scripts are provided "as-is", without any guarantees as to performance 
or results. It is the responsibility of the user to test these scripts 
fully before running them in production.

Many parameters and implementation decisions are optimized for our use of 
the Google Cloud Platform. In some cases the scripts may need to be 
modified in order to be run successfully on a different platform. 


