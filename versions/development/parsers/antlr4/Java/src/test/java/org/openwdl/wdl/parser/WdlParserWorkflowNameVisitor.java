package org.openwdl.wdl.parser;

public class WdlParserWorkflowNameVisitor extends WdlParserBaseVisitor<String> {

    @Override
    public String visitWorkflow(WdlParser.WorkflowContext ctx) {
        String x = ctx.Identifier().getText();
        visitChildren(ctx);
        return x;
    }
}
