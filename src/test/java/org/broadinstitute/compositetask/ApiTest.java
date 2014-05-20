package org.broadinstitute.compositetask;

import org.testng.annotations.Test;
import org.testng.annotations.BeforeMethod;
import org.testng.Assert;

import java.io.File;
import java.io.IOException;
import java.util.Set;

import org.broadinstitute.parser.SyntaxError;

import org.broadinstitute.compositetask.CompositeTask;

public class ApiTest
{
    private CompositeTask task;

    @BeforeMethod
    private void createCompositeTaskObject() {
        try {
            File source = new File("test-files/api/0.wdl");
            String relative = new File(".").toURI().relativize(source.toURI()).getPath();
            this.task = new CompositeTask(source, relative);
        } catch(IOException error) {
            Assert.fail("IOException reading file: " + error);
        } catch(SyntaxError error) {
            Assert.fail("Not expecting syntax error: " + error);
        }
    }

    @Test
    public void testGetNodesMethodReturnsTheRightNumberOfNodes() {
        Assert.assertEquals(this.task.getNodes().size(), 2, "Expecting 2 nodes, found " + this.task.getNodes().size());
    }

    @Test
    public void testGetStepMethodReturnsTheCorrectTopLevelStep() {
        CompositeTaskStep step = this.task.getStep("atask");
        Assert.assertNotNull(step, "Expected one step with name 'atask'");
        Assert.assertEquals(step.getName(), "atask", "Expecting one step with name 'atask'");
        Assert.assertEquals(step.getParent(), this.task, "Expecting the parent of 'atask' step to be the composite task");
    }

    @Test
    public void testTopLevelStepHasCorrectOutputMappingsToVariableX() {
        CompositeTaskStep step = this.task.getStep("atask");
        boolean found = false;
        for ( CompositeTaskStepOutput output : step.getOutputs() ) {
            if ( output.getVariable().getName().equals("x") ) {
                found = true;
                Assert.assertEquals(output.getType(), "File", "Expected the variable 'x' to be a File mapping");
                Assert.assertEquals(output.getMethod(), "assign", "Expected the mapping method to be 'assign'");
                Assert.assertEquals(output.getPath(), "foo.txt", "Expected the output file path to be 'foo.txt'");
            }
        }
        if ( !found ) Assert.fail("Expected to find one output to 'atask' to variable 'x'");
    }

    @Test
    public void testTopLevelStepHasCorrectOutputMappingsToVariableY() {
        CompositeTaskStep step = this.task.getStep("atask");
        boolean found = false;
        for ( CompositeTaskStepOutput output : step.getOutputs() ) {
            if ( output.getVariable().getName().equals("y") ) {
                found = true;
                Assert.assertEquals(output.getType(), "FirstLine", "Expected the variable 'y' to be a File mapping");
                Assert.assertEquals(output.getMethod(), "assign", "Expected the mapping method to be 'assign'");
                Assert.assertEquals(output.getPath(), "bar.txt", "Expected the output file path to be 'bar.txt'");
            }
        }
        if ( !found ) Assert.fail("Expected to find one output to 'atask' to variable 'y'");
    }

    @Test
    public void testSingleTopLevelForLoopExistsWithSubTask() {
        Set<CompositeTaskNode> nodes = this.task.getNodes();
        CompositeTaskStep innerStep = this.task.getStep("btask");
        Assert.assertNotNull(innerStep, "Expected a step with name 'btask' to exist");
        CompositeTaskForLoop loop = (CompositeTaskForLoop) innerStep.getParent();
        Assert.assertEquals(loop.getParent(), this.task, "Expected the loop's parent node to be the composite task");
        Assert.assertEquals(loop.getCollection().getName(), "foobar", "Expecting one loop with a collection called 'foobar'");
        Assert.assertEquals(loop.getVariable().getName(), "item", "Expecting one loop with a variable called 'item'");
    }

    @Test
    public void testReplaceTaskInWdlWithNewTaskVersion() throws SyntaxError {
      Assert.assertNotNull(this.task.getStep("atask"));
      Assert.assertNull(this.task.getStep("atask_replace"));
      this.task.replace("atask", null, "atask_replace", "100");
      Assert.assertNull(this.task.getStep("atask"));
      Assert.assertNotNull(this.task.getStep("atask_replace"));
    }

    @Test
    public void testReplaceTaskWithSpecificVersionInWdlWithNewTaskVersion() throws SyntaxError {
      Assert.assertNotNull(this.task.getStep("atask"));
      Assert.assertNull(this.task.getStep("atask_replace"));
      this.task.replace("atask", "0", "atask_replace", "100");
      Assert.assertNull(this.task.getStep("atask"));
      Assert.assertNotNull(this.task.getStep("atask_replace"));
    }

    @Test
    public void testReplaceTaskInWdlWithNewTaskVersionFailsIfTaskDoesntExist() throws SyntaxError {
      Assert.assertNotNull(this.task.getStep("atask"));
      Assert.assertNull(this.task.getStep("atask_replace"));
      this.task.replace("XYZ_atask", null, "atask_replace", "100");
      Assert.assertNotNull(this.task.getStep("atask"));
      Assert.assertNull(this.task.getStep("atask_replace"));
    }
}
