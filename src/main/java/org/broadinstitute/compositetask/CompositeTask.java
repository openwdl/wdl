package org.broadinstitute.compositetask;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.HashMap;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.broadinstitute.parser.Ast;
import org.broadinstitute.parser.AstNode;
import org.broadinstitute.parser.AstList;
import org.broadinstitute.parser.ParseTree;
import org.broadinstitute.parser.ParseTreeNode;
import org.broadinstitute.parser.SourceCode;
import org.broadinstitute.parser.Terminal;
import org.broadinstitute.parser.SyntaxError;
import org.broadinstitute.parser.CompositeTaskParser;
import org.broadinstitute.parser.TokenStream;

public class CompositeTask implements CompositeTaskScope {

    private ParseTree parse_tree;
    private Ast ast;
    private WdlSyntaxErrorFormatter error_formatter;
    private Set<CompositeTaskNode> nodes;
    private String name;
    private CompositeTaskScope parent;

    private class CompositeTaskAstVerifier {
        private WdlSyntaxErrorFormatter syntaxErrorFormatter;
        private Map<String, CompositeTaskVariable> variables;
        private Map<CompositeTaskVariable, Terminal> output_variables;
        private Map<String, Terminal> output_files;
        private Map<String, Terminal> step_names;

        CompositeTaskAstVerifier(WdlSyntaxErrorFormatter syntaxErrorFormatter) {
            this.syntaxErrorFormatter = syntaxErrorFormatter;
            this.variables = new HashMap<String, CompositeTaskVariable>();
            this.output_variables = new HashMap<CompositeTaskVariable, Terminal>();
            this.output_files = new HashMap<String, Terminal>();
            this.step_names = new HashMap<String, Terminal>();
        }

        public Ast verify(AstNode wdl_ast) throws SyntaxError {
            Ast composite_task = null;

            if ( wdl_ast instanceof AstList ) {
                if ( ((AstList) wdl_ast).size() != 1 ) {
                    throw new SyntaxError("Source code must contain only one top level composite_task definition.");
                }

                composite_task = (Ast) ((AstList) wdl_ast).get(0);
            } else if (wdl_ast instanceof Ast) {
                composite_task = (Ast) wdl_ast;
                String node_type = composite_task.getName();
                if (!node_type.equals("CompositeTask")) {
                    throw new SyntaxError("Source code does not contain a composite task definition");
                }
            } else {
                throw new SyntaxError("Unknown syntax error");
            }

            AstList ctNodes = (AstList) composite_task.getAttribute("body");
            CompositeTask.this.nodes = new LinkedHashSet<CompositeTaskNode>();
            CompositeTask.this.name = ((Terminal) composite_task.getAttribute("name")).getSourceString();

            for ( AstNode ctNode : ctNodes ) {
                Ast node = (Ast) ctNode;
                CompositeTask.this.nodes.add(verify(node));
            }

            set_parents(CompositeTask.this);

            Pattern expressionPattern = Pattern.compile("\\$\\{([^}]+)\\}");
            for ( Map.Entry<String, Terminal> output_file : this.output_files.entrySet() ) {
              Matcher matcher = expressionPattern.matcher(output_file.getValue().getSourceString());
              while ( matcher.find() ) {
                String filename_var = matcher.group(1);
                for ( Map.Entry<CompositeTaskVariable, Terminal> step_output : this.output_variables.entrySet() ) {
                  String output_var = step_output.getKey().getName();
                  if ( output_var.equals(filename_var) ) {
                    throw new SyntaxError(this.syntaxErrorFormatter.variable_used_as_filename_and_step_output(output_file.getValue(), matcher.start(), step_output.getValue()));
                  }
                }
              }
            }

            return composite_task;
        }

        private void set_parents(CompositeTaskScope scope) {
            for ( CompositeTaskNode node : scope.getNodes() ) {
                node.setParent(scope);
                if ( node instanceof CompositeTaskScope ) {
                    set_parents((CompositeTaskScope) node);
                }
            }
        }

        private CompositeTaskVariable make_variable(String name, String member) {
            String key = name + ((member == null) ? "" : member);
            if ( !this.variables.containsKey(key) ) {
                this.variables.put(key, new CompositeTaskVariable(name, member));
            }
            return this.variables.get(key);
        }

        private CompositeTaskVariable ast_to_variable(Ast ast) {
            Terminal name = (Terminal) ast.getAttribute("name");
            Terminal member = (Terminal) ast.getAttribute("member");
            return make_variable(name.getSourceString(), (member == null) ? null : member.getSourceString());
        }

        private CompositeTaskNode verify(Ast ast) throws SyntaxError {
            if ( ast.getName().equals("Step") ) {
                return verify_step(ast);
            } else if ( ast.getName().equals("ForLoop") ) {
                return verify_for(ast);
            } else if ( ast.getName().equals("CompositeTask") ) {
                return verify_composite_task(ast);
            } else {
                throw new SyntaxError("Unknown node found in abstract syntax tree.");
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

            Terminal name_terminal;
            if ( step.getAttribute("name") != null ) {
                name_terminal = (Terminal) step.getAttribute("name");
            } else {
                name_terminal = task_name;
            }

            String name = name_terminal.getSourceString();
            if ( this.step_names.containsKey(name) ) {
                throw new SyntaxError(this.syntaxErrorFormatter.duplicate_step_names(name_terminal, this.step_names.get(name)));
            }
            this.step_names.put(name, name_terminal);

            Set<CompositeTaskStepInput> step_inputs = new LinkedHashSet<CompositeTaskStepInput>();
            Set<CompositeTaskStepOutput> step_outputs = new LinkedHashSet<CompositeTaskStepOutput>();

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
                            step_inputs.add( new CompositeTaskStepInput(parameter.getSourceString(), variable) );
                        }
                    }

                    if ( entry_ast.getName().equals("StepOutputList") ) {
                        AstList output_list = (AstList) entry_ast.getAttribute("outputs");
                        for ( AstNode output_node : output_list ) {
                            Ast output = (Ast) output_node;
                            Terminal filepath = (Terminal) output.getAttribute("expression");
                            Ast step_output = (Ast) output.getAttribute("var");
                            String mode = ((Terminal) output.getAttribute("mode")).getSourceString();

                            CompositeTaskVariable variable = ast_to_variable((Ast) step_output.getAttribute("var"));
                            Terminal variable_terminal = (Terminal) ((Ast) ((Ast) output.getAttribute("var")).getAttribute("var")).getAttribute("name");
                            String method = null;

                            if ( step_output.getName().equals("OutputVariable") ) {
                                method = "assign";
                            } else if ( step_output.getName().equals("OutputListAppend") ) {
                                method = "append";
                            }

                            if (this.output_variables.containsKey(variable)) {
                                throw new SyntaxError(this.syntaxErrorFormatter.duplicate_output_variable(variable_terminal, this.output_variables.get(variable)));
                            } else {
                                this.output_variables.put(variable, variable_terminal);
                            }

                            if (this.output_files.containsKey(filepath.getSourceString())) {
                                // We don't need this syntax error anymore, but perhaps useful in the future. */
                                /* throw new SyntaxError(
                                  this.syntaxErrorFormatter.duplicate_output_file(filepath, this.output_files.get(filepath.getSourceString())));
                                */
                            } else {
                                this.output_files.put(filepath.getSourceString(), filepath);
                            }

                            step_outputs.add( new CompositeTaskStepOutput(mode, method, filepath.getSourceString(), variable) );
                        }
                    }
                }
            }

            return new CompositeTaskStep(name, subtask, step_inputs, step_outputs);
        }

        private CompositeTaskForLoop verify_for(Ast for_node_ast) throws SyntaxError {
            Set<CompositeTaskNode> nodes = new LinkedHashSet<CompositeTaskNode>();

            String collection = ((Terminal) for_node_ast.getAttribute("collection")).getSourceString();
            String item = ((Terminal) for_node_ast.getAttribute("item")).getSourceString();
            CompositeTaskVariable collection_var = make_variable(collection, null);
            CompositeTaskVariable item_var = make_variable(item, null);

            for ( AstNode for_sub_node : (AstList) for_node_ast.getAttribute("body") ) {
                CompositeTaskNode sub_node = verify((Ast) for_sub_node);

                if ( sub_node instanceof CompositeTaskStep ) {
                    CompositeTaskStep step = (CompositeTaskStep) sub_node;
                    boolean found = false;
                    for ( CompositeTaskStepInput input : step.getInputs() ) {
                        if (input.getVariable().getName().equals(item_var.getName())) {
                            found = true;
                        } 
                    }

                    if ( !found ) {
                        throw new SyntaxError(this.syntaxErrorFormatter.step_doesnt_use_loop_iterator((Terminal) for_node_ast.getAttribute("item"), this.step_names.get(step.getName())));
                    }
                }

                nodes.add(sub_node);
            }

            return new CompositeTaskForLoop(collection_var, item_var, nodes);
        }

        private CompositeTask verify_composite_task(Ast ast) throws SyntaxError {
            Set<CompositeTaskNode> nodes = new LinkedHashSet<CompositeTaskNode>();
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

    private CompositeTask(String name, Set<CompositeTaskNode> nodes) {
        this.name = name;
        this.nodes = nodes;
        this.parent = null;
    }

    public CompositeTask(SourceCode source_code) throws SyntaxError {
        this.error_formatter = new WdlSyntaxErrorFormatter();
        this.error_formatter.setSourceCode(source_code);
        ParseTreeNode node = getParseTree(source_code);
        this.parse_tree = (ParseTree) node;
        AstList ast_list = (AstList) node.toAst();
        CompositeTaskAstVerifier verifier = new CompositeTaskAstVerifier(this.error_formatter);
        this.ast = verifier.verify(ast_list);
        this.parent = null;
    }

    public CompositeTask(File source_code, String resource) throws SyntaxError, IOException {
        this(new CompositeTaskSourceCode(source_code, resource));
    }

    public CompositeTask(File source_code) throws SyntaxError, IOException {
        this(new CompositeTaskSourceCode(source_code));
    }

    public CompositeTask(String source_code, String resource) throws SyntaxError {
        this(new CompositeTaskSourceCode(source_code, resource));
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
        return new CompositeTaskGraph(this);
    }

    public CompositeTaskStep getStep(String name) {
        return getStep(this, name);
    }

    public Set<CompositeTaskSubTask> getTasks() {
        return getTasks(this);
    }

    public Ast getAst() {
        return this.ast;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void addNode(CompositeTaskNode node) {
    }

    public void setParent(CompositeTaskScope parent) {
        this.parent = parent;
    }

    public CompositeTaskScope getParent() {
        return this.parent;
    }

    public boolean contains(CompositeTaskNode node) {
        for ( CompositeTaskNode sub_node : this.nodes ) {
            if ( node.equals(sub_node) ) {
                return true;
            }

            if ( sub_node instanceof CompositeTaskScope ) {
                CompositeTaskScope scope = (CompositeTaskScope) sub_node;
                if ( scope.contains(node) ) {
                    return true;
                }
            }
        }
        return false;
    }

    public int compareTo(CompositeTaskVertex other) {
      return this.toString().compareTo(other.toString());
    }

    public String toString() {
        return "[CompositeTask name="+this.name+"]";
    }

    /** Private methods **/

    private ParseTreeNode getParseTree(SourceCode source_code) throws SyntaxError {
        CompositeTaskParser parser = new CompositeTaskParser(this.error_formatter);
        Lexer lexer = new Lexer();
        List<Terminal> terminals = lexer.getTokens(source_code);
        TokenStream tokens = new TokenStream(terminals);
        return parser.parse(tokens);
    }

    private static Set<CompositeTaskSubTask> getTasks(CompositeTaskScope scope) {
        Set<CompositeTaskSubTask> tasks = new HashSet<CompositeTaskSubTask>();
        for ( CompositeTaskNode node : scope.getNodes() ) {
            if ( node instanceof CompositeTaskStep ) {
                CompositeTaskStep step = (CompositeTaskStep) node;
                tasks.add(step.getTask());
            } else if ( node instanceof CompositeTaskScope ) {
                CompositeTaskScope subScope = (CompositeTaskScope) node;
                tasks.addAll( getTasks(subScope) );
            }
        }
        return tasks;
    }

    private static CompositeTaskStep getStep(CompositeTaskScope scope, String name) {
        for ( CompositeTaskNode node : scope.getNodes() ) {
            if ( node instanceof CompositeTaskStep ) {
                CompositeTaskStep step = (CompositeTaskStep) node;
                if ( step.getName().equals(name) ) {
                    return step;
                }
            } else if ( node instanceof CompositeTaskScope ) {
                CompositeTaskStep step = getStep((CompositeTaskScope) node, name);
                if ( step != null ) {
                    return step;
                }
            }
        }
        return null;
    }
}
