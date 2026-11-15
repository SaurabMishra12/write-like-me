from pathlib import Path
import json
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("command,genre", [("Email", "email"), ("Academic", "academic"), ("Blog", "blog"), ("Speak", "speaking"), ("Explain", "blog"), ("Minimal", "general"), ("Compare", "general"), ("Learn", "general"), ("Audit", "general"), ("Rewrite", "general")])
def test_commands_load_relevant_workflow(tool, command, genre):
    r = tool("engine").route("Write Like Me: " + command, ROOT)
    assert r["genre"] == genre
    assert r["workflow_text"]
    assert r["profile"]["schema_version"] == 1
    assert len(r["loaded_files"]) <= 5


def test_natural_request_routes(tool):
    assert tool("engine").route("Draft an email to a professor", ROOT)["genre"] == "email"


def test_unknown_command_fails(tool):
    with pytest.raises(ValueError):
        tool("engine").route("Write Like Me: Teleport", ROOT)


def test_guardian_veto_propagates_to_final(tool):
    r = tool("engine").review("Error is 0.5.", "Error is 0.1.", root=ROOT)
    assert r["delivery_status"] == "blocked"
    assert r["candidate_text"] is None


def test_editor_never_auto_approves_semantic_change(tool):
    r = tool("engine").review("This test passed.", "This test succeeded.", root=ROOT)
    assert r["delivery_status"] == "review_required"


def test_compare_reports_changes_without_inventing_a_winner(tool):
    r = tool("compare_revisions").compare("Read the figure.", "Read the figure carefully.")
    assert r["diff"]
    assert r["preferred_version"] is None


def test_profile_must_be_a_mapping(tool, tmp_path):
    path = tmp_path / "bad-profile.yaml"
    path.write_text("[]")
    with pytest.raises(ValueError, match="mapping"):
        tool("engine")._load_yaml(path)


def test_excluding_evidence_disables_dependent_patterns(tool, tmp_path):
    for folder in ("profiles", "workflows"):
        shutil.copytree(ROOT / folder, tmp_path / folder)
    path = tmp_path / "profiles" / "voice-profile.yaml"
    profile = json.loads(path.read_text())
    profile["evidence"]["excluded_ids"] = ["A01"]
    path.write_text(json.dumps(profile))
    r = tool("engine").route("Write Like Me: Rewrite", tmp_path)
    assert all("A01" not in p["evidence_ids"] for p in r["profile"]["personal_patterns"])
    assert r["profile"]["evidence"]["category_A"]["status"] == "recompute_required_after_exclusion"
    assert path.read_text() == json.dumps(profile)
