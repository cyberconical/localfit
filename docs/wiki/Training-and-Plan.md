# Training and plan

## Your plan

Localfit builds your plan in the setup on first start (see [[Plan generator|Plan-Generator]]). The plan consists of weeks, and every week has one session per weekday that you did not mark as free. A weekday holds a **run** or one **other sport**: strength, bouldering, calisthenics, stretching, yoga, swimming, cycling, a free workout, or nothing.

Which runs you get depends on your goal and level:

| Goal | Plan length | Race day |
|---|---|---|
| 5 km | 4 to 12 weeks, depending on level | yes |
| 10 km | 6 to 18 weeks | yes |
| Half marathon | 12 to 30 weeks | yes |
| Marathon | 18 to 36 weeks | yes |
| Get fitter | 12 weeks | none |

Race plans count backwards from your race day, so the last week is race week and the plan always ends on the day you chose. If the race is closer than the plan needs, you join in the matching week; if it is further away, the plan starts later. Settings shows a note about this.

### The phases

| Phase | Content |
|---|---|
| Start (new runners) | Alternate running and walking. Joints, tendons and ligaments get used to the load. Pace doesn't matter. |
| Base | Run without breaks, the long run grows, first playful changes of pace (strides, fartlek). |
| Build | Intervals, fartlek and tempo runs join in, the long run grows towards its peak. |
| Peak (race goals) | Pace in the target range (the goal pace if you entered a goal time), the longest runs of the plan. |
| Hold (get fitter) | The same rhythm at a steady load. |
| Taper | Less volume, so you stand at the start line rested on race day: 1 week for 5 km and 10 km, 2 for the half marathon, 3 for the marathon. |

Every fourth week is a **recovery week** ("Breathe") with shorter runs. The week before the race is a dress rehearsal where a longer plan allows it. In race week the last session is the race itself.

Week titles and descriptions exist in English and German. Switching the language under Settings changes them all; the interval structure stays identical.

### Changing the plan

Under Settings, "Your plan", the button "Change goal, week or sports" opens the setup again. A new plan starts with week 1 on the next Monday, and adjustments you made to single sessions are reset. Your logged entries stay saved (and in your backup), but because the weeks restart they may no longer show up in the plan. Single sessions can be adjusted at any time without changing the plan, see "Adjusting sessions" below.

### The classic plan

Backups from the earlier 27-week half marathon app are restored with their plan unchanged (two runs per week on Wednesday and Sunday, five phases, race on Sunday of week 27). The setup is skipped for them. You can set up a generated plan under Settings, "Your plan", "Set up a new plan".

## Goal pace in descriptions

If you entered a goal time, runs in the peak phase and the race itself use the **goal pace**: goal time divided by the race distance. If the goal time changes, the pace in all descriptions follows. Without a goal time the descriptions use effort ("comfortably hard") instead of a number.

## Logging runs

Tap a session to open it. For runs you enter:

- **kilometers** (for example 5.2, or 5,2 in German) and **time** (mm:ss or h:mm:ss)
- **feel** on a scale from “Tough” via “Okay”, “Good” and “Strong” to “Top”
- **the watched body part**: all good, slight pull or hurts (only if you entered one in Settings)
- **shoes**: barefoot shoes or regular shoes
- **time of day**: morning, midday, evening or night

The app then answers with a fitting line, for example for your first run, a new record or your fastest pace. If the watched body part hurts, it suggests 2 to 3 days of rest and repeating the previous week.

A new **longest run** is added to your records automatically, provided you already have a record for it.

If you prefer recording with GPS, see [[GPS recording|GPS-Recording]]. The result lands pre-filled in the same form; you check the values and save.

## Something else instead of the run

If a run doesn't happen, you can record what you did instead: sauna, rest day, swimming, cycling, yoga or sick. The app comments kindly and advises not to make up the run. This choice is not offered for a run that is already logged, so a logged run can't be overwritten by accident. Delete the entry or change the type under “Adjusting sessions”.

## “Done today?” Quick logging

In the “This week” view there are buttons for run and the other sports in your plan. One tap logs what you did today:

- If it's **in today's plan**, it's checked off.
- **Something else** replaces today's session.
- If the session was planned **on another day this week**, it moves to today.
- Otherwise it is added as an **extra session**.

“Undo” in the message reverts it.

## Adjusting sessions

Every session can be changed without changing the plan itself. Your changes lie as a layer on top of the plan:

- another weekday
- your own title and description
- different planned minutes (runs only, not the race)
- a different **type for any session**, runs included: Run, Strength, Bouldering, Calisthenics, Stretching, Yoga, Swimming, Cycling or Workout (only the race itself is fixed). A logged run stays stored when its session becomes another sport and comes back when you switch to Run again
- extra sessions can be removed from the plan; runs cannot

“Back to plan” restores the suggestion at any time. Technical details: [[Data model|Data-Model]], section `edits`.

## Strength and stability

The “Strength & stability” section shows your weekly rhythm and seven exercises: squats, reverse lunges, step-ups, single-leg glute bridge, side steps with a mini band, calf raises, and plank with side plank. It also gives a rule for the watched body part: a slight pull up to 2 out of 10 is okay. If it gets stronger or is worse the next morning, take 2 to 3 days of rest and repeat the previous week.
