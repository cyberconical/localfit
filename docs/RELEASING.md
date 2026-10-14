# Releasing Localfit

This is the checklist for everything that cannot be done from inside the repository: accounts, keys, secrets, the first build and Google Play. Do the steps in order.

## 1. Put the code on GitHub

1. Create an empty repository `cyberconical/localfit` (public, no README, no license; they are already here).
2. Push this folder:
   ```
   git remote add origin git@github.com:cyberconical/localfit.git
   git push -u origin main
   ```
3. In the repository settings enable the **Wiki** (and create one page with any content) so that the "Publish wiki" workflow can fill it. Optional.
4. Optional: under Settings, Branches, protect `main` and require the checks `build` and `test`.

If you use a different owner or name, search the repository for `cyberconical/localfit` and replace it (README, PRIVACY.md, docs, `plugins/run-tracker/package.json`). The Android package ID `io.github.cyberconical.localfit` is set in `.github/workflows/build.yml` (`APP_ID`) and in the plugin's namespace. **It can never be changed after the first upload to Google Play**, so decide now.

## 2. Create the signing key (once)

The same key signs the APK you hand out and the AAB you upload to Google Play (as the *upload key*). Google keeps the real app signing key itself once you use Play App Signing.

```
keytool -genkeypair -v -keystore localfit-upload.keystore -alias localfit \
  -keyalg RSA -keysize 4096 -validity 10000
```

Choose one strong password and use it for both the keystore and the key (the build uses a single password for both). Then:

1. **Back up `localfit-upload.keystore` and the password** in a password manager and on a second device. Never commit them (`.gitignore` blocks `*.keystore`).
2. Create the secret value: `base64 -w0 localfit-upload.keystore` (on macOS: `base64 -i localfit-upload.keystore`).
3. In GitHub, Settings, Secrets and variables, Actions, add two **secrets**:
   - `KEYSTORE_BASE64`: the base64 text
   - `KEYSTORE_PASSWORD`: the password

If you lose the upload key, Google can reset it after identity checks, but APKs installed outside Play would no longer update.

## 3. The first build, and check it

1. GitHub, Actions, "Build Android", "Run workflow" on `main`. Wait a few minutes.
2. If it fails, open the failed step and fix it (the build has never run on GitHub yet; the most likely trouble spots are the Capacitor 8 project template and the signing step). Send me the log, or paste it into an AI assistant together with `.github/workflows/build.yml`.
3. When it is green, download the artifact `localfit-android` and unzip it. You get `localfit.apk` and `localfit.aab`.
4. **Install `localfit.apk` on a real phone** and go through this list. This is the part nobody has tested yet:
   - The app opens and shows the setup (not a blank white screen). If it is blank, the removal of the internet permission may be the cause: set `REMOVE_INTERNET: "false"` in `build.yml` and build again. Please also keep the diagnostic log (Settings) and open an issue.
   - The setup looks right on your phone (all steps, both languages, light and dark), and you can finish it.
   - A plan appears, you can log a session, the Settings page shows "Your plan".
   - "Record with GPS": the permission dialogs appear, the notification shows, recording continues with the screen off, the run can be saved. Test with a real walk.
   - Voice announcements (if you want them) and the vibration cues for intervals.
   - Save and load a backup.
   - Rotate the phone and switch the language.

## 3b. The test channel with Obtainium (branch `dev`)

Work happens on the branch **`dev`**. Every push to `dev` is built, signed and published as a **pre-release** called `dev-<build number>` with `localfit.apk` attached. Obtainium installs these on your phone, so you do not have to download and copy APKs by hand. The five newest dev builds are kept, older ones are deleted automatically.

One-time setup on the phone:

1. In Obtainium, "Add app", paste `https://github.com/cyberconical/localfit`.
2. Open the app's settings in the add dialog and switch on **"Include prereleases"** (without it Obtainium only sees normal releases).
3. Add and install. Later: open Obtainium, "Check for updates", and update.

Notes:

- Dev builds use the same app ID and the same key as the real app, so they update each other and a later stable release installs over them. Your data stays.
- `versionCode` is the build number, so each new dev build is newer than the one before.
- To switch back to stable only, switch "Include prereleases" off.
- Dev builds are not for Google Play. Upload to Play only what you released from `main`.

## 3c. From dev to a real release

1. Push your changes to `dev` and test the dev build on your phone.
2. Open a **pull request from `dev` to `main`** (GitHub offers a "Compare & pull request" button after a push). The checks `build` and `test` run on it.
3. Merge the pull request.
4. Releases, "Draft a new release", new tag (for example `v0.1.0`), target `main`, publish. The build attaches the signed `localfit.apk` and `localfit.aab`.
5. For Google Play, upload that `localfit.aab`, see step 6.

## 4. Optional: a map for your region

The release has no basemap by default (routes are drawn as a line). To bundle one, add a repository **variable** (not secret) `BASEMAP_BBOX` with `west,south,east,north`, for example `13.0,52.3,13.8,52.7` for Berlin, and build again. Keep the area small, see `map/README.md`. The official build uses Berlin (`12.95,52.30,13.85,52.72`). The setup screen tells users that street maps are only available for Berlin, Germany: when you change the region, also change `MAP_REGION` in `index.html`. If you do this, the app uses OpenStreetMap data; the copyright notice is already in the README and in `map/README.md`. Consider adding "© OpenStreetMap contributors" to the Play description.

## 5. Take screenshots

The old screenshots belonged to the previous app and were removed. Take 4 to 8 phone screenshots from the real app (demo data is fine, never real routes of yours): the setup, the week view, a plan, a recording, the stats, German and dark mode. Play wants 16:9 or 9:16 PNG or JPEG between 320 and 3840 px on the long side. Put them into `docs/screenshots/` and into the README if you like.

## 6. Google Play Console

### Account (once)

1. Create a developer account at https://play.google.com/console. One-time fee of 25 USD. You must verify your identity (a government ID and a payment profile), which can take a few days.
2. Choose "personal" or "organization". **Personal accounts created after 13 November 2023 must run a closed test with at least 12 testers for 14 continuous days before they can apply for production access.** An organization account (needs a D-U-N-S number) does not. Plan for this: it is the longest step.

### Create the app

1. "Create app": name `Localfit: Private Training` (or just `Localfit`), default language English (United States) or German, type App, free.
2. Accept the declarations. Note that the package ID is fixed by the first AAB you upload.
3. Dashboard, "Set up your app": fill in everything listed there. The texts are in `docs/store/listing.md`:
   - Privacy policy URL: `https://github.com/cyberconical/localfit/blob/main/PRIVACY.md`
   - App access: all functionality available without login
   - Ads: none
   - Content rating: questionnaire, expect "Everyone"
   - Target audience: 18+
   - Data safety: no data collected or shared (answers in `listing.md`)
   - Health apps declaration: fitness app, no medical features
   - Government apps, financial features: no
4. **Foreground service declaration** (App content, "Foreground service permissions"): type Location. Answers and the screen recording you need to make are described in `docs/store/listing.md`.
5. Store listing: the texts from `listing.md`, the icon `docs/store/icon-512.png`, the feature graphic `docs/store/feature-graphic-1024x500.png`, your screenshots. Add a German translation if you like ("Manage translations").
6. Contact email for the listing: use an address you are happy to make public.

### Upload the first build

1. Testing, Closed testing, "Create track" (or use the default "Alpha"), "Create new release".
2. Accept Play App Signing when asked (recommended; your upload key is the one from step 2).
3. Upload `localfit.aab` from the release or the artifact. Google checks the target API (36) and the permissions.
4. Release name and notes (for example "First test version").
5. Testers: create an email list with 12 or more people who have a Google account and an Android phone. Send them the opt-in link from the track page. They must **stay opted in for 14 days in a row**.
6. After the time has passed: Dashboard, "Apply for production" (answer the questions about your testing), then create a production release with the same or a newer AAB.

### Every later version

1. GitHub, Releases, "Draft a new release", new tag such as `v1.0.1`, publish. The build attaches `localfit.apk` and `localfit.aab`. `versionCode` is the build number and rises by itself.
2. Download the new `localfit.aab`, create a new release on your Play track and upload it.

## 7. Before you call it done

- Check that the name is free to use: search "Localfit" in the Play Store, in the trademark databases (TMview, DPMA, USPTO) and on GitHub. Names can collide even when the Play Store shows nothing.
- Google Play's target API requirement rises every year (new apps and updates must target API 36 from 31 August 2026, with extensions possible until 1 November 2026). The build checks `targetSdkVersion = 36`; update it together with Capacitor when Google raises the level again.
- Keep the keystore backup somewhere safe.

## Facts the app depends on

- Minimum Android 7.0 (API 24), target and compile SDK 36, Capacitor 8, Node 22, Java 21, Gradle from the Capacitor template.
- Permissions in the release: precise and approximate location, foreground service (location), notifications, wake lock, vibration. No internet, no background location.
- The app never talks to a network. This is the claim in the store listing and in `PRIVACY.md`. The CI check "INTERNET permission is still in the merged manifest" protects it.
