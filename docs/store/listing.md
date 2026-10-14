# Google Play listing

Texts to paste into the Play Console. Graphics are in this folder (`icon-512.png`, `feature-graphic-1024x500.png`; re-create with `python3 tools/store-graphics.py`). Phone screenshots (at least 2, ideally 4 to 8) must be taken from the real app, see docs/RELEASING.md.

## App name (max 30 characters)

Localfit: Private Training

## Short description (max 80 characters)

Local-first training plans. No account, no tracking, no cloud.

## Full description (max 4000 characters)

Localfit builds a training plan around your goal and your week, and keeps everything on your phone.

On first start you choose a goal (5 km, 10 km, half marathon, marathon or simply getting fitter), your experience and what you do on which weekday: running, strength, bouldering, calisthenics, stretching, yoga, swimming, cycling or a free workout. Localfit generates the plan on the spot, counts back from your race day and adds intervals, tempo runs, recovery weeks and a taper.

PRIVATE BY DESIGN
• No account, no sign-in, no cloud
• No ads, no analytics, no trackers, no Google services
• The app has no internet permission at all, so it cannot send your data anywhere
• Your entries live in the app's private storage

PLAN
• Goals from 5 km to marathon, or a 12-week fitness block
• Sessions per week and sports of your choice
• Run/walk start for new runners, long runs, intervals, goal-pace sessions if you enter a goal time
• Adjust any session, or rebuild the plan whenever life changes

GPS RECORDING (OPTIONAL)
• Distance, time, pace and every kilometer, with the screen off
• Live map and route you can zoom; street map currently for Berlin, Germany only (map data © OpenStreetMap contributors), elsewhere a plain track
• Vibration cues for intervals
• Optional voice announcements with your phone's own text-to-speech
• A privacy zone around your start that is never saved

EVERYTHING ELSE
• Habits with streaks
• Statistics: kilometers per week, pace trend, shoes and time of day compared
• Learnings and issues you can mark as solved
• English and German, light and dark
• Backup and restore as a single file

Localfit is free and open source (GPL-3.0). The code is on GitHub.

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
