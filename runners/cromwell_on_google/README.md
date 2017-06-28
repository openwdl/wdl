This directory contains utilities that facilitate running WDLs through the Broad's Cromwell execution engine on the Google Cloud Platform. 

#### wdl_runner

The `wdl_runner` is a wrapper package that handles spinning up a Cromwell server on a GCP VM and launching a WDL workflow by submitting it to the newly created Cromwell server. See the `wdl_runner` [README](wdl_runner/README.md) for a detailed tutorial that explains how to use it in practice.

#### monitoring_tools

These are scripts that facilitate monitoring the status of WDL workflows run on GCP. The main monitoring script is `monitor_wdl_pipeline.sh`. It accepts an operation ID for a pipeline, extracts the LOGGING, WORKSPACE, and OUTPUT directories from the operation and then examines these directories to glean some insights into the status of the operation.

Note that if the WORKSPACE and/or OUTPUT directories for the specified operation are already populated (for example by another operation), this script will emit incorrect output.