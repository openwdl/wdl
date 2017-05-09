# Parsers for WDL

This directory contains pregenerated parsers for WDL in a variety of languages. Except for the Java parser, all of these are provided *as-is*. We believe that they work but do not have the resources to validate that claim. However if you're willing to help us fix any issues you come across we'll work with you to do so."

# How to rebuild

Typing `make` in this directory will trigger builds for all of the languages and produce the appropriate files. This requires you to have [Hermes](https://github.com/scottfrazer/hermes) installed on your system. To do this you might need to use a virtualenv, e.g. ``mkvirtualenv py3 -p `which python3` ``

