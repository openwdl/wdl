package org.openwdl.wdl.parser;

import java.util.Stack;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.LexerNoViableAltException;
import org.antlr.v4.runtime.Token;
import org.apache.commons.text.StringEscapeUtils;

public abstract class WDLBaseLexer extends Lexer {

    private Stack<Boolean> curlyStack;
    private int _previousTokenType;
    private boolean _withinSQuote = false;
    private boolean _withinDQuote = false;

    public WDLBaseLexer self;

    public WDLBaseLexer(CharStream charStream) {
        super(charStream);
        curlyStack = new Stack<>();
        self = this;
    }

    @Override
    public Token nextToken() {
        CommonToken token = (CommonToken) super.nextToken();

        int currentType = token.getType();
        if (_mode == WdlLexer.SquoteInterpolatedString) {
            if (token.getType() == WdlLexer.SQuoteUnicodeEscape) {
                token = new CommonToken(WdlLexer.SQuoteStringPart, unescape(token.getText()));
            }

        } else if (_mode == WdlLexer.DquoteInterpolatedString) {

            if (token.getType() == WdlLexer.DQuoteUnicodeEscape) {
                token = new CommonToken(WdlLexer.DQuoteStringPart, unescape(token.getText()));
            }

        } else if (_mode == WdlLexer.Command) {

            if (token.getType() == WdlLexer.CommandUnicodeEscape) {
                token = new CommonToken(WdlLexer.CommandStringPart, unescape(token.getText()));
            }

        } else if (_mode == WdlLexer.HereDocCommand) {

            if (token.getType() == WdlLexer.HereDocUnicodeEscape) {
                token = new CommonToken(WdlLexer.HereDocStringPart, unescape(token.getText()));
            }

        }
        if (_channel == DEFAULT_TOKEN_CHANNEL) {
            _previousTokenType = currentType;
        }
        return token;
    }


    public void StartSQuoteInterpolatedString() {

        if (!_withinSQuote) {
            _withinSQuote = true;
            pushMode(WdlLexer.SquoteInterpolatedString);
        } else {
            throw new LexerNoViableAltException(this, _input, _input.index(), null);
        }

    }

    public void StartDQuoteInterpolatedString() {
        if (!_withinDQuote) {
            _withinDQuote = true;
            pushMode(WdlLexer.DquoteInterpolatedString);
        } else {
            throw new LexerNoViableAltException(this, _input, _input.index(), null);
        }

    }

    public void FinishSQuoteInterpolatedString() {
        _withinSQuote = false;
        popMode();
    }


    public void FinishDQuoteInterpolatedString() {
        _withinDQuote = false;
        popMode();
    }


    public boolean IsCommand() {
        return _previousTokenType == WdlLexer.COMMAND;
    }

    public void PopModeOnCurlBracketClose() {
        if (!curlyStack.empty()) {
            if (curlyStack.pop()) {
                popMode();
            }
        }
    }

    public void PopCurlBrackOnClose() {
        curlyStack.pop();
    }

    public void PushCommandAndBrackEnter() {
        pushMode(WdlLexer.Command);
        curlyStack.push(true);
    }

    public void PushCurlBrackOnEnter(int shouldPop) {
        curlyStack.push(shouldPop == 1);
    }

    private String unescape(String text) {
        return StringEscapeUtils.unescapeJava(text);
    }


}