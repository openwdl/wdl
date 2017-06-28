#!/bin/bash

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# poll.sh
#
# Polls the completion status of a Google Genomics operation until
# the operation is completed.
#
# When the operation is marked as "done: true", the script emits a
# brief status summary of the operation such that one can easily determine
# whether the operation was successful. For example:
#
#   done: true
#   metadata:
#     events:
#     - description: start
#       startTime: '2016-08-05T23:08:26.432090867Z'
#     - description: pulling-image
#       startTime: '2016-08-05T23:08:26.432154840Z'
#     - description: localizing-files
#       startTime: '2016-08-05T23:09:03.947223371Z'
#     - description: running-docker
#       startTime: '2016-08-05T23:09:03.947277516Z'
#     - description: delocalizing-files
#       startTime: '2016-08-06T00:26:22.863609038Z'
#     - description: ok
#       startTime: '2016-08-06T00:26:24.296178476Z'
#   name: operations/OPERATION-ID  
#
# If an error has occurred, then the top-level "errors" object will be present.
#
# To have the script emit the entire operation, set the environment variable:
#
#   OUTPUT_LEVEL="verbose"

set -o errexit
set -o nounset

readonly SCRIPT_DIR=$(dirname "${0}")

# Bring in operation utility functions
source ${SCRIPT_DIR}/operations_util.sh

# MAIN

# Check usage
if [[ $# -ne 1 ]] && [[ $# -ne 2 ]]; then
  2>&1 echo "Usage: $0 OPERATION-ID <poll-interval-seconds>"
  exit 1
fi

# Extract command-line arguments
readonly OPERATION_ID="${1}"
readonly POLL_INTERVAL_SECONDS="${2:-60}"  # Default 60 seconds between requests

# Loop until operation complete
while [[ $(get_operation_done_status "${OPERATION_ID}") == "false" ]]; do
  echo "Operation not complete. Sleeping ${POLL_INTERVAL_SECONDS} seconds"
  sleep ${POLL_INTERVAL_SECONDS}
done

# Emit the operation details
echo
echo "Operation complete"
if [[ ${OUTPUT_LEVEL:-} == "verbose" ]]; then
  get_operation_all "${OPERATION_ID}"
else
  get_operation_status "${OPERATION_ID}"
fi

