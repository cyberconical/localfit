#!/usr/bin/env bash
# Prepares the Android project in ./android from index.html. Used by the GitHub build (.github/workflows/build.yml)
# and meant for the F-Droid build recipe, so both make the same app. It does not run Gradle:
#   tools/build-android.sh && cd android && ./gradlew assembleRelease
#
# Needs: Node 22, Java 21 (Gradle), Python 3 with Pillow (launcher icons), the Android SDK (ANDROID_HOME).
# Settings (environment, all optional):
#   VERSION_NAME, VERSION_CODE   default: version.properties
#   REGION_FILE, REGION_BBOX     basemap extract (.pmtiles) and its box "west,south,east,north"; default: map/data/berlin.*
#   APP_ID, APP_NAME             default: io.github.cyberconical.localfit, LocalFit
#   REMOVE_INTERNET              "true" (default) removes the INTERNET permission, the app never uses the network
set -euo pipefail
cd "$(dirname "$0")/.."

APP_ID=${APP_ID:-io.github.cyberconical.localfit}
APP_NAME=${APP_NAME:-LocalFit}
REMOVE_INTERNET=${REMOVE_INTERNET:-true}
prop() { sed -n "s/^$1=//p" version.properties | head -1 | tr -d '\r'; }
VERSION_NAME=${VERSION_NAME:-$(prop versionName)}
VERSION_CODE=${VERSION_CODE:-$(prop versionCode)}
[ -n "$VERSION_NAME" ] && [ -n "$VERSION_CODE" ] || { echo "version.properties has no versionName/versionCode" >&2; exit 1; }
REGION_FILE=${REGION_FILE:-map/data/berlin.pmtiles}
if [ -z "${REGION_BBOX:-}" ]; then
  REGION_BBOX=$(python3 -c "import json; print(','.join(str(x) for x in json.load(open('map/data/berlin.json'))['bbox']))")
fi
echo "LocalFit $VERSION_NAME (code $VERSION_CODE), map: $REGION_FILE [$REGION_BBOX]"

rm -rf www android
mkdir -p www/map
cp index.html www/
cp -r fonts www/
# the map support files; the big region data (map/data) is cut into pieces below
find map -mindepth 1 -maxdepth 1 ! -name data -exec cp -r {} www/map/ \;
if [ -f "$REGION_FILE" ]; then
  # 1 MB pieces: the Android file server cannot do partial reads of one big file (see index.html, baseSource)
  mkdir -p www/map/region
  split -b 1048576 -d -a 4 --additional-suffix=.pmtiles "$REGION_FILE" www/map/region/p
  BBOX="$REGION_BBOX" python3 -c "import json,os; b=[float(x) for x in os.environ['BBOX'].split(',')]; json.dump({'bbox':b}, open('www/map/region.json','w'))"
  echo "basemap pieces: $(ls www/map/region | wc -l)"
else
  echo "No basemap file, using the line map"
fi

npm ci --no-audit --no-fund
echo "{\"appId\":\"$APP_ID\",\"appName\":\"$APP_NAME\",\"webDir\":\"www\"}" > capacitor.config.json
npx cap add android

# No Google services and no automatic cloud backup of app data
python3 - <<'PY'
import re
p = "android/app/build.gradle"
t = open(p).read()
t = re.sub(r"try \{\s*def servicesJSON.*?\n\}\s*catch\(Exception e\) \{.*?\n\}\n?", "", t, flags=re.S)
# keep the big map file uncompressed in the APK, so the WebView can read pieces of it without unpacking it from the start
t = re.sub(r"(?m)^android \{\n", "android {\n    androidResources {\n        noCompress 'pmtiles'\n    }\n", t, count=1)
open(p, "w").write(t)
p = "android/build.gradle"
t = open(p).read()
t = "\n".join(l for l in t.splitlines() if "com.google.gms:google-services" not in l) + "\n"
open(p, "w").write(t)
PY
sed -i 's/android:allowBackup="true"/android:allowBackup="false"/' android/app/src/main/AndroidManifest.xml
if [ "$REMOVE_INTERNET" = "true" ]; then sed -i '/android.permission.INTERNET/d' android/app/src/main/AndroidManifest.xml; fi
grep -q "noCompress 'pmtiles'" android/app/build.gradle || { echo "pmtiles would be compressed in the APK" >&2; exit 1; }
if grep -rn "google-services" android --include=*.gradle; then echo "Google services plugin is still included" >&2; exit 1; fi
grep -q 'android:allowBackup="false"' android/app/src/main/AndroidManifest.xml || { echo "allowBackup is not disabled" >&2; exit 1; }
grep -q 'targetSdkVersion = 36' android/variables.gradle || { echo "targetSdkVersion is not 36" >&2; cat android/variables.gradle; exit 1; }

# launcher icons from the one drawing in tools/icons.py (same mark as the store icon)
python3 -c "import PIL" 2>/dev/null || pip install --break-system-packages pillow
python3 tools/icons.py android android/app/src/main/res

npx cap sync android
sed -i "s/versionCode 1/versionCode $VERSION_CODE/" android/app/build.gradle
sed -i "s/versionName \"1.0\"/versionName \"$VERSION_NAME\"/" android/app/build.gradle
grep -q "versionCode $VERSION_CODE\$" android/app/build.gradle || { echo "versionCode was not set" >&2; exit 1; }
grep -q "versionName \"$VERSION_NAME\"" android/app/build.gradle || { echo "versionName was not set" >&2; exit 1; }
grep -n "versionCode\|versionName\|applicationId" android/app/build.gradle
