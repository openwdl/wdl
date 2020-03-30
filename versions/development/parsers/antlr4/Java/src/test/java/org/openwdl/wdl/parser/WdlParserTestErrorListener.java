package org.openwdl.wdl.parser;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.antlr.v4.runtime.BaseErrorListener;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.Recognizer;

public class WdlParserTestErrorListener extends BaseErrorListener {

    private List<SyntaxError> errors = new ArrayList<>();
    private final boolean assertNoErrors;

    public WdlParserTestErrorListener() {
        this(false);
    }

    public WdlParserTestErrorListener(boolean assertNoErrors) {
        this.assertNoErrors = assertNoErrors;
    }

    @Override
    public void syntaxError(Recognizer<?, ?> recognizer, Object offendingSymbol, int line, int charPositionInLine, String msg, RecognitionException e) {
        System.out.println(offendingSymbol);
        SyntaxError error = new SyntaxError(offendingSymbol, line, charPositionInLine, msg);
        if (!assertNoErrors) {
            errors.add(error);
        } else {
            throw new AssertionError("No errors expected: " + error.toString());
        }
    }


    public List<SyntaxError> getErrors() {
        return errors;
    }

    public boolean hasErrors() {
        return errors != null && errors.size() > 0;
    }


    public String getErrorString() {
        return "\n" + String.join("\n", errors.stream().map(SyntaxError::toString).collect(Collectors.toList()));
    }

    public static class SyntaxError {

        private final Object offendingSymbol;
        private final int line;
        private final int position;
        private final String message;

        SyntaxError(Object offendingSymbol, int line, int position, String message) {
            this.offendingSymbol = offendingSymbol;
            this.line = line;
            this.position = position;
            this.message = message;
        }

        public Object getOffendingSymbol() {
            return offendingSymbol;
        }

        public int getLine() {
            return line;
        }

        public int getPosition() {
            return position;
        }

        public String getMessage() {
            return message;
        }

        public AssertionError getAssertionError() {
            return new AssertionError(toString());
        }

        @Override
        public String toString() {
            return "line " + line + ":" + position + " " + message;
        }
    }
}
