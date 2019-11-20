const assert = require("assert");
const fs = require("fs");
const path = require("path");
const antlr4 = require("antlr4/index");
const ReportingErrorListener = require("./utils").WdlParserErrorListener;
const WdlLexer = require("../src/WdlLexer").WdlLexer;
const WdlParser = require("../src/WdlParser").WdlParser;

describe("WdlParseTests", function () {

    let error_files = [];
    let success_files = [];

    before(function () {
        let currentDir = __dirname;
        let examplesDir = path.join(currentDir, "../../examples");
        fs.readdir(examplesDir, function (err, files) {
            if (err) {
                throw new Error("Could not local example files - " + err)
            }

            files.forEach(function (f) {
                if (f.endsWith(".error")) {
                    error_files.push(path.join(examplesDir, f));
                } else {
                    success_files.push(path.join(examplesDir, f));
                }
            });
        });
    });

    it("Should parse wdl files successfully", function () {

        for (let i = 0; i < success_files.length; i++) {
            let wdlFile = success_files[i];
            console.log(wdlFile + " - Should Succeed");
            var charStream = antlr4.CharStreams.fromPathSync(wdlFile, "utf-8");
            let lexer = new WdlLexer(charStream);
            let s = new antlr4.CommonTokenStream(lexer);
            let parser = new WdlParser(input = s);
            let errorListener = new ReportingErrorListener();
            parser.removeErrorListeners();
            parser.addErrorListener(errorListener);
            parser.document();
            assert.equal(errorListener.hasError(),false);
        }

    });

    it("Should fail to parse error files", function () {
        for (let i = 0; i < error_files.length; i++) {
            let wdlFile = error_files[i];
            console.log(wdlFile + " - Should Fail");
            var charStream = antlr4.CharStreams.fromPathSync(wdlFile, "utf-8");
            let lexer = new WdlLexer(charStream);
            let s = new antlr4.CommonTokenStream(lexer);
            let parser = new WdlParser(input = s);
            let errorListener = new ReportingErrorListener();
            parser.removeErrorListeners();
            parser.addErrorListener(errorListener);
            parser.document();
            assert.equal(errorListener.hasError(),true);
        }

    })

});
