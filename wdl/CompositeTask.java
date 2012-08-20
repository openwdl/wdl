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
  private Set<CompositeTaskNode> nodes;
  private Set<CompositeTaskEdge> edges;
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

      AstList steps = (AstList) composite_task.getAttribute("body");

      for ( AstNode step : steps ) {
        CompositeTask.this.nodes.add( verify((Ast) step) );
      }

      /* outputs: Map of String variable_name -> Set<CompositeTaskOutput> which represents a set of
       * entities that write an output to that variable.  e.g. output: File("foo.txt") as bar would
       * add an entry to outputs at key 'bar'.  No two outputs should write to the same variable.
       *
       * inputs: Map of String variable_name -> Set<CompositeTaskInput> which represents the set of
       * nodes that need variable_name as a prerequisite.  Note that this also includes Scope nodes
       * like 'for' or 'composite_task' nodes.  Also note that get_node_inputs() actually generates
       * scope inputs based on the union of all of the inputs of its sub-nodes, which isn't terribly
       * useful because a lot of those could be satisfied internally.  For example:
       *
       * composite_task test {
       *   step foo[version=0] {
       *     output: File("foo.txt") as bar
       *   }
       *
       *   step baz[version=0] {
       *     input: x=bar, y=var
       *   }
       * }
       *
       * the composite task will have inputs bar and var (on top of the inputs from step foo and baz).
       * However, 'bar' is already satisfied by step foo so the composite task really only needs 'foo'
       */
      Map<String, Set<CompositeTaskOutput>> outputs = get_node_outputs(CompositeTask.this);
      Map<String, Set<CompositeTaskInput>> inputs = get_node_inputs(CompositeTask.this);

      /* Map outputs -> inputs, creating the edges in the graph */
      for ( Map.Entry<String, Set<CompositeTaskOutput>> entry : outputs.entrySet() ) {
        String variable = entry.getKey();
        Set<CompositeTaskOutput> output_set = entry.getValue();
        for ( CompositeTaskOutput output: output_set ) {
          if ( output.getNode() == CompositeTask.this ) {
            continue;
          }
          if ( inputs.get(variable) != null  ) {
            for ( CompositeTaskInput input : inputs.get(variable) ) {
              if ( input.getNode() == CompositeTask.this ) {
                continue;
              }
              if ( input.getNode() == output.getNode() ) {
                continue;
              }
              if ( output.getNode() instanceof CompositeTaskScope &&
                   in_scope((CompositeTaskScope) output.getNode(), input.getNode()) ) {
                continue;
              }
              if ( input.getNode() instanceof CompositeTaskScope &&
                   in_scope((CompositeTaskScope) input.getNode(), output.getNode()) ) {
                continue;
              }
              CompositeTaskEdge edge = new CompositeTaskEdge(output, input, variable);
              CompositeTask.this.edges.add(edge);
            }
          }
        }
      }

      for ( Map.Entry<String, Set<CompositeTaskInput>> entry : inputs.entrySet() ) {
        Set<CompositeTaskInput> in_set = entry.getValue();
        String variable = entry.getKey();

        Iterator<CompositeTaskInput> iter = in_set.iterator();
        while (iter.hasNext()) {
          CompositeTaskInput in = iter.next();
          if ( in.getNode() instanceof CompositeTaskScope ) {
            if ( outputs_variable(in.getNode(), variable) ) {
              iter.remove();
            }
          }
        }
      }

      for ( Map.Entry<String, Set<CompositeTaskInput>> entry : inputs.entrySet() ) {
        String variable = entry.getKey();
        Set<CompositeTaskInput> ins = entry.getValue();
        for ( CompositeTaskInput input : ins ) {
          if ( input.getNode() == CompositeTask.this ) {
            CompositeTask.this.inputs.add(variable);
          }
        }
      }

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

    private boolean outputs_variable(CompositeTaskNode node, String variable) {
      if (node instanceof CompositeTaskScope) {
        CompositeTaskScope scope = (CompositeTaskScope) node;
        boolean answer = false;
        for ( CompositeTaskNode scope_node : scope.getNodes() ) {
          answer |= outputs_variable(scope_node, variable);
        }
        return answer;
      } else if (node instanceof CompositeTaskStep) {
        CompositeTaskStep step = (CompositeTaskStep) node;
        for ( CompositeTaskEdge edge : CompositeTask.this.edges ) {
          if ( edge.getVariable().equals(variable) && edge.getStart().getNode() == step) {
            return true;
          }
        }
      }
      return false;
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

    private Map<String, Set<CompositeTaskInput>> get_node_inputs(CompositeTaskNode node) throws SyntaxError {
      Map<String, Set<CompositeTaskInput>> inputs = new HashMap<String, Set<CompositeTaskInput>>();
      if ( node instanceof CompositeTaskStep ) {
        AstList node_body = (AstList) node.getAst().getAttribute("body");
        for ( AstNode elem : node_body ) {
          if ( elem instanceof Ast && ((Ast) elem).getName().equals("StepInputList") ) {
            for ( AstNode input_node : (AstList) ((Ast) elem).getAttribute("inputs") ) {
              Ast input = (Ast) input_node;
              if ( input.getName().equals("StepInput") ) {
                String parameter = ((Terminal) input.getAttribute("parameter")).getSourceString();
                String variable = variable_to_string((Ast) input.getAttribute("value"));
                if ( !inputs.containsKey(variable) ) {
                  inputs.put(variable, new HashSet<CompositeTaskInput>());
                }
                inputs.get(variable).add( new CompositeTaskInput(node, parameter) );
              }
            }
          }
        }
      } else if ( node instanceof CompositeTaskScope ) {
        /* TODO: just change the behavior of this loop to include Scopes in the */
        for ( CompositeTaskNode sub_node : ((CompositeTaskScope) node).getNodes() ) {
          for ( Map.Entry<String, Set<CompositeTaskInput>> input : get_node_inputs(sub_node).entrySet() ) {
            String variable = input.getKey();
            Set<CompositeTaskInput> in = input.getValue();

            if ( !inputs.containsKey(variable) ) {
              inputs.put(variable, new HashSet<CompositeTaskInput>());
            }

            inputs.get(variable).addAll(in);
            inputs.get(variable).add(new CompositeTaskInput(node));
          }
        }

        if ( node instanceof CompositeTaskForScope ) {
          String collection = ((CompositeTaskForScope) node).getCollectionName();
          if ( !inputs.containsKey(collection) ) {
            inputs.put(collection, new HashSet<CompositeTaskInput>());
          }
          inputs.get(collection).add(new CompositeTaskInput(node));
        }
      }
      return inputs;
    }

    private Map<String, Set<CompositeTaskOutput>> get_node_outputs(CompositeTaskNode node) throws SyntaxError {
      Map<String, Set<CompositeTaskOutput>> outputs = new HashMap<String, Set<CompositeTaskOutput>>();
      if ( node instanceof CompositeTaskStep ) {
        AstList node_body = (AstList) node.getAst().getAttribute("body");
        for ( AstNode elem : node_body ) {
          if ( elem instanceof Ast && ((Ast) elem).getName().equals("StepOutputList") ) {
            for ( AstNode output_node : (AstList) ((Ast) elem).getAttribute("outputs") ) {
              Ast output = (Ast) output_node;
              if ( output.getName().equals("StepFileOutput") ) {
                String file_path = ((Terminal) output.getAttribute("file")).getSourceString();
                String variable = variable_to_string((Ast) output.getAttribute("as"));
                if ( !outputs.containsKey(variable) ) {
                  outputs.put(variable, new HashSet<CompositeTaskOutput>());
                }
                outputs.get(variable).add( new CompositeTaskOutput(node, "File", file_path) );
              }
            }
          }
        }
      } else if ( node instanceof CompositeTaskScope ) {
        Map<String, CompositeTaskOutput> scope_outputs = new HashMap<String, CompositeTaskOutput>();
        for ( CompositeTaskNode sub_node : ((CompositeTaskScope) node).getNodes() ) {
          for ( Map.Entry<String, Set<CompositeTaskOutput>> output : get_node_outputs(sub_node).entrySet() ) {
            String variable = output.getKey();
            Set<CompositeTaskOutput> out = output.getValue();
            if ( !outputs.containsKey(variable) ) {
              outputs.put(variable, new HashSet<CompositeTaskOutput>());
            }

            outputs.get(variable).addAll(out);

            for ( CompositeTaskOutput o : out ) {
              if ( !scope_outputs.containsKey(variable) ) {
                scope_outputs.put(variable, new CompositeTaskOutput(node, o.getType(), o.getPath()));
              }
            }
          }
        }

        for ( Map.Entry<String, CompositeTaskOutput> entry : scope_outputs.entrySet() ) {
          outputs.get(entry.getKey()).add(entry.getValue());
        }
      }
      return outputs;
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

    private CompositeTaskNode verify_step(Ast step) throws SyntaxError {
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

      return new CompositeTaskStep(step, ctStepName, ctSubTask);
    }

    private CompositeTaskNode verify_for(Ast for_node_ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode for_sub_node : (AstList) for_node_ast.getAttribute("body") ) {
        nodes.add( verify((Ast) for_sub_node) );
      }

      String collection = ((Terminal) for_node_ast.getAttribute("collection")).getSourceString();
      String item = ((Terminal) for_node_ast.getAttribute("item")).getSourceString();

      return new CompositeTaskForScope(for_node_ast, collection, item, nodes);
    }

    private CompositeTaskNode verify_composite_task(Ast ast) throws SyntaxError {
      Set<CompositeTaskNode> nodes = new HashSet<CompositeTaskNode>();

      for ( AstNode sub : (AstList) ast.getAttribute("body") ) {
        nodes.add( verify((Ast) sub) );
      }

      return new CompositeTaskBaseScope(ast, nodes);
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

  CompositeTask(String name, Set<CompositeTaskNode> nodes, Set<CompositeTaskEdge> edges, Set<String> inputs) {
    this.name = name;
    this.nodes = nodes;
    this.edges = edges;
    this.inputs = inputs;
  }

  CompositeTask(String name) {
    this.name = name;
    this.nodes = new HashSet<CompositeTaskNode>();
    this.edges = new HashSet<CompositeTaskEdge>();
    this.inputs = new HashSet<String>();
  }

  CompositeTask(SourceCode source_code) throws SyntaxError {
    this.error_formatter = new WdlSyntaxErrorFormatter();
    this.error_formatter.setSourceCode(source_code);
    ParseTreeNode node = getParseTree(source_code);
    this.parse_tree = (ParseTree) node;
    AstList ast_list = (AstList) node.toAst();
    CompositeTaskAstVerifier verifier = new CompositeTaskAstVerifier(this.error_formatter);
    this.nodes = new HashSet<CompositeTaskNode>();
    this.edges = new HashSet<CompositeTaskEdge>();
    this.inputs = new HashSet<String>();
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

  public Set<CompositeTaskEdge> getEdges() {
    return this.edges;
  }

  public CompositeTaskStep getStep(String name) {
    for ( CompositeTaskNode node : this.nodes ) {
      if ( node instanceof CompositeTaskStep ) {
        CompositeTaskStep step = (CompositeTaskStep) node;
        if ( step.getName().equals(name) ) {
          return step;
        }
      }
    }
    return null;
  }

  public CompositeTaskOutput getOutput(String name) {
    for ( CompositeTaskEdge edge : this.edges ) {
      if ( edge.getVariable().equals(name) ) {
        return edge.getStart();
      }
    }
    return null;  
  }

  public Set<CompositeTaskSubTask> getTasks() {
    Set<CompositeTaskSubTask> tasks = new HashSet<CompositeTaskSubTask>();
    for (CompositeTaskNode node : this.nodes) {
      if ( node instanceof CompositeTaskStep ) {
        tasks.add( ((CompositeTaskStep) node).getTask() );
      } else if ( node instanceof CompositeTaskScope ) {
        tasks.addAll( getTasks((CompositeTaskScope) node));
      }
    }
    return tasks;
  }

  private Set<CompositeTaskSubTask> getTasks(CompositeTaskScope scope) {
    Set<CompositeTaskSubTask> tasks = new HashSet<CompositeTaskSubTask>();
    for (CompositeTaskNode node : scope.getNodes()) {
      if ( node instanceof CompositeTaskStep ) {
        tasks.add( ((CompositeTaskStep) node).getTask() );
      } else if ( node instanceof CompositeTaskScope ) {
        tasks.addAll( getTasks((CompositeTaskScope) node));
      }
    }
    return tasks;
  }

  public Set<String> getInputs() {
    // Per task:
    //   1) get input variables for task
    //   2) remove 'parameter' value for all edges with to=task
    // Named inputs 
    // add for loop collection values
    return this.inputs;
  }

  public Map<CompositeTaskNode, Set<CompositeTaskNode>> getDependencyGraph() {
    return null;
  }

  public Ast getAst() {
    return this.ast;
  }

  public void setNodes(Set<CompositeTaskNode> nodes) {
    this.nodes = nodes;
  }

  public void setEdges(Set<CompositeTaskEdge> edges) {
    this.edges = edges;
  }

  public void setName(String name) {
    this.name = name;
  }

  public void addEdge(CompositeTaskEdge edge) {
    this.edges.add(edge);
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
