package org.broadinstitute.compositetask;

import org.testng.annotations.Test;
import org.testng.annotations.DataProvider;
import org.testng.Assert;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;
import java.util.ArrayList;

import org.broadinstitute.compositetask.CompositeTask;
import org.broadinstitute.compositetask.SyntaxError;

public class CompositeTaskTest 
{
    @DataProvider(name="parsingTests")
    public Object[][] parsingTests() {
        File parsingTestDir = new File(System.getProperty("test.files"), "parsing");
        Collection<Object[]> composite_tasks = new ArrayList<Object[]>();

        for ( String subDir : parsingTestDir.list() ) {
            composite_tasks.add(new Object[] { new File(parsingTestDir, subDir) });
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
        if ( !tokens.exists() ) {
            /*
            SourceCode code = new CompositeTaskSourceCode(new File(args[0]));
            Lexer lexer = new Lexer();
            List<Terminal> terminals = lexer.getTokens(code);
            System.out.println("[");
            System.out.println(Utility.join(terminals, ",\n"));
            System.out.println("]");
            */

            System.out.println("Created " + tokens);
        }
    }

    @Test(dataProvider="parsingTests")
    public void testParseTree(File dir) {
        File source = new File(dir, "source.wdl");
        File parsetree = new File(dir, "parsetree");
        CompositeTask ctask = getCompositeTask(source);

        if ( ctask == null ) {
            Assert.fail("Null Composite Task");
        }

        if ( !parsetree.exists() ) {
            try {
                FileWriter out = new FileWriter(parsetree);
                out.write(ctask.getParseTree().toPrettyString());
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + parsetree + ": " + error);
            }

            System.out.println("Created " + parsetree);
        }
    }

    @Test(dataProvider="parsingTests")
    public void testAbstractSyntaxTree(File dir) {
        File source = new File(dir, "source.wdl");
        File ast = new File(dir, "ast");
        CompositeTask ctask = getCompositeTask(source);

        if ( !ast.exists() ) {
            try {
                FileWriter out = new FileWriter(ast);
                out.write(ctask.getAst().toPrettyString());
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write " + ast + ": " + error);
            }

            System.out.println("Created " + ast);
        }
    }

    @Test
    public void testTrivial() {
        Assert.assertEquals(1, 1);
    }
}
