#!/usr/bin/env bash

SCRIPTS_DIR=$(cd "$(dirname "$0")" || exit; pwd -P)
JAVASCRIPT_DIR=$(dirname "${SCRIPTS_DIR}")
BASE_DIR=$(dirname "${JAVASCRIPT_DIR}")

pushd "${BASE_DIR}" || exit
	antlr4 -Dlanguage=JavaScript -o ${JAVASCRIPT_DIR}/src/ -listener -visitor wdl_parser.g4 WdlLexer.g4
popd || exit
