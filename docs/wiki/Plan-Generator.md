# Plan generator

Localfit does not ship one fixed plan. On first start, a short setup asks for a few things and builds a plan on the device. Nothing is sent anywhere; the generator is ordinary code in `index.html`.

## The setup

**Step 1: Goal and level**

- **Goal**: 5 km, 10 km, half marathon, marathon or "Get fitter" (no race).
- **Level**: new to running, some running experience, or a solid base. The level sets how long the plan is, how big the first long run is and whether the plan begins with run/walk weeks.
- **Race day** (race goals): defaults to a sensible date for the goal and level. It must be at least a week away.
- **Goal time** (optional, race goals): as `h:mm:ss`. If you enter one, the plan uses your goal pace in the peak phase and the race. If you leave it empty the plan works by effort.

**Step 2: Your week**

- Choose how many sessions you want per week (2, 3, 4 or 5) as a starting point, then change every weekday: a run, one of the other sports or free.
- A race goal needs at least one run a week. A half marathon or marathon needs at least two.

**Step 3: Your plan**

A summary: goal, dates, number of weeks, sessions per week. "Create plan" builds it.

The language of the setup is switchable on the first screen. Backups from the earlier 27-week version skip the setup.

## What the generator builds

For every week the generator decides the **long run** (in minutes), then fills the remaining run days. With one run a week it is the long run; with more, an easy run, a quality run, and so on, the long run always on the last run day of the week.

| Element | Rule |
|---|---|
| Run/walk start | New runners begin with 3 to 6 weeks of alternating running and walking (about 15 % of the plan). |
| Base phase | Easy runs with strides, then fartlek. |
| Build phase | Rotating intervals, fartlek and tempo runs. |
| Peak phase | Goal-pace runs and intervals if you have a goal time, otherwise tempo and intervals. |
| Recovery | Every fourth week, the long run drops to 70 % of the previous. |
| Taper | The last 1 (5 km, 10 km), 2 (half) or 3 (marathon) weeks, with shorter runs and light other sessions. |
| Race week | A short run and a few strides, then the race on the chosen day. |
| Other sports | Placed on the weekdays you chose, with a short text each. In taper and race week they become light. |

Peak long run in minutes per goal: 5 km 50, 10 km 75, half marathon 120, marathon 180. The plan never plans a long run bigger than that.

Everything the generator writes in a run description follows the sentence patterns that the GPS coach parses, so intervals, fartlek and goal-pace blocks are also cued by vibration while you record. See [[Analysis engine|Analysis-Engine]].

## Properties you can rely on

- Session ids are stable: `w{week}-{mon|tue|wed|thu|fri|sat|sun}`, as in the classic plan.
- The plan ends on race day and no session comes after it.
- Weekly volume never jumps by more than the generator's own rules allow (the build is tested over thousands of combinations).
- English and German texts are generated side by side.

## Changing the generator

All of it sits in one block of `index.html`: the table `GOALS`, the helpers `planParams()` and `buildGenerated()` and the small functions that write one session (`sEasy`, `sFartlek`, `sTempo`, `sIntervals`, `sGoalPace`, `sRunWalk`, `sLong`, …). See [[Customizing the plan|Customizing-the-Plan]].
