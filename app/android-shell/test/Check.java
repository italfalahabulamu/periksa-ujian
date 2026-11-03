import java.lang.reflect.*;
import java.net.*;
import java.util.*;
import java.util.regex.*;

/** Memeriksa referensi API di bytecode (hasil javap) terhadap android.jar, dan menautkan kelas aplikasi lewat verifier JVM. */
public class Check {
    static ClassLoader cl;
    static Class<?> prim(String d) {
        switch (d) { case "I": return int.class; case "Z": return boolean.class; case "V": return void.class; case "J": return long.class;
            case "B": return byte.class; case "C": return char.class; case "S": return short.class; case "F": return float.class; case "D": return double.class; }
        return null;
    }
    static Class<?> typeOf(String d) throws Exception {
        if (d.startsWith("[")) return Array.newInstance(typeOf(d.substring(1)), 0).getClass();
        if (d.startsWith("L")) return Class.forName(d.substring(1, d.length() - 1).replace('/', '.'), false, cl);
        return prim(d);
    }
    static List<String> params(String desc) {
        List<String> out = new ArrayList<>();
        int i = 1;
        while (desc.charAt(i) != ')') {
            int j = i;
            while (desc.charAt(j) == '[') j++;
            if (desc.charAt(j) == 'L') j = desc.indexOf(';', j);
            out.add(desc.substring(i, j + 1));
            i = j + 1;
        }
        return out;
    }
    static boolean find(Class<?> c, String name, Class<?>[] p, Class<?> ret, boolean wantStatic) {
        for (Class<?> k = c; k != null; k = k.getSuperclass()) {
            for (Method m : k.getDeclaredMethods())
                if (m.getName().equals(name) && Arrays.equals(m.getParameterTypes(), p) && m.getReturnType() == ret) return !wantStatic || Modifier.isStatic(m.getModifiers());
            for (Class<?> i : k.getInterfaces()) if (find(i, name, p, ret, wantStatic)) return true;
        }
        for (Class<?> i : c.getInterfaces()) if (find(i, name, p, ret, wantStatic)) return true;
        return false;
    }
    public static void main(String[] a) throws Exception {
        cl = new URLClassLoader(new URL[]{new java.io.File(a[0]).toURI().toURL(), new java.io.File(a[1]).toURI().toURL()}, null);
        int ok = 0, bad = 0;
        Pattern P = Pattern.compile("(invokevirtual|invokespecial|invokestatic|invokeinterface)\\s+#\\d+(?:,\\s*\\d+)?\\s*//\\s*(?:Interface)?Method\\s+([^.\\s]+)\\.\"?([^:\"]+)\"?:(\\(.*)");
        for (String line : new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(a[2]))).split("\n")) {
            Matcher m = P.matcher(line.trim());
            if (!m.find()) continue;
            String kind = m.group(1), owner = m.group(2), name = m.group(3), desc = m.group(4).trim();
            try {
                Class<?> c = Class.forName(owner.replace('/', '.'), false, cl);
                List<String> ps = params(desc);
                Class<?>[] pt = new Class<?>[ps.size()];
                for (int i = 0; i < pt.length; i++) pt[i] = typeOf(ps.get(i));
                Class<?> rt = typeOf(desc.substring(desc.indexOf(')') + 1));
                boolean found;
                if (name.equals("<init>")) { try { c.getDeclaredConstructor(pt); found = true; } catch (NoSuchMethodException e) { found = false; } }
                else found = find(c, name, pt, rt, kind.equals("invokestatic"));
                if (found) ok++; else { bad++; System.out.println("TIDAK ADA: " + kind + " " + owner + "." + name + desc); }
            } catch (Throwable t) { bad++; System.out.println("GAGAL MUAT: " + owner + "." + name + " -> " + t); }
        }
        System.out.println("referensi API: " + ok + " cocok, " + bad + " bermasalah");

        // override harus benar-benar menimpa metode Android (kalau tidak, tidak pernah dipanggil)
        Object[][] ov = {
            {"android.webkit.WebChromeClient", "onShowFileChooser", new String[]{"android.webkit.WebView", "android.webkit.ValueCallback", "android.webkit.WebChromeClient$FileChooserParams"}, boolean.class},
            {"android.app.Activity", "onActivityResult", new String[]{"int", "int", "android.content.Intent"}, void.class},
            {"android.app.Activity", "onBackPressed", new String[]{}, void.class},
            {"android.app.Activity", "onCreate", new String[]{"android.os.Bundle"}, void.class}};
        for (Object[] o : ov) {
            Class<?> sup = Class.forName((String) o[0], false, cl);
            String[] pn = (String[]) o[2];
            Class<?>[] pt = new Class<?>[pn.length];
            for (int i = 0; i < pn.length; i++) { String n = pn[i]; Class<?> pc = switch (n) { case "int" -> int.class; default -> Class.forName(n, false, cl); }; pt[i] = pc; }
            Method mm = null;
            for (Class<?> k = sup; k != null && mm == null; k = k.getSuperclass()) try { mm = k.getDeclaredMethod((String) o[1], pt); } catch (NoSuchMethodException e) { }
            boolean exists = mm != null && mm.getReturnType() == o[3] && !Modifier.isFinal(mm.getModifiers()) && !Modifier.isStatic(mm.getModifiers());
            System.out.println((exists ? "override sah:   " : "OVERRIDE SALAH: ") + o[0] + "." + o[1] + (mm != null ? "  [" + Modifier.toString(mm.getModifiers()) + "]" : ""));
            if (!exists) bad++;
        }
        // verifier JVM: muat + tautkan semua kelas aplikasi (verifikasi tipe bytecode)
        for (String n : new String[]{"id.periksaujian.mock.MainActivity", "id.periksaujian.mock.Chrome", "id.periksaujian.mock.Bridge"}) {
            try { Class.forName(n, true, cl); System.out.println("lolos verifier JVM: " + n); }
            catch (Throwable t) { bad++; System.out.println("GAGAL VERIFIER: " + n + " -> " + t); }
        }
        System.exit(bad == 0 ? 0 : 1);
    }
}
