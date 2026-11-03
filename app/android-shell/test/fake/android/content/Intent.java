package android.content;
import java.util.*;
/** Tiruan minimal: hanya mencatat apa yang diminta aplikasi. */
public class Intent {
    public String action, type, dataString, chooserTitle; public Intent wrapped;
    public Map<String, String> extras = new LinkedHashMap<>();
    public Intent() {}
    public Intent(String action) { this.action = action; }
    public Intent setType(String t) { this.type = t; return this; }
    public Intent putExtra(String k, String v) { extras.put(k, v); return this; }
    public static Intent createChooser(Intent target, CharSequence title) { Intent c = new Intent("android.intent.action.CHOOSER"); c.wrapped = target; c.chooserTitle = String.valueOf(title); return c; }
}
