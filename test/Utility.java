import java.util.Collection;
import java.util.Iterator;
import java.io.IOException;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.nio.*;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;
class Utility {
  public static String join(Collection<?> s, String delimiter) {
    StringBuilder builder = new StringBuilder();
    Iterator iter = s.iterator();
    while (iter.hasNext()) {
      builder.append(iter.next());
      if (!iter.hasNext()) {
        break;
      }
      builder.append(delimiter);
    }
    return builder.toString();
  }
  public static String getIndentString(int spaces) {
    StringBuilder sb = new StringBuilder();
    for(int i = 0; i < spaces; i++) {
      sb.append(' ');
    }
    return sb.toString();
  }
  public static String base64_encode(byte[] bytes) {
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
  public static String readStdin() throws IOException {
    InputStreamReader stream = new InputStreamReader(System.in, "utf-8");
    char buffer[] = new char[System.in.available()];
    try {
      stream.read(buffer, 0, System.in.available());
    } finally {
      stream.close();
    }
    return new String(buffer);
  }
  public static String readFile(String path) throws IOException {
    FileInputStream stream = new FileInputStream(new File(path));
    try {
      FileChannel fc = stream.getChannel();
      MappedByteBuffer bb = fc.map(FileChannel.MapMode.READ_ONLY, 0, fc.size());
      /* Instead of using default, pass in a decoder. */
      return Charset.defaultCharset().decode(bb).toString();
    }
    finally {
      stream.close();
    }
  }
}
