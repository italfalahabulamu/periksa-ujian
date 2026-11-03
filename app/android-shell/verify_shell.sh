#!/usr/bin/env bash
# Verifikasi statis + perilaku kode native APK tanpa emulator.
# 1) dex -> jar (dex2jar), 2) cek referensi API dan override terhadap android.jar (stub), 3) jalankan di JVM
# terhadap kerangka Android tiruan (test/fake) dan periksa permintaan ke Android (test/harness).
# Pemakaian: verify_shell.sh <apk> <android.jar> <folder-dex2jar> <folder-kerja>
set -euo pipefail
APK="${1:?apk}"; STUB="${2:?android.jar (stub API 33)}"; D2J="${3:?folder dex-tools-v2.4}"; W="${4:?folder kerja}"
HERE="$(cd "$(dirname "$0")" && pwd)"; T="$HERE/test"
rm -rf "$W"; mkdir -p "$W/cls" "$W/fakecls" "$W/hcls"
python3 -I - "$APK" "$W" <<'PY'
import sys, zipfile
apk, w = sys.argv[1:3]
zipfile.ZipFile(apk).extract('classes.dex', w)
PY
bash "$D2J/d2j-dex2jar.sh" -f -o "$W/app.jar" "$W/classes.dex" >/dev/null 2>&1
# dex2jar tidak menulis stackmap frame; turunkan versi class ke 49 agar JVM memakai verifier inferensi tipe lama
python3 -I - "$W/app.jar" "$W/app49.jar" <<'PY'
import sys, zipfile
src = zipfile.ZipFile(sys.argv[1]); dst = zipfile.ZipFile(sys.argv[2], 'w', zipfile.ZIP_DEFLATED)
for i in src.infolist():
    d = src.read(i.filename)
    if i.filename.endswith('.class'): d = d[:6] + (49).to_bytes(2, 'big') + d[8:]
    dst.writestr(i.filename, d)
dst.close()
PY
javac -d "$W/cls" "$T/Check.java" 2>&1 | grep -v "Picked up" || true
for c in MainActivity Chrome Bridge; do javap -c -p -cp "$W/app.jar:$STUB" "id.periksaujian.mock.$c" 2>&1 | grep -v "Picked up"; done > "$W/javap.txt"
echo "== 1. API dan verifier =="
java -cp "$W/cls" Check "$W/app49.jar" "$STUB" "$W/javap.txt" 2>&1 | grep -v "Picked up"
echo "== 2. Perilaku di JVM (kerangka Android tiruan) =="
javac -d "$W/fakecls" $(find "$T/fake" -name '*.java') 2>&1 | grep -v "Picked up" || true
javac -cp "$W/fakecls:$W/app49.jar" -d "$W/hcls" "$T/harness/id/periksaujian/mock/Harness.java" 2>&1 | grep -v "Picked up" || true
java -cp "$W/hcls:$W/fakecls:$W/app49.jar" id.periksaujian.mock.Harness 2>&1 | grep -v "Picked up"
