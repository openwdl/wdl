import sys
import os
import re
from typing import TextIO

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from wdl_parser.WdlLexer import WdlLexer

DEFAULT_EXAMPLE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../examples")

PATTERN = re.compile(r"#EXPECTED_ERROR\s+line:(?P<linenum>[0-9]+)\s(msg:(?P<msg>\s(\"[^\n\r]+\"|'[^\n\r]+')))?.*?")


def get_example_files(error: bool):
    example_dir = os.environ.get("WDL_TEXT_EXAMPLES", DEFAULT_EXAMPLE_DIR)
    print(example_dir)
    files = [f for f in os.listdir(example_dir) if
             os.path.isfile(os.path.join(example_dir, f))]
    parameters = []
    for file in files:
        if error:
            if file.endswith(".error"):
                parameters.append((FileStream(os.path.join(example_dir, file), "utf-8"), file))
        else:
            if not file.endswith(".error"):
                parameters.append((FileStream(os.path.join(example_dir, file), "utf-8"), file))

    return parameters


class CommentAggregatingTokenSource(WdlLexer):

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.comments = []

    def nextToken(self) -> Token:
        token = super().nextToken()
        if token.type == self.COMMENT:
            self.comments.append(token.text)
        return token


class WdlParserTestErrorListener(ErrorListener):

    def __init__(self) -> None:
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append({"line": line, "position": column, "message": msg})

    def hasError(self):
        return len(self.errors) > 0

    def errorStrings(self):
        if self.hasError():
            errorString = ""
            for error in self.errors:
                errorString +="\nline {}:{} - {}".format(error["line"],error["position"],error["message"])
            return errorString
        else:
            return ""