This directory contains WDL scripts organized in the following
categories:

####`tutorials/`
Scripts used in
[tutorials](https://software.broadinstitute.org/wdl/userguide/topic?
name=wdl-tutorials) in the WDL user guide. These scripts demonstrate
various features of WDL using GATK analyses as backdrop. A link to the
corresponding tutorial is included in the header of each script.

####`broad_pipelines/`
Pipeline scripts used in production at the Broad Institute. These are
intended to serve as reference implementation of the GATK Best Practices
workflows and may require specific resources for execution. See the
directory README for more information on each script. 

####`wrappers/gatk/`
GATK tools have been wrapped into individual WDL tasks using a json-
to-WDL wrapper script. These task-only WDL scripts can be imported
into a pipeline for your use, and contain all possible parameters available
to each tool. See the directory README for more information on using these
scripts.
