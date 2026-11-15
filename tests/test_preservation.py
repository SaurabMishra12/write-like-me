import pytest


@pytest.mark.parametrize("before,after", [
    ("Accuracy is 91.2% on 50 cases.", "Accuracy is 92.1% on 50 cases."),
    ("We used fifty examples.", "We used sixty examples."),
    ("Measured on 2026-11-15.", "Measured on 2026-11-16."),
    ("Richard Feynman gave the talk.", "Richard Hamming gave the talk."),
    ("Dr Rao measured it.", "Dr Roy measured it."),
    ("It did not improve accuracy.", "It did improve accuracy."),
    ("It may improve accuracy.", "It will improve accuracy."),
    ("The effect is not significant.", "The effect is significant."),
    ("We observed a decrease.", "We observed an increase."),
    ("Run `solver --seed 7`.", "Run `solver --seed 8`."),
    ("```python\nx += 1\n```", "```python\nx -= 1\n```"),
    ("Time is O(n log n).", "Time is O(n)."),
])
def test_truth_sensitive_mutations_veto(tool, before, after):
    assert tool("preservation_checker").check(before, after)["decision"] == "veto"


@pytest.mark.parametrize("before,after", [
    (r"Let $x^2$ be fixed.", r"Let $x^3$ be fixed."),
    (r"Use $$a=b+c$$.", r"Use $$a=b-c$$."),
    (r"Use \(x+y\).", r"Use \(x-y\)."),
    (r"Use \[x+y\].", r"Use \[x-y\]."),
    ("\\begin{align}\na&=b \\\\\nc&=d\n\\end{align}", "\\begin{align}\na&=z \\\\\nc&=d\n\\end{align}"),
    (r"\newcommand{\gain}{0.5}", r"\newcommand{\gain}{0.7}"),
])
def test_latex_mutations_veto(tool, before, after):
    assert tool("preservation_checker").check(before, after)["decision"] == "veto"


def test_changed_meaning_is_not_cleared_by_token_preservation(tool):
    r = tool("preservation_checker").check("The method is reliable.", "The method is unreliable.")
    assert r["decision"] in {"veto", "review_required"}
    assert not r["semantic_verified"]


def test_explicit_lowercase_entity_lock(tool):
    r = tool("preservation_checker").check("Use numpy here.", "Use scipy here.", locks={"terms": ["numpy"]})
    assert r["decision"] == "veto"


def test_added_experience_is_blocked(tool):
    r = tool("preservation_checker").check("I study graphs.", "I study graphs. I led a team at NASA.")
    assert r["decision"] == "veto"


def test_clear_original_is_left_unchanged(tool):
    text = "The run failed because the input was empty."
    r = tool("preservation_checker").check(text, text)
    assert r["decision"] == "identical"
    assert r["edit_ratio"] == 0


def test_minimal_mode_limits_rewriting(tool):
    r = tool("preservation_checker").check("Read the chart.", "Please examine the visual evidence carefully before drawing a conclusion.", minimal=True)
    assert r["decision"] == "veto"
    assert any(x["kind"] == "edit_budget" for x in r["violations"])


def test_cannot_certify_grammar_or_voice(tool):
    r = tool("preservation_checker").check("The code works.", "The code work.")
    assert r["decision"] == "review_required"
    assert r["grammar_verified"] is False
    assert r["voice_verified"] is False


@pytest.mark.parametrize("before,after", [
    ("Use ``x + y`` here.", "Use ``x - y`` here."),
    ("```python\nx += y\n````", "```python\nx -= y\n````"),
])
def test_markdown_code_delimiters_are_protected(tool, before, after):
    assert tool("preservation_checker").check(before, after)["decision"] == "veto"


@pytest.mark.parametrize("before,after", [
    ("In this hypothetical example, I helped test a parser.", "I helped test a parser."),
    ("This is a planned experiment.", "This is an experiment."),
    ("This constructed example reports a toy result.", "This example reports a result."),
])
def test_evidence_status_cannot_be_silently_promoted(tool, before, after):
    result = tool("preservation_checker").check(before, after)
    assert result["decision"] == "veto"
    assert any(v["kind"] == "evidence_status" for v in result["violations"])
