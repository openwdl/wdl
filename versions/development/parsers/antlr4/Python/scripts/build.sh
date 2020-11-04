#!/usr/bin/env bash

SCRIPTS_DIR=$(cd $(dirname "$0"); pwd -P)
PYTHON_DIR=$(dirname "${SCRIPTS_DIR}")
BASE_DIR=$(dirname "${PYTHON_DIR}")

pushd "${BASE_DIR}"
	antlr4 -Dlanguage=Python3 -o ${PYTHON_DIR}/wdl_parser/ WdlLexer.g4
	antlr4 -Dlanguage=Python3 -o ${PYTHON_DIR}/wdl_parser/  -listener -visitor WdlParser.g4
popd
