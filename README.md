# Localfit

[![Latest release](https://img.shields.io/github/v/release/cyberconical/localfit?label=release&color=black)](https://github.com/cyberconical/localfit/releases/latest)
[![License: GPL-3.0-or-later](https://img.shields.io/badge/license-GPL--3.0--or--later-black)](LICENSE)
[![Android 7.0+](https://img.shields.io/badge/Android-7.0%2B-black)](#install)
[![No tracking](https://img.shields.io/badge/tracking-none-black)](#privacy)

**Local-first training plans. No account, no tracking, no cloud.**

Tell Localfit your goal, your level and your week, and it builds a training plan for you: running, strength, bouldering, yoga and more. Log sessions, record runs with GPS, keep habits and see your statistics. It works completely offline and all data stays on your device.

## Highlights

- **A plan built around you.** On first start a short setup asks for your goal (5 km, 10 km, half marathon, marathon, or general fitness), your experience, how many sessions you want per week and what you do on which weekday. The plan is generated on the spot and fits your race day.
- **Sports you already know.** Running, strength, bouldering, calisthenics, stretching, yoga, swimming, cycling and free workouts. Mix them as you like.
- **GPS recording that survives a locked screen.** Distance, time, pace, every kilometer and the route, with a live map from the first fix. Interval cues by vibration.
- **Voice announcements, optional.** Every 500 m or 1 km a voice says distance, recent pace and average pace (English, with your phone's own offline text-to-speech).
- **Private by design.** No account, no server, no ads, no trackers, no Google services. The release build does not even request the internet permission. A privacy zone around your start is never stored.
- **Habits and stats.** Your own habits with streaks, kilometers per week, pace trend, shoes and time of day compared, learnings you can mark as solved.
- **The backup is the app.** One file holds the app and all your entries.
- **English or German, light or dark.** Black and white, following your phone.

## Install

Localfit is not in a store yet. The easiest way is [Obtainium](https://github.com/ImranR98/Obtainium), which detects new versions automatically:

1. Install Obtainium.
2. In Obtainium, tap "Add app" and paste `https://github.com/cyberconical/localfit`.
3. Tap "Add" and then "Install". Android asks once for permission to install apps from this source.

Alternatively, download `localfit.apk` from the [latest release](https://github.com/cyberconical/localfit/releases/latest) and install it by hand.

Requirement: Android 7.0 or newer.

## Getting started

1. Open the app. The setup asks for your goal, level and weekly rhythm and builds your plan. It takes about a minute.
2. Log your first session in the **Training** tab, or tap "Record with GPS" for a run.
3. Change the plan any time under Settings, "Your plan". Existing entries are kept.
4. Save a backup regularly, see [Backup](#backup).

## Your plan

The plan generator is plain code in `index.html`, not a service: no data leaves the phone. It knows five goals (5 km, 10 km, half marathon, marathon, general fitness) and three levels (new to running, some running, solid base). A plan with a race has phases from base building to the taper and ends on your race day; a fitness plan runs for 12 weeks. Runs come with intervals, tempo work or run/walk blocks, depending on level and phase, in a form the GPS coach understands. Other sports are scheduled on the weekdays you pick. How the generator works and how to change it: [docs/wiki/Training-and-Plan.md](docs/wiki/Training-and-Plan.md) and [docs/wiki/Customizing-the-Plan.md](docs/wiki/Customizing-the-Plan.md).

If you used the previous 27-week half marathon version of this app, restoring your old backup keeps that plan exactly as it was.

## Features

**Training**
- A generated plan with up to seven sessions per week across nine sport types.
- Log runs with kilometers, time, feel, shoes and time of day.
- Log what you did today with one tap. Every session can be adjusted, and "Back to plan" restores the suggestion.
- Optional GPS recording: distance, time, pace, every kilometer and the route. It only tracks, and the screen may stay off.
- A live map while recording, showing your position, the accuracy circle and the track so far.
- Optional voice announcements every 500 m or 1 km, in English.
- The route appears as a map in the run and, overlaid, in the stats. Drag to move it, pinch or double tap to zoom, or open it full screen. GPS noise is smoothed so the line follows your path. You can bundle an offline basemap for your region at build time (see [map/README.md](map/README.md)); without it the route is drawn as a clean line.

**Habits**
- Create your own habits, check them off per day or enter a number.
- Streaks and weekly average at a glance.

**Stats**
- Weekly overview per sport, kilometers per week and pace trend.
- Comparison by shoe type and time of day.
- Record learnings and issues and mark them as solved.

**Settings**
- Language: English or German.
- Your plan: goal, level, weekly rhythm, race day and goal time. Rebuild it whenever your life changes.
- A body part you want to keep an eye on, for example your knee.
- Records and personal goals per sport.
- GPS and route: privacy zone around the start, whether the route is saved, voice announcements, and a test mode for inaccurate GPS.
- Diagnostics: an anonymous log for when a recording stops.

## Privacy

- All entries live in the app's private storage. There is no server and no account.
- The app calls no servers. It uses no Google services, no ads and no trackers. The font ships with the app, and so does the optional map. The official release is built without the internet permission, so the app could not reach a server even if it wanted to.
- Location is used only during a recording and is never sent. The app reads the device's GPS directly, not Google's location services. Raw fixes stay in memory. Only the result is stored, with the route if you want.
- An adjustable **privacy zone** (300 m by default) around the start is never stored. Distance and time still count in full. It protects against the obvious but is no substitute for caution: someone who knows your route can guess the area.
- Under Settings there is a **diagnostic log** that helps find out why a recording stops. It only records technical events, never places, distances, dates, names or a device ID. You can view, share, delete or switch it off. It only leaves the device if you share it.
- Android does not back up the app data to the cloud. Your entries only leave the device if you share a backup yourself.
- Uninstalling the app or clearing its data deletes your entries. Updates keep them.
- Data on the device is stored unencrypted in the app's private storage, like most apps. The device's own screen lock and storage encryption protect it.

The full statement is in [PRIVACY.md](PRIVACY.md).

### Backup

- **Save:** Tap "Save backup" at the top and choose a place in the share menu, for example Drive or Files.
- **Restore:** Tap "Load backup" at the very bottom and choose the file.

The backup file contains all your entries and routes, unencrypted. Don't share it via public links and never upload it to a public repository.

## Documentation

Guides, the architecture and the low-code manifesto are in the [wiki](https://github.com/cyberconical/localfit/wiki). Its pages live in `docs/wiki/` and are published from there. How to publish a release, including Google Play, is in [docs/RELEASING.md](docs/RELEASING.md).

## Development

The app is one file, `index.html`, without frameworks, plus the bundled font in `fonts` and the map libraries in `map`. It is packaged as an Android app with [Capacitor](https://capacitorjs.com), with its own Java plugin for GPS in the background. GitHub Actions does the build.

To try it in the browser:

```
python3 -m http.server
```

Then open `http://localhost:8000`. The browser stores data separately from the app, so your real data stays untouched. GPS recording works in the browser only while the screen is on, and voice announcements and the diagnostic log exist only in the Android app.

How to customize the app, publish a release and what the data model contains is in [docs/development.md](docs/development.md) and in the wiki.

```
index.html                    the app (English source text, German catalog in the script "i18n")
plugins/run-tracker/          GPS recording and voice announcements for Android (no Google services)
map/                          offline map libraries, styles and fonts (a regional basemap can be added by the build)
fonts/                        Instrument Sans font with license text
tools/                        generator for the store graphics, plan generator test
docs/RELEASING.md             keys, secrets, Google Play steps
docs/store/                   store listing texts and graphics
docs/development.md           customizing, data model, publishing
docs/wiki/                    the wiki pages
.github/workflows/build.yml   build, signing and upload to the release
.github/workflows/wiki.yml    publishes docs/wiki to the GitHub wiki
PRIVACY.md                    privacy policy (also the public URL for Google Play)
LICENSE                       GNU General Public License v3
README.md                     this file
```

## Origin

Localfit grew out of a single-purpose half marathon training app and keeps its classic 27-week plan for existing users.

## License

This project is licensed under the [GNU General Public License, version 3](LICENSE) or, at your option, any later version (GPL-3.0-or-later). You may use, change and share the app. Changes you share must stay open under the same license.

Third-party parts keep their own licenses: [MapLibre GL JS](https://maplibre.org) and PMTiles (BSD-3-Clause), the map style by Protomaps (BSD-3-Clause), map data (c) [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) (ODbL) if you bundle a map, and the [Instrument Sans](https://github.com/Instrument/instrument-sans) and Noto Sans fonts (SIL Open Font License 1.1). Details are in `map/README.md` and `fonts/OFL.txt`.
