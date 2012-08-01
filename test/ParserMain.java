import org.json.*;
import java.io.*;
class ParserMain {
  private static Parser getParser(String name) throws Exception {
    if (name.equals("wdl")) {
      return new WdlParser();
    }
    throw new Exception("Invalid grammar name: " + name);
  }
  public static void main(String args[]) {
    final String grammars = "wdl";
    if ( args.length < 2 ) {
      System.out.println("Usage: ParserMain <" + grammars + "> <parsetree,ast>");
      System.exit(-1);
    }
    final String grammar = args[0].toLowerCase();
    try {
      Parser parser = getParser(grammar);
      TerminalMap terminals = parser.getTerminalMap();
      TokenStream tokens = new TokenStream(terminals);
      String contents = Utility.readStdin();
      JSONArray arr = new JSONArray(contents);
      for ( int i = 0; i < arr.length(); i++ ) {
        JSONObject token = arr.getJSONObject(i);
        tokens.add(new Terminal(
          terminals.get(token.getString("terminal")),
          token.getString("terminal"),
          token.getString("source_string"),
          token.getString("resource"),
          token.getInt("line"),
          token.getInt("col")
        ));
      }
      ParseTreeNode parsetree = parser.parse(tokens);
      if ( args.length > 1 && args[1].equals("ast") ) {
        AstNode ast = parsetree.toAst();
        if ( ast != null ) {
          System.out.println(ast.toPrettyString());
        } else {
          System.out.println("None");
        }
      } else {
        System.out.println(parsetree.toPrettyString());
      }
    } catch (Exception e) {
      System.err.println(e.getMessage());
      System.exit(-1);
    }
  }
}
