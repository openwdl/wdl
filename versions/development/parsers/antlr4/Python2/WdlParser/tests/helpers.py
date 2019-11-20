import sys

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from ..WdlLexerPython import WdlLexerPython


class CommentAggregatingTokenSource(WdlLexerPython):

    def __init__(self, input=None, output=sys.stdout):
        super(CommentAggregatingTokenSource,self).__init__(input, output)
        self.comments = []

    def nextToken(self):
        token = super(CommentAggregatingTokenSource,self).nextToken()
        if token.type == self.COMMENT:
            self.comments.append(token.text)
        return token


class WdlParserTestErrorListener(ErrorListener):

    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append({"line": line, "position": column, "message": msg})

    def hasError(self):
        return len(self.errors) > 0

    def errorStrings(self):
        if self.hasError():
            errorString = ""
            for error in self.errors:
                errorString += "\nline {}:{} - {}".format(error["line"], error["position"], error["message"])
            return errorString
        else:
            return ""
