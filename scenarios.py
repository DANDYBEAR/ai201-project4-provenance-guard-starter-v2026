"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

import csv
from pathlib import Path


def _attack_text(attack_id: str) -> str:
    """Reuse a known calibration input without duplicating the attack text."""
    path = Path(__file__).parent / "attack_set" / "attacks.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["id"] == attack_id:
                return row["text"]
    raise ValueError(f"attack {attack_id!r} was not found in {path}")


PERSONAL_STYLE_SAMPLES = [
    (
        "I had to restart this assignment because I missed one small setting. "
        "After I slowed down and read the file again, the problem made more sense."
    ),
    (
        "When I learn new code I like to test one part at a time. If I change too "
        "many things together, I dont know which change caused the error."
    ),
    (
        "My group had a hard time picking who would do each part of the project. "
        "We made a short list and split the work, which made it less confusing."
    ),
    (
        "I went to the store after class and forgot the main thing I needed. I got "
        "snacks and a drink, but I had to go back later for the charger."
    ),
    (
        "The bus was late this morning so I got to class a few minutes behind. I "
        "sent a message before class started because I did not want it to look like I forgot."
    ),
    (
        "I understand the lesson better when I can see a real example. Reading the "
        "definition helps, but trying it myself is what makes it stay in my head."
    ),
    (
        "I tried making dinner without checking the recipe first. It came out okay, "
        "but I used too much salt and next time I will measure it."
    ),
    (
        "I cleaned my room this weekend and found notes from an older class. I kept "
        "the useful pages and threw away the papers I knew I would never read again."
    ),
    (
        "The hardest part of this project was not writing the code. It was figuring "
        "out what the results meant and how to explain them in a simple way."
    ),
    (
        "I usually write my first draft fast and fix it after. That works better for "
        "me because stopping for every sentence makes me lose my idea."
    ),
]


AI_SAMPLES = [
    (
        "Effective project management requires careful planning, clear communication, "
        "and consistent evaluation. By following these principles, teams can improve "
        "productivity, reduce risk, and achieve successful outcomes."
    ),
    (
        "Technology plays an important role in modern education. It provides students "
        "with access to useful resources, supports collaboration, and creates new "
        "opportunities for personalized learning."
    ),
    (
        "A healthy lifestyle depends on several important habits. Regular exercise, "
        "balanced nutrition, and adequate sleep contribute to physical wellness, "
        "mental clarity, and long-term quality of life."
    ),
    (
        "Organizations must adapt to a rapidly changing environment. Strategic "
        "leadership, continuous innovation, and data-driven decision making enable "
        "businesses to remain competitive and serve customers effectively."
    ),
    (
        "Environmental sustainability is a shared responsibility. Individuals, "
        "businesses, and governments can conserve resources, reduce waste, and promote "
        "practices that protect the planet for future generations."
    ),
]

SCENARIOS = [
    {
        "name": "personal-style false positives",
        "criterion": 1,
        # The user asked the assistant to draft these at their diction level.
        # They are useful proxy inputs, but are not represented as human-authored.
        "texts": PERSONAL_STYLE_SAMPLES,
    },
    {
        "name": "source score spread",
        "criterion": 2,
        "groups": {"human": 5, "ai": 5},
        "texts": PERSONAL_STYLE_SAMPLES[:5] + AI_SAMPLES,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # These previously produced three examples in each configured band.
        "texts": [
            *[_attack_text(item) for item in ("EV01", "EV05", "PI02")],
            *[_attack_text(item) for item in ("EV03", "EV04", "PI06")],
            *[_attack_text(item) for item in ("EV10", "FP05", "FP03")],
        ],
    },
    {
        "name": "appeal path",
        "criterion": 4,
        "kind": "appeal",
        "texts": PERSONAL_STYLE_SAMPLES[:5],
    },
    {
        "name": "bad text input",
        "criterion": 5,
        "kind": "bad_input",
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \t\n", "creator_id": "eval_bad_whitespace"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "x" * 20_001, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
