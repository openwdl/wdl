import java.util.regex.*;
import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.nio.*;
import java.nio.charset.*;
import java.nio.channels.*;

class WdlSourceCode implements SourceCode{
  private File source;
  private String resource;
  private String contents;
  private int line;
  private int col;
  private StringBuilder currentLine;
  private List<String> lines;

  WdlSourceCode(String source, String resource) {
    init(source, resource);
  }

  WdlSourceCode(File source) throws IOException {
    this(source, "utf-8", source.getCanonicalPath());
  }

  WdlSourceCode(File source, String resource) throws IOException {
    this(source, "utf-8", resource);
  }

  WdlSourceCode(File source, String encoding, String resource) throws IOException, FileNotFoundException {
    FileChannel channel = new FileInputStream(source).getChannel();
    MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ_ONLY, 0, channel.size());
    Charset cs = Charset.forName(encoding);
    CharsetDecoder cd = cs.newDecoder();
    CharBuffer cb = cd.decode(buffer);
    init(cb.toString(), resource);
  }

  private void init(String contents, String resource) {
    this.contents = contents;
    this.resource = resource;
    this.line = 1;
    this.col = 1;
    this.lines = new ArrayList<String>();
    this.currentLine = new StringBuilder();
  }

  public void advance(int amount) {
    String str = this.contents.substring(0, amount);
    for ( byte b : str.getBytes() ) {
      if ( b == (byte) '\n' || b == (byte) '\r' ) {
        this.line++;
        this.col = 1;
      } else {
        this.col++;
      }
    }
    this.contents = this.contents.substring(amount);
  }

  public String getString() {
    return this.contents;
  }

  public String getResource() {
    return this.resource;
  }

  public int getLine() {
    return this.line;
  }

  public int getColumn() {
    return this.col;
  }

  public String getLine(int lineno) {
    return null; // TODO
  }

  public List<String> getLines() {
    return null; // TODO
  }
}

class LexerMatch {
  private Terminal terminal;
  LexerMatch() { this.terminal = null; }
  LexerMatch(Terminal terminal) { this.terminal = terminal; }
  public Terminal getTerminal() { return this.terminal; }
}

class TokenLexer {
  private Pattern regex;
  private WdlParser.TerminalId terminal;

  TokenLexer(Pattern regex, WdlParser.TerminalId terminal) {
    this.regex = regex;
    this.terminal = terminal;
  }

  LexerMatch match(SourceCode source) {
    Matcher m = this.regex.matcher(source.getString());
    LexerMatch rval = null;
    if ( m.find() ) {
      String sourceString = m.group();

      if (this.terminal != null)
        rval = new LexerMatch(new Terminal(this.terminal.id(), this.terminal.string(), Utility.base64_encode(sourceString.getBytes()), source.getResource(), source.getLine(), source.getColumn()));
      else
        rval = new LexerMatch();

      source.advance(sourceString.length());
    }
    return rval;
  }
}

public class Lexer {
  public static void main(String[] args) {
    // 'as', 'assign', 'colon', 'comma', 'composite_task', 'file', 'for', 'identifier', 'in', 'input', 'lbrace', 'lparen', 'lsquare', 'number', 'output', 'rbrace', 'rparen', 'rsquare', 'semi', 'step', 'string'
    ArrayList<TokenLexer> regex = new ArrayList<TokenLexer>();
    regex.add( new TokenLexer(Pattern.compile("\\/\\*.*?\\*\\/", Pattern.DOTALL), null) );
    regex.add( new TokenLexer(Pattern.compile("//.*"), null) );
    regex.add( new TokenLexer(Pattern.compile("^composite_task(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_COMPOSITE_TASK) );
    regex.add( new TokenLexer(Pattern.compile("^output(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_OUTPUT) );
    regex.add( new TokenLexer(Pattern.compile("^input(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_INPUT) );
    regex.add( new TokenLexer(Pattern.compile("^step(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_STEP) );
    regex.add( new TokenLexer(Pattern.compile("^File(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_FILE) );
    regex.add( new TokenLexer(Pattern.compile("^for(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_FOR) );
    regex.add( new TokenLexer(Pattern.compile("^as(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_AS) );
    regex.add( new TokenLexer(Pattern.compile("^in(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_IN) );
    regex.add( new TokenLexer(Pattern.compile("^\\."), WdlParser.TerminalId.TERMINAL_DOT) );
    regex.add( new TokenLexer(Pattern.compile("^,"), WdlParser.TerminalId.TERMINAL_COMMA) );
    regex.add( new TokenLexer(Pattern.compile("^:"), WdlParser.TerminalId.TERMINAL_COLON) );
    regex.add( new TokenLexer(Pattern.compile("^;"), WdlParser.TerminalId.TERMINAL_SEMI) );
    regex.add( new TokenLexer(Pattern.compile("^="), WdlParser.TerminalId.TERMINAL_ASSIGN) );
    regex.add( new TokenLexer(Pattern.compile("^\\["), WdlParser.TerminalId.TERMINAL_LSQUARE) );
    regex.add( new TokenLexer(Pattern.compile("^\\]"), WdlParser.TerminalId.TERMINAL_RSQUARE) );
    regex.add( new TokenLexer(Pattern.compile("^\\{"), WdlParser.TerminalId.TERMINAL_LBRACE) );
    regex.add( new TokenLexer(Pattern.compile("^\\}"), WdlParser.TerminalId.TERMINAL_RBRACE) );
    regex.add( new TokenLexer(Pattern.compile("^\\("), WdlParser.TerminalId.TERMINAL_LPAREN) );
    regex.add( new TokenLexer(Pattern.compile("^\\)"), WdlParser.TerminalId.TERMINAL_RPAREN) );
    regex.add( new TokenLexer(Pattern.compile("^\"([^\\\\\"\\n]|\\[\\\"'nrbtfav\\?]|\\[0-7]{1,3}|\\\\x[0-9a-fA-F]+|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*\""), WdlParser.TerminalId.TERMINAL_STRING) );
    regex.add( new TokenLexer(Pattern.compile("^([a-zA-Z_]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)([a-zA-Z_0-9]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"), WdlParser.TerminalId.TERMINAL_IDENTIFIER) );
    regex.add( new TokenLexer(Pattern.compile("^[-]?(\\.[0-9]+|[0-9]+(\\.[0-9]*)?)"), WdlParser.TerminalId.TERMINAL_NUMBER) );
    regex.add( new TokenLexer(Pattern.compile("^\\s+"), null) );

    if ( args.length < 1 ) {
      System.err.println("Usage: Lexer <input file>");
      System.exit(-1);
    }

    try {
      SourceCode code = new WdlSourceCode(new File(args[0]));
      ArrayList<String> terminal_strings = new ArrayList<String>();
      boolean progress = true;

      while (progress) {
        progress = false;
        for ( TokenLexer lexer : regex ) {
          LexerMatch match = lexer.match(code);
          if (match != null) {
            progress = true;
            if (match.getTerminal() != null) {
              terminal_strings.add( "  " + match.getTerminal() );
            }
            break;
          }
        }
      }

      System.out.println("[");
      System.out.println( Utility.join(terminal_strings, ",\n") );
      System.out.println("]");
      System.out.flush();
    } catch (IOException e) {
      System.err.println(e);
      System.exit(-1);
    }
  }
}
