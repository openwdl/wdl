#!/bin/bash

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# operations_util.sh

# get_operation_value
#
# Request just the specified value of the operation
function get_operation_value() {
  local operation_id="${1}"
  local field="${2}"

  gcloud alpha genomics operations describe ${operation_id} \
      --format='value('${field}')'
}
readonly -f get_operation_value

# get_operation_done_status
#
# Request just the value of the operation top-level "done" field.
# Returns the value in all lower-case.
function get_operation_done_status() {
  local operation_id="${1}"

  gcloud alpha genomics operations describe ${operation_id} \
      --format='value(done)' \
    | tr 'A-Z' 'a-z'
}
readonly -f get_operation_done_status

# get_operation_status
#
# Return basic status information about the pipeline:
#
#  * done
#  * error
#  * metadata.events
#  * name
#
function get_operation_status() {
  local operation_id="${1}"

  gcloud alpha genomics operations describe ${operation_id} \
    --format='yaml(done, error, metadata.events, name)'
}
readonly -f get_operation_status

# get_operation_compute_resources
#
# Return the Compute Engine resources for the operation (if present)
#
function get_operation_compute_resources() {
  local operation_id="${1}"

  gcloud alpha genomics operations describe ${operation_id} \
    --format='yaml(metadata.runtimeMetadata.computeEngine)'
}
readonly -f get_operation_compute_resources

# get_operation_all
#
# Requests the full details of the operation in YAML format
function get_operation_all() {
  local operation_id="${1}"

  gcloud alpha genomics operations describe ${operation_id} \
    --format yaml
}
readonly -f get_operation_all

