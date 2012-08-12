import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

class WdlMain {
  public static void main(String[] args) {

    try {
      CompositeTask wdl = new CompositeTask(new File(args[0]));
      Ast ast = wdl.getAst();
      Map<String, Ast> steps = wdl.getSteps();
      for ( Map.Entry<String, Ast> entry : steps.entrySet() ) {
        System.out.println("--- Step " + entry.getKey());
      }
    } catch (IOException error) {
      System.err.println(error);
      System.exit(-1);
    } catch (SyntaxError error) {
      System.err.println(error);
      System.exit(-1);
    }
  }
}
