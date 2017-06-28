#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# get_yaml_value.py
#
# Utility script for extracting values from YAML.
# This will typically be called from shell scripts, which typically
# have fairly hacky ways of extracting values from YAML.
#
# An example usage would be where a shell script has YAML output from
# a gcloud command for an genomics operation and needs to extract fields:
#
#  OP=$(gcloud --format=yaml alpha genomics operations describe "${OP_ID}")
#  CTIME=$(python get_yaml_value.py "${OP}" "metadata.createTime")
#  ETIME=$(python get_yaml_value.py "${OP}" "metadata.endTime")
#
# Note that gcloud directly supports extracting fields, so the above could also
# be:
#
#  CTIME=$(gcloud alpha genomics operations describe "${OP_ID}"
#           --format='value(metadata.createTime)')
#  ETIME=$(gcloud alpha genomics operations describe "${OP_ID}"
#          --format='value(metadata.endTime)')
#
# but then requires an API call to get each value.
#
# Note that if the value requested does not exist in the YAML, this script
# exits with an error code (1).

from __future__ import print_function

import sys
import yaml

if len(sys.argv) != 3:
  print("Usage: %s [yaml] [field]" % sys.argv[0], file=sys.stderr)
  sys.exit(1)

def main(yaml_string, field):
  data = yaml.load(yaml_string)

  # field is expected to be period-separated: foo.bar.baz
  fields = field.split('.')

  # Walk the list of fields and check that the key exists.
  curr = data
  for key in fields:
    if key in curr:
      curr = curr[key]
    else:
      sys.exit(1)
  
  print(curr)

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])
