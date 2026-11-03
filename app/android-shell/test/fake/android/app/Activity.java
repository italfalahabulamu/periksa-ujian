package android.app;
import android.content.*; import android.os.Bundle; import android.view.View;
public class Activity extends Context {
    public static final int RESULT_CANCELED = 0, RESULT_OK = -1;
    public View contentView; public Intent started, startedForResult; public int startedCode = -999, superBack = 0;
    protected void onCreate(Bundle b) {}
    public void setContentView(View v) { contentView = v; }
    public void startActivity(Intent i) { started = i; }
    public void startActivityForResult(Intent i, int code) { startedForResult = i; startedCode = code; }
    protected void onActivityResult(int req, int res, Intent data) {}
    public void onBackPressed() { superBack++; }
}
