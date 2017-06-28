#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# file_util.py

import logging
import simplejson
import string
import subprocess

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

import sys_util


def file_safe_substitute(file_name, mapping):
  """Performs placeholder replacement on a file, saving contents in place."""

  with open(file_name, 'rb') as f:
    file_contents = f.read()
    return string.Template(file_contents).safe_substitute(mapping)


def gsutil_cp(source_files, dest_dir):
  """Copies files to GCS and exits on error."""

  cp_cmd = ['gsutil', 'cp'] + source_files + [dest_dir]

  logging.info("Copying %s to %s", source_files, dest_dir)

  # Copies can fail, so include retries...
  for attempt in range(3):
    p = subprocess.Popen(cp_cmd, stderr=subprocess.PIPE)
    return_code = p.wait()
    if not return_code:
      return

    logging.warn("Copy %s to %s failed: attempt %d",
                 source_files, dest_dir, attempt)

  sys_util.exit_with_error(
      "copying files from %s to %s failed: %s" % (
          source_files, dest_dir, p.stderr.read()))


def verify_gcs_dir_empty_or_missing(path):
  """Verify that the output "directory" does not exist or is empty."""

  # Use the storage API directly instead of gsutil.
  # gsutil does not return explicit error codes and so to detect
  # a non-existent path would require capturing and parsing the error message.

  # Verify the input is a GCS path
  if not path.startswith('gs://'):
    sys_util.exit_with_error("Path is not a GCS path: '%s'" % path)

  # Tokenize the path into bucket and prefix
  parts = path[len('gs://'):].split('/', 1)
  bucket = parts[0]
  prefix = parts[1] if len(parts) > 1 else None

  # Get the storage endpoint
  credentials = GoogleCredentials.get_application_default()
  service = discovery.build('storage', 'v1', credentials=credentials,
                            cache_discovery=False)

  # Build the request - only need the name
  fields = 'nextPageToken,items(name)'
  request = service.objects().list(
      bucket=bucket, prefix=prefix, fields=fields, maxResults=2)

  # If we get more than 1 item, we are done (directory not empty)
  # If we get zero items, we are done (directory empty)
  # If we get 1 item, then we need to check if it is a "directory object"

  items = []
  while request and len(items) < 2:
    try:
      response = request.execute()
    except HttpError as err:
      error = simplejson.loads(err.content)
      error = error['error']

      sys_util.exit_with_error(
          "%s %s: '%s'" % (error['code'], error['message'], path))

    items.extend(response.get('items', []))
    request = service.objects().list_next(request, response)

  if not items:
    return True

  if len(items) == 1 and items[0]['name'].rstrip('/') == prefix.rstrip('/'):
    return True

  return False


if __name__ == '__main__':
  pass

