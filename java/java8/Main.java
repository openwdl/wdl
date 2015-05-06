import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("java Main <file.wdl>");
        }
        File wdl = new File(args[0]);
        try {
            String wdlSource = new Scanner(wdl, "UTF-8").useDelimiter("\\A").next();
            WdlParser parser = new WdlParser();
            WdlParser.TokenStream tokens = new WdlParser.TokenStream(parser.lex(wdlSource, wdl.getName()));
            WdlParser.Ast ast = (WdlParser.Ast) parser.parse(tokens).toAst();
            System.out.println(ast.toPrettyString());
        } catch(FileNotFoundException e) {
            System.err.println(e);
        } catch(WdlParser.SyntaxError e) {
            System.err.println(e);
        }
    }
}
