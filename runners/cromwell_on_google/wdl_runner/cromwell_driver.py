#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# cromwell_driver.py
#
# This script provides a library interface to Cromwell, namely:
#  * Start the Cromwell server
#  * Submit execution requests to Cromwell
#  * Poll Cromwell for job status

import logging
import os
import subprocess
import time

import requests

import sys_util


class CromwellDriver(object):

  def __init__(self, cromwell_conf, cromwell_jar):
    self.cromwell_conf = cromwell_conf
    self.cromwell_jar = cromwell_jar

    self.cromwell_proc = None

  def start(self):
    """Start the Cromwell service."""
    if self.cromwell_proc:
      logging.info("Request to start Cromwell: already running")
      return

    self.cromwell_proc = subprocess.Popen([
        'java',
        '-Dconfig.file=' + self.cromwell_conf,
        '-Xmx4g',
        '-jar', self.cromwell_jar,
        'server'])

    logging.info("Started Cromwell")

  def fetch(self, wf_id=None, post=False, files=None, method=None):
    url = 'http://localhost:8000/api/workflows/v1'
    if wf_id is not None:
      url = os.path.join(url, wf_id)
    if method is not None:
      url = os.path.join(url, method)
    if post:
      r = requests.post(url, files=files)
    else:
      r = requests.get(url)
    return r.json()

  def submit(self, wdl, workflow_inputs, workflow_options, sleep_time=15):
    """Post new job to the server and poll for completion."""

    # Add required input files
    with open(wdl, 'rb') as f:
      wdl_source = f.read()
    with open(workflow_inputs, 'rb') as f:
      wf_inputs = f.read()

    files = {
        'wdlSource': wdl_source,
        'workflowInputs': wf_inputs,
    }

    # Add workflow options if specified
    if workflow_options:
      with open(workflow_options, 'rb') as f:
        wf_options = f.read()
        files['workflowOptions'] = wf_options

    # After Cromwell start, it may take a few seconds to be ready for requests.
    # Poll up to a minute for successful connect and submit.

    job = None
    max_time_wait = 60
    wait_interval = 5

    time.sleep(wait_interval)
    for attempt in range(max_time_wait/wait_interval):
      try:
        job = self.fetch(post=True, files=files)
        break
      except requests.exceptions.ConnectionError as e:
        logging.info("Failed to connect to Cromwell (attempt %d): %s",
          attempt + 1, e)
        time.sleep(wait_interval)

    if not job:
      sys_util.exit_with_error(
          "Failed to connect to Cromwell after {0} seconds".format(
              max_time_wait))

    if job['status'] != 'Submitted':
      sys_util.exit_with_error(
          "Job status from Cromwell was not 'Submitted', instead '{0}'".format(
              job['status']))

    # Job is running.
    cromwell_id = job['id']
    logging.info("Job submitted to Cromwell. job id: %s", cromwell_id)

    # Poll Cromwell for job completion.
    attempt = 0
    max_failed_attempts = 3
    while True:
      time.sleep(sleep_time)

      # Cromwell occassionally fails to respond to the status request.
      # Only give up after 3 consecutive failed requests.
      try:
        status_json = self.fetch(wf_id=cromwell_id, method='status')
        attempt = 0
      except requests.exceptions.ConnectionError as e:
        attempt += 1
        logging.info("Error polling Cromwell job status (attempt %d): %s",
          attempt, e)

        if attempt >= max_failed_attempts:
          sys_util.exit_with_error(
            "Cromwell did not respond for %d consecutive requests" % attempt)

        continue

      status = status_json['status']
      if status == 'Succeeded':
        break
      elif status == 'Submitted':
        pass
      elif status == 'Running':
        pass
      else:
        sys_util.exit_with_error(
            "Status of job is not Submitted, Running, or Succeeded: %s" % status)

    logging.info("Cromwell job status: %s", status)

    # Cromwell produces a list of outputs and full job details
    outputs = self.fetch(wf_id=cromwell_id, method='outputs')
    metadata = self.fetch(wf_id=cromwell_id, method='metadata')

    return outputs, metadata


if __name__ == '__main__':
  pass
