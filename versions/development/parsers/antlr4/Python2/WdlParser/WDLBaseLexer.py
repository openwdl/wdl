import sys

from antlr4 import *
from antlr4.Token import CommonToken
from antlr4.error.Errors import LexerNoViableAltException

this = None


class WDLBaseLexer(Lexer):


    def __init__(self, input, output):
        super(WDLBaseLexer, self).__init__(input, output=output)
        self.curlyStack = list()
        self._previousTokenType = None
        self._withinSQuote = False
        self._withinDQuote = False

    def nextToken(self):

        token = super(WDLBaseLexer, self).nextToken()
        currentType = token.type
        if self._mode == self.SquoteInterpolatedString and token.type == self.SQuoteStringPart:
            text = self.unnescape(token.text)
            token = CommonToken(type=token.type)
            token.text = text
        if self._mode == self.DquoteInterpolatedString and token.type == self.DQuoteStringPart:
            text = self.unnescape(token.text)
            token = CommonToken(type=token.type)
            token.text = text
        if self._mode == self.Command and token.type == self.CommandStringPart:
            text = self.unnescape(token.text)
            token = CommonToken(type=token.type)
            token.text = text
        if self._mode == self.HereDocCommand and token.type == self.HereDocStringPart:
            text = self.unnescape(token.text)
            token = CommonToken(type=token.type)
            token.text = text

        if self._channel == self.DEFAULT_TOKEN_CHANNEL:
            self._previousTokenType = currentType
        return token

    def unnescape(self, text):
        return text.encode().decode("unicode_escape")

    def StartSQuoteInterpolatedString(self):
        if not self._withinSQuote:
            self._withinSQuote = True
            self.pushMode(self.SquoteInterpolatedString)
        else:
            raise LexerNoViableAltException(lexer=self, input=self._input, startIndex=self._input.index,
                                            deadEndConfigs=None)

    def StartDQuoteInterpolatedString(self):
        if not self._withinDQuote:
            self._withinDQuote = True
            self.pushMode(self.DquoteInterpolatedString)
        else:
            raise LexerNoViableAltException(lexer=self, input=self._input, startIndex=self._input.index,
                                            deadEndConfigs=None)

    def FinishSQuoteInterpolatedString(self):
        self._withinSQuote = False
        self.popMode()

    def FinishDQuoteInterpolatedString(self):
        self._withinDQuote = False
        self.popMode()

    def IsCommand(self):
        return self._previousTokenType == self.COMMAND

    def PopModeOnCurlBracketClose(self):
        if len(self.curlyStack) > 0:
            if self.curlyStack.pop():
                self._channel = self.SkipChannel
                self.popMode()

    def PopCurlBrackOnClose(self):
        self.curlyStack.pop()

    def PushCommandAndBrackEnter(self):
        self.pushMode(self.Command)
        self.curlyStack.append(True)

    def PushCurlBrackOnEnter(self, shouldPop):
        self.curlyStack.append(shouldPop == 1)

    def IsInterpolationStart(self):
        previousChar = chr(self._input.LA(-2))
        return previousChar == "~"

    def IsAnyInterpolationStart(self):
        previousChar = chr(self._input.LA(-2))
        return previousChar == "$" or previousChar == "~"
