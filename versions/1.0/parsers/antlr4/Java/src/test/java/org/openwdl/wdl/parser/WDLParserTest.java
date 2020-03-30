package org.openwdl.wdl.parser;

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.ParseTree;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.openwdl.wdl.parser.WdlParser.*;
import org.openwdl.wdl.parser.WdlParserTestErrorListener.SyntaxError;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class WDLParserTest {

    private static String examplesDirectory;

    private static Pattern expectedErrorPattern = Pattern.compile(
            "#EXPECTED_ERROR\\s+line:(?<linenum>[0-9]+)\\s+(?<msg>msg:(\\\"[^\\n\\r]+\\\"|'[^\\n\\r]))?.*");

    @BeforeAll
    public static void setup() {

        examplesDirectory = System.getProperty("examples-directory");
        Assertions.assertNotNull("Examples directory must be set", examplesDirectory);
    }

    public static Stream<Arguments> successfullWdlFiles() throws IOException {
        List<Arguments> testArguments = new ArrayList<>();
        File exampleDir = new File(examplesDirectory);

        for (File wdlFile : exampleDir.listFiles()) {
            if (!wdlFile.getName().endsWith(".error")) {
                String name = wdlFile.getName();
                testArguments.add(Arguments.of(Files.readAllBytes(wdlFile.toPath()), name));
            }
        }
        return testArguments.stream();
    }

    @ParameterizedTest(name = "[{index}]_testWdlFiles_shouldParseSuccessFully")
    @MethodSource("successfullWdlFiles")
    public void testWdlFiles_shouldParseSuccessFully(byte[] fileBytes, String fileName) {
        System.out.println("Testing WDL File: " + fileName + " should Successfully parse");
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        CodePointBuffer codePointBuffer = CodePointBuffer.withBytes(ByteBuffer.wrap(fileBytes));
        TokenSource tokenSource = new WdlLexer(CodePointCharStream.fromBuffer(codePointBuffer));
        WdlParser parser = new WdlParser(new CommonTokenStream(tokenSource));
        parser.removeErrorListeners();
        parser.addErrorListener(errorListener);
        DocumentContext context = parser.document();

        Assertions.assertAll("Input WDL should not have any errors",
                             () -> Assertions.assertFalse(errorListener.hasErrors(), errorListener::getErrorString));

        System.out.println("Successfully parsed input");

    }

    public static Stream<Arguments> failingWdlFiles() throws IOException {
        List<Arguments> testArguments = new ArrayList<>();
        File exampleDir = new File(examplesDirectory);

        for (File wdlFile : exampleDir.listFiles()) {
            if (wdlFile.getName().endsWith(".error")) {
                String name = wdlFile.getName();
                testArguments.add(Arguments.of(Files.readAllBytes(wdlFile.toPath()), name));
            }
        }
        return testArguments.stream();
    }

    @ParameterizedTest
    @MethodSource("failingWdlFiles")
    public void testWdlFiles_shouldFailParsing(byte[] fileBytes, String fileName) {
        System.out.println("Testing WDL File: " + fileName + " should fail to parse");
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        CodePointBuffer codePointBuffer = CodePointBuffer.withBytes(ByteBuffer.wrap(fileBytes));
        CommentAggregatingTokenSource tokenSource = new CommentAggregatingTokenSource(CodePointCharStream.fromBuffer(
                codePointBuffer));
        WdlParser parser = new WdlParser(new CommonTokenStream(tokenSource));
        parser.removeErrorListeners();
        parser.addErrorListener(errorListener);
        parser.document();

        Assertions.assertTrue(errorListener.hasErrors());

        List<SyntaxError> errors = errorListener.getErrors();
        List<String> comments = tokenSource.getComments();

        if (comments != null && comments.size() > 0) {
            for (String comment : comments) {
                Matcher matcher = expectedErrorPattern.matcher(comment);
                if (matcher.find()) {
                    int line = Integer.parseInt(matcher.group("linenum"));
                    String message = matcher.group("msg");
                    Assertions.assertTrue(errors.stream().anyMatch(error -> error.getLine() == line),
                                          message != null ? message : "Expecting an error at line: " + line);
                }
            }
        }

    }

    @Test
    public void testDquoteStringInterpolation() {
        String interpolation = "\"some string part ~{ident + ident} some string part after\"";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);

        StringContext stringContext = parser.string();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(stringContext);
        Assertions.assertEquals("some string part ", stringContext.string_part().getText());
        String_expr_with_string_partContext exprWithStringPartContext = stringContext.string_expr_with_string_part(0);
        Assertions.assertEquals(" some string part after", exprWithStringPartContext.string_part().getText());
        ExprContext exprTree = exprWithStringPartContext.string_expr_part().expr();
        Assertions.assertEquals("ident+ident", exprTree.getText());
        Expr_infixContext exprContext = exprTree.expr_infix();
        Infix1Context infix1Context = (Infix1Context) exprContext.getChild(0);
        Infix2Context infix2Context = (Infix2Context) infix1Context.getChild(0);
        Infix3Context infix3Context = (Infix3Context) infix2Context.getChild(0);
        AddContext addContext = (AddContext) infix3Context.getChild(0);
        Assertions.assertEquals("ident", addContext.expr_infix3().getText());
        Assertions.assertEquals("ident", addContext.expr_infix4().getText());
    }

    @Test
    public void testSquoteStringInterpolation() {
        String interpolation = "'some string part ~{ident + ident} some string part after'";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);

        StringContext stringContext = parser.string();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(stringContext);
        Assertions.assertEquals("some string part ", stringContext.string_part().getText());
        String_expr_with_string_partContext exprWithStringPartContext = stringContext.string_expr_with_string_part(0);
        Assertions.assertEquals(" some string part after", exprWithStringPartContext.string_part().getText());
        ExprContext exprTree = exprWithStringPartContext.string_expr_part().expr();
        Assertions.assertEquals("ident+ident", exprTree.getText());
        Expr_infixContext exprContext = exprTree.expr_infix();
        Infix1Context infix1Context = (Infix1Context) exprContext.getChild(0);
        Infix2Context infix2Context = (Infix2Context) infix1Context.getChild(0);
        Infix3Context infix3Context = (Infix3Context) infix2Context.getChild(0);
        AddContext addContext = (AddContext) infix3Context.getChild(0);
        Assertions.assertEquals("ident", addContext.expr_infix3().getText());
        Assertions.assertEquals("ident", addContext.expr_infix4().getText());

    }

    @Test
    public void testSquoteStringInterpolationInfiniteRecursion() {
        String interpolation = "'some string part ~{ident + 'hello ${ident}' + ident} some string part after'";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);


        StringContext stringContext = parser.string();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(stringContext);
        Assertions.assertEquals("some string part ", stringContext.string_part().getText());
        String_expr_with_string_partContext exprWithStringPartContext = stringContext.string_expr_with_string_part(0);
        Assertions.assertEquals(" some string part after", exprWithStringPartContext.string_part().getText());
        ExprContext exprTree = exprWithStringPartContext.string_expr_part().expr();
        Assertions.assertEquals("ident+'hello ${ident}'+ident", exprTree.getText());
        Expr_infixContext exprContext = exprTree.expr_infix();
        Infix1Context infix1Context = (Infix1Context) exprContext.getChild(0);
        Infix2Context infix2Context = (Infix2Context) infix1Context.getChild(0);
        Infix3Context infix3Context = (Infix3Context) infix2Context.getChild(0);
        AddContext addContext = (AddContext) infix3Context.getChild(0);
        Assertions.assertEquals("ident+'hello ${ident}'", addContext.expr_infix3().getText());
        Assertions.assertEquals("ident", addContext.expr_infix4().getText());
        Infix5Context infix5Context = (Infix5Context) addContext.expr_infix3().getChild(2);

        ParseTree tree = infix5Context.getChild(0).getChild(0);
        Assertions.assertEquals(tree.getClass(), PrimitivesContext.class);
        tree = tree.getChild(0);
        Assertions.assertEquals(tree.getClass(), Primitive_literalContext.class);
        tree = tree.getChild(0);
        Assertions.assertEquals(tree.getClass(), StringContext.class);
        StringContext innerStringContext = (StringContext) tree;
        String_partContext innersquoteStringContext = innerStringContext.string_part();
        Assertions.assertNotNull(innersquoteStringContext);
        Assertions.assertEquals("hello ", innersquoteStringContext.getText());
        ParseTree innerExprTree = innerStringContext.string_expr_with_string_part(0).string_expr_part().expr();
        Assertions.assertEquals(exprTree.getClass().getName(), ExprContext.class.getName());
        Assertions.assertEquals("ident", innerExprTree.getText());

    }

    @Test
    public void testCommandStringInterpolation() {
        String interpolation = "command { some string part\necho ~{ident + ident}\nsome string part after }";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);

        Task_commandContext commandContext = parser.task_command();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(commandContext);
        Assertions.assertEquals(" some string part\necho ", commandContext.task_command_string_part().getText());
        List<Task_command_expr_with_stringContext> exprWithStringContexts = commandContext.task_command_expr_with_string();
        Assertions.assertEquals(exprWithStringContexts.size(), 1);
        Task_command_expr_with_stringContext exprWithStringContext = exprWithStringContexts.get(0);
        Assertions.assertEquals("\nsome string part after ",
                                exprWithStringContext.task_command_string_part().getText());
        ExprContext exprTree = exprWithStringContext.task_command_expr_part().expr();
        Assertions.assertEquals("ident+ident", exprTree.getText());
        Expr_infixContext exprContext = (exprTree).expr_infix();
        Infix1Context infix1Context = (Infix1Context) exprContext.getChild(0);
        Infix2Context infix2Context = (Infix2Context) infix1Context.getChild(0);
        Infix3Context infix3Context = (Infix3Context) infix2Context.getChild(0);
        AddContext addContext = (AddContext) infix3Context.getChild(0);
        Assertions.assertEquals("ident", addContext.expr_infix3().getText());
        Assertions.assertEquals("ident", addContext.expr_infix4().getText());

    }

    @Test
    public void testHeredocCommandInterpolation() {
        String interpolation = "command <<< some string part\necho ~{ident + ident}\nsome string part after >>>";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);

        Task_commandContext commandContext = parser.task_command();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(commandContext);
        Assertions.assertEquals(" some string part\necho ", commandContext.task_command_string_part().getText());
        List<Task_command_expr_with_stringContext> exprWithStringContexts = commandContext.task_command_expr_with_string();
        Assertions.assertEquals(exprWithStringContexts.size(), 1);
        Task_command_expr_with_stringContext exprWithStringContext = exprWithStringContexts.get(0);
        Assertions.assertEquals("\nsome string part after ",
                                exprWithStringContext.task_command_string_part().getText());
        ExprContext exprTree = exprWithStringContext.task_command_expr_part().expr();
        Assertions.assertEquals("ident+ident", exprTree.getText());
        Expr_infixContext exprContext = (exprTree).expr_infix();
        Infix1Context infix1Context = (Infix1Context) exprContext.getChild(0);
        Infix2Context infix2Context = (Infix2Context) infix1Context.getChild(0);
        Infix3Context infix3Context = (Infix3Context) infix2Context.getChild(0);
        AddContext addContext = (AddContext) infix3Context.getChild(0);
        Assertions.assertEquals("ident", addContext.expr_infix3().getText());
        Assertions.assertEquals("ident", addContext.expr_infix4().getText());

    }

    @Test
    public void testHeredocCommandInterpolation_OnlyRecognizesTilde() {
        String interpolation = "command <<< ${somevar} ~{ident + ident} >>>";
        WdlParser parser = getParser(interpolation);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);

        Task_commandContext commandContext = parser.task_command();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(commandContext);
        Assertions.assertEquals(" ${somevar} ", commandContext.task_command_string_part().getText());
        ExprContext exprTree = commandContext.task_command_expr_with_string(0).task_command_expr_part().expr();
        Assertions.assertEquals("ident+ident",exprTree.getText());
    }

    @Test
    public void testVersionString() {
        String version = "version 1.0";
        WdlParser parser = getParser(version);

        DocumentContext documentContext = parser.document();
        Assertions.assertNotNull(documentContext);
        VersionContext versionContext = documentContext.version();
        Assertions.assertNotNull(versionContext);
        Assertions.assertEquals(versionContext.RELEASE_VERSION().getSymbol().getText(), "1.0");
    }


    @Test
    public void testImportStatementWithAlias() {
        String importString = "import \"some-url.com/foo.wdl\" as Foo \n alias Bar as Biz alias Baz as Boz";
        WdlParser parser = getParser(importString);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(errorListener);
        Import_docContext importDocContext = parser.import_doc();
        Assertions.assertFalse(errorListener.hasErrors());

        Assertions.assertNotNull(importDocContext.IMPORT());
        Assertions.assertNotNull(importDocContext.string());
        Assertions.assertEquals("some-url.com/foo.wdl",
                                importDocContext.string().string_part().getText());
        Assertions.assertNotNull(importDocContext.AS());
        Assertions.assertNotNull(importDocContext.Identifier());
        Assertions.assertNotNull(importDocContext.import_alias());
        Assertions.assertEquals(2, importDocContext.import_alias().size());
        Assertions.assertEquals("Bar", importDocContext.import_alias().get(0).Identifier(0).getSymbol().getText());
        Assertions.assertEquals("Biz", importDocContext.import_alias().get(0).Identifier(1).getSymbol().getText());
        Assertions.assertEquals("Foo", importDocContext.Identifier().getSymbol().getText());
    }


    @Test
    public void testExpressionPlaceHolder() {
        String document = "version 1.0\n" + "\n" + "task foo {\n" + "  input {\n" + "    Int min_std_max_min\n" + "    String prefix\n" + "  }\n" + "  command {\n" + "    echo ${prefix}\n" + "    echo ${sep=',' min_std_max_min}\n" + "  }\n" + "}";
        WdlParser parser = getParser(document);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(ConsoleErrorListener.INSTANCE);
        parser.addErrorListener(errorListener);
        DocumentContext documentContext = parser.document();
        Assertions.assertFalse(errorListener.hasErrors());
    }

    @Test
    public void testDocumentHasAppropriateChildren() {

        String document = "version 1.0" + "\nstruct foo {" + " File f" + "}" + "\ntask bar {" + " input { foo inp } command <<< echo ~{inp.f} >>>" + "}" + "\nworkflow biz {" + " input { foo inp } " + "\n call bar as boz { input: inp = inp }" + "\n}";

        WdlParser parser = getParser(document);
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        parser.addErrorListener(ConsoleErrorListener.INSTANCE);
        parser.addErrorListener(errorListener);
        DocumentContext documentContext = parser.document();
        Assertions.assertFalse(errorListener.hasErrors());
        Assertions.assertNotNull(documentContext.version());
        Assertions.assertEquals(2, documentContext.document_element().size());
        List<Document_elementContext> elementContexts = documentContext.document_element();
        Assertions.assertEquals(StructContext.class.getName(), elementContexts.get(0).getChild(0).getClass().getName());
        Assertions.assertEquals(TaskContext.class.getName(), elementContexts.get(1).getChild(0).getClass().getName());
        Assertions.assertEquals(WorkflowContext.class.getName(),
                                documentContext.workflow().getClass().getName());

    }

    private WdlParser getParser(String inp) {
        CodePointBuffer codePointBuffer = CodePointBuffer.withBytes(ByteBuffer.wrap(inp.getBytes()));
        WdlLexer lexer = new WdlLexer(CodePointCharStream.fromBuffer(codePointBuffer));
        WdlParser parser = new WdlParser(new CommonTokenStream(lexer));
        parser.removeErrorListeners();
        return parser;
    }

}
