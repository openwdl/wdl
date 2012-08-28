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
        rval = new LexerMatch(new Terminal(this.terminal.id(), this.terminal.string(), sourceString, source.getResource(), source.getLine(), source.getColumn()));
      else
        rval = new LexerMatch();

      source.advance(sourceString.length());
    }
    return rval;
  }
}

public class Lexer {

  private ArrayList<TokenLexer> regex;

  Lexer() {
    this.regex = new ArrayList<TokenLexer>();
    this.regex.add( new TokenLexer(Pattern.compile("\\/\\*.*?\\*\\/", Pattern.DOTALL), null) );
    this.regex.add( new TokenLexer(Pattern.compile("//.*"), null) );
    this.regex.add( new TokenLexer(Pattern.compile("^composite_task(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_COMPOSITE_TASK) );
    this.regex.add( new TokenLexer(Pattern.compile("^output(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_OUTPUT) );
    this.regex.add( new TokenLexer(Pattern.compile("^input(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_INPUT) );
    this.regex.add( new TokenLexer(Pattern.compile("^step(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_STEP) );
    this.regex.add( new TokenLexer(Pattern.compile("^File(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_FILE) );
    this.regex.add( new TokenLexer(Pattern.compile("^for(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_FOR) );
    this.regex.add( new TokenLexer(Pattern.compile("^as(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_AS) );
    this.regex.add( new TokenLexer(Pattern.compile("^in(?=[^a-zA-Z_]|$)"), WdlParser.TerminalId.TERMINAL_IN) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\."), WdlParser.TerminalId.TERMINAL_DOT) );
    this.regex.add( new TokenLexer(Pattern.compile("^,"), WdlParser.TerminalId.TERMINAL_COMMA) );
    this.regex.add( new TokenLexer(Pattern.compile("^:"), WdlParser.TerminalId.TERMINAL_COLON) );
    this.regex.add( new TokenLexer(Pattern.compile("^;"), WdlParser.TerminalId.TERMINAL_SEMI) );
    this.regex.add( new TokenLexer(Pattern.compile("^="), WdlParser.TerminalId.TERMINAL_ASSIGN) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\["), WdlParser.TerminalId.TERMINAL_LSQUARE) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\]"), WdlParser.TerminalId.TERMINAL_RSQUARE) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\{"), WdlParser.TerminalId.TERMINAL_LBRACE) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\}"), WdlParser.TerminalId.TERMINAL_RBRACE) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\("), WdlParser.TerminalId.TERMINAL_LPAREN) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\)"), WdlParser.TerminalId.TERMINAL_RPAREN) );
    this.regex.add( new TokenLexer(Pattern.compile("^\"([^\\\\\"\\n]|\\[\\\"'nrbtfav\\?]|\\[0-7]{1,3}|\\\\x[0-9a-fA-F]+|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*\""), WdlParser.TerminalId.TERMINAL_STRING) );
    this.regex.add( new TokenLexer(Pattern.compile("^([a-zA-Z_]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)([a-zA-Z_0-9]|\\\\[uU]([0-9a-fA-F]{4})([0-9a-fA-F]{4})?)*"), WdlParser.TerminalId.TERMINAL_IDENTIFIER) );
    this.regex.add( new TokenLexer(Pattern.compile("^[-]?(\\.[0-9]+|[0-9]+(\\.[0-9]*)?)"), WdlParser.TerminalId.TERMINAL_NUMBER) );
    this.regex.add( new TokenLexer(Pattern.compile("^\\s+"), null) );
  }

  public List<Terminal> getTokens(SourceCode code) {
    ArrayList<Terminal> tokens = new ArrayList<Terminal>();
    boolean progress = true;

    while (progress) {
      progress = false;
      for ( TokenLexer lexer : regex ) {
        LexerMatch match = lexer.match(code);
        if (match != null) {
          progress = true;
          if (match.getTerminal() != null) {
            tokens.add(match.getTerminal());
          }
          break;
        }
      }
    }

    return tokens;
  }
  public static void main(String[] args) {
    try {
      SourceCode code = new WdlSourceCode(new File(args[0]));
      Lexer lexer = new Lexer();
      List<Terminal> terminals = lexer.getTokens(code);
      System.out.println("[");
      System.out.println(Utility.join(terminals, ",\n"));
      System.out.println("]");
    } catch( IOException e ) {
      System.err.println(e);
    }
  }
}
