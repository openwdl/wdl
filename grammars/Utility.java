import java.util.Collection;
import java.util.Iterator;
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
}
