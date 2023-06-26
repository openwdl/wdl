#!/usr/bin/env bash

SCRIPTS_DIR=$(cd $(dirname "$0"); pwd -P)
PYTHON_DIR=$(dirname "${SCRIPTS_DIR}")
BASE_DIR=$(dirname "${PYTHON_DIR}")

pushd "${BASE_DIR}"
	antlr4 -v 4.13.0 -Dlanguage=Python3 -o ${PYTHON_DIR}/wdl_parser/ -listener -visitor WdlV1Parser.g4 WdlV1Lexer.g4
popd
