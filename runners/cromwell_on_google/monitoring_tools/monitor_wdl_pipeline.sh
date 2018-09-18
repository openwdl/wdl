#!/bin/bash

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# monitor_wdl_pipeline.sh
#
# Simple script that can be used to monitor the status of a WDL pipeline
# run by the Broad's Cromwell (https://github.com/broadinstitute/cromwell) 
# on GCP.
#
# The script accepts an operation ID for a pipeline, extracts the
# LOGGING, WORKSPACE, and OUTPUT directories from the operation and then
# examines these directories to glean some insights into the status of the
# operation.
#
# Note: if the WORKSPACE and/or OUTPUT directories for the specified operation
#       are already populated (for example by another operation), this script
#       will emit incorrect output.

set -o errexit
set -o nounset

readonly SCRIPT_DIR=$(dirname "${0}")
readonly REPO_ROOT=$(cd ${SCRIPT_DIR}/ && pwd) 

# Bring in polling utility functions
source ${REPO_ROOT}/operations_util.sh

# FUNCTIONS

# gsutil_ls
#
# Run "gsutil ls" masking stderr output and the non-zero exit code
function gsutil_ls() {
  gsutil ls $* 2>/dev/null || true
}
readonly -f gsutil_ls

# line_count
#
# Emit the number of lines of text in a string.
function line_count() {
  local lines="${1}"
  if [[ -z "${lines}" ]]; then
    echo "0"
  else
    echo "${lines}" | wc -l
  fi
}
readonly line_count

# indent
#
# Indent stdin two spaces
function indent() {
  sed -e 's#^#  #'
}
readonly -f indent

# MAIN

if [[ $# -lt 1 ]]; then
  2>&1 echo "Usage: $0 OPERATION-ID <poll-interval>"
  exit 1
fi

readonly OPERATION_ID="${1}"
readonly POLL_INTERVAL_SECONDS="${2:-60}"  # Default: 60 seconds between requests
readonly POLL_WAIT_MAX="${3:-}"            # Default: wait forever

# Get GCS paths from the operation
LOGGING=$(get_operation_value "${OPERATION_ID}" \
            "metadata.request.pipelineArgs.logging.gcsPath")
WORKSPACE=$(get_operation_value "${OPERATION_ID}" \
            "metadata.request.pipelineArgs.inputs.WORKSPACE")
OUTPUTS=$(get_operation_value "${OPERATION_ID}" \
            "metadata.request.pipelineArgs.inputs.OUTPUTS")

echo "Logging: ${LOGGING}"
echo "Workspace: ${WORKSPACE}"
echo "Outputs: ${OUTPUTS}"

# Loop until operation complete or POLL_WAIT_MAX
POLL_WAIT_TOTAL=0
LOGS_COUNT=-1
PREEMPT_COUNT=-1
OUTPUT_COUNT=-1
while [[ $(get_operation_done_status "${OPERATION_ID}") == "false" ]]; do

  echo
  echo "$(date '+%Y-%m-%d %H:%M:%S'): operation not complete"

  # Check that we haven't been polling too long
  if [[ -n "${POLL_WAIT_MAX}" ]] && \
     [[ "${POLL_WAIT_TOTAL}" -ge "${POLL_WAIT_MAX}" ]]; then
    echo "Total wait time (${POLL_WAIT_TOTAL} seconds) has exceeded the max (${POLL_WAIT_MAX})."
    exit 2
  fi

  # Gather info. These directories can be empty for a while during execution

  # Logs should be 0 to 3 files and should be the first to show up
  GS_LOGS=$(gsutil_ls "${LOGGING}/${OPERATION_ID#operations/}*")
  GS_WS=$(gsutil_ls "${WORKSPACE}/**" | sed -e 's#^'${WORKSPACE}/'##')
  GS_OUT=$(gsutil_ls "${OUTPUTS}")

  # The Cromwell filesystem is going to be:
  #   <workspace>/<workflow-name>/<cromwell-job-id>/call-<stage>
  # with some variety to what is under each "call-<stage>"
  #
  # If the call is unsharded (not a scatter), then the call-<stage>
  # directory contains objects like:
  #   exec.sh -- The code that gets executed on the VM.
  #   <stage>-rc.txt -- Contains the return code for the stage.
  #                     This file will not be exist until the stage completes.
  #                     If the VM is preempted, this file will never be written.
  #   <stage>-stdout.txt -- stdout captured during execution of exec.sh.
  #   <stage>-stderr.txt -- stderr captured during execution of exec.sh.
  #   <stage>.txt -- Genomics Pipeliens operations log.
  #
  # If the stage is sharded, then for each shard there will be a folder under
  # call-<stage> named "shard-<n>" where numbering starts at 0.
  #
  # If the Pipelines VM was preempted, then a subdirectory will be found under
  # call-<stage> named "attempt-<m>" where numbering starts at 2.
  #
  # For sharded and preemptible stages then, one may find:
  # call-<stage>/shard-<n>/attempt-<m>

  # From the list of the files in the workspace directory, extract useful
  # sets of files from which we can glean status:
  # All "exec.sh" files: indicates that the call and/or shard and/or attempt
  #   has started.
  # All "-rc.txt" files: indicates that the call and/or shard and/or attempt
  #   has completed.
  # All "attempt-*/exec.sh" files: indicates that a previous attempt failed
  #   and is assume to be due to preemption (*this is *not* checked explicitly).

  WS_EXECS=$(echo "${GS_WS}" | grep '/exec.sh$' || true)
  WS_RCS=$(echo "${GS_WS}" | grep '\-rc.txt$' || true)
  WS_PREEMPTS=$(echo "${GS_WS}" | grep 'attempt-[0-9]\+/exec.sh$' || true)

  # Emit status

  GS_LOGS_COUNT=$(line_count "${GS_LOGS}")
  if [[ "${GS_LOGS_COUNT}" -ne "${LOGS_COUNT}" ]]; then
    if [[ -n "${GS_LOGS}" ]]; then
      echo "Operation logs found: "
      echo "${GS_LOGS}" | sed -e 's#^'${LOGGING}/'##g' | indent
    else
      echo "No operations logs found."
    fi
    LOGS_COUNT="${GS_LOGS_COUNT}"
  fi

  if [[ -n "${WS_EXECS}" ]]; then
    if [[ -n "${WS_RCS}" ]]; then
      echo "Calls (including shards) completed: "$(line_count "${WS_RCS}")
    fi

    # To determine what is running, find all call or call/shard paths that
    # have an "exec.sh" with no "*-rc.txt" file.
    WS_CALLS_STARTED=$(
      echo "${WS_EXECS}" \
        | sed -E \
              -e 's#[^/]+/[^/]+/##' \
              -e 's#/exec.sh##' \
              -e 's#/attempt-[0-9]+##' \
        | sort -u)
    WS_CALLS_COMPLETE=$(
      echo "${WS_RCS}" \
        | sed -E \
              -e 's#[^/]+/[^/]+/##' \
              -e 's#/[^/]+-rc.txt##' \
              -e 's#/attempt-[0-9]+##' \
        | sort -u)

    IN_PROGRESS=$(\
      comm -2 -3  \
        <(echo "${WS_CALLS_STARTED}") \
        <(echo "${WS_CALLS_COMPLETE}"))
    if [[ -n ${IN_PROGRESS} ]]; then
      echo "Calls started but not complete:"
      echo "${IN_PROGRESS}" | indent
    else
      echo "No calls currently in progress."
      echo "(Transitioning to next stage or copying final output)." | indent
    fi

    WS_PREEMPT_COUNT=$(line_count "${WS_PREEMPTS}")
    if [[ "${WS_PREEMPT_COUNT}" -ne "${PREEMPT_COUNT}" ]]; then
      echo "Total Preemptions: ${WS_PREEMPT_COUNT}"
      PREEMPT_COUNT="${WS_PREEMPT_COUNT}"
    fi
  fi

  GS_OUTPUT_COUNT=$(line_count "${GS_OUT}")
  if [[ "${GS_OUTPUT_COUNT}" -ne "${OUTPUT_COUNT}" ]]; then
    echo "There are ${GS_OUTPUT_COUNT} output files"

    OUTPUT_COUNT="${GS_OUTPUT_COUNT}"
  fi

  echo "Sleeping ${POLL_INTERVAL_SECONDS} seconds"
  sleep ${POLL_INTERVAL_SECONDS}
  POLL_WAIT_TOTAL=$((POLL_WAIT_TOTAL + POLL_INTERVAL_SECONDS))
done

echo
echo "$(date '+%Y-%m-%d %H:%M:%S'): operation complete"

echo
echo "Completed operation status information"
get_operation_status "${OPERATION_ID}" | indent

echo
echo "Operation output"
gsutil_ls "${OUTPUTS}" | indent

echo
echo "Preemption retries:"
WS_PREEMPTS=$(gsutil_ls ${WORKSPACE}/**/attempt-*/exec.sh)
if [[ -n "${WS_PREEMPTS}" ]]; then
  echo "${WS_PREEMPTS}" \
    | sed -E \
          -e 's#^'${WORKSPACE}'/[^/]+/[^/]+/##' \
          -e 's#/exec.sh##' \
    | indent

  echo "Total preemptions: " $(echo "${WS_PREEMPTS}" | wc -l)
else
  echo "None" | indent
fi
