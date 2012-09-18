import org.testng.annotations.Test;
import static org.testng.AssertJUnit.*;
import org.broadinstitute.compositetask.CompositeTask;

public class MyTest
{
  @Test 
  public void testTrivial()
  {
    assertEquals(3, 3);
    assertEquals(0, 0);
    assertEquals(4, 4);
  }
}
