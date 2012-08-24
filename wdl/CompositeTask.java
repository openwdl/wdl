import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Iterator;
import org.jgrapht.DirectedGraph;

class CompositeTask implements CompositeTaskScope {

  private ParseTree parse_tree;
  private Ast ast;
  private WdlSyntaxErrorFormatter error_formatter;
  private Set<CompositeTaskNode> nodes;
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
      CompositeTask.this.nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode ctNode : ctNodes ) {
        Ast node = (Ast) ctNode;
        CompositeTask.this.nodes.add(verify(node));
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
       *    variable -> scope (for) : Variable is the loop collection
       *    variable -> step        : Step needs variable as an input
       *    step -> variable        : Variable is an output of step
       *    variable -> variable    : Doesn't exist.
       *    scope -> scope          : Doesn't exist.
       *    step -> scope           : Doesn't exist.
       *    step -> step            : Doesn't exist.
       *
       */

      return composite_task;
    }

    private CompositeTaskVariable make_variable(String name, String member) {

    }

    private CompositeTaskVariable ast_to_variable(Ast ast) {
      Terminal name = (Terminal) ast.getAttribute("name");
      Terminal member = (Terminal) ast.getAttribute("member");
      return new CompositeTaskVariable(name.getSourceString(), (member == null) ? null : member.getSourceString());
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

      CompositeTaskSubTask subtask = new CompositeTaskSubTask(
        task_name.getSourceString(),
        task_version.getSourceString()
      );

      String name;
      if ( step.getAttribute("name") != null ) {
        name = ((Terminal) step.getAttribute("name")).getSourceString();
      } else {
        name = task_name.getSourceString();
      }

      Set<CompositeTaskStepInput> inputs = new HashSet<CompositeTaskStepInput>();
      Set<CompositeTaskStepOutput> outputs = new HashSet<CompositeTaskStepOutput>();

      AstList body = (AstList) step.getAttribute("body");

      if ( body != null ) {
        for ( AstNode entry : body ) {
          Ast entry_ast = (Ast) entry;

          if ( entry_ast.getName().equals("StepInputList") ) {
            AstList input_list = (AstList) entry_ast.getAttribute("inputs");
            for ( AstNode input_node : input_list ) {
              Ast input = (Ast) input_node;
              Terminal parameter = (Terminal) input.getAttribute("parameter");
              CompositeTaskVariable variable = ast_to_variable((Ast) input.getAttribute("value"));
              inputs.add( new CompositeTaskStepInput(parameter.getSourceString(), variable) );
            }
          }

          if ( entry_ast.getName().equals("StepOutputList") ) {
            AstList output_list = (AstList) entry_ast.getAttribute("outputs");
            for ( AstNode output_node : output_list ) {
              Ast output = (Ast) output_node;
              Terminal filepath = (Terminal) output.getAttribute("file");
              CompositeTaskVariable variable = ast_to_variable((Ast) output.getAttribute("as"));
              outputs.add( new CompositeTaskStepOutput("File", filepath.getSourceString(), variable) );
            }
          }
        }
      }

      return new CompositeTaskStep(name, subtask, inputs, outputs);
    }

    private CompositeTaskForLoop verify_for(Ast for_node_ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode for_sub_node : (AstList) for_node_ast.getAttribute("body") ) {
        nodes.add( verify((Ast) for_sub_node) );
      }

      String collection = ((Terminal) for_node_ast.getAttribute("collection")).getSourceString();
      String item = ((Terminal) for_node_ast.getAttribute("item")).getSourceString();

      return new CompositeTaskForLoop(new CompositeTaskVariable(collection), new CompositeTaskVariable(item), nodes);
    }

    private CompositeTask verify_composite_task(Ast ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();
      Terminal ctName = (Terminal) ast.getAttribute("name");

      for ( AstNode sub : (AstList) ast.getAttribute("body") ) {
        nodes.add( verify((Ast) sub) );
      }

      return new CompositeTask(ctName.getSourceString(), nodes);
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
    this.nodes = nodes;
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

  public CompositeTaskGraph getGraph() {
    return new CompositeTaskGraph();
  }

  public CompositeTaskStep getStep(String name) {
    return null;
  }

  public Set<CompositeTaskSubTask> getTasks() {
    return null;
  }

  private Set<CompositeTaskSubTask> getTasks(CompositeTaskScope scope) {
    return null;
  }

  public Ast getAst() {
    return this.ast;
  }

  public void setName(String name) {
    this.name = name;
  }

  public void addNode(CompositeTaskNode node) {
  }

  public String toString() {
    return "[CompositeTask name="+this.name+"]";
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
