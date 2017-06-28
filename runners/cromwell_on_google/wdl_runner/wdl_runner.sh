#!/bin/bash

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

set -o errexit
set -o nounset

readonly INPUT_PATH=/pipeline/input

# WDL, INPUTS, and OPTIONS file contents are all passed into
# the pipeline as environment variables - write them out as
# files.
mkdir -p "${INPUT_PATH}"
echo "${WDL}" > "${INPUT_PATH}/wf.wdl"
echo "${WORKFLOW_INPUTS}" > "${INPUT_PATH}/wf.inputs.json"
echo "${WORKFLOW_OPTIONS}" > "${INPUT_PATH}/wf.options.json"

# Set the working directory to the location of the scripts
readonly SCRIPT_DIR=$(dirname $0)
cd "${SCRIPT_DIR}"

# Execute the wdl_runner
python -u wdl_runner.py \
 --wdl "${INPUT_PATH}"/wf.wdl \
 --workflow-inputs "${INPUT_PATH}"/wf.inputs.json \
 --working-dir "${WORKSPACE}" \
 --workflow-options "${INPUT_PATH}"/wf.options.json \
 --output-dir "${OUTPUTS}"

