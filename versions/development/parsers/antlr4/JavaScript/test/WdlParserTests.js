const assert = require("assert");
const fs = require("fs");
const path = require("path");
const antlr4 = require("antlr4/index");
const ReportingErrorListener = require("./utils").WdlParserErrorListener;
const WdlLexer = require("../src/WdlLexer").WdlLexer;
const WdlParser = require("../src/WdlParser").WdlParser;


describe("WdlParseTests", function () {

    var errorFiles = [];
    var successFiles = [];

    let currentDir = __dirname;
    let examplesDir = path.join(currentDir, "../../examples");

    fs.readdirSync(examplesDir).forEach(function (f) {
        if (f.endsWith(".error")) {
            errorFiles.push(path.join(examplesDir, f));
        } else {
            successFiles.push(path.join(examplesDir, f));
        }
    });


    successFiles.forEach(function (wdlFile) {
        it(wdlFile + " Should parse wdl files successfully", function () {
            var charStream = antlr4.CharStreams.fromPathSync(wdlFile, "utf-8");
            let lexer = new WdlLexer(charStream);
            let s = new antlr4.CommonTokenStream(lexer);
            let parser = new WdlParser(input = s);
            let errorListener = new ReportingErrorListener();
            parser.removeErrorListeners();
            parser.addErrorListener(errorListener);
            parser.document();
            assert.equal(errorListener.hasError(), false,JSON.stringify(errorListener.errors) );
        });
    });

    errorFiles.forEach(function (wdlFile) {
        it(wdlFile + " should fail to parse error files", function () {
            var charStream = antlr4.CharStreams.fromPathSync(wdlFile, "utf-8");
            let lexer = new WdlLexer(charStream);
            let s = new antlr4.CommonTokenStream(lexer);
            let parser = new WdlParser(input = s);
            let errorListener = new ReportingErrorListener();
            parser.removeErrorListeners();
            parser.addErrorListener(errorListener);
            parser.document();
            assert.equal(errorListener.hasError(), true);
        })
    });
});
