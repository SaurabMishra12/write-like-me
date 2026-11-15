import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run(name, *args):
    return subprocess.run([sys.executable, str(ROOT / "tools" / name), *map(str, args)], capture_output=True, text=True)


@pytest.mark.parametrize("replacement,code,decision", [("Error is 0.1.", 2, "veto"), ("Error is 0.5.", 0, "identical"), ("The error is 0.5.", 3, "review_required")])
def test_preservation_cli_exit_contract(tmp_path, replacement, code, decision):
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    a.write_text("Error is 0.5.")
    b.write_text(replacement)
    before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (a, b)]
    r = run("preservation_checker.py", a, b)
    assert r.returncode == code, r.stderr
    assert json.loads(r.stdout)["decision"] == decision
    assert before == [hashlib.sha256(p.read_bytes()).hexdigest() for p in (a, b)]


def test_all_four_analysis_clis_read_real_files(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    a.write_text("Read the figure.")
    b.write_text("Read the figure carefully.")
    assert json.loads(run("style_analyzer.py", a).stdout)["words"] == 3
    assert json.loads(run("writing_auditor.py", a).stdout)["authorship_inference"] == "not_performed"
    assert json.loads(run("compare_revisions.py", a, b).stdout)["preferred_version"] is None
    guarded = run("engine.py", "review", a, b)
    assert guarded.returncode == 3
    assert json.loads(guarded.stdout)["delivery_status"] == "review_required"


def test_learn_creates_proposal_and_cannot_overwrite(tmp_path):
    corpus = tmp_path / "corpus.json"
    corpus.write_text(json.dumps({"samples": [{"id": "one", "category": "A", "split": "profile", "source_group": "one", "genre": "informal", "authorship_confidence": "high", "text": "Explain it clearly."}]}))
    current = tmp_path / "current.yaml"
    current.write_text('{"version": "original"}\n')
    proposal = tmp_path / "proposed.yaml"
    r = run("corpus_manager.py", corpus, "--proposal", proposal, "--current-profile", current)
    assert r.returncode == 0, r.stderr
    assert "--- current-profile" in r.stdout
    assert current.read_text() == '{"version": "original"}\n'
    assert json.loads(proposal.read_text())["personal_evidence_ids"] == ["one"]
    assert run("corpus_manager.py", corpus, "--proposal", proposal).returncode != 0
    assert run("corpus_manager.py", corpus, "--proposal", tmp_path / "voice-profile.yaml").returncode != 0


def test_context_load_is_actual_and_readonly():
    r = run("engine.py", "context", "Write Like Me: Email")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["genre"] == "email"
    assert data["host_model_required"]
    assert not data["writes_or_sends"]
