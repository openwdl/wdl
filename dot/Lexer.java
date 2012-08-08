import java.util.regex.*;
import java.util.concurrent.Callable;
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

class SourceCode {
  private File source;
  private String resource;
  private String contents;
  private int line;
  private int col;
  private int nchars;

  SourceCode(String source, String resource) {
    this.contents = source;
    this.resource = resource;
    this.line = 1;
    this.col = 1;
    this.nchars = 0;
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
    this.resource = resource;
    this.line = 1;
    this.col = 1;
  }

  public int getCharactersProcessed() {
    return this.nchars;
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
    this.nchars += amount;
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

  public int getCol() {
    return this.col;
  }
}

class LexerMatch {
  private List<Terminal> terminals;
  LexerMatch() { this.terminals = null; }
  LexerMatch(List<Terminal> terminals) { this.terminals = terminals; }
  public List<Terminal> getTerminals() { return this.terminals; }
  public void append(Terminal terminal) {this.terminals.add(terminal);}
}

abstract class TokenMatchCallback implements Callable<LexerMatch> {
  protected Terminal terminal;
  protected LexerState state;
  protected void setContext(Terminal terminal, LexerState state) {
    this.terminal = terminal;
    this.state = state;
  }
  public abstract LexerMatch call();
}

class TokenLexer {
  private Pattern regex;
  private DotParser.TerminalId terminal;
  private TokenMatchCallback handler;

  TokenLexer(Pattern regex, DotParser.TerminalId terminal) {
    this(regex, terminal, null);
  }

  TokenLexer(Pattern regex, DotParser.TerminalId terminal, TokenMatchCallback handler) {
    this.regex = regex;
    this.terminal = terminal;
    this.handler = handler;
  }

  LexerMatch match(SourceCode source, LexerState state) {
    Matcher m = this.regex.matcher(source.getString());
    LexerMatch rval = null;

    String code = source.getString().length() > 20 ? source.getString().substring(0, 20) : source.getString();

    if ( m.find() ) {
      String sourceString = m.group();
      Terminal terminal = null;

      if ( this.terminal != null ) {
        terminal = new Terminal(this.terminal.id(), this.terminal.string(), Utility.base64_encode(sourceString.getBytes()), source.getResource(), source.getLine(), source.getCol());
      }

      source.advance(sourceString.length());

      if ( this.handler != null ) {
        this.handler.setContext(terminal, state);
        return this.handler.call();
      } else {
        ArrayList<Terminal> list = new ArrayList<Terminal>();
        if ( terminal != null )
          list.add(terminal);
        return new LexerMatch(list);
      }
    }
    return rval;
  }
}

class LexerState {
  private ArrayList<Terminal> cache;
  private int square_bracket;
  LexerState() {
    this.cache = new ArrayList<Terminal>();
    this.square_bracket = 0;
  }
  public void add(Terminal terminal) {
    this.cache.add(terminal);
  }
  public List<Terminal> getCache() {
    return this.cache;
  }
  public void clearCache() {
    this.cache = new ArrayList<Terminal>();
  }
  public void square_inc() {
    this.square_bracket++;
  }
  public void square_dec() {
    this.square_bracket--;
  }
  public int square_level() {
    return this.square_bracket;
  }

  private boolean cache_contains(DotParser.TerminalId input) {
    if ( this.cache.size() > 0 ) {
      for ( Terminal t : this.cache ) {
        if ( t.getId() == input.id() ) {
          return true;
        }
      }
    }
    return false;
  }

  private boolean cache_contains_edgeop() {
    return cache_contains(DotParser.TerminalId.TERMINAL_DASHDASH) || cache_contains(DotParser.TerminalId.TERMINAL_ARROW);
  }

  public LexerMatch stmt_end() {
    /*
    stmt_end)
      i) if cache = ['identifier' + 'assign' + 'identifier'], hint = value_assign_hint
      ii) if cache contains edgeop, hint = edge_stmt_hint
      iii) if cache[0] = 'identifier' and cache does not contain edgeop, hint = node_stmt_hint
      iv) if cache[-1] != 'semi', semi = 'semi'
    */

    ArrayList<Terminal> tokens = new ArrayList<Terminal>();
    Terminal hint = null, semi = null;

    if ( this.cache.size() == 0 ) {
      return null;
    }

    if ( this.cache.size() >= 3 &&
         this.cache.get(0).getId() == DotParser.TerminalId.TERMINAL_IDENTIFIER.id() && 
         this.cache.get(1).getId() == DotParser.TerminalId.TERMINAL_ASSIGN.id() &&
         this.cache.get(2).getId() == DotParser.TerminalId.TERMINAL_IDENTIFIER.id() ) {
      DotParser.TerminalId t = DotParser.TerminalId.TERMINAL_VALUE_ASSIGN_HINT;
      hint = new Terminal( t.id(), t.string(), "", "Context-disambiguating token", this.cache.get(0).getLine(), this.cache.get(0).getColumn());
    }
    else if ( cache_contains_edgeop() ) {
      DotParser.TerminalId t = DotParser.TerminalId.TERMINAL_EDGE_STMT_HINT;
      hint = new Terminal( t.id(), t.string(), "", "Context-disambiguating token", this.cache.get(0).getLine(), this.cache.get(0).getColumn());
    }
    else if ( this.cache.get(0).getId() == DotParser.TerminalId.TERMINAL_IDENTIFIER.id() ) {
      DotParser.TerminalId t = DotParser.TerminalId.TERMINAL_NODE_STMT_HINT;
      hint = new Terminal( t.id(), t.string(), "", "Context-disambiguating token", this.cache.get(0).getLine(), this.cache.get(0).getColumn());
    }

    if ( this.cache.get(this.cache.size()-1).getId() != DotParser.TerminalId.TERMINAL_SEMI.id() ) {
      DotParser.TerminalId t = DotParser.TerminalId.TERMINAL_SEMI;
      semi = new Terminal( t.id(), t.string(), "", "Auto-inserted semi-colon", this.cache.get(0).getLine(), this.cache.get(0).getColumn());
    }

    if ( hint != null ) {
      tokens.add(hint);
    }

    tokens.addAll(this.cache);
    
    if ( semi != null ) {
      tokens.add(semi);
    }

    this.clearCache();
    return new LexerMatch(tokens);
  }
}

public class Lexer {
  private static class BackslashNewlineCallback extends TokenMatchCallback {
    /* called on \\[\r\n] */
    public LexerMatch call() {
      return null;
    }
  }
  private static class RightBraceOrEOFCallback extends TokenMatchCallback {
    /* called on }[\r\n]* or EOF */
    public LexerMatch call() {
      if ( this.state.getCache().size() > 0 ) {
        LexerMatch match = this.state.stmt_end();
        match.append(this.terminal);
        return match;
      } else {
        this.state.add(this.terminal);
        LexerMatch match = new LexerMatch(this.state.getCache());
        this.state.clearCache();
        return match;
      }
    }
  }
  private static class LeftBraceCallback extends TokenMatchCallback {
    /* called on {[\r\n]* */
    public LexerMatch call() {
      if ( this.state.getCache().size() > 0 ) {
        this.state.add(this.terminal);
        LexerMatch match = new LexerMatch(this.state.getCache());
        this.state.clearCache();
        return match;
      }
      // output tokens in cache and clear cache.
      return null;
    }
  }
  private static class NewLineCallback extends TokenMatchCallback {
    /* called on [\r\n]+ */
    public LexerMatch call() {
      if ( this.state.square_level() == 0 ) {
        return this.state.stmt_end();
      }
      // if not within square brackets, goto stmt_end.
      return null;
    }
  }
  private static class LeftSquareBracketCallback extends TokenMatchCallback {
    /* called on \\[ */
    public LexerMatch call() {
      if ( this.terminal != null ) {
        this.state.square_inc();
        this.state.add(this.terminal);
      }
      return null;
    }
  }
  private static class RightSquareBracketCallback extends TokenMatchCallback {
    /* called on \\] */
    public LexerMatch call() {
      if ( this.terminal != null ) {
        this.state.square_dec();
        this.state.add(this.terminal);
      }
      return null;
    }
  }
  private static class TokenCallback extends TokenMatchCallback {
    /* Called on all other tokens */
    public LexerMatch call() {
      if ( this.terminal != null ) {
        this.state.add(this.terminal);
      }
      return null;
    }
  }
  public static void main(String[] args) {
    ArrayList<TokenLexer> regex = new ArrayList<TokenLexer>();
    TokenCallback cb = new TokenCallback();
    regex.add( new TokenLexer(Pattern.compile("^digraph(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_DIGRAPH, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^graph(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_GRAPH, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^subgraph(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_SUBGRAPH, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^strict(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_STRICT, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^edge(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_EDGE, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^node(?=[^a-zA-Z_]|$)"), DotParser.TerminalId.TERMINAL_NODE, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^;"), DotParser.TerminalId.TERMINAL_SEMI, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\}[\r\n]*"), DotParser.TerminalId.TERMINAL_RBRACE, new RightBraceOrEOFCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\{[\r\n]*"), DotParser.TerminalId.TERMINAL_LBRACE, new LeftBraceCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\["), DotParser.TerminalId.TERMINAL_LSQUARE, new LeftSquareBracketCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\]"), DotParser.TerminalId.TERMINAL_RSQUARE, new RightSquareBracketCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\u002d\u002d"), DotParser.TerminalId.TERMINAL_DASHDASH, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\u002d\u003e"), DotParser.TerminalId.TERMINAL_ARROW, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^,"), DotParser.TerminalId.TERMINAL_COMMA, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^:"), DotParser.TerminalId.TERMINAL_COLON, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^="), DotParser.TerminalId.TERMINAL_ASSIGN, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\\\[\r\n]"), DotParser.TerminalId.TERMINAL_ASSIGN, new BackslashNewlineCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^([a-zA-Z\u0200-\u0377_]([0-9a-zA-Z\u0200-\u0377_])*|\"(\\\"|[^\"])*?\"|[-]?(\\.[0-9]+|[0-9]+(\\.[0-9]*)?))"), DotParser.TerminalId.TERMINAL_IDENTIFIER, new TokenCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^[\r\n]+"), null, new NewLineCallback()) );
    regex.add( new TokenLexer(Pattern.compile("^\\s+"), null, new TokenCallback()) );

    if ( args.length < 1 ) {
      System.err.println("Usage: Lexer <input file>");
      System.exit(-1);
    }

    try {
      SourceCode code = new SourceCode(new File(args[0]));
      LexerState state = new LexerState();
      ArrayList<Terminal> terminals = new ArrayList<Terminal>();
      int consumed;
      boolean progress = true;

      while (progress) {
        progress = false;
        consumed = code.getCharactersProcessed();
        for ( TokenLexer lexer : regex ) {
          LexerMatch match = lexer.match(code, state);

          if (match != null) {
            terminals.addAll(match.getTerminals());
          }

          if ( consumed < code.getCharactersProcessed() ) {
            progress = true;
            break;
          }
        }
      }

      ArrayList<String> strs = new ArrayList<String>();
      for (Terminal t : terminals) {
        strs.add("  " + t.toString());
      }
      System.out.println("[");
      System.out.println( Utility.join(strs, ",\n") );
      System.out.println("]");
      System.out.flush();
    } catch (IOException e) {
      System.err.println(e);
      System.exit(-1);
    }
  }
}
