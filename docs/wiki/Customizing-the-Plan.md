# Customizing the plan

There are two ways: **in the app**, just for you, or **in the code**, for everyone who installs the app.

## In the app

- **The whole plan**: Settings, "Your plan", "Change goal, week or sports" opens the setup again: goal, level, race day, goal time and what you do on each weekday. See [[Plan generator|Plan-Generator]].
- **Single sessions** via "Adjust session": day, title, description, minutes, type, remove. "Back to plan" restores the suggestion.

If you change the description of a run, the intervals of the GPS recording change too, because the app reads them from the text. See [[GPS recording|GPS-Recording]].

## In the code: the generator

Plans are made by `buildGenerated()` in the `app` script of `index.html`. Every text exists in English and German, written next to each other with `bi("English", "Deutsch")`.

### `GOALS`

```js
"10k": { km:10, taper:1, peak:75, start:{new:35,some:35,solid:50},
         min:{new:12,some:8,solid:6}, max:{new:18,some:14,solid:10}, name:bi("10 km","10 km") }
```

- `km`: race distance (0 means no race).
- `taper`: number of taper weeks at the end.
- `peak`: longest long run in minutes.
- `start`: length of the first long run in minutes, per level.
- `min` / `max`: shortest and longest plan in weeks, per level.

To add a goal, add an entry here, add its key to `GOALORDER`, give it a race title in `RACETITLE` and add its German strings to the catalog.

### Session writers

Small functions return one run: `sEasy`, `sStrides`, `sFartlek`, `sTempo`, `sIntervals`, `sGoalPace`, `sRunWalk`, `sLong`, `sRecover`, `sFresh`. Each returns `R(title, minutes, description)` with texts in both languages. `quality()` and `runFor()` inside `buildGenerated()` decide which of them is used in which phase.

- `{HMP}` in a description is replaced with the goal pace (the name is historical; it is the pace for the chosen distance).
- Common titles are constants: `RW` (run & walk), `EASY`, `STEADY`, `LONG`, `STRIDES`, `FARTLEK`, `INTERVALS`, `HMP`, `BREATHE`.

### Descriptions the GPS engine understands

So that intervals are recognized, write them in one of these forms. Both languages work; keep the English and German versions structurally identical.

| Form | English | German |
|---|---|---|
| Repetition in parentheses | `5× (3 min easy run, 1 min walk)` | `5× (3 Min. locker laufen, 1 Min. gehen)` |
| Repetition with recovery | `5× 2 min fast with 1:30 min jog` | `5× 2 Min. zügig mit 1:30 Min. traben` |
| Repetition without recovery (2 min jog assumed) | `3× 5 min at goal pace` | `3× 5 Min. im Zieltempo` |
| Last minutes | `the last 20 min at goal pace` | `die letzten 20 Min. im Zieltempo` |
| Block | `20 min fartlek`, `15 min fast`, `20 min at goal pace` | `20 Min. Tempowechsel`, `15 Min. zügig`, `20 Min. im Zieltempo` |
| Frame | `10 min warm-up, …, 10 min cool-down.` | `10 Min. ein, …, 10 Min. aus.` |

More under [[Analysis engine|Analysis-Engine]]. A sentence that doesn't match gives a free run. That is not an error.

### The classic plan

The earlier 27-week half marathon plan still exists as `PHASES` and `PLAN` for old backups (`profile.planType === "classic"`). Do not edit it unless you want to change what existing users see.

### Things to keep in mind

- Session **IDs** (`w3-wed`) must not change, otherwise stored entries no longer match.
- Stored sport and day tokens (`Lauf`, `Kraft`, `Aus`, …) stay German, see [[Data model|Data-Model]].
- After a change, run the generator over many goal, level and weekday combinations and check that both languages give the same intervals (see [[Contributing and testing|Contributing-and-Testing]]) and publish a new release, see [[Build and release|Build-and-Release]].

For changing it with AI: [[Customizing with AI|Customizing-with-AI]].
