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

    @Test(dataProvider="parsingTests")
    public void testLexicalAnalysis(File dir) {
        File tokens = new File(dir, "tokens");
        if ( !tokens.exists() ) {
            System.out.println("Created " + tokens);
        }
    }

    @Test(dataProvider="parsingTests")
    public void testParseTree(File dir) {
        File source = new File(dir, "source.wdl");
        File parsetree = new File(dir, "parsetree");
        CompositeTask ctask = null;

        try {
            ctask = new CompositeTask(source);
        } catch(SyntaxError error) {
            Assert.fail("Not expecting syntax error: " + error);
        } catch(IOException error) {
            Assert.fail("IOException reading file: " + error);
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
        File ast = new File(dir, "ast");
        if ( !ast.exists() ) {
            System.out.println("Created " + ast);
        }
    }

    @Test
    public void testTrivial() {
        Assert.assertEquals(1, 1);
    }
}
