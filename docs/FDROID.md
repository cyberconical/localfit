# F-Droid

F-Droid builds the app itself from the source in this repository and signs it with its own key. You do not upload an APK. It can run in parallel to Google Play.

## Done in this repository

- `fastlane/metadata/android/en-US/`: title, descriptions, icon, feature graphic and screenshots, as F-Droid reads them. Generated from `docs/store/listing.md` and the store images with `python3 tools/fastlane.py`. Run it again after you change the listing or the images.

## Still open (needed before the merge request)

1. **A fixed `versionCode` in the source.** Today the CI build sets it to the build number (`github.run_number`), which F-Droid cannot see. The version has to live in a file in the repository and be used by the CI as well.
2. **One build script for CI and F-Droid.** The Android project is generated during the build (`npx cap add android`, patches for Google services, backup, internet permission, icons). F-Droid needs the same steps in its build recipe, so they should move from `build.yml` into a script in `tools/` that both call.
3. **The map.** The CI downloads the Berlin extract from build.protomaps.com while building. For F-Droid the map data must come from a source it accepts (a file in the repository or a fixed download), otherwise the F-Droid version has no map. Map data is © OpenStreetMap contributors (ODbL).
4. **Changelogs.** One short file per version: `fastlane/metadata/android/en-US/changelogs/<versionCode>.txt` (500 characters at most).
5. **A tagged release** whose tag matches the version name (for example `v0.3.0`).

## Steps on GitLab (you)

1. Open https://gitlab.com/fdroid/fdroiddata and click **Fork**. Pick your own namespace. (Do not use "New project": a fork is what is needed.)
2. When the points above are done, the build file `metadata/io.github.cyberconical.localfit.yml` is added to the fork and a merge request is opened against `fdroid/fdroiddata`. Reviewers will ask questions; answer them in the merge request.
3. After the merge it takes about 24 to 48 hours until the app shows up in F-Droid.

## Good to know

- F-Droid signs with its own key. The F-Droid, Play and GitHub (Obtainium) builds therefore have different signatures and cannot update each other. To switch, make a backup in the app, uninstall, install the other build and restore the backup.
- Reviewers decide whether npm (used by Capacitor) is acceptable for the build. Expect questions.
