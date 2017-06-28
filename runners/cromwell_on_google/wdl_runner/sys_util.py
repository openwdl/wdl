#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# sys_util.py

import logging
import os
import sys


def exit_with_error(err_string):
  """Emit the specified error string and exit with an exit code of 1."""
  sys.stderr.write("ERROR: {0}\n".format(err_string))
  sys.exit(1)


def copy_from_env(env_vars, environ):
  """Returns a dict of required environment variables."""

  result = {}
  for e in env_vars:
    val = environ.get(e, None)
    if val is None:
      exit_with_error("the " + e + " environment variable must be set")
    logging.info(e + "->" + os.environ[e])
    result[e] = val

  return result


if __name__ == '__main__':
  pass

