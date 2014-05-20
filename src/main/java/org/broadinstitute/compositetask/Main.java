package org.broadinstitute.compositetask;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.broadinstitute.parser.Utility;
import org.broadinstitute.parser.Ast;
import org.broadinstitute.parser.ParseTree;
import org.broadinstitute.parser.SyntaxError;
import org.broadinstitute.parser.Terminal;

public class Main {

  public static void usage() {
    System.err.println("Usage: <.wdl file> <tokens,ast,parsetree,entities,graph,format,format-ansi,format-html>");
    System.err.println();
    System.err.println("Actions:");
    System.err.println("  tokens: tokenize the source code");
    System.err.println("  ast: parse source code and output an abstract syntax tree");
    System.err.println("  parsetree: parse source code and output a parsetree");
    System.err.println("  entities: output an abbreviated view of all entities and which scope they're nested in");
    System.err.println("  graph: output the set of verticies and edges for the directed acyclic graph");
    System.err.println("  format: reformat source code");
    System.err.println("  format-ansi: reformat source code and colorize for the terminal");
    System.err.println("  format-html: reformat source code and add HTML span tags");
    System.err.println("  replace <task[:version]> <new task:version>: replace a task/version with a different task/version");
    System.exit(-1);
  }

  public static void main(String[] args) {

    if (args.length < 2) {
      usage();
    }

    try {

      if ( args[1].equals("tokens") ) {
          Lexer lexer = new Lexer();
          List<Terminal> terminals = lexer.getTokens(new CompositeTaskSourceCode(new File(args[0])));
          for ( Terminal terminal : terminals ) {
              System.out.println(terminal);
          }
          System.exit(0);
      }

      CompositeTask ctask = new CompositeTask(new File(args[0]));

      if ( args[1].equals("ast") ) {
        Ast ast = ctask.getAst();
        System.out.println(ast.toPrettyString());
      } else if ( args[1].equals("parsetree") ) {
        ParseTree tree = ctask.getParseTree();
        System.out.println(tree.toPrettyString());
      } else if ( args[1].equals("entities") ) {
        print_tree(ctask);
      } else if ( args[1].equals("graph") ) {
        CompositeTaskGraph graph = ctask.getGraph();

        System.out.println("VERTICIES");
        System.out.println("---------");
        for ( CompositeTaskVertex v : graph.vertexSet() ) {
          System.out.println(v);
        }
        System.out.println("");

        System.out.println("EDGES");
        System.out.println("-----");
        for ( CompositeTaskEdge v : graph.edgeSet() ) {
          System.out.println(v);
        }

      } else if ( args[1].equals("format-ansi") ) {
        CompositeTaskSourceCodeFormatter formatter = new CompositeTaskSourceCodeFormatter(new AnsiColorizer());
        String formatted = formatter.format(ctask);
        System.out.println(formatted);
      } else if ( args[1].equals("format-html") ) {
        CompositeTaskSourceCodeFormatter formatter = new CompositeTaskSourceCodeFormatter(new HtmlColorizer());
        String formatted = formatter.format(ctask);
        System.out.println(formatted);
      } else if ( args[1].equals("format") ) {
        CompositeTaskSourceCodeFormatter formatter = new CompositeTaskSourceCodeFormatter();
        String formatted = formatter.format(ctask);
        System.out.println(formatted);
      } else if ( args[1].equals("replace") ) {
        if (args.length < 4 || !args[3].contains(":")) {
          System.err.println("Usage: replace <task[:version]> <task:version> e.g. `replace my_task my_task:45`");
          System.exit(-1);
        }

        String from, from_version, to, to_version;
        from = from_version = to = to_version = null;

        from = args[2];
        if ( args[2].contains(":") ) {
          String[] parts = args[2].split(":");
          from = parts[0];
          from_version = parts[1];
        }

        String[] parts = args[3].split(":");
        to = parts[0];
        to_version = parts[1];

        ctask.replace(from, from_version, to, to_version);
        CompositeTaskSourceCodeFormatter formatter = new CompositeTaskSourceCodeFormatter();
        String formatted = formatter.format(ctask);
        System.out.println(formatted);
      } else {
        usage();
      }
    } catch (IOException error) {
      System.err.println(error);
      System.exit(-1);
    } catch (SyntaxError error) {
      System.err.println(error);
      System.exit(-1);
    }
  }

  public static void print_tree(CompositeTask ctask) {
    print_tree(ctask, 0);
  }

  public static void print_tree(CompositeTaskScope scope, int depth) {
    Set<CompositeTaskNode> nodes = scope.getNodes();
    for ( CompositeTaskNode node : nodes ) {
      System.out.println(Utility.getIndentString(depth) + node);
      if ( node instanceof CompositeTaskScope ) {
        print_tree((CompositeTaskScope) node, depth + 2);
      }
    }
  }
}
