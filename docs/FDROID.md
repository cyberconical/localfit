# F-Droid

F-Droid builds the app itself from the source in this repository and signs it with its own key. You do not upload an APK. It can run in parallel to Google Play.

## Done in this repository

- **Fixed version.** `version.properties` holds `versionName` and `versionCode` (the CI checks both and that the release tag matches). Test builds from `dev` count up from it.
- **One build script.** `tools/build-android.sh` makes the Android project; the GitHub build and F-Droid use the same one. Dependencies are pinned in `package.json` and `package-lock.json`.
- **The Berlin map is in the repository** (`map/data/berlin.pmtiles`, 37 MB, © OpenStreetMap contributors, ODbL, extract of a Protomaps build), so no download is needed while building.
- **Changelog** per version in `fastlane/metadata/android/en-US/changelogs/<versionCode>.txt`.
- **Draft build file** in `docs/fdroid/`.
- `fastlane/metadata/android/en-US/`: title, descriptions, icon, feature graphic and screenshots, as F-Droid reads them. Generated from `docs/store/listing.md` and the store images with `python3 tools/fastlane.py`. Run it again after you change the listing or the images.

## Still open

- **Node 22 on the F-Droid build server.** Capacitor 8 needs Node 22; the build file installs Python for the icons but not yet Node. The reviewers will say what the build server offers.
- **Gradle.** The build uses the Gradle wrapper that Capacitor generates, which downloads Gradle. F-Droid may want its own Gradle instead.
- **First test.** Run `fdroid lint` and `fdroid build` on the build file (it is a draft in `docs/fdroid/`), or let the GitLab pipeline of the fork do it.

## Steps on GitLab (you)

1. Open https://gitlab.com/fdroid/fdroiddata and click **Fork**. Pick your own namespace. (Do not use "New project": a fork is what is needed.)
2. When the points above are done, the build file `metadata/io.github.cyberconical.localfit.yml` (draft: `docs/fdroid/`) is added to the fork and a merge request is opened against `fdroid/fdroiddata`. Reviewers will ask questions; answer them in the merge request.
3. After the merge it takes about 24 to 48 hours until the app shows up in F-Droid.

## Good to know

- F-Droid signs with its own key. The F-Droid, Play and GitHub (Obtainium) builds therefore have different signatures and cannot update each other. To switch, make a backup in the app, uninstall, install the other build and restore the backup.
- Reviewers decide whether npm (used by Capacitor) is acceptable for the build. Expect questions.
