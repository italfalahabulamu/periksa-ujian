package android.webkit;
import android.content.Intent; import android.net.Uri;
public class WebChromeClient {
    public WebChromeClient() {}
    public boolean onShowFileChooser(WebView w, ValueCallback<Uri[]> cb, FileChooserParams p) { return false; }
    public static abstract class FileChooserParams {
        public abstract Intent createIntent();
        public static Uri[] parseResult(int resultCode, Intent data) {
            if (resultCode != -1 || data == null || data.dataString == null) return null;
            return new Uri[]{new Uri(data.dataString)};
        }
    }
}
