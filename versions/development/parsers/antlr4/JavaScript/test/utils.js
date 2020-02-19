const ErrorListener = require("antlr4/error").ErrorListener;

function WdlParserErrorListener() {
    ErrorListener.call(this);
    this.errors = [];
    return this;
}

WdlParserErrorListener.prototype = Object.create(ErrorListener.prototype);
WdlParserErrorListener.prototype.constructor = WdlParserErrorListener;
WdlParserErrorListener.INSTANCE = new WdlParserErrorListener();
WdlParserErrorListener.prototype.syntaxError = function (recognizer, offendingSymbol, line, column, msg, e) {
    this.errors.push({"line": line, "position": column, "message": msg});
};

WdlParserErrorListener.prototype.hasError = function () {
    return this.errors.length > 0;
};


exports.WdlParserErrorListener = WdlParserErrorListener;
