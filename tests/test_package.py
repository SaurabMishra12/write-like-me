import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "build_package.py"


def seed(root):
    root.mkdir()
    (root / "SKILL.md").write_text("---\nname: write-like-me\ndescription: Editorial workflow\n---\n", encoding="utf-8")
    (root / "README.md").write_text("Public instructions\n", encoding="utf-8")
    return root


def invoke(root, destination, python_flags=()):
    return subprocess.run(
        [sys.executable, *python_flags, str(SCRIPT), "--root", str(root), "--output", str(destination)],
        capture_output=True, text=True, timeout=20,
    )


def test_export_excludes_private_configuration_caches_and_raw_samples(tmp_path):
    root = seed(tmp_path / "source")
    excluded = [
        "private/personal-samples.json", ".git/config", ".codex/config.toml",
        ".agents/skills/secret.md", ".aws/credentials", ".env",
        "tools/__pycache__/secret.pyc", ".pytest_cache/secret",
        "dist/previous.zip", "research/raw-samples.json",
        "research/source-locators.json", "evaluation/private/heldout.json",
        "local-only.txt",
    ]
    for name in excluded:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("PRIVATE_SENTINEL", encoding="utf-8")
    result = root / "evaluation/results/synthetic.json"
    result.parent.mkdir(parents=True)
    result.write_text('{"kind":"synthetic","score":1}\n', encoding="utf-8")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        assert "write-like-me/SKILL.md" in names
        assert "write-like-me/evaluation/results/synthetic.json" in names
        assert all(name.startswith("write-like-me/") for name in names)
        assert not any("PRIVATE_SENTINEL" in archive.read(name).decode("utf-8") for name in names)
        assert all("write-like-me/" + name not in names for name in excluded)


def test_archive_manifest_and_sidecar_verify_actual_exported_bytes(tmp_path):
    root = seed(tmp_path / "source")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        manifest = archive.read("write-like-me/SHA256SUMS").decode("utf-8")
        records = [line.split("  ", 1) for line in manifest.splitlines()]
        expected_members = set(archive.namelist()) - {"write-like-me/SHA256SUMS"}
        assert {"write-like-me/" + path for _, path in records} == expected_members
        for digest, path in records:
            assert digest == hashlib.sha256(archive.read("write-like-me/" + path)).hexdigest()
    digest, filename = destination.with_suffix(".zip.sha256").read_text().strip().split("  ", 1)
    assert filename == "release.zip"
    assert digest == hashlib.sha256(destination.read_bytes()).hexdigest()


def test_only_root_gitignore_ships_while_private_dotfiles_stay_excluded(tmp_path):
    root = seed(tmp_path / "source")
    ignore_bytes = b"private/\n__pycache__/\n.pytest_cache/\ndist/\n*.pyc\n"
    (root / ".gitignore").write_bytes(ignore_bytes)
    for name in [".git/config", ".agents/private.md", ".aws/credentials", ".env", "docs/.gitignore"]:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("PRIVATE_SENTINEL")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        assert archive.read("write-like-me/.gitignore") == ignore_bytes
        assert [name for name in archive.namelist() if "/." in name] == ["write-like-me/.gitignore"]


@pytest.mark.parametrize("kind", ["file", "directory"])
def test_export_rejects_public_symlinks_without_following_them(tmp_path, kind):
    root = seed(tmp_path / "source")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_text("PRIVATE_SENTINEL")
    docs = root / "docs"
    docs.mkdir()
    if kind == "file":
        (docs / "linked.md").symlink_to(outside / "secret.md")
    else:
        (docs / "linked").symlink_to(outside, target_is_directory=True)
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode != 0
    assert "symlink" in completed.stderr.lower()
    assert not destination.exists()


def test_agent_roles_and_project_instructions_ship_but_hidden_agent_config_does_not(tmp_path):
    root = seed(tmp_path / "source")
    files = {
        "agents/factual-guardian.md": "Preserve factual claims.\n",
        "agents/protocol.md": "Use one shared ledger.\n",
        "AGENTS.md": "Project instructions.\n",
        "CLAUDE.md": "Host adapter pointer.\n",
        ".agents/skills/private.md": "PRIVATE_SENTINEL",
    }
    for name, text in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        for name in ["agents/factual-guardian.md", "agents/protocol.md", "AGENTS.md", "CLAUDE.md"]:
            assert "write-like-me/" + name in names
            assert archive.read("write-like-me/" + name).decode("utf-8") == files[name]
        assert not any("/.agents/" in name for name in names)


def test_export_records_profile_transformations_without_rewriting_checkout_freeze(tmp_path):
    root = seed(tmp_path / "source")
    profile = root / "profiles/voice-profile.yaml"
    profile.parent.mkdir()
    original_bytes = b'{"evidence":{"private_manifest":"private/samples.json","count":4}}\n'
    profile.write_bytes(original_bytes)
    checkout_digest = hashlib.sha256(original_bytes).hexdigest()
    freeze = root / "evaluation/results/profile-freeze.json"
    freeze.parent.mkdir(parents=True)
    freeze_bytes = json.dumps({"profiles/voice-profile.yaml": checkout_digest}).encode("utf-8")
    freeze.write_bytes(freeze_bytes)
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["transformed_files"] == ["profiles/voice-profile.yaml"]
    with zipfile.ZipFile(destination) as archive:
        transformed_bytes = archive.read("write-like-me/profiles/voice-profile.yaml")
        export_digest = hashlib.sha256(transformed_bytes).hexdigest()
        assert export_digest != checkout_digest
        manifest = json.loads(archive.read("write-like-me/EXPORT-MANIFEST.json"))
        assert manifest["transformations"] == [{
            "path": "profiles/voice-profile.yaml",
            "operation": "remove_private_provenance_metadata",
            "checkout_sha256": checkout_digest,
            "export_sha256": export_digest,
        }]
        assert "checkout" in manifest["freeze_scope"].lower()
        assert archive.read("write-like-me/evaluation/results/profile-freeze.json") == freeze_bytes
    assert profile.read_bytes() == original_bytes
    assert freeze.read_bytes() == freeze_bytes



def test_zip_bytes_do_not_depend_on_source_mtimes_permissions_or_creation_order(tmp_path):
    root = seed(tmp_path / "source")
    docs = root / "docs"
    docs.mkdir()
    (docs / "z.md").write_text("Z\n")
    (docs / "a.md").write_text("A\n")
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    one = invoke(root, first)
    assert one.returncode == 0, one.stderr
    os.utime(docs / "z.md", (1730000000, 1730000000))
    (docs / "z.md").chmod(0o700)
    original = (docs / "a.md").read_bytes()
    (docs / "a.md").unlink()
    (docs / "a.md").write_bytes(original)
    two = invoke(root, second)
    assert two.returncode == 0, two.stderr
    assert first.read_bytes() == second.read_bytes()


def test_private_profile_provenance_is_removed_from_export_only(tmp_path):
    root = seed(tmp_path / "source")
    profiles = root / "profiles"
    profiles.mkdir()
    profile = profiles / "voice-profile.yaml"
    original = {
        "status": "provisional",
        "evidence": {"count": 4, "private_manifest": "/private/raw.json", "message_id": "PRIVATE_SENTINEL"},
        "nested": [{"source_locator": "PRIVATE_SENTINEL", "confidence": "low"}],
    }
    profile.write_text(json.dumps(original), encoding="utf-8")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        exported = json.loads(archive.read("write-like-me/profiles/voice-profile.yaml"))
        assert exported == {
            "status": "provisional", "evidence": {"count": 4},
            "nested": [{"confidence": "low"}],
        }
    assert json.loads(profile.read_text()) == original


def test_non_json_yaml_with_private_provenance_fails_closed(tmp_path):
    root = seed(tmp_path / "source")
    profiles = root / "profiles"
    profiles.mkdir()
    (profiles / "voice.yaml").write_text("status: provisional\nsource_locator: /private/raw.txt\n")
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode != 0
    assert "provenance" in completed.stderr.lower()
    assert not destination.exists()


@pytest.mark.parametrize("yaml_text", [
    '"source_locator": PRIVATE_SENTINEL\nstatus: provisional\n',
    "SOURCE_LOCATOR: PRIVATE_SENTINEL\nstatus: provisional\n",
    "evidence: {count: 4, source_locator: PRIVATE_SENTINEL}\n",
    'evidence: {"source_\\u006cocator": PRIVATE_SENTINEL}\n',
    "evidence:\n  source_locator: PRIVATE_SENTINEL\nevidence: {count: 4}\n",
    "evidence: !!pairs [{source_locator: PRIVATE_SENTINEL}]\n",
])
def test_yaml_quoting_case_flow_and_escapes_cannot_hide_private_provenance(tmp_path, yaml_text):
    root = seed(tmp_path / "source")
    profile = root / "profiles/voice.yaml"
    profile.parent.mkdir()
    profile.write_text(yaml_text)
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode != 0
    assert "provenance" in completed.stderr.lower()
    assert not destination.exists()
    assert profile.read_text() == yaml_text


def test_nested_uppercase_json_provenance_is_sanitized(tmp_path):
    root = seed(tmp_path / "source")
    profile = root / "profiles/voice.yaml"
    profile.parent.mkdir()
    profile.write_text('{"evidence":[{"SOURCE_LOCATOR":"PRIVATE_SENTINEL","count":4}]}')
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        assert json.loads(archive.read("write-like-me/profiles/voice.yaml")) == {
            "evidence": [{"count": 4}],
        }


def test_duplicate_json_parents_cannot_hide_a_private_provenance_branch(tmp_path):
    root = seed(tmp_path / "source")
    profile = root / "profiles/voice.json"
    profile.parent.mkdir()
    profile.write_text('{"evidence":{"source_locator":"PRIVATE_SENTINEL"},"evidence":{"count":4}}')
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode != 0
    assert "provenance" in completed.stderr.lower()
    assert not destination.exists()


def test_root_profile_pointer_exports_without_optional_yaml_parser(tmp_path):
    root = seed(tmp_path / "source")
    pointer = "# Canonical editable profile\nschema_version: 1\nprofile_path: profiles/voice-profile.yaml\n"
    (root / "voice-profile.yaml").write_text(pointer)
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination, python_flags=("-S",))
    assert completed.returncode == 0, completed.stderr
    with zipfile.ZipFile(destination) as archive:
        assert archive.read("write-like-me/voice-profile.yaml").decode() == pointer


def test_other_non_json_yaml_requires_parser_when_site_packages_are_unavailable(tmp_path):
    root = seed(tmp_path / "source")
    profile = root / "profiles/voice.yaml"
    profile.parent.mkdir()
    profile.write_text('evidence: {"source_\\u006cocator": PRIVATE_SENTINEL}\n')
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination, python_flags=("-S",))
    assert completed.returncode != 0
    assert "provenance" in completed.stderr.lower()
    assert not destination.exists()


def test_missing_skill_cannot_produce_a_misleading_release(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    destination = tmp_path / "release.zip"
    completed = invoke(root, destination)
    assert completed.returncode != 0
    assert "skill.md" in completed.stderr.lower()
    assert not destination.exists()

