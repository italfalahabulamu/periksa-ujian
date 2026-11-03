package android.webkit;
import android.content.Context; import android.view.View;
public class WebView extends View {
    public static WebView last; public WebSettings settings = new WebSettings(); public String url, jsName; public Object jsObj;
    public WebViewClient client; public WebChromeClient chrome; public boolean canBack; public int backs;
    public WebView(Context c) { super(c); last = this; }
    public WebSettings getSettings() { return settings; }
    public void setWebViewClient(WebViewClient c) { client = c; }
    public void setWebChromeClient(WebChromeClient c) { chrome = c; }
    public void addJavascriptInterface(Object o, String n) { jsObj = o; jsName = n; }
    public void loadUrl(String u) { url = u; }
    public boolean canGoBack() { return canBack; }
    public void goBack() { backs++; }
}
