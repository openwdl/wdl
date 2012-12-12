package org.broadinstitute.compositetask;

import org.testng.annotations.Test;
import org.testng.annotations.DataProvider;
import org.testng.Assert;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;
import java.util.ArrayList;

import org.broadinstitute.parser.SyntaxError;
import org.broadinstitute.parser.Utility;

import org.broadinstitute.compositetask.CompositeTask;

public class SyntaxErrorTest
{
    @DataProvider(name="syntaxErrorTests")
    public Object[][] parsingTests() {
        File parsingTestDir = new File("test-files", "syntax-error");
        Collection<Object[]> composite_tasks = new ArrayList<Object[]>();

        for ( String subDir : parsingTestDir.list() ) {
            composite_tasks.add(new Object[] { new File(parsingTestDir, subDir) });
        }

        return composite_tasks.toArray(new Object[0][]);
    }

    private CompositeTask getCompositeTask(File source) throws SyntaxError {
        try {
            return new CompositeTask(source);
        } catch(IOException error) {
            Assert.fail("IOException reading file: " + error);
        }

        return null;
    }

    @Test(dataProvider="syntaxErrorTests")
    public void testCompositeTaskReportsBackCorrectSyntaxErrors(File dir) {
        File errors = new File(dir, "errors");
        File source = new File(dir, "source.wdl");
        String actual = null;

        try {
            CompositeTask ctask = getCompositeTask(source);
        } catch (SyntaxError syntax_error) {
            actual = syntax_error.toString();
        }

        if ( !errors.exists() ) {
            try {
                FileWriter out = new FileWriter(errors);
                out.write(actual);
                out.close();
            } catch (IOException error) {
                Assert.fail("Could not write errors file: " + error);
            }

            System.out.println("Created " + errors);
        }

        try {
            String expected = Utility.readFile(errors.getAbsolutePath());
            Assert.assertEquals(actual, expected, "Syntax errors did not match");
        } catch (IOException error) {
            Assert.fail("Cannot read " + errors.getAbsolutePath());
        }
    }
}
