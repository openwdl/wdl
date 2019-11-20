const antlr4 = require("antlr4/index");
const LexerNoViableAltException = require("antlr4/error/Errors").LexerNoViableAltException;
const CommonToken = require("antlr4/Token").CommonToken;
const wdlLexer = require("./WdlLexer");
const uunescape = require("unescape-unicode");


function WDLBaseLexer(input) {
    antlr4.Lexer.call(this, input);
    this.curlyStack = [];
    this._previousTokenType = null;
    this._withinSQuote = false;
    this._withinDQuote = false;
    return this;
}

WDLBaseLexer.prototype = Object.create(antlr4.Lexer.prototype);
WDLBaseLexer.prototype.constructor = antlr4.Lexer;

WDLBaseLexer.prototype.nextToken = function () {
    let token = antlr4.Lexer.prototype.nextToken.call(this);
    let currentToken = token.type;
    if (this._mode === wdlLexer.WdlLexer.SquoteInterpolatedString && token.type === wdlLexer.WdlLexer.SQuoteUnicodeEscape) {
        let text = this.unescape(token.text);
        token = new CommonToken(type = wdlLexer.WdlLexer.SQuoteStringPart);
        token.text = text;
    } else if (this._mode === wdlLexer.WdlLexer.DquoteInterpolatedString && token.type === wdlLexer.WdlLexer.DQuoteUnicodeEscape) {
        let text = this.unescape(token.text);
        token = new CommonToken(type = wdlLexer.WdlLexer.DQuoteStringPart);
        token.text = text;
    } else if (this._mode === wdlLexer.WdlLexer.Command && token.type === wdlLexer.WdlLexer.CommandUnicodeEscape) {
        let text = this.unescape(token.text);
        token = new CommonToken(type = wdlLexer.WdlLexer.CommandStringPart);
        token.text = text;
    } else if (this._mode === wdlLexer.WdlLexer.HereDocCommand && token.type === wdlLexer.WdlLexer.HereDocUnicodeEscape) {
        let text = this.unescape(token.text);
        token = new CommonToken(type = wdlLexer.WdlLexer.HereDocStringPart);
        token.text = text;
    }

    if (this._channel === antlr4.Lexer.DEFAULT_TOKEN_CHANNEL) {
        this._previousTokenType = currentToken;
    }

    return token;
};

WDLBaseLexer.prototype.unescape = function (text) {
    return uunescape(text);
};

WDLBaseLexer.prototype.StartSQuoteInterpolatedString = function () {
    if (!this._withinSQuote) {
        this._withinSQuote = true;
        this.pushMode(wdlLexer.WdlLexer.SquoteInterpolatedString);
    } else {
        throw new LexerNoViableAltException(lexer = this, input = this._input, startIndex = this._index, deadEndConfigs = null);
    }
};

WDLBaseLexer.prototype.StartDQuoteInterpolatedString = function () {
    if (!this._withinDQuote) {
        this._withinDQuote = true;
        this.pushMode(wdlLexer.WdlLexer.DquoteInterpolatedString);
    } else {
        throw new LexerNoViableAltException(lexer = this, input = this._input, startIndex = this._index, deadEndConfigs = null);
    }
};

WDLBaseLexer.prototype.FinishSQuoteInterpolatedString = function () {
    this._withinSQuote = false;
    this.popMode();
};

WDLBaseLexer.prototype.FinishDQuoteInterpolatedString = function () {
    this._withinDQuote = false;
    this.popMode();
};

/**
 * @return {boolean}
 */
WDLBaseLexer.prototype.IsCommand = function () {
    return this._previousTokenType === wdlLexer.WdlLexer.COMMAND;
};

WDLBaseLexer.prototype.PopModeOnCurlBracketClose = function () {
    if (this.curlyStack.length > 0) {
        if (this.curlyStack.pop()) {
            this._channel = wdlLexer.WdlLexer.SkipChannel;
            this.popMode();
        }
    }
};

WDLBaseLexer.prototype.PopCurlBrackOnClose = function () {
    this.curlyStack.pop();
};

WDLBaseLexer.prototype.PushCommandAndBrackEnter = function () {
    this.pushMode(wdlLexer.WdlLexer.Command);
    this.curlyStack.push(true);
};

WDLBaseLexer.prototype.PushCurlBrackOnEnter = function (shouldPop) {
    this.curlyStack.push(shouldPop === 1);
};

/**
 * @return {boolean}
 */
WDLBaseLexer.prototype.IsInterpolationStart = function () {
    let previousChar = this._input.LA(-2);
    return previousChar === "~".charCodeAt(0);
};

/**
 * @return {boolean}
 */
WDLBaseLexer.prototype.IsAnyInterpolationStart = function () {
    let previousChar = this._input.LA(-2);
    return previousChar === '$'.charCodeAt(0) || previousChar === '~'.charCodeAt(0);
};

exports.WDLBaseLexer = WDLBaseLexer;
