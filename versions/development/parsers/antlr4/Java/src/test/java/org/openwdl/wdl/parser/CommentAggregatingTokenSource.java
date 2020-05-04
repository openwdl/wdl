package org.openwdl.wdl.parser;

import java.util.ArrayList;
import java.util.List;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.Token;

public class CommentAggregatingTokenSource extends WdlLexer {


    private List<String> comments = new ArrayList<>();


    public CommentAggregatingTokenSource(CharStream input) {
        super(input);
    }


    @Override
    public Token nextToken() {
        CommonToken token = (CommonToken) super.nextToken();
        if (token.getType() == WdlLexer.COMMENT) {
            comments.add(token.getText());
        }
        return token;
    }

    public List<String> getComments() {
        return comments;
    }

}
