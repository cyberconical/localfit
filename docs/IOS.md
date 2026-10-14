# LocalFit for iPhone (App Store): what it takes

Status: **not started.** The Android app is ready for Google Play; the iPhone version needs real work first. This page is the honest list.

## What already works on iOS

The app itself (`index.html`) is a web app and runs in Capacitor's iOS WebView. The Capacitor plugins for files and sharing (`@capacitor/filesystem`, `@capacitor/share`) support iOS. Plan, log, habits, stats, backup, language, dark mode all work unchanged.

## What has to be built

1. **The GPS plugin in Swift.** `plugins/run-tracker` is Android-only (Java foreground service). The app talks to it through these methods, and an iOS plugin with the same names and results makes the JavaScript work without changes: `start`, `pause`, `resume`, `stop`, `getStatus`, `getFixes`, `saveState`, `testVoice`, `diagLog`, `getLog`, `clearLog`, `setLogEnabled`.
   - Location: `CLLocationManager`, `allowsBackgroundLocationUpdates = true`, `showsBackgroundLocationIndicator = true`, capability "Background Modes: Location updates".
   - Voice announcements: `AVSpeechSynthesizer` (with an audio session that ducks music).
   - Interval cues: iOS has no vibration patterns like Android; use haptic feedback (`UIImpactFeedbackGenerator`) or a short sound.
   - The pace and analysis logic (`PaceTracker`) is plain Java and has to be ported (the analysis in `index.html` is already shared).
   - Estimate: a few days for someone who knows Swift.
2. **An iOS project.** `npm install @capacitor/ios@8`, `npx cap add ios`. As on Android, generate it in CI and keep it out of git, or commit it, your choice.
3. **Data safety of the web storage.** On iOS the system can clear a WebView's `localStorage` when the phone is very low on storage. Before release, mirror the data set into a file (the Filesystem plugin) and restore from it on start if `localStorage` is empty. Without this a user could lose their entries. Test this on a device.
4. **Xcode settings**: iPhone only (otherwise Apple demands iPad screenshots), minimum iOS 15 or newer, the location usage text (`NSLocationWhenInUseUsageDescription`), the background mode, and a **privacy manifest** (`PrivacyInfo.xcprivacy`). Declare no tracking and no collected data types.

## What you need to do and pay

1. **Apple Developer Program**: 99 USD per year, https://developer.apple.com/programs/ . Identity verification; an organisation also needs a D-U-N-S number.
2. **A Mac with Xcode** for the first build and for signing, or a GitHub Actions macOS runner with your certificate and provisioning profile as secrets (a bigger setup; fastlane or `xcodebuild` plus an App Store Connect API key).
3. **App Store Connect**: create the app with the bundle ID (use `io.github.cyberconical.localfit`, register it first under Certificates, Identifiers and Profiles), then:
   - Name `LocalFit` (30 characters max; "LocalFit: Private Training" fits), subtitle (30 characters, for example "Private running plans"), description, keywords, support URL (the GitHub page), privacy policy URL (`PRIVACY.md`).
   - **App Privacy** questionnaire: data not collected.
   - Age rating questionnaire, export compliance (the app uses no encryption beyond the standard one: answer accordingly), category Health & Fitness.
   - Screenshots: use `docs/store/apple/` (1290 x 2796, the 6.9-inch size; Apple scales it to smaller phones).
   - A short review note: no login needed, how to try the GPS recording (a few steps outside, or simulate a run in Xcode).
4. **TestFlight** first: upload the build (Xcode, "Distribute App", or `xcrun altool`/Transporter), add internal testers (up to 100, no review) and test a real run with the screen locked.
5. Submit for review. Typical review time is about a day or two.

## Things the review can catch

- **Guideline 4.2 (minimum functionality)**: Apple rejects apps that are only a website in a wrapper. LocalFit has a native location service, background recording, voice and works offline, so it qualifies, but say so in the review note.
- **Location permission text** must explain the real use (recording a run), and the app must work (for example show the plan) if the user denies it.
- **Background location** needs a justification; it is "when in use with background updates", not "always".

## Licence

LocalFit is GPL-3.0. Apple's App Store terms are in conflict with the GPL for code you distribute under it, so the licence needs care: as the **sole copyright holder** you may publish your own code in the App Store (you are not bound by the GPL for your own work), but as soon as you accept contributions from other people, their code is only under the GPL and cannot simply be put in the App Store without their consent. Before accepting outside contributions, either ask contributors to agree to a licence exception for app stores (a contributor agreement) or decide to publish on the App Store only from code you own. A lawyer or the FSF's licensing guidance can confirm this for your case; this page is not legal advice.
