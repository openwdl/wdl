package org.openwdl.wdl.parser;

import org.antlr.v4.runtime.tree.TerminalNode;

public class WdlWorkflowNameListener extends WdlParserBaseListener {

    String workflowName;

    @Override
    public void exitWorkflow(WdlParser.WorkflowContext ctx) {
        TerminalNode node = ctx.Identifier();
        System.out.println(ctx.start.getLine());
        System.out.println(ctx.start.getCharPositionInLine());
        String x = ctx.getText();
        workflowName = ctx.Identifier().getText();
        super.enterWorkflow(ctx);
    }
}
