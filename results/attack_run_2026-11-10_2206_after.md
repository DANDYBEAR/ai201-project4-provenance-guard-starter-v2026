# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 22:06
- Auto-marked BROKE (5xx, crash, no response): **0**
- Manually judged from each attack's target: **56**
- Final verdicts: **31 HELD, 25 BROKE**

The Verdict column was completed using the same rules as the before run. The
only intended change was route validation for unscorable input.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `95c02469-18c5-45f1-a969-a6b43c940187` | human | 0.337 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1353cc04-a1ca-4154-b635-70b6486d676a` | unsure | 0.378 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `776eb533-2777-4c3f-82c4-e0c1863210bf` | unsure | 0.501 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d1ea2546-eaac-4f32-bafc-88a516b49723` | unsure | 0.549 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `aab77ae7-72e2-48b4-9bed-e3c164a2640e` | human | 0.265 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `cfc8295a-316f-4e5b-a1fb-8e68850bfc14` | unsure | 0.407 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `af4ec1ec-c8aa-43a4-8411-900110cb29eb` | unsure | 0.474 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `9a9bd276-b780-4415-9cfb-a215183aade6` | unsure | 0.353 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `18b9dc34-3af0-405f-bf89-51f3e7719d10` | unsure | 0.511 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `14ab3a81-2a6a-4e85-a46d-6c6e3b7988af` | ai | 0.858 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ffc2f337-ad73-451c-acba-e9a95b0bfd1f` | unsure | 0.553 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `9be3f859-b11f-45aa-943d-ed6bca5956bb` | ai | 0.689 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1fd2971e-87c6-4b7a-9ed7-b6809e2ac3dc` | ai | 0.696 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `bad7fdb4-d447-4c9f-93a0-2019ec38307d` | ai | 0.650 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `6003b656-49db-4601-bb79-7c592dfc4444` | ai | 0.753 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `0460995e-493b-4025-82da-451b23c28c18` | ai | 0.655 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5b97f8ec-a44e-43f0-bfa7-70fa118c8711` | ai | 0.676 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `2d67137a-9373-432d-95a3-cc22cbeb6fcf` | human | 0.342 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `804d902c-fa5c-44bd-ab2d-5c659637a5e8` | human | 0.335 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e553d13c-781a-43e6-a7c9-33f281029c3a` | human | 0.182 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `fd721318-073e-4e54-886a-b02eb8b53689` | unsure | 0.474 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2a574922-7829-40f2-b5b7-39bb76100de5` | unsure | 0.410 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `394dfb1f-f3fb-4fd8-8316-9ea95f92d9e2` | unsure | 0.413 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `40aaca00-d074-45b8-93a1-e43439d843da` | unsure | 0.529 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7b1e07be-0789-401d-8436-7bd9c5d8d5ee` | human | 0.214 | BROKE |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0e6c0e17-fa14-4969-8efa-92f919d4af6a` | human | 0.214 | BROKE |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `434ced3b-caa9-4991-9d3b-9a2b7a967435` | human | 0.214 | BROKE |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5ffeaf35-c347-47d5-9f9f-ef2133180bbb` | human | 0.214 | BROKE |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2ce8565b-e606-4c9c-9805-203d6afeca1a` | human | 0.214 | BROKE |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5e2c8e78-b8ef-4b2d-b360-2713091416d8` | human | 0.214 | BROKE |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1d4fac76-6c67-42c2-aae1-39c0fbd00731` | human | 0.214 | BROKE |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `593d86fe-d3b4-480e-b23e-287303645132` | human | 0.214 | BROKE |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `82bab60a-4af8-43da-84d4-e1d6cedb2637` | human | 0.214 | BROKE |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5dfcf7ba-4265-44b8-b99e-a0bdedd0d273` | human | 0.214 | BROKE |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 2 | 6 |
| `flood_same_creator` | 12 | 2 | 10 |
| `malformed` | 20 | 20 | 0 |
| `prompt_injection` | 6 | 6 | 0 |
| **Total** | **56** | **31** | **25** |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "95c02469-18c5-45f1-a969-a6b43c940187",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3366,
  "model_score": 0.1635,
  "style_score": 0.5097,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1353cc04-a1ca-4154-b635-70b6486d676a",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3778,
  "model_score": 0.5943,
  "style_score": 0.1613,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "776eb533-2777-4c3f-82c4-e0c1863210bf",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5013,
  "model_score": 0.6662,
  "style_score": 0.3365,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "d1ea2546-eaac-4f32-bafc-88a516b49723",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5486,
  "model_score": 0.6114,
  "style_score": 0.4858,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "aab77ae7-72e2-48b4-9bed-e3c164a2640e",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2647,
  "model_score": 0.3212,
  "style_score": 0.2083,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "cfc8295a-316f-4e5b-a1fb-8e68850bfc14",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4066,
  "model_score": 0.5727,
  "style_score": 0.2405,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "af4ec1ec-c8aa-43a4-8411-900110cb29eb",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4736,
  "model_score": 0.5862,
  "style_score": 0.3609,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "9a9bd276-b780-4415-9cfb-a215183aade6",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3533,
  "model_score": 0.2452,
  "style_score": 0.4615,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "18b9dc34-3af0-405f-bf89-51f3e7719d10",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5108,
  "model_score": 0.7042,
  "style_score": 0.3173,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "14ab3a81-2a6a-4e85-a46d-6c6e3b7988af",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8583,
  "model_score": 0.9792,
  "style_score": 0.7374,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "ffc2f337-ad73-451c-acba-e9a95b0bfd1f",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5528,
  "model_score": 0.6175,
  "style_score": 0.4881,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "9be3f859-b11f-45aa-943d-ed6bca5956bb",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6889,
  "model_score": 0.7387,
  "style_score": 0.6391,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "1fd2971e-87c6-4b7a-9ed7-b6809e2ac3dc",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6957,
  "model_score": 0.8051,
  "style_score": 0.5862,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "bad7fdb4-d447-4c9f-93a0-2019ec38307d",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.65,
  "model_score": 0.8329,
  "style_score": 0.467,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "6003b656-49db-4601-bb79-7c592dfc4444",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7526,
  "model_score": 0.8005,
  "style_score": 0.7047,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0460995e-493b-4025-82da-451b23c28c18",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6553,
  "model_score": 0.8814,
  "style_score": 0.4293,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "5b97f8ec-a44e-43f0-bfa7-70fa118c8711",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.676,
  "model_score": 0.8816,
  "style_score": 0.4704,
  "label": "We found patterns often associated with AI-generated writing, but this is not proof of authorship. The writer can appeal this result for human review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "2d67137a-9373-432d-95a3-cc22cbeb6fcf",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3418,
  "model_score": 0.3223,
  "style_score": 0.3613,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "804d902c-fa5c-44bd-ab2d-5c659637a5e8",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3354,
  "model_score": 0.4625,
  "style_score": 0.2082,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "e553d13c-781a-43e6-a7c9-33f281029c3a",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1822,
  "model_score": 0.2044,
  "style_score": 0.16,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "fd721318-073e-4e54-886a-b02eb8b53689",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4737,
  "model_score": 0.5943,
  "style_score": 0.3531,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2a574922-7829-40f2-b5b7-39bb76100de5",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.41,
  "model_score": 0.4998,
  "style_score": 0.3202,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "394dfb1f-f3fb-4fd8-8316-9ea95f92d9e2",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4129,
  "model_score": 0.6401,
  "style_score": 0.1857,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "40aaca00-d074-45b8-93a1-e43439d843da",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5286,
  "model_score": 0.5583,
  "style_score": 0.4989,
  "label": "We cannot reliably tell how this text was written. No conclusion about the writer should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "7b1e07be-0789-401d-8436-7bd9c5d8d5ee",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "0e6c0e17-fa14-4969-8efa-92f919d4af6a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "434ced3b-caa9-4991-9d3b-9a2b7a967435",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "5ffeaf35-c347-47d5-9f9f-ef2133180bbb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "2ce8565b-e606-4c9c-9805-203d6afeca1a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "5e2c8e78-b8ef-4b2d-b360-2713091416d8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "1d4fac76-6c67-42c2-aae1-39c0fbd00731",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "593d86fe-d3b4-480e-b23e-287303645132",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "82bab60a-4af8-43da-84d4-e1d6cedb2637",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "5dfcf7ba-4265-44b8-b99e-a0bdedd0d273",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2144,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person. Automated checks can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
