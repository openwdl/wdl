#!/usr/bin/env bash

SCRIPTS_DIR=$(cd $(dirname "$0"); pwd -P)
PYTHON_DIR=$(dirname "${SCRIPTS_DIR}")
BASE_DIR=$(dirname "${PYTHON_DIR}")

pushd "${BASE_DIR}"
	antlr4 -Dlanguage=Python2 -o ${PYTHON_DIR}/WdlParser/ -listener -visitor  WdlLexerPython.g4
	antlr4 -Dlanguage=Python2 -DtokenVocab=WdlLexerPython -o ${PYTHON_DIR}/WdlParser/  -listener -visitor WdlParser.g4
popd
