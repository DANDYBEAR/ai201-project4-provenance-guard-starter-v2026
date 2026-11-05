# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives stay at or below 10%

For a set of 10 pieces written entirely by people, no more than 1 may receive
the high-confidence AI label in any one trial. I will run the same set in three
trials, so this limit must hold separately in all three trials rather than only
after averaging their results.

**Why this target:** A false accusation can damage a writer's credibility and
is more costly than allowing some AI-written text through. A 10% ceiling is
strict enough to expose a detector that routinely mistakes plain human writing
for AI without pretending that this imperfect method can reach zero errors.

---

## 2. Clearly different sources have a visible score spread

For 5 clearly human-written samples and 5 unedited AI-generated samples, the
AI set's mean combined score must be at least `0.20` higher than the human
set's mean combined score in each of three trials.

**Why this target:** A twenty-point gap on a 0–1 scale is large enough for the
scores to support useful label boundaries. Comparing group means also avoids
claiming that every individual sample will be separable when both signals have
real blind spots.

---

## 3. Every label is reachable

Using a calibration set of 9 submissions, every trial must produce at
least 1 `human`, 1 `unsure`, and 1 `ai` guess. The returned reader-facing label
must match the guess and its configured score range for all 9 submissions.

**Why this target:** A three-label design is misleading if one label can never
be returned. Requiring examples on both sides and inside the uncertainty band
also catches gaps, overlaps, or reversed threshold comparisons.

---

## 4. Appeals always enter review and remain auditable

For 5 valid `content_id` values, all 5 appeal requests must return HTTP `200`,
return the matching ID with `status: "under_review"`, and append exactly 1
appeal log entry containing the submitted reasoning. An appeal using an unknown
ID must return HTTP `404` and append 0 appeal entries.

**Why this target:** The appeal is the writer's only direct remedy for a false
positive, so partial success is not acceptable. Checking both the response and
append-only log proves that the visible confirmation corresponds to a durable,
reviewable event and that invalid IDs cannot create orphan records.

---

## 5. Bad text input fails safely and consistently

Each of these 5 `/submit` cases must return HTTP `400` with JSON `error` and
`message` fields and must not call either scoring signal: a missing `text`
field, `text: ""`, whitespace-only text, a non-string `text`, and text longer
than `20,000` characters. None may return HTTP `500` or create a decision log
entry.

**Why this target:** These cases define an observable boundary between a bad
request and an internal failure. The 20,000-character cap permits substantial
writing while preventing the service from spending model time on input far
beyond the detector's configured 400-token reading window.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
