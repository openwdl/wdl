package org.openwdl.wdl.parser;

public class VisitorTest extends WdlParserBaseVisitor<String> {

    @Override
    public String aggregateResult(String aggregate, String nextResult) {
        return super.aggregateResult(aggregate, nextResult);
    }
}
