import pytest


def records():
    tasks = [{"id": "one", "genre": "general", "request": "Report the value.", "facts": "Value is 7.", "locks": ["7"]}]
    baselines = [{"task_id": "one", "condition_B": "Value is 7.", "condition_C": "The value is 8."}]
    guided = [{"task_id": "one", "condition_D": "The value is 7."}]
    return tasks, baselines, guided


def test_surface_match_is_not_semantic_verification(tool):
    r = tool("evaluate_benchmark").evaluate(*records())
    assert len(r["rows"]) == 3
    assert all(row["semantic_verified"] is False for row in r["rows"])
    bad = next(row for row in r["rows"] if row["condition"] == "C")
    assert bad["missing_required_spans"] == ["7"]


def test_blind_packet_hides_condition_mapping(tool):
    m = tool("evaluate_benchmark")
    packet, key = m.blind_packet(*records(), seed=19)
    again, again_key = m.blind_packet(*records(), seed=19)
    assert packet == again and key == again_key
    assert set(key["one"].values()) == {"B", "C", "D"}
    assert all("condition" not in c for c in packet["tasks"][0]["candidates"])


def test_missing_generation_fails_closed(tool):
    tasks, base, guided = records()
    with pytest.raises(ValueError, match="task"):
        tool("evaluate_benchmark").evaluate(tasks, base, [])
