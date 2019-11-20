#!/usr/bin/env bash

SCRIPTS_DIR=$(cd $(dirname "$0"); pwd -P)
JAVASCRIPT_DIR=$(dirname "${SCRIPTS_DIR}")
BASE_DIR=$(dirname "${JAVASCRIPT_DIR}")

pushd "${BASE_DIR}"
	antlr4 -Dlanguage=JavaScript -o ${JAVASCRIPT_DIR}/src/ -listener -visitor WdlParser.g4 WdlLexer.g4
popd
