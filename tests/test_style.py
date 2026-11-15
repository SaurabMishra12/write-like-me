import pytest


def test_measurable_lengths(tool):
    r = tool("style_analyzer").analyze("One sentence. Here are four words.")
    assert r["words"] == 6
    assert r["sentences"] == 2
    assert r["sentence_words"]["mean"] == 3
    assert r["sentence_words"]["median"] == 3


def test_decimal_not_sentence_boundary(tool):
    r = tool("style_analyzer").analyze("Error was 0.5. It fell.")
    assert r["sentences"] == 2


def test_unicode_and_empty(tool):
    m = tool("style_analyzer")
    assert m.analyze("")["sentence_words"]["mean"] is None
    assert m.analyze("यह normal check है।")["words"] == 4
    assert m.analyze("यह normal check है।")["scripts"]["devanagari_characters"] > 0


def test_word_is_not_an_authorship_fingerprint(tool):
    r = tool("writing_auditor").audit("We delve into the archive to locate the letter.", genre="academic")
    assert not r["findings"]
    assert r["authorship_inference"] == "not_performed"


def test_repeated_scaffolding_is_contextual(tool):
    text = "Furthermore, the work is useful. Moreover, the work is useful. Additionally, the work is useful."
    r = tool("writing_auditor").audit(text, genre="academic")
    assert any(x["pattern"] == "mechanical_transitions" for x in r["findings"])


def test_lists_legitimate_in_documentation(tool):
    text = "- Install Python.\n- Run the script.\n- Read the output.\n- Inspect errors."
    r = tool("writing_auditor").audit(text, genre="technical")
    assert not any(x["pattern"] == "list_density" for x in r["findings"])


def test_no_detector_probability_or_global_quality_score(tool):
    r = tool("writing_auditor").audit("The result is clear.")
    assert "ai_probability" not in r
    assert "quality_score" not in r
