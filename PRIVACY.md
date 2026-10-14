# Privacy policy

*LocalFit, last updated October 2026.*

LocalFit is a training app that works entirely on your device. This page says what the app does with your data. The short version: **it collects nothing, sends nothing and has no account.**

## What the app stores

Everything you enter (your plan, logged sessions, notes, habits, records, goals, settings) and, if you record a run with GPS, its distance, time, pace, kilometer splits and optionally the route. This is stored only in the app's private storage on your phone. The developer has no access to it.

## What the app sends

Nothing. The app has no server, no account, no analytics, no advertising, no crash reporting and no third-party code that talks to a network. The official release is built without Android's internet permission, so the operating system would not even let it connect. It uses no Google services.

## Location

The app asks for your location only when you tap "Record with GPS". It reads the phone's GPS directly (not Google's location services) while a recording runs, in a foreground service with a visible notification, so that recording continues when the screen is off. Location is never sent anywhere. Raw GPS points stay in memory; only the result is saved, and the route only if you leave "Save route" on. An adjustable privacy zone around the start (300 m by default) is never saved. The app does not use background location access.

## Other permissions

| Permission | Why |
|---|---|
| Precise and approximate location | GPS recording (Android requires both to be requested together on newer versions) |
| Foreground service (location) | keeps a recording running while the screen is off |
| Notifications | shows the notification while a recording is running |
| Wake lock | keeps interval cues on time during a recording |
| Vibration | cues when an interval changes |

## Voice announcements

If you switch them on, the app uses your phone's own text-to-speech engine. What the speech engine does is governed by that engine's provider; the app sends it only a short sentence such as the distance and pace.

## Diagnostic log

The app keeps a small anonymous technical log (events such as "service started"), which helps find out why a recording stopped. It contains no places, distances, dates, names or device identifiers. It stays on the device unless you choose "Share" in Settings. You can switch it off or delete it.

## Backups

Android's automatic cloud backup is turned off for this app. If you use "Save backup", the file goes wherever you share it. It is not encrypted and contains all your entries, so do not put it in a public place.

## Your control

Uninstalling the app or clearing its data deletes everything it stores. There is no other copy.

## Children

The app does not collect personal information from anyone, including children.

## Changes

If this policy changes, the new version is published at this address with a new date.

## Contact

Questions: open an issue at https://github.com/cyberconical/localfit/issues
