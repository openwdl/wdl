package org.broadinstitute.compositetask;

import org.testng.annotations.Test;
import org.testng.annotations.DataProvider;
import org.testng.Assert;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;
import java.util.ArrayList;
import java.util.List;

import org.broadinstitute.parser.SyntaxError;
import org.broadinstitute.parser.SourceCode;
import org.broadinstitute.parser.Terminal;
import org.broadinstitute.parser.Utility;

import org.broadinstitute.compositetask.CompositeTask;
import org.broadinstitute.compositetask.CompositeTaskSourceCode;
import org.broadinstitute.compositetask.Lexer;

public class ParsingTest 
{
    @DataProvider(name="parsingTests")
    public Object[][] parsingTests() {
        File parsingTestDir = new File("test-files", "parsing");
        Collection<Object[]> composite_tasks = new ArrayList<Object[]>();

        for ( String subDir : parsingTestDir.list() ) {
            File testDir = new File(parsingTestDir, subDir);
            File skipFile = new File(testDir, "skip");
            if ( ! skipFile.exists() ) {
              composite_tasks.add(new Object[] { testDir });
            }
        }

        return composite_tasks.toArray(new Object[0][]);
    }

    private CompositeTask getCompositeTask(File source) {
        try {
            return new CompositeTask(source);
        } catch(IOException error) {
            Assert.fail("IOException reading file: " + error);
        } catch(SyntaxError error) {
            Assert.fail("Not expecting syntax error: " + error);
        }

        return null;
    }

    @Test(dataProvider="parsingTests")
    public void testLexicalAnalysis(File dir) {
        File tokens = new File(dir, "tokens");
        File source = new File(dir, "source.wdl");
        String actual = null;
  
        try {
            SourceCode code = new CompositeTaskSourceCode(source);
            Lexer lexer = new Lexer();
            List<Terminal> terminals = lexer.getTokens(code);
            actual = "[\n  " + Utility.join(terminals, ",\n  ") + "\n]\n";
        } catch (IOException error) {
            Assert.fail("Could not read source code: " + error);
        }

        if ( !tokens.exists() ) {
            try {
                FileWriter out = new FileWriter(tokens);
                out.write(actual);
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write tokens file: " + error);
            }

            System.out.println("Created " + tokens);
        }

        try {
            String expected = Utility.readFile(tokens.getAbsolutePath());
            Assert.assertEquals(actual, expected, "Tokens list did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + tokens.getAbsolutePath());
        }
    }

    @Test(dataProvider="parsingTests")
    public void testParseTreeIsGeneratedFromSourceCodeCorrectly(File dir) {
        File source = new File(dir, "source.wdl");
        File parsetree = new File(dir, "parsetree");
        CompositeTask ctask = getCompositeTask(source);
        String actual = ctask.getParseTree().toPrettyString();

        if ( ctask == null ) {
            Assert.fail("Null Composite Task");
        }

        if ( !parsetree.exists() ) {
            try {
                FileWriter out = new FileWriter(parsetree);
                out.write(actual);
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + parsetree + ": " + error);
            }

            System.out.println("Created " + parsetree);
        }

        try {
            String expected = Utility.readFile(parsetree.getAbsolutePath());
            Assert.assertEquals(actual, expected, "Parse trees did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + parsetree.getAbsolutePath());
        }
    }

    @Test(dataProvider="parsingTests")
    public void testAbstractSyntaxTreeIsGeneratedFromSourceCodeCorrectly(File dir) {
        File source = new File(dir, "source.wdl");
        File ast = new File(dir, "ast");
        CompositeTask ctask = getCompositeTask(source);
        String actual = ctask.getAst().toPrettyString();

        if ( !ast.exists() ) {
            try {
                FileWriter out = new FileWriter(ast);
                out.write(actual);
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + ast + ": " + error);
            }

            System.out.println("Created " + ast);
        }

        try {
            String expected = Utility.readFile(ast.getAbsolutePath());
            Assert.assertEquals(actual, expected, "Abstract syntax trees did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + ast.getAbsolutePath());
        }
    }

    @Test(dataProvider="parsingTests")
    public void testSourceFormatterOutputsCorrectlyFormattedSourceCode(File dir) {
        File source = new File(dir, "source.wdl");
        File formatted_file = new File(dir, "formatted");
        CompositeTask ctask = getCompositeTask(source);
        CompositeTaskSourceCodeFormatter formatter = new CompositeTaskSourceCodeFormatter();
        String actual = formatter.format(ctask);

        if ( !formatted_file.exists() ) {
            try {
                FileWriter out = new FileWriter(formatted_file);
                out.write(actual);
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + formatted_file + ": " + error);
            }

            System.out.println("Created " + formatted_file);
        }

        try {
            String expected = Utility.readFile(formatted_file.getAbsolutePath());
            Assert.assertEquals(actual, expected, "Formatted source code files did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + formatted_file.getAbsolutePath());
        }
    }

    public static <T extends Comparable<? super T>> List<T> asSortedList(Collection<T> c) {
        List<T> list = new ArrayList<T>(c);
        java.util.Collections.sort(list);
        return list;
    }

    @Test(dataProvider="parsingTests")
    public void testCompositeTaskGeneratesCorrectGraph(File dir) {
        File source = new File(dir, "source.wdl");
        File graph_file = new File(dir, "graph");
        CompositeTask ctask = getCompositeTask(source);
        CompositeTaskGraph graph = ctask.getGraph();

        StringBuilder actual = new StringBuilder();
        actual.append("VERTICIES\n");
        actual.append("---------\n");
        for ( CompositeTaskVertex v : asSortedList(graph.vertexSet()) ) {
          actual.append(v + "\n");
        }
        actual.append("\n");

        actual.append("EDGES\n");
        actual.append("-----\n");
        for ( CompositeTaskEdge v : asSortedList(graph.edgeSet()) ) {
          actual.append(v + "\n");
        }

        if ( !graph_file.exists() ) {
            try {
                FileWriter out = new FileWriter(graph_file);
                out.write(actual.toString());
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + graph_file + ": " + error);
            }

            System.out.println("Created " + graph_file);
        }

        try {
            String expected = Utility.readFile(graph_file.getAbsolutePath());
            Assert.assertEquals(actual.toString(), expected, "Graphs did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + graph_file.getAbsolutePath());
        }
    }
}
