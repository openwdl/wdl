#!/bin/bash

hermes generate ../grammar.hgr --name=wdl --directory=wdl
mv wdl/wdl_parser.py wdl/parser.py
