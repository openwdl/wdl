import java.io.File;
import java.io.IOException;

class WdlMain {
  public static void main(String[] args) {
    WdlSyntaxErrorFormatter error_formatter = new WdlSyntaxErrorFormatter();
    SourceCode code = null;

    try {
      code = new WdlSourceCode(new File(args[0]));
    } catch (IOException error) {
      System.err.println(error);
      System.exit(-1);
    }

    Lexer lexer = new Lexer();
    WdlParser parser = new WdlParser(error_formatter);
    TerminalMap terminals = parser.getTerminalMap();
    TokenStream tokens = new TokenStream(terminals);
    tokens.addAll(lexer.getTokens(code));
    error_formatter.setTerminalMap(terminals);

    try {
      ParseTreeNode parsetree = parser.parse(tokens);

      if ( args.length >= 2 && args[1].equals("ast") ) {
        AstNode ast = parsetree.toAst();
        if ( ast != null ) {
          System.out.println(ast.toPrettyString());
        } else {
          System.out.println("None");
        }
      } else {
        System.out.println(parsetree.toPrettyString());
      }
    } catch (SyntaxError error) {
      System.err.println(error);
    }
  }
}
