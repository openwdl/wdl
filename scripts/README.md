This directory contains WDL scripts organized in the following alphabetically listed categories:

####`broad_dsde_workflows/`
Workflow scripts developed by the Data Sciences and Data Engineering (DSDE) group at the Broad Institute. These scripts cover a variety of use cases, typically complementary to the production workflows provided in `broad_pipelines`, e.g. for formatting inputs correctly for the production pipelines, or serving as alternatives for use with divergent datatypes or with legacy tools and resources. Although they are not blessed by the Broad production team, these workflows are officially supported on the WDL user forum. See the directory README for additional guidelines.

####`broad_pipelines/`
Workflow scripts used in Broad Genomic Services production pipelines at the Broad Institute. These are intended to serve as reference implementations of the GATK Best Practices workflows and may require specific resources for execution. See the directory README for more information on each script. 

####`tutorials/`
Workflow scripts used in
[tutorials](https://software.broadinstitute.org/wdl/userguide/topic?
name=wdl-tutorials) in the WDL user guide. These scripts demonstrate
various features of WDL using GATK analyses as backdrop. A link to the
corresponding tutorial is included in the header of each script.

####`wrappers/gatk/`
GATK tools have been wrapped into individual WDL tasks using a json-
to-WDL wrapper script. These task-only WDL scripts can be imported
into a pipeline for your use, and contain all possible parameters available
to each tool. See the directory README for more information on using these
scripts.
