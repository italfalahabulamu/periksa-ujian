package id.periksaujian.mock;
import android.app.Activity; import android.content.Intent; import android.net.Uri; import android.webkit.*;
import java.lang.reflect.Method;

/** Menjalankan kode native hasil rakitan terhadap kerangka Android tiruan dan memeriksa apa yang diminta dari Android. */
public class Harness {
    static int pass = 0, fail = 0;
    static void check(String name, boolean ok, Object detail) { if (ok) { pass++; System.out.println("  ok    " + name); } else { fail++; System.out.println("  GAGAL " + name + " :: " + detail); } }
    static final class Cb implements ValueCallback<Uri[]> { boolean called; Uri[] got = new Uri[0]; public void onReceiveValue(Uri[] v) { called = true; got = v; } }
    static final class Params extends WebChromeClient.FileChooserParams { final Intent i = new Intent("android.intent.action.GET_CONTENT"); public Intent createIntent() { return i; } }

    public static void main(String[] args) throws Exception {
        MainActivity a = new MainActivity();
        a.onCreate(null);
        WebView w = WebView.last;
        System.out.println("[onCreate]");
        check("WebView dibuat dan dipasang sebagai isi layar", w != null && a.contentView == w, a.contentView);
        check("JavaScript aktif", w.settings.js, null);
        check("penyimpanan DOM (localStorage) aktif", w.settings.dom, null);
        check("memuat berkas web dari aset aplikasi", "file:///android_asset/index.html".equals(w.url), w.url);
        check("WebViewClient dipasang (navigasi tetap di dalam aplikasi)", w.client != null, null);
        check("WebChromeClient aplikasi dipasang", w.chrome instanceof Chrome, w.chrome);
        check("bridge terdaftar dengan nama AndroidBridge", "AndroidBridge".equals(w.jsName) && w.jsObj instanceof Bridge, w.jsName);

        System.out.println("[bridge: bagikan CSV]");
        Method share = Bridge.class.getMethod("share", String.class, String.class);
        check("share() bertanda @JavascriptInterface (wajib agar bisa dipanggil dari JS)", share.isAnnotationPresent(JavascriptInterface.class), null);
        for (Method m : Bridge.class.getDeclaredMethods()) if (m.getDeclaringClass() == Bridge.class && java.lang.reflect.Modifier.isPublic(m.getModifiers()) && !m.isAnnotationPresent(JavascriptInterface.class))
            check("tidak ada metode publik tanpa anotasi: " + m.getName(), false, m);
        String csv = "﻿kode_peserta;benar\r\n8A-001;31\r\n";
        share.invoke(w.jsObj, "nilai-8A.csv", csv);
        Intent c = a.started;
        check("memulai activity pemilih (chooser)", c != null && "android.intent.action.CHOOSER".equals(c.action), c == null ? null : c.action);
        Intent t = c == null ? null : c.wrapped;
        check("aksi ACTION_SEND bertipe text/plain", t != null && "android.intent.action.SEND".equals(t.action) && "text/plain".equals(t.type), t == null ? null : t.action + " " + t.type);
        check("isi CSV dikirim utuh (termasuk BOM dan CRLF)", t != null && csv.equals(t.extras.get("android.intent.extra.TEXT")), t == null ? null : t.extras);
        check("nama berkas menjadi subjek", t != null && "nilai-8A.csv".equals(t.extras.get("android.intent.extra.SUBJECT")), t == null ? null : t.extras);
        check("judul pemilih tidak kosong", c != null && c.chooserTitle != null && !c.chooserTitle.isEmpty(), c == null ? null : c.chooserTitle);

        System.out.println("[pemilih berkas untuk foto LJK]");
        WebChromeClient ch = w.chrome; Params p = new Params(); Cb cb1 = new Cb();
        boolean handled = ch.onShowFileChooser(w, cb1, p);
        check("pemilih ditangani aplikasi (return true)", handled, null);
        check("callback disimpan sebagai pending", a.pending == cb1, null);
        check("activity pemilih dimulai dengan intent dari FileChooserParams", a.startedForResult == p.i && a.startedCode == 1, a.startedCode);
        Intent data = new Intent(); data.dataString = "content://media/external/images/42";
        a.onActivityResult(a.startedCode, Activity.RESULT_OK, data);
        check("hasil pilihan diteruskan ke WebView sebagai Uri", cb1.called && cb1.got != null && cb1.got.length == 1 && "content://media/external/images/42".equals(cb1.got[0].toString()), cb1.got);
        check("pending dibersihkan setelah hasil", a.pending == null, null);
        a.onActivityResult(1, Activity.RESULT_OK, data);
        check("hasil ganda tanpa pending tidak menyebabkan galat", true, null);

        Cb cb2 = new Cb(), cb3 = new Cb();
        ch.onShowFileChooser(w, cb2, p);
        ch.onShowFileChooser(w, cb3, p);
        check("pemilih kedua membatalkan yang pertama (callback menerima null)", cb2.called && cb2.got == null, cb2.got);
        check("callback terbaru menjadi pending", a.pending == cb3, null);
        a.onActivityResult(1, Activity.RESULT_CANCELED, null);
        check("pembatalan pengguna: callback menerima null, bukan menggantung", cb3.called && cb3.got == null && a.pending == null, cb3.got);

        System.out.println("[tombol kembali]");
        w.canBack = true; a.onBackPressed();
        check("ada riwayat: WebView mundur satu layar, aplikasi tidak keluar", w.backs == 1 && a.superBack == 0, w.backs + "/" + a.superBack);
        w.canBack = false; a.onBackPressed();
        check("tanpa riwayat: aplikasi menutup (pemanggilan super)", w.backs == 1 && a.superBack == 1, w.backs + "/" + a.superBack);

        System.out.println("\n" + pass + " lulus, " + fail + " gagal");
        System.exit(fail == 0 ? 0 : 1);
    }
}
