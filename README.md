# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A client sends `POST /submit` a JSON object containing the writer's `text`
   and `creator_id`.
2. The `/submit` route parses and validates those fields. It rejects malformed,
   missing, empty, or unreasonably large input instead of trying to score it.
3. The route creates a unique `content_id`, which connects this decision to its
   audit history and to any later appeal.
4. `detector.py::model_signal` reads the text with the local language model and
   adds `model_score`, a 0–1 measure of how predictable the wording is. Higher
   means more AI-like.
5. `stylometry.py::style_signal` measures the text's sentence-length variation,
   vocabulary repetition, and punctuation, and adds `style_score`, also on a
   0–1 scale where higher means more AI-like.
6. `scoring.py::combine_signals` combines the two signals into `confidence`.
   Then `scoring.py::score_to_label` turns that number into a machine-readable
   `guess` and a plain-English `label`.
7. `audit.py::log_decision` stores the ID, writer, two signal scores, combined
   score, guess, label, and status. The route returns the same decision fields,
   and the client displays the label to the reader.

### False-positive trace

Consider a real writer using short sentences and common words, perhaps because
English is not their first language. Suppose the model signal reads that very
predictable prose as AI-like, the combined score is `0.72`, and the AI boundary
is `0.65`. The service returns `guess: "ai"` and the reader sees: "This text has
patterns that our two checks associate with AI-generated writing. This result
is not proof of authorship, and the writer can appeal it."

The writer can send the returned `content_id` and their explanation to
`POST /appeal`. The service verifies the ID, appends the appeal to the audit
log, changes the item's status to `under_review`, and confirms that a person
should review the decision. The original score remains in the append-only log;
the appeal does not silently erase it. This is why I plan to keep an uncertainty
band between the human and AI labels: borderline evidence should not become a
confident accusation.

### Endpoint contracts

`POST /submit`

- Request JSON: `text` (string, the writing to assess) and `creator_id` (string,
  the writer/account identifier).
- Success response JSON: `content_id` (string UUID), `guess` (`"human"`,
  `"unsure"`, or `"ai"`), `confidence` (number from 0.0 to 1.0; the combined
  AI-likelihood score), `label` (reader-facing string), `model_score` (number
  from 0.0 to 1.0), and `style_score` (number from 0.0 to 1.0).
- Invalid-input response JSON: `error` (short machine-readable code) and
  `message` (plain-English explanation), with an appropriate 4xx status.

`POST /appeal`

- Request JSON: `content_id` (string returned by `/submit`) and `reasoning`
  (string explaining why the writer disputes the decision).
- Success response JSON: `content_id` (string), `status` (`"under_review"`),
  and `message` (plain-English confirmation).
- Unknown-ID or invalid-input response JSON: `error` and `message`, with an
  appropriate 4xx status. An unknown ID must not create an orphan appeal.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the submitted word sequence is to the
local GPT-2 model. It calculates perplexity and converts it to a 0–1 score;
lower perplexity becomes a higher, more AI-like score.

**Why that might differ between human and AI writing:** A language model
generates by repeatedly choosing likely next words, so generated prose often
contains sequences another model finds easy to predict. Human prose may include
more surprising word choices, specific details, and abrupt turns.

**What it can't see:** It cannot see authorship or intent. Predictable human
writing—plain language, a young writer's work, or writing by someone using a
second language—can look AI-like. In the other direction, rare or ornate AI
wording can look human merely because GPT-2 finds it surprising. The configured
token limit also means it cannot evaluate text beyond the portion it reads.

### Signal two — the style signal

**What it measures:** The surface shape of the text: variation in sentence
length, vocabulary repetition through the type-token ratio, and the amount and
variety of punctuation. These measurements will be combined into a 0–1 score
where higher means more AI-like.

**Why that might differ between human and AI writing:** Generated prose often
settles into even, medium-length sentences, repeats a narrower vocabulary, and
uses punctuation in regular patterns. Human writing is often lumpier, with
short and long sentences, uneven repetition, and idiosyncratic punctuation.

**What it can't see:** It cannot understand meaning, factual accuracy,
authorship, or intent. Cosmetic edits such as adding typos, splitting sentences,
changing punctuation, or inserting a quotation can move the score without
changing who wrote the underlying ideas. Genre and text length can also change
these statistics, especially when a short sample provides too little variation.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
