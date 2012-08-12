import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

class CompositeTask {

  private ParseTree parse_tree;
  private Ast ast;
  private WdlSyntaxErrorFormatter error_formatter;

  private class CompositeTaskAstVerifier {
    private WdlSyntaxErrorFormatter syntaxErrorFormatter;

    CompositeTaskAstVerifier(WdlSyntaxErrorFormatter syntaxErrorFormatter) {
      this.syntaxErrorFormatter = syntaxErrorFormatter;
    }

    public Ast verify(AstNode wdl_ast) throws SyntaxError {
      if ( !(wdl_ast instanceof AstList) ) {
        throw new SyntaxError("Ast is not a list");
      }

      if ( ((AstList) wdl_ast).size() != 1 ) {
        throw new SyntaxError("Composite Task definition should contain only one top level composite_task definition.");
      }

      Ast composite_task = (Ast) ((AstList) wdl_ast).get(0);

      /* a)  Error on two 'input' or 'output' in a Step
       * b)  Step names are unique in their scope (global or for)
       * c)  No version specified for task
       * d)  Two outputs have the same name
       */

      AstList steps = (AstList) composite_task.getAttribute("body");
      for ( AstNode step : steps ) {
        Ast step_ast = (Ast) step;
        Ast task = (Ast) step_ast.getAttribute("task");
        AstList task_attrs = (AstList) task.getAttribute("attributes");

        boolean version_found = false;

        for ( AstNode task_attr : task_attrs ) {
          Terminal key = (Terminal) ((Ast) task_attr).getAttribute("key");
          if ( key.getSourceString().equals("version") ) {
            version_found = true;
          }
        }

        if ( version_found == false ) {
          Terminal task_name = getTaskName(step_ast);
          throw new SyntaxError(this.syntaxErrorFormatter.missing_version(task_name));
        }
      }

      return composite_task;
    }

    private Terminal getTaskName(Ast step) {
      return (Terminal) ((Ast)step.getAttribute("task")).getAttribute("name");
    }
  }

  /** Constructors **/

  CompositeTask(SourceCode source_code) throws SyntaxError {
    this.error_formatter = new WdlSyntaxErrorFormatter();
    this.error_formatter.setSourceCode(source_code);
    ParseTreeNode node = getParseTree(source_code);
    this.parse_tree = (ParseTree) node;
    AstList ast_list = (AstList) node.toAst();
    CompositeTaskAstVerifier verifier = new CompositeTaskAstVerifier(this.error_formatter);
    this.ast = verifier.verify(ast_list);
  }

  CompositeTask(File source_code) throws SyntaxError, IOException {
    this(new WdlSourceCode(source_code));
  }

  CompositeTask(String source_code, String resource) throws SyntaxError {
    this(new WdlSourceCode(source_code, resource));
  }

  /** Public Methods **/

  public ParseTree getParseTree() {
    return this.parse_tree;
  }

  public Ast getAst() {
    return this.ast;
  }

  public Map<String, Ast> getSteps() {
    Map<String, Ast> map = new HashMap<String, Ast>();
    AstList steps = (AstList) this.ast.getAttribute("body");
    for ( AstNode step : steps ) {
      Ast step_ast = (Ast) step;
      if ( step_ast.getName().equals("Step") ) {
        map.put(getStepName(step_ast), step_ast);
      }
    }
    return map;
  }

  /** Private methods **/
  private String getStepName(Ast step) {
    Terminal name = (Terminal) step.getAttribute("name");
    Terminal task_name = (Terminal) ((Ast)step.getAttribute("task")).getAttribute("name");
    return (name != null) ? name.getSourceString() : task_name.getSourceString();
  }

  private ParseTreeNode getParseTree(SourceCode source_code) throws SyntaxError {
    WdlParser parser = new WdlParser(this.error_formatter);
    Lexer lexer = new Lexer();
    List<Terminal> terminals = lexer.getTokens(source_code);
    TokenStream tokens = new TokenStream(terminals);
    return parser.parse(tokens);
  }
}
