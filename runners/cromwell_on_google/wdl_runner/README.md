# Run a WDL workflow

## Overview

This example demonstrates running a multi-stage workflow on
Google Cloud Platform.

* The workflow is launched with the Google Genomics [Pipelines API](https://cloud.google.com/genomics/v1alpha2/pipelines).
* The workflow is defined using the Broad Institute's
[Workflow Definition Language](https://software.broadinstitute.org/wdl/) (WDL).
* The workflow stages are orchestrated by the Broad Institute's
[Cromwell](https://github.com/broadinstitute/cromwell).

When submitted using the Pipelines API, the workflow runs
on multiple [Google Compute Engine](https://cloud.google.com/compute/)
virtual machines.
First a master node is created for Cromwell, and then Cromwell submits
each stage of the workflow as one or more separate pipelines.

Execution of a running Pipeline proceeds as:

1. Create Compute Engine virtual machine

2. On the VM, in a Docker container, execute wdl_runner.py

    a. Run Cromwell (server)

    b. Submit workflow, inputs, and options to Cromwell server

    c. Poll for completion as Cromwell executes:

        1) Call pipelines.run() to execute call 1
        2) Poll for completion of call 1
        3) Call pipelines.run() to execute call 2
        4) Poll for completion of call 2
        <etc. until all WDL "calls" complete>

    d. Copy workflow metadata to output path

    e. Copy workflow outputs to output path

3. Destroy Compute Engine Virtual machine

## Setup Overview

Code packaging for the Pipelines API is done through
[Docker](https://www.docker.com/) images.  The instructions provided
here explain how to create your own Docker image, although a copy
of this Docker image has already been built and made available by
the Broad Institute.

### Code summary

The code in the wdl_runner Docker image includes:

* [OpenJDK 8](http://openjdk.java.net/projects/jdk8/) runtime engine (JRE)
* [Python 2.7](https://www.python.org/download/releases/2.7/) interpreter
* [Cromwell release 29](https://github.com/broadinstitute/cromwell/releases/tag/29)
* [Python and shell scripts from this repository](.)

Take a look at the [Dockerfile](./Dockerfile) for full details.

## (0) Prerequisites

1. Clone or fork this repository.

2. Enable the Genomics, Cloud Storage, and Compute Engine APIs on a new
   or existing Google Cloud Project using the [Cloud Console](https://console.cloud.google.com/flows/enableapi?apiid=genomics,storage_component,compute_component&redirect=https://console.cloud.google.com)

3. Follow the Google Genomics [getting started instructions](https://cloud.google.com/genomics/install-genomics-tools#install-genomics-tools) to install and authorize the Google Cloud SDK.

4. Follow the Cloud Storage instructions for [Creating Storage Buckets](https://cloud.google.com/storage/docs/creating-buckets) to create a bucket for workflow output and logging 

5. If you plan to create your own Docker images, then
[install docker](https://docs.docker.com/engine/installation/#installation)

## (1) Create and stage the wdl_runner Docker image

*If you are going to use the published version of the docker image,
then skip this step.*

Every Google Cloud project provides a private repository for saving and
serving Docker images called the [Google Container Registry](https://cloud.google.com/container-registry/docs/).

The following instructions allow you to stage a Docker image in your project's
Container Registry with all necessary code for orchestrating your workflow.

### (1a) Create the Docker image.

```
git clone https://github.com/broadinstitute/wdl.git
cd runners/cromwell_on_google/wdl_runner/
docker build -t ${USER}/wdl_runner .
```

### (1b) Push the Docker image to a repository.

In this example, we push the container to
[Google Container Registry](https://cloud.google.com/container-registry/)
via the following commands:

```
docker tag ${USER}/wdl_runner gcr.io/YOUR-PROJECT-ID/wdl_runner
gcloud docker -- push gcr.io/YOUR-PROJECT-ID/wdl_runner
```

* Replace `YOUR-PROJECT-ID` with your project ID.

## (2) Run a test workflow in the cloud

The file [wdl_pipeline.yaml](wdl_pipeline.yaml)
defines a pipeline for running WDL workflows. By default, it uses the
docker image built by the Broad Institute from this repository:

```
docker:
  imageName: gcr.io/broad-dsde-outreach/wdl_runner:<datestamp>
```

If you have built your own Docker image, then change the imageName:

```
docker:
  imageName: gcr.io/YOUR-PROJECT-ID/wdl_runner
```

* Replace `YOUR-PROJECT-ID` with your project ID.

#### Run the following command:

* Replace `YOUR-BUCKET` with a bucket in your project.

```
gcloud \
  alpha genomics pipelines run \
  --pipeline-file wdl_pipeline.yaml \
  --zones us-central1-f \
  --inputs-from-file WDL=test-wdl/ga4ghMd5.wdl \
  --inputs-from-file WORKFLOW_INPUTS=test-wdl/ga4ghMd5.inputs.json \
  --inputs-from-file WORKFLOW_OPTIONS=test-wdl/basic.papi.us.options.json \
  --inputs WORKSPACE=gs://YOUR-BUCKET/wdl_runner/work \
  --inputs OUTPUTS=gs://YOUR-BUCKET/wdl_runner/output \
  --logging gs://YOUR-BUCKET/wdl_runner/logging
```

The output will be an operation ID for the Pipeline.

## (3) Monitor the pipeline operation

This github repo includes a shell script,
[../monitoring_tools/monitor_wdl_pipeline.sh](../monitoring_tools/monitor_wdl_pipeline.sh),
for monitoring the status of a pipeline launched using ``wdl_pipeline.yaml``.

```
$ ./monitoring_tools/monitor_wdl_pipeline.sh YOUR-NEW-OPERATION-ID
Logging: gs://YOUR-BUCKET/wdl_runner/logging
Workspace: gs://YOUR-BUCKET/wdl_runner/work
Outputs: gs://YOUR-BUCKET/wdl_runner/output

2017-10-04 00:18:45: operation not complete
No operations logs found.
There are 0 output files
Sleeping 60 seconds

2017-10-04 00:19:50: operation not complete
Sleeping 60 seconds

2017-10-04 00:20:54: operation not complete
Calls started but not complete:
  ga4ghMd5/CALL_HASH/call-md5
Total Preemptions: 0
Sleeping 60 seconds

2017-10-04 00:21:59: operation not complete
Calls (including shards) completed:  1
Calls started but not complete:
  ga4ghMd5/CALL_HASH/call-md5
Sleeping 60 seconds

2017-10-04 00:23:04: operation complete
Completed operation status information
  done: true
  metadata:
    events:
    - description: start
      startTime: '2017-10-04T04:18:59.394089075Z'
    - description: pulling-image
      startTime: '2017-10-04T04:18:59.394719563Z'
    - description: localizing-files
      startTime: '2017-10-04T04:19:38.809811533Z'
    - description: running-docker
      startTime: '2017-10-04T04:19:38.809854495Z'
    - description: delocalizing-files
      startTime: '2017-10-04T04:22:22.720332568Z'
    - description: ok
      startTime: '2017-10-04T04:22:24.464250806Z'
  name: operations/YOUR-NEW-OPERATION-ID
Operation output
  gs://YOUR-BUCKET/wdl_runner/output/md5sum.txt
  gs://YOUR-BUCKET/wdl_runner/output/wdl_run_metadata.json

Preemption retries:
  None
```

## (4) Check the results

Check the operation output for a top-level `errors` field.
If none, then the operation should have finished successfully.

## (5) Check that the output exists

* Replace `YOUR-BUCKET` with the bucket you used in the previous command.

```
$ gsutil ls -l gs://YOUR-BUCKET/wdl_runner/output
        33  2017-10-04T04:22:21Z  gs://YOUR-BUCKET/wdl_runner/output/md5sum.txt
      5264  2017-10-04T04:22:18Z  gs://YOUR-BUCKET/wdl_runner/output/wdl_run_metadata.json
TOTAL: 2 objects, 5297 bytes (5.17 KiB)
```

## (6) Check the output

```
$ gsutil cat gs://YOUR-BUCKET/pipelines-api-examples/wdl_runner/output/md5sum.txt
00579a00e3e7fa0674428ac7049423e2
```

## (7) Clean up the intermediate workspace files

When Cromwell runs, per-stage output and other intermediate files are
written to the WORKSPACE path you specified in the `gcloud` command above.

If you wish to remove these files, run:

```
gsutil -m rm gs://YOUR-BUCKET/wdl_runner/work/**
```

