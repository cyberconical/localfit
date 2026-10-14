# Localfit

A lean Android app for local-first training: a plan built for your goal and your week, a log for running and other sports, GPS recording, habits and statistics in one place. It runs completely offline. All data stays on your device.

What makes it special is how it is built: **a single file** (`index.html`), no framework, no server, with a tiny Android shell. That is why it can be customized with AI assistants even without programming skills. The idea behind it is in the [[Low-code manifesto|Low-Code-Manifesto]].

## At a glance

| | |
|---|---|
| Plan | generated on first start: goal (5 km to marathon or general fitness), level, and your own week of runs and other sports |
| Platform | Android 7.0 or newer |
| Languages | English (default) and German, switchable under Settings |
| Data | only on the device: no account, no server, no Google services |
| GPS | optional, with interval cues by vibration, a privacy zone around the start, and a smoothed route on a movable, zoomable map (no map tiles) |
| Code | `index.html` (about 260 KB) plus a Java plugin for the GPS service |
| Design | black and white, follows the device's light or dark mode |
| License | GPL-3.0-or-later |

## Where to go

**Using the app**

- [[Installation|Installation]]: Obtainium, APK, updates
- [[Getting started|Getting-Started]]: the first five minutes
- [[Training and plan|Training-and-Plan]]: your plan, phases, adjusting sessions, logging runs
- [[Plan generator|Plan-Generator]]: the setup and how plans are built
- [[GPS recording|GPS-Recording]]: distance, intervals, privacy zone, map
- [[Habits|Habits]]
- [[Stats|Stats]]: key figures, weekly overview per sport, learnings
- [[Settings|Settings]]
- [[Backup and data|Backup-and-Data]]
- [[Privacy|Privacy]]
- [[FAQ and glossary|FAQ-and-Glossary]]

**Understanding how it is built**

- [[Low-code manifesto|Low-Code-Manifesto]]: the principles behind the app
- [[Architecture|Architecture]]: building blocks, data flows, diagrams
- [[Data model|Data-Model]]: the data set, storage keys, backward compatibility
- [[Analysis engine|Analysis-Engine]]: reading segments, computing distance, smoothing and building the route
- [[Android plugin|Android-Plugin]]: foreground service, bridge, diagnostic log
- [[Translations|Translations]]: how English and German work, adding a language
- [[Build and release|Build-and-Release]]: GitHub Actions, signing, checks

**Changing it yourself**

- [[Customizing with AI|Customizing-with-AI]]: template, recipes, checklist
- [[Customizing the plan|Customizing-the-Plan]]: goals, session writers, descriptions
- [[Contributing and testing|Contributing-and-Testing]]
- [[Troubleshooting|Troubleshooting]]: when something doesn't work, including the diagnostic log
