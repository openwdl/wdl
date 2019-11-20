package org.openwdl.wdl.parser;


import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;
import org.antlr.v4.runtime.CodePointBuffer;
import org.antlr.v4.runtime.CodePointCharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.TokenSource;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.openwdl.wdl.parser.WdlParserTestErrorListener.SyntaxError;

public class WDLParserTest {

    private static String examplesDirectory;

    private static Pattern expectedErrorPattern = Pattern
        .compile("#EXPECTED_ERROR\\s+line:(?<linenum>[0-9]+)\\s+(?<msg>msg:(\\\"[^\\n\\r]+\\\"|'[^\\n\\r]))?.*");


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

    @ParameterizedTest
    @MethodSource("successfullWdlFiles")
    public void testWdlFiles_shouldParseSuccessFully(byte[] fileBytes, String fileName) {
        System.out.println("Testing WDL File: " + fileName + " should Successfully parse");
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        CodePointBuffer codePointBuffer = CodePointBuffer.withBytes(ByteBuffer.wrap(fileBytes));
        TokenSource tokenSource = new WdlLexer(CodePointCharStream.fromBuffer(codePointBuffer));
        WdlParser parser = new WdlParser(new CommonTokenStream(tokenSource));
        parser.removeErrorListeners();
        parser.addErrorListener(errorListener);
        parser.document();

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
    public void testWdlFiles_shouldFailParings(byte[] fileBytes, String fileName) {
        System.out.println("Testing WDL File: " + fileName + " should fail to parse");
        WdlParserTestErrorListener errorListener = new WdlParserTestErrorListener();
        CodePointBuffer codePointBuffer = CodePointBuffer.withBytes(ByteBuffer.wrap(fileBytes));
        CommentAggregatingTokenSource tokenSource = new CommentAggregatingTokenSource(CodePointCharStream
            .fromBuffer(codePointBuffer));
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


}
