package org.broadinstitute.compositetask;

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

import org.broadinstitute.parser.SourceCode;

public class CompositeTaskSourceCode implements SourceCode {
  private File source;
  private String resource;
  private String contents;
  private int line;
  private int col;
  private StringBuilder currentLine;
  private List<String> lines;

  CompositeTaskSourceCode(String source, String resource) {
    init(source, resource);
  }

  CompositeTaskSourceCode(File source) throws IOException {
    this(source, "utf-8", source.getCanonicalPath());
  }

  CompositeTaskSourceCode(File source, String resource) throws IOException {
    this(source, "utf-8", resource);
  }

  CompositeTaskSourceCode(File source, String encoding, String resource) throws IOException, FileNotFoundException {
    FileInputStream in = new FileInputStream(source);
    FileChannel channel = in.getChannel();
    MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ_ONLY, 0, channel.size());
    Charset cs = Charset.forName(encoding);
    CharsetDecoder cd = cs.newDecoder();
    CharBuffer cb = cd.decode(buffer);
    in.close();

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
        this.lines.add(this.currentLine.toString());
        this.currentLine = new StringBuilder();
        this.line++;
        this.col = 1;
      } else {
        this.currentLine.append((char)b);
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
    return this.lines.get(lineno-1);
  }

  public List<String> getLines() {
    return this.lines;
  }
}
