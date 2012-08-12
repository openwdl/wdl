import java.io.File;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.nio.channels.FileChannel;
import java.nio.MappedByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.nio.CharBuffer;
import java.util.ArrayList;
import java.util.List;
import java.io.FileInputStream;

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
