This document describes the protocol that was used to submit the entry "Cromwell via Google Genomics Pipelines API wdl_runner" in the GA4GH Tool Execution Challenge, Phase 1 (https://www.synapse.org/#!Synapse:syn8080305). 

This protocol is based on the "Broad Institute GATK on Google Genomics" tutorial at https://cloud.google.com/genomics/v1alpha2/gatk, which demonstrates how to run a WDL pipeline through the Google Genomics Pipelines API wdl_runner.

To replicate this work, change the GCS bucket paths and set the Google Project and local paths (which are set using environment variables in the protocol below) as appropriate.


### Obtain challenge materials

1. Get the raw WDL from https://raw.githubusercontent.com/briandoconnor/dockstore-tool-md5sum/master/Dockstore.wdl and save to file ga4ghMd5.wdl

2. Get the JSON content {"ga4ghMd5.inputFile": "md5sum.input"} and save to file ga4ghMd5.json

3. Get the input text "this is the test file that will be used when calculating an md5sum" and save to file md5sum.input


### Prepare for execution

4. Add files to WDL repository under scripts/ga4gh/tool_execution_challenge_phase1 (need local copy of WDL and JSON to invoke in the execution command, plus a dummy workflow options file).

5. Upload files to GCS at gs://ga4gh-tool-execution-challenge/phase1 (need copy of input file on GCS).


### Execute through Google Genomics Pipelines API 

6. Run the following command:

````
gcloud alpha genomics pipelines run \
  --pipeline-file workflows/wdl_pipeline.yaml \
  --zones us-central1-f \
  --logging gs://ga4gh-tool-execution-challenge/phase1/logs \
  --inputs-from-file WDL=${WDL_SCR}/ga4gh/tool_execution_challenge_phase1/ga4ghMd5.wdl \
  --inputs-from-file WORKFLOW_INPUTS=${WDL_SCR}/ga4gh/tool_execution_challenge_phase1/ga4ghMd5.json \
  --inputs-from-file WORKFLOW_OPTIONS=${WDL_SCR}/ga4gh/tool_execution_challenge_phase1/empty.options.json \
  --inputs WORKSPACE=gs://ga4gh-tool-execution-challenge/phase1/work \
  --inputs OUTPUTS=gs://ga4gh-tool-execution-challenge/phase1/out \
  --project $P_OUTREACH
````

where ${WDL_SCR} is a local path to the WDL scripts directory.

This returns `Running [operations/EOeigKSoKxi10d7o7tjQmHYg7qv-spECKg9wcm9kdWN0aW9uUXVldWU].`

The status of the job can be monitored by running the following command: 

````
gcloud alpha genomics operations describe EOeigKSoKxi10d7o7tjQmHYg7qv-spECKg9wcm9kdWN0aW9uUXVldWU \
    --format='yaml(done, error, metadata.events)'
````

When the job has completed successfully, this is what is returned:


````
done: true
metadata:
  events:
  - description: start
    startTime: '2017-02-28T11:35:14.458414638Z'
  - description: pulling-image
    startTime: '2017-02-28T11:35:14.458467173Z'
  - description: localizing-files
    startTime: '2017-02-28T11:35:56.281473416Z'
  - description: running-docker
    startTime: '2017-02-28T11:35:56.281499402Z'
  - description: delocalizing-files
    startTime: '2017-02-28T11:37:21.569738442Z'
  - description: ok
    startTime: '2017-02-28T11:37:23.273628610Z'
````

The output file md5sum.txt is written at gs://ga4gh-tool-execution-challenge/phase1/out and contains the result, 00579a00e3e7fa0674428ac7049423e2.



