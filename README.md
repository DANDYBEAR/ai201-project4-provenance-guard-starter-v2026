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
is `0.65`. The service returns `guess: "ai"` and the reader sees: "We found
patterns often associated with AI-generated writing, but this is not proof of
authorship. The writer can appeal this result for human review."

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
where higher means more AI-like. Inside the style score, normalized sentence
spread counts for `0.50`, vocabulary diversity for `0.35`, and internal
punctuation density for `0.15`; punctuation receives the least weight because
it is especially easy to manipulate.

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

**The rule:** Take an equal-weighted average of the model score and style
score, after validating that both are on the 0–1 scale. Both signals have real
but different blind spots, so neither gets to overrule the other by itself.
When they strongly disagree, their average moves toward `0.50`, which treats
the disagreement as uncertainty instead of turning one weak signal into a
confident accusation.

**The numbers:** `0.50 × model_score + 0.50 × style_score`, rounded to four
decimal places. The weights live in `config.py` as
`WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5`. The current
threshold settings are `0.35` for human and `0.65` for AI, leaving the middle
as the uncertainty band; reader-facing labels are added in Milestone 5.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

I ran both signals on the same three pieces used for the model-only check:

| Same test piece | Model | Style | Combined | Agreement |
|---|---:|---:|---:|---|
| Formulaic AI-style prose | 0.8203 | 0.4781 | 0.6492 | Split |
| Specific human anecdote | 0.4202 | 0.4505 | 0.4354 | Agree: humanward |
| Borderline neutral report | 0.4336 | 0.2861 | 0.3599 | Agree: humanward |

**A case where my two signals split, and what my rule does with it:** The
formulaic AI sample scored `0.8203` on the model signal but only `0.4781` on
the style signal, a gap of `0.3422`. The equal-weight rule returned `0.6492`,
pulling the model's strong AI reading back to the edge of the uncertainty band.
The style score was lower because this short sample had unusually high
vocabulary variety and enough punctuation to look less machine-like to the
surface-only measures.

### Milestone 4 calibration

| Deliberately chosen input | Model | Style | Combined | What I learned |
|---|---:|---:|---:|---|
| Clearly AI, unedited | 0.7833 | 0.3107 | 0.5470 | The signals split; the average becomes uncertain. |
| Clearly human, public-domain narrative | 0.5054 | 0.5181 | 0.5117 | Both signals were uncertain on a short, regular passage. |
| Formal human, public speech | 0.6875 | 0.5203 | 0.6039 | Formal, predictable human prose risks a false positive. |
| Lightly edited AI | 0.2908 | 0.1169 | 0.2039 | Surface edits fooled both signals toward human. |

The last two cases are the important failure pair. The formal human sample is
more AI-like than the edited AI sample, so neither a weighted average nor a
threshold can repair those inputs after both signals point the wrong way. The
audit log therefore records both component scores, not only the combined one.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35, inclusive | We think this was probably written by a person. Automated checks can be wrong. |
| unsure | greater than 0.35 and less than 0.65 | We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result. |
| high-confidence AI | 0.65–1.00, inclusive | We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says directly that the system cannot make a reliable judgment and tells the
reader not to treat uncertainty as evidence against the writer. From the
writer's perspective, it communicates "the tool does not know" rather than
"you are suspicious," so there is no accusation they are expected to rebut.

**Reachability check with real submissions:**

| Returned guess | Combined score | Content ID |
|---|---:|---|
| human | 0.2039 | `29ca20f1-dc56-42ad-84b4-c5456c96f313` |
| unsure | 0.6039 | `b568df53-3966-463a-b393-9315cf86c137` |
| ai | 0.8620 | `670e4575-55c8-41c6-859b-e5faab944bc0` |

All three ranges are reachable. The input that reached the human range was
lightly edited AI text, so reachability is not evidence that the judgment was
correct; it is another concrete example of the style signal's blind spot.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

Before wiring the route, I ran `detector.py` by itself on three samples:

| Sample | Perplexity | Model signal |
|---|---:|---:|
| Formulaic AI-style prose | 17.4 | 0.8203 |
| Specific human anecdote | 55.0 | 0.4202 |
| Borderline neutral report | 53.2 | 0.4336 |

The AI-style sample scored much higher, but the human and borderline samples
were close. That matches the model signal's blind spot: predictability is not
the same as authorship.

I started this validation run with `PORT=5053` so it was isolated from earlier
development-server checks.

```powershell
curl.exe -sS -X POST http://127.0.0.1:5053/submit -H "Content-Type: application/json" -d '{\"text\": \"The system works well. The system works fast. The system works every day. The system helps many users. The system gives good results. The system makes work easy.\", \"creator_id\": \"label-ai-check\"}'
```

```json
{
  "confidence": 0.862,
  "content_id": "670e4575-55c8-41c6-859b-e5faab944bc0",
  "creator_id": "label-ai-check",
  "guess": "ai",
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "model_score": 0.8603,
  "style_score": 0.8637
}
```

**An appeal**

```powershell
curl.exe -sS -X POST http://127.0.0.1:5053/appeal -H "Content-Type: application/json" -d '{\"content_id\": \"670e4575-55c8-41c6-859b-e5faab944bc0\", \"reasoning\": \"I wrote this myself. The repeated sentence structure was a deliberate plain-language choice.\"}'
```

```json
{
  "content_id": "670e4575-55c8-41c6-859b-e5faab944bc0",
  "message": "Your appeal was recorded and is now under human review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
curl.exe -sS "http://127.0.0.1:5053/log?limit=4"
```

```json
{
  "count": 4,
  "entries": [
    {
      "combined_score": 0.862,
      "content_id": "670e4575-55c8-41c6-859b-e5faab944bc0",
      "creator_id": "label-ai-check",
      "guess": "ai",
      "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
      "model_score": 0.8603,
      "status": "decided",
      "style_score": 0.8637,
      "timestamp": "2026-11-05T01:57:35+00:00"
    },
    {
      "combined_score": 0.2039,
      "content_id": "29ca20f1-dc56-42ad-84b4-c5456c96f313",
      "creator_id": "label-human-check",
      "guess": "human",
      "label": "We think this was probably written by a person. Automated checks can be wrong.",
      "model_score": 0.2908,
      "status": "decided",
      "style_score": 0.1169,
      "timestamp": "2026-11-05T01:57:41+00:00"
    },
    {
      "combined_score": 0.6039,
      "content_id": "b568df53-3966-463a-b393-9315cf86c137",
      "creator_id": "label-unsure-check",
      "guess": "unsure",
      "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
      "model_score": 0.6875,
      "status": "decided",
      "style_score": 0.5203,
      "timestamp": "2026-11-05T01:57:46+00:00"
    },
    {
      "content_id": "670e4575-55c8-41c6-859b-e5faab944bc0",
      "creator_id": "label-ai-check",
      "event": "appeal",
      "reasoning": "I wrote this myself. The repeated sentence structure was a deliberate plain-language choice.",
      "status": "under_review",
      "timestamp": "2026-11-05T01:57:52+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to help trace the submission pipeline, name
  both signals' blind spots, and turn the assignment prompts into five
  measurable acceptance criteria before I built the service.
- *What came back:* It proposed a seven-step route-to-label trace, an endpoint
  contract, a false-positive scenario, and numerical criteria for false
  positives, score spread, label reachability, appeals, and invalid input.
- *What I changed:* I tied the trace to this starter's actual files and audit
  fields, set the input limit to 20,000 characters, and made the 10% false-
  positive limit apply separately to each of three trials instead of hiding a
  bad run inside an overall average.

**Moment 2**

- *What I asked for:* I asked AI to help implement and test the style signal,
  combine it with the model signal, write reader-facing labels, and build the
  appeal route without skipping the required standalone and `curl` checks.
- *What came back:* It suggested normalized sentence spread, vocabulary ratio,
  and punctuation measures; an equal-weight combining rule; cautious label
  text; and an append-only appeal flow. The calibration exposed a serious
  failure: formal human prose scored `0.6039`, while lightly edited AI scored
  only `0.2039`.
- *What I changed:* I gave punctuation only 15% of the style score because it
  is easy to manipulate, kept disagreement near the unsure band, revised the
  AI label to say the result is not proof and offer human review, and recorded
  the surprising calibration results instead of tuning them away.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
A real writer may revise and resubmit several times in a short burst, so ten
submissions in a minute leaves room for normal iteration. Two hundred per day
is much more than an individual writer should need, while still stopping a
script from sending the thousand variations it would use to map the detector's
thresholds.

**What a caller counts as:** A `creator_id`, falling back to the remote address
when the request does not contain a usable creator ID. Per-creator limiting
does not punish several writers sharing one network, although an attacker who
can freely create IDs could evade it; production identity would therefore need
to authenticate the creator ID.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Baseline result: **25 HELD, 31 BROKE**. The complete generated evidence is in
`results/attack_run_2026-11-04_2122.md`.

| ID | Family | Status | Guess | Verdict |
|---|---|---:|---|---|
| EV01 | evasion | 200 | human | BROKE |
| EV02 | evasion | 200 | unsure | BROKE |
| EV03 | evasion | 200 | unsure | BROKE |
| EV04 | evasion | 200 | unsure | BROKE |
| EV05 | evasion | 200 | human | BROKE |
| EV06 | evasion | 200 | unsure | BROKE |
| EV07 | evasion | 200 | unsure | BROKE |
| EV08 | evasion | 200 | unsure | BROKE |
| EV09 | evasion | 200 | unsure | BROKE |
| EV10 | evasion | 200 | ai | HELD |
| FP01 | false positive | 200 | unsure | HELD |
| FP02 | false positive | 200 | ai | BROKE |
| FP03 | false positive | 200 | ai | BROKE |
| FP04 | false positive | 200 | ai | BROKE |
| FP05 | false positive | 200 | ai | BROKE |
| FP06 | false positive | 200 | ai | BROKE |
| FP07 | false positive | 200 | ai | BROKE |
| FP08 | false positive | 200 | human | HELD |
| PI01 | prompt injection | 200 | human | HELD |
| PI02 | prompt injection | 200 | human | HELD |
| PI03 | prompt injection | 200 | unsure | HELD |
| PI04 | prompt injection | 200 | unsure | HELD |
| PI05 | prompt injection | 200 | unsure | HELD |
| PI06 | prompt injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 500 | — | BROKE |
| MF03 | malformed | 200 | human | BROKE |
| MF04 | malformed | 500 | — | BROKE |
| MF05 | malformed | 500 | — | BROKE |
| MF06 | malformed | 500 | — | BROKE |
| MF07 | malformed | 500 | — | BROKE |
| MF08 | malformed | 400 | — | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 400 | — | HELD |
| RQ11 | malformed | 400 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood | 200 | human | BROKE |
| FL01_02 | flood | 200 | human | BROKE |
| FL01_03 | flood | 200 | human | BROKE |
| FL01_04 | flood | 200 | human | BROKE |
| FL01_05 | flood | 200 | human | BROKE |
| FL01_06 | flood | 200 | human | BROKE |
| FL01_07 | flood | 200 | human | BROKE |
| FL01_08 | flood | 200 | human | BROKE |
| FL01_09 | flood | 200 | human | BROKE |
| FL01_10 | flood | 200 | human | BROKE |
| FL01_11 | flood | 429 | — | HELD |
| FL01_12 | flood | 429 | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp":"2026-11-05T02:22:07+00:00","content_id":"95aa4612-36e8-4e49-bffb-d5d7d3204e0c","creator_id":"attacker_EV01","guess":"human","model_score":0.1635,"style_score":0.5097,"combined_score":0.3366,"label":"We think this was probably written by a person. Automated checks can be wrong.","status":"decided"}
{"timestamp":"2026-11-05T02:22:08+00:00","content_id":"ad421179-5304-43e7-afea-ecdede24c070","creator_id":"attacker_EV10","guess":"ai","model_score":0.9792,"style_score":0.7374,"combined_score":0.8583,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.","status":"decided"}
{"timestamp":"2026-11-05T02:22:09+00:00","content_id":"b6704c66-af77-448f-860c-cf22b954394a","creator_id":"attacker_FP02","guess":"ai","model_score":0.7387,"style_score":0.6391,"combined_score":0.6889,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.","status":"decided"}
{"timestamp":"2026-11-05T02:22:09+00:00","content_id":"f8612e7a-4626-409c-84cb-ed561feb2a0d","creator_id":"attacker_FP03","guess":"ai","model_score":0.8051,"style_score":0.5862,"combined_score":0.6957,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.","status":"decided"}
{"timestamp":"2026-11-05T02:22:09+00:00","content_id":"fce31200-3341-4e3c-b2aa-35c3c4cbfc96","creator_id":"attacker_FP05","guess":"ai","model_score":0.8005,"style_score":0.7047,"combined_score":0.7526,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.","status":"decided"}
{"timestamp":"2026-11-05T02:22:10+00:00","content_id":"a3088992-7f43-4858-9734-7672863f037b","creator_id":"attacker_PI05","guess":"unsure","model_score":0.6401,"style_score":0.1857,"combined_score":0.4129,"label":"We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.","status":"decided"}
{"timestamp":"2026-11-05T02:22:10+00:00","content_id":"739b26d1-77b8-47a1-9bb7-4167dc3b9bff","creator_id":"attacker_MF03","guess":"human","model_score":0.0,"style_score":0.25,"combined_score":0.125,"label":"We think this was probably written by a person. Automated checks can be wrong.","status":"decided"}
{"timestamp":"2026-11-05T02:22:11+00:00","creator_id":"attacker_RQ01","event":"rejected","status":"rejected","reason":"invalid_text","http_status":400}
{"timestamp":"2026-11-05T02:22:12+00:00","content_id":"f55f3243-6df5-429d-bdff-11fe6bc9fbf3","creator_id":"attacker_flood","guess":"human","model_score":0.0287,"style_score":0.4,"combined_score":0.2144,"label":"We think this was probably written by a person. Automated checks can be wrong.","status":"decided"}
{"timestamp":"2026-11-05T02:22:12+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"10 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03.** A non-native English speaker writing carefully was labeled AI with a
combined score of 0.6957. Both signals pushed in the same wrong direction
(`model_score` 0.8051 and `style_score` 0.5862), so this was not a marginal
threshold miss. It is the outcome I would least want to defend because the
system turned careful second-language writing into evidence against its writer.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Personal-style false positives | ≤ 1 of 10 labeled AI | 2/10 | 2/10 | 2/10 | MISSED |
| 2. Clearly different sources have a score spread | AI mean − human mean ≥ 0.20 | −0.1284 | −0.1284 | −0.1284 | MISSED |
| 3. Every label is reachable | 3/3 labels; 9/9 correct mappings | 3/3; 9/9 | 3/3; 9/9 | 3/3; 9/9 | MET |
| 4. Appeals enter review and remain auditable | 5/5 valid; unknown ID is 404 with 0 logs | 5/5; 404/0 | 5/5; 404/0 | 5/5; 404/0 | MET |
| 5. Bad text fails safely | 5/5 return 400 with 0 decisions | 5/5 | 5/5 | 5/5 | MET |

For Criterion 2, each trial's personal-style proxy mean was `0.6010` and the
AI set's mean was `0.4725`, producing the negative gap shown above. The
Criterion 1 samples were drafted by the assistant at my requested diction
level, so they are disclosed as proxy inputs rather than claimed as independent
human-authorship evidence.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

File: `results/run_2026-11-04_2136_before.md`.
Function: `run_eval.py::main` (with `run_appeal_trial` and
`run_bad_input_trial` for Criteria 4 and 5)

**Criterion 1 — Trial 1**

```json
[{"status":200,"guess":"unsure","confidence":0.5046,"model_score":0.4664,"style_score":0.5428},{"status":200,"guess":"unsure","confidence":0.5904,"model_score":0.5732,"style_score":0.6075},{"status":200,"guess":"unsure","confidence":0.6149,"model_score":0.6524,"style_score":0.5773},{"status":200,"guess":"ai","confidence":0.6667,"model_score":0.6713,"style_score":0.6621},{"status":200,"guess":"unsure","confidence":0.6282,"model_score":0.6206,"style_score":0.6358},{"status":200,"guess":"unsure","confidence":0.4187,"model_score":0.3606,"style_score":0.4769},{"status":200,"guess":"unsure","confidence":0.4556,"model_score":0.586,"style_score":0.3253},{"status":200,"guess":"unsure","confidence":0.4911,"model_score":0.3997,"style_score":0.5826},{"status":200,"guess":"ai","confidence":0.6642,"model_score":0.8742,"style_score":0.4542},{"status":200,"guess":"unsure","confidence":0.361,"model_score":0.2037,"style_score":0.5184}]
```

**Criterion 2 — Trial 1** (first five are personal-style proxies; last five
are unedited AI-generated samples)

```json
[{"status":200,"guess":"unsure","confidence":0.5046,"model_score":0.4664,"style_score":0.5428},{"status":200,"guess":"unsure","confidence":0.5904,"model_score":0.5732,"style_score":0.6075},{"status":200,"guess":"unsure","confidence":0.6149,"model_score":0.6524,"style_score":0.5773},{"status":200,"guess":"ai","confidence":0.6667,"model_score":0.6713,"style_score":0.6621},{"status":200,"guess":"unsure","confidence":0.6282,"model_score":0.6206,"style_score":0.6358},{"status":200,"guess":"unsure","confidence":0.5795,"model_score":0.772,"style_score":0.3869},{"status":200,"guess":"unsure","confidence":0.5181,"model_score":0.8255,"style_score":0.2106},{"status":200,"guess":"unsure","confidence":0.437,"model_score":0.7581,"style_score":0.1159},{"status":200,"guess":"unsure","confidence":0.4134,"model_score":0.6837,"style_score":0.1431},{"status":200,"guess":"unsure","confidence":0.4147,"model_score":0.8196,"style_score":0.0097}]
```

**Criterion 3 — Trial 1**

```json
[{"status":200,"guess":"human","confidence":0.3366,"label":"We think this was probably written by a person. Automated checks can be wrong."},{"status":200,"guess":"human","confidence":0.2647,"label":"We think this was probably written by a person. Automated checks can be wrong."},{"status":200,"guess":"human","confidence":0.1822,"label":"We think this was probably written by a person. Automated checks can be wrong."},{"status":200,"guess":"unsure","confidence":0.5013,"label":"We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result."},{"status":200,"guess":"unsure","confidence":0.5486,"label":"We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result."},{"status":200,"guess":"unsure","confidence":0.5286,"label":"We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result."},{"status":200,"guess":"ai","confidence":0.8583,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review."},{"status":200,"guess":"ai","confidence":0.7526,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review."},{"status":200,"guess":"ai","confidence":0.6957,"label":"We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review."}]
```

**Criterion 4 — Trial 1**

```json
[{"case":1,"submit_status":200,"content_id":"f49f6766-6e78-4688-a6e8-c59ea4aa7635","appeal_status":200,"appeal_content_id":"f49f6766-6e78-4688-a6e8-c59ea4aa7635","status":"under_review","reasoning":"Trial 1, case 1: I wrote this and request human review.","appeal_entries_added":1,"reasoning_recorded":true},{"case":2,"submit_status":200,"content_id":"15c32ab7-8b8e-453f-be5e-05e82f6986b6","appeal_status":200,"appeal_content_id":"15c32ab7-8b8e-453f-be5e-05e82f6986b6","status":"under_review","reasoning":"Trial 1, case 2: I wrote this and request human review.","appeal_entries_added":1,"reasoning_recorded":true},{"case":3,"submit_status":200,"content_id":"99cae2a7-dfe7-412d-8d16-6a898cd9c2dc","appeal_status":200,"appeal_content_id":"99cae2a7-dfe7-412d-8d16-6a898cd9c2dc","status":"under_review","reasoning":"Trial 1, case 3: I wrote this and request human review.","appeal_entries_added":1,"reasoning_recorded":true},{"case":4,"submit_status":200,"content_id":"57e5986d-160b-4b60-9127-168145d69b65","appeal_status":200,"appeal_content_id":"57e5986d-160b-4b60-9127-168145d69b65","status":"under_review","reasoning":"Trial 1, case 4: I wrote this and request human review.","appeal_entries_added":1,"reasoning_recorded":true},{"case":5,"submit_status":200,"content_id":"9b75b8ed-c0c9-44db-9d05-6f02fb296cbf","appeal_status":200,"appeal_content_id":"9b75b8ed-c0c9-44db-9d05-6f02fb296cbf","status":"under_review","reasoning":"Trial 1, case 5: I wrote this and request human review.","appeal_entries_added":1,"reasoning_recorded":true},{"case":"unknown_content_id","content_id":"unknown-1-6059947c-8b92-4943-bfc3-18bc499efa69","appeal_status":404,"error":"content_not_found","appeal_entries_added":0}]
```

**Criterion 5 — Trial 1**

```json
[{"status":400,"error":"invalid_text","message":"text must be a non-empty string.","decision_entries_added":0},{"status":400,"error":"invalid_text","message":"text must be a non-empty string.","decision_entries_added":0},{"status":400,"error":"invalid_text","message":"text must be a non-empty string.","decision_entries_added":0},{"status":400,"error":"invalid_text","message":"text must be a non-empty string.","decision_entries_added":0},{"status":400,"error":"text_too_long","message":"text must be 20,000 characters or fewer.","decision_entries_added":0}]
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
