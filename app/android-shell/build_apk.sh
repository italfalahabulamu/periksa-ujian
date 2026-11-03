#!/usr/bin/env bash
# Merakit APK pembungkus WebView dari app/mock/index.html tanpa Android SDK.
# Butuh: java, serta apktool.jar dan uber-apk-signer.jar (lihat README.md).
# Pemakaian: build_apk.sh <folder-alat> <folder-keluaran>
set -euo pipefail
TOOLS="${1:?folder berisi apktool.jar dan uber-apk-signer.jar}"
OUT="${2:?folder keluaran}"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$OUT"
cp -r "$HERE"/AndroidManifest.xml "$HERE"/apktool.yml "$HERE"/smali "$HERE"/res "$WORK"/
mkdir -p "$WORK/assets" && cp "$HERE/../mock/index.html" "$WORK/assets/index.html"
java -jar "$TOOLS/apktool.jar" b "$WORK" -p "$WORK/fw" -o "$WORK/unsigned.apk"
java -jar "$TOOLS/uber-apk-signer.jar" -a "$WORK/unsigned.apk" -o "$WORK/signed" --allowResign
cp "$WORK"/signed/*aligned*Signed.apk "$OUT/periksa-ujian-mock.apk"
java -jar "$TOOLS/uber-apk-signer.jar" --onlyVerify -a "$OUT/periksa-ujian-mock.apk"
echo "APK: $OUT/periksa-ujian-mock.apk"
