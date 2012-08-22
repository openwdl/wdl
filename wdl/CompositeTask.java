import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Iterator;

class CompositeTask implements CompositeTaskScope {

  private ParseTree parse_tree;
  private Ast ast;
  private WdlSyntaxErrorFormatter error_formatter;
  private Set<String> inputs;
  private String name;

  private class CompositeTaskAstVerifier {
    private WdlSyntaxErrorFormatter syntaxErrorFormatter;

    CompositeTaskAstVerifier(WdlSyntaxErrorFormatter syntaxErrorFormatter) {
      this.syntaxErrorFormatter = syntaxErrorFormatter;
    }

    public Ast verify(AstNode wdl_ast) throws SyntaxError {
      Ast composite_task = null;

      if ( wdl_ast instanceof AstList ) {
        if ( ((AstList) wdl_ast).size() != 1 ) {
          throw new SyntaxError("Composite Task definition should contain only one top level composite_task definition.");
        }

        composite_task = (Ast) ((AstList) wdl_ast).get(0);
      } else if (wdl_ast instanceof Ast) {
        composite_task = (Ast) wdl_ast;
        String node_type = composite_task.getName();
        if (!node_type.equals("CompositeTask")) {
          throw new SyntaxError("TODO");
        }
      } else {
        throw new SyntaxError("TODO");
      }

      /* a)  Error on two 'input' or 'output' in a Step
       * b)  Step names are unique in their scope (global or for)
       * c)  No version specified for task
       * d)  Two outputs have the same name
       */

      AstList ctNodes = (AstList) composite_task.getAttribute("body");
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode ctNode : ctNodes ) {
        Ast node = (Ast) ctNode;
        if (node.getName().equals("Step")) {
          nodes.add(new CompositeTaskStep(ast));
        } else if (node.getName().equals("ForLoop")) {
          nodes.add(new CompositeTaskForLoop(ast));
        } else if (node.getName().equals("CompositeTask")) {
          nodes.add(new CompositeTaskStep(ast));
        } else {
          throw new SyntaxError("TODO");
        }
      }

      /* Graph definition:
       * 
       * Verticies:
       *    scope, step, variable
       *
       * Edges:
       *    scope -> step           : Step is dependent on scope completing
       *    scope (for) -> variable : Variable is the loop variable (not collection).
       *                              Each for loop contains exactly one of these edges
       *    scope -> scope          : Doesn't exist.
       *    variable -> scope (for) : Variable is the loop collection
       *    variable -> step        : Step needs variable as an input
       *    variable -> variable    : Doesn't exist.
       *    step -> variable        : Variable is an output of step
       *    step -> scope           : Doesn't exist.
       *    step -> step            : Doesn't exist.
       *
       */

      return composite_task;
    }

    private boolean in_scope(CompositeTaskScope scope, CompositeTaskNode node) {
      boolean answer = false;
      for ( CompositeTaskNode scope_node : scope.getNodes() ) {
        answer |= (node == scope_node);
        if ( scope_node instanceof CompositeTaskScope ) {
          answer |= in_scope((CompositeTaskScope) scope_node, node);
        }
      }
      return answer;
    }

    private String variable_to_string(Ast variable) {
      String name;
      Terminal asName = (Terminal) variable.getAttribute("name");
      Terminal asMember = (Terminal) variable.getAttribute("member");
      name = asName.getSourceString();

      if ( false && asMember != null ) {
        name += "." + asMember.getSourceString();
      }
      return name;
    }

    private CompositeTaskNode verify(Ast ast) throws SyntaxError {
      if ( ast.getName().equals("Step") ) {
        return verify_step(ast);
      } else if ( ast.getName().equals("ForLoop") ) {
        return verify_for(ast);
      } else if ( ast.getName().equals("CompositeTask") ) {
        return verify_composite_task(ast);
      } else {
        throw new SyntaxError("TODO");
      }
    }

    private CompositeTaskStep verify_step(Ast step) throws SyntaxError {
      Ast task = (Ast) step.getAttribute("task");
      Terminal task_name = getTaskName(task);
      Terminal task_version = getTaskVersion(task);

      if ( task_version == null ) {
        throw new SyntaxError(this.syntaxErrorFormatter.missing_version(task_name));
      }

      CompositeTaskSubTask ctSubTask = new CompositeTaskSubTask(
        task_name.getSourceString(),
        task_version.getSourceString()
      );

      String ctStepName;
      if ( step.getAttribute("name") != null ) {
        ctStepName = ((Terminal) step.getAttribute("name")).getSourceString();
      } else {
        ctStepName = task_name.getSourceString();
      }

      return new CompositeTaskStep(ctStepName, ctSubTask);
    }

    private CompositeTaskForLoop verify_for(Ast for_node_ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode for_sub_node : (AstList) for_node_ast.getAttribute("body") ) {
        nodes.add( verify((Ast) for_sub_node) );
      }

      String collection = ((Terminal) for_node_ast.getAttribute("collection")).getSourceString();
      String item = ((Terminal) for_node_ast.getAttribute("item")).getSourceString();

      return new CompositeTaskForLoop(collection, item, nodes);
    }

    private CompositeTask verify_composite_task(Ast ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode sub : (AstList) ast.getAttribute("body") ) {
        nodes.add( verify((Ast) sub) );
      }

      return new CompositeTask(nodes);
    }

    private Terminal getTaskName(Ast task) {
      return (Terminal) task.getAttribute("name");
    }

    private Terminal getTaskVersion(Ast task) {
      AstList task_attrs = (AstList) task.getAttribute("attributes");

      if ( task_attrs != null ) {
        for ( AstNode task_attr : task_attrs ) {
          Terminal key = (Terminal) ((Ast) task_attr).getAttribute("key");
          Terminal value = (Terminal) ((Ast) task_attr).getAttribute("value");
          if ( key.getSourceString().equals("version") ) {
            return value;
          }
        }
      }

      return null;
    }
  }

  /** Constructors **/

  CompositeTask(String name, Set<CompositeTaskNode> nodes) {
    this.name = name;
  }

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

  public String getName() {
    return this.name;
  }

  public Set<CompositeTaskNode> getNodes() {
    return this.nodes;
  }

  public CompositeTaskStep getStep(String name) {
    return null;
  }

  public Set<CompositeTaskSubTask> getTasks() {
    return null;
  }

  private Set<CompositeTaskSubTask> getTasks(CompositeTaskScope scope) {
    return tasks;
  }

  public Ast getAst() {
    return this.ast;
  }

  public void setName(String name) {
    this.name = name;
  }

  public void addNode(CompositeTaskNode node) {
    this.nodes.add(node);
  }

  /** Private methods **/

  private ParseTreeNode getParseTree(SourceCode source_code) throws SyntaxError {
    WdlParser parser = new WdlParser(this.error_formatter);
    Lexer lexer = new Lexer();
    List<Terminal> terminals = lexer.getTokens(source_code);
    TokenStream tokens = new TokenStream(terminals);
    return parser.parse(tokens);
  }
}
