# Google Play listing

Texts to paste into the Play Console. Graphics are in this folder (`icon-512.png`, `feature-graphic-1024x500.png`; re-create with `python3 tools/store-graphics.py`). Phone screenshots: the finished, captioned set is in `play/` (1080x1920) and, for the App Store, `apple/` (1290x2796), made with `python3 tools/store-screenshots.py` from the raw screens in `docs/screenshots/`.

## App name (max 30 characters)

Localfit: Private Training

## Short description (max 80 characters)

Local-first training plans. No account, no tracking, no cloud.

## Full description (max 4000 characters)

The private, open-source way to train. No account, no cloud, no ads.

Localfit builds a training plan around your goal and your week, records your runs on a map, and keeps everything on your phone. Nothing is uploaded, nothing is shared, there is no feed. The app has no internet permission at all, and the code is open source so you can check.

YOUR PLAN
• Choose a goal: 5 km, 10 km, half marathon, marathon, or simply get fitter
• Pick your level and what you do on which weekday: running, strength, bouldering, calisthenics, stretching, yoga, swimming, cycling or a free workout
• Localfit generates the plan on the spot, counts back from your race day and adds intervals, tempo runs, recovery weeks and a taper
• Adjust any session, or rebuild the plan whenever life changes

RUN WITH GPS (OPTIONAL)
• Distance, time, pace and every kilometer, with the screen off
• Live map and route map you can zoom; offline street map currently for Berlin, Germany (map data © OpenStreetMap contributors), elsewhere your track is drawn as a clean line
• All your routes on one map
• Vibration cues for intervals and optional voice announcements (English) with your phone's own text-to-speech
• A privacy zone around your start that is never saved

PRIVATE BY DESIGN
• No account, no sign-in, no cloud, no social feed
• No ads, no analytics, no trackers, no Google services
• No internet permission: the app cannot send your data anywhere
• Entries live in the app's private storage; backup and restore as a single file you control

MORE
• Habits with streaks
• Statistics: kilometers per week, pace trend, shoes and time of day compared, learnings and issues you can mark as solved
• English and German, light and dark

Free and open source (GPL-3.0). Source code and issues: github.com/cyberconical/localfit

Localfit is a training aid, not medical advice. If you are unsure whether a plan is right for you, talk to a doctor first.

## Category and tags

Category: Health & Fitness. Tags (pick what the console offers): fitness, running, workout, exercise tracker.

## Contact details (required)

Email: *use an address you are happy to show publicly*. Website: https://github.com/cyberconical/localfit
Privacy policy URL: https://github.com/cyberconical/localfit/blob/main/PRIVACY.md (or enable GitHub Pages and use that).

## Data safety form

| Question | Answer |
|---|---|
| Does your app collect or share any of the required user data types? | **No** |
| Is all of the user data collected by your app encrypted in transit? | not applicable (nothing is collected or transmitted) |
| Do you provide a way for users to request that their data be deleted? | not applicable (no data leaves the device; uninstalling deletes everything) |

Rationale: Google defines "collect" as transmitting data off the device. Localfit has no network access and sends nothing. Location is only processed on the device. If Google's console asks you to declare anything about location anyway, answer "processed on device only, not collected".

## App content declarations

- **Privacy policy**: URL above.
- **Ads**: no ads.
- **App access**: all functionality is available without login or special access.
- **Content rating**: answer the questionnaire honestly (no violence, no user-generated content shared with others, no purchases); expect "Everyone".
- **Target audience**: 18 and over is the safe choice for a training app (avoids the Families policy requirements).
- **Health apps declaration**: the console asks whether the app is a health app. Answer yes for fitness tracking, it is a fitness app with no medical features. Add the disclaimer that it is not medical advice (already in the description).
- **Government app / financial features / news**: no.

## Foreground service permission declaration (location)

The console asks about every foreground service type. For `FOREGROUND_SERVICE_LOCATION`:

- **Core functionality**: recording the route, distance and pace of a run.
- **Why a foreground service is needed**: the user starts a recording and then locks the screen or switches apps; Android would otherwise stop location updates. The service shows a persistent notification ("Recording your run") and ends when the recording ends.
- **User-initiated**: yes, the user taps "Record with GPS" and the recording runs until they stop it.
- **Video**: Google asks for a short screen recording that shows the feature: start the app, tap "Record with GPS", grant the permission, show the notification, lock the screen, unlock, stop the recording. Upload it as an unlisted YouTube link or file as the form allows.
- The app does **not** request background location (`ACCESS_BACKGROUND_LOCATION`), so no background location declaration is needed. The CI build fails if that permission ever shows up.
