import pytest


def sample(sid="one", category="A", split="profile", group="source", **kwargs):
    return {"id": sid, "category": category, "split": split, "source_group": group, "genre": "informal", "authorship_confidence": "high", "text": "Explain the result clearly.", **kwargs}


def test_ai_and_unknown_prose_not_learned(tool):
    corpus = {"samples": [sample(), sample("two", "C", group="other"), sample("three", "E", group="third")], "excluded_ids": []}
    r = tool("corpus_manager").propose_profile(corpus)
    assert r["personal_evidence_ids"] == ["one"]
    assert "two" in r["quarantined_ids"]
    assert "three" in r["quarantined_ids"]


def test_exclusion_revokes_sample(tool):
    r = tool("corpus_manager").propose_profile({"samples": [sample()], "excluded_ids": ["one"]})
    assert r["personal_evidence_ids"] == []


def test_same_source_cannot_leak_across_splits(tool):
    with pytest.raises(ValueError, match="split"):
        tool("corpus_manager").validate({"samples": [sample(), sample("two", split="heldout")]})


def test_post2017_not_canon(tool):
    with pytest.raises(ValueError, match="2018"):
        tool("corpus_manager").validate({"samples": [sample(category="P", original_year=2020, source_url="https://example.org")]})


def test_no_unconfirmed_authorship_promoted(tool):
    r = tool("corpus_manager").propose_profile({"samples": [sample(authorship_confidence="uncertain")]})
    assert r["personal_evidence_ids"] == []


def test_metrics_eligibility_must_be_boolean(tool):
    with pytest.raises(ValueError, match="metrics_eligible"):
        tool("corpus_manager").validate({"samples": [sample(metrics_eligible="false")]})
