import java.util.regex.*;
import java.util.ArrayList;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.nio.*;
import java.nio.charset.*;
import java.nio.channels.*;

class SourceCode {
  private File source;
  private String resource;
  private String contents;

  SourceCode(String source, String resource) {
    this.contents = source;
    this.resource = resource;
  }

  SourceCode(File source) throws IOException {
    this(source, "utf-8", source.getCanonicalPath());
  }

  SourceCode(File source, String resource) throws IOException {
    this(source, "utf-8", resource);
  }

  SourceCode(File source, String encoding, String resource) throws IOException, FileNotFoundException {
    FileChannel channel = new FileInputStream(source).getChannel();
    MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ_ONLY, 0, channel.size());
    Charset cs = Charset.forName(encoding);
    CharsetDecoder cd = cs.newDecoder();
    CharBuffer cb = cd.decode(buffer);
    this.contents = cb.toString();
  }

  public void advance(int amount) {
    this.contents = this.contents.substring(amount);
  }

  public String getString() {
    return this.contents;
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

  private String base64_encode(byte[] bytes) {
    int b64_len = ((bytes.length + ( (bytes.length % 3 != 0) ? (3 - (bytes.length % 3)) : 0) ) / 3) * 4;
    int cycle = 0, b64_index = 0;
    byte[] alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".getBytes();
    byte[] b64 = new byte[b64_len];
    byte[] buffer = new byte[3];
    Arrays.fill(buffer, (byte) -1);

    for (byte b : bytes) {
      int index = cycle % 3;
      buffer[index] = b;
      boolean last = (cycle == (bytes.length - 1));
      if ( index == 2 || last ) {
        if ( last ) {
          if ( buffer[1] == -1 ) buffer[1] = 0;
          if ( buffer[2] == -1 ) buffer[2] = 0;
        }

        b64[b64_index++] = alphabet[buffer[0] >> 2];
        b64[b64_index++] = alphabet[((buffer[0] & 0x3) << 4) | ((buffer[1] >> 4) & 0xf)];
        b64[b64_index++] = alphabet[((buffer[1] & 0xf) << 2) | ((buffer[2] >> 6) & 0x3)];
        b64[b64_index++] = alphabet[buffer[2] & 0x3f];

        if ( buffer[1] == 0 ) b64[b64_index - 2] = (byte) '=';
        if ( buffer[2] == 0 ) b64[b64_index - 1] = (byte) '=';

        Arrays.fill(buffer, (byte) -1);
      }
      cycle++;
    }
    return new String(b64);
  }

  TokenLexer(Pattern regex, WdlParser.TerminalId terminal) {
    this.regex = regex;
    this.terminal = terminal;
  }

  LexerMatch match(SourceCode source) {
    Matcher m = this.regex.matcher(source.getString());
    if ( m.find() ) {
      String sourceString = m.group();
      source.advance(sourceString.length());

      if (this.terminal != null)
        return new LexerMatch(new Terminal(this.terminal.id(), this.terminal.string(), base64_encode(sourceString.getBytes()), "file", 0, 0));
      else
        return new LexerMatch();
    }
    return null;
  }
}

public class Lexer {
  public static void main(String[] args) {
    ArrayList<TokenLexer> regex = new ArrayList<TokenLexer>();
    regex.add( new TokenLexer(Pattern.compile("^scatter-gather(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_SCATTER_GATHER) );
    regex.add( new TokenLexer(Pattern.compile("^String(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_STRING) );
    regex.add( new TokenLexer(Pattern.compile("^workflow(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_WORKFLOW) );
    regex.add( new TokenLexer(Pattern.compile("^File(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_FILE) );
    regex.add( new TokenLexer(Pattern.compile("^output(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_OUTPUT) );
    regex.add( new TokenLexer(Pattern.compile("^step(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_STEP) );
    regex.add( new TokenLexer(Pattern.compile("^command(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_COMMAND) );
    regex.add( new TokenLexer(Pattern.compile("^action(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_ACTION) );
    regex.add( new TokenLexer(Pattern.compile("^,"), WdlParser.TerminalId.TERMINAL_COMMA) );
    regex.add( new TokenLexer(Pattern.compile("^:"), WdlParser.TerminalId.TERMINAL_COLON) );
    regex.add( new TokenLexer(Pattern.compile("^\\}"), WdlParser.TerminalId.TERMINAL_RBRACE) );
    regex.add( new TokenLexer(Pattern.compile("^;"), WdlParser.TerminalId.TERMINAL_SEMI) );
    regex.add( new TokenLexer(Pattern.compile("^\\{"), WdlParser.TerminalId.TERMINAL_LBRACE) );
    regex.add( new TokenLexer(Pattern.compile("^="), WdlParser.TerminalId.TERMINAL_EQUALS) );
    regex.add( new TokenLexer(Pattern.compile("^\\("), WdlParser.TerminalId.TERMINAL_LPAREN) );
    regex.add( new TokenLexer(Pattern.compile("^\\)"), WdlParser.TerminalId.TERMINAL_RPAREN) );
    regex.add( new TokenLexer(Pattern.compile("^\"([^\\\\\"\\n]|\\[\\\"'nrbtfav\\?]|\\[0-7]{1,3}|\\\\x[0-9a-fA-F]+|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*\""), WdlParser.TerminalId.TERMINAL_STRING_LITERAL) );
    regex.add( new TokenLexer(Pattern.compile("^([a-zA-Z_]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)([a-zA-Z_0-9]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"), WdlParser.TerminalId.TERMINAL_IDENTIFIER) );
    regex.add( new TokenLexer(Pattern.compile("^\\s+"), null) );

    if ( args.length < 1 ) {
      System.err.println("Usage: Lexer <input file>");
      System.exit(-1);
    }

    try {
      SourceCode code = new SourceCode(new File(args[0]));
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
