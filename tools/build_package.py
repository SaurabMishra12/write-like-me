#!/usr/bin/env python3
"""Build a deterministic public skill archive without installing it."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import zipfile


PUBLIC_ROOT_FILES = {
    "SKILL.md", "README.md", "LICENSE", "VOICE_PROFILE.md", "WRITING_EXAMPLES.md",
    "WRITING_PATTERNS.md", "STYLE_CONFIDENCE_REPORT.md", "voice-profile.yaml",
    "pyproject.toml", "requirements.txt", "pytest.ini", "AGENTS.md", "CLAUDE.md",
    ".gitignore",
}
PUBLIC_DIRECTORIES = {
    "adapters", "agents", "docs", "evaluation", "examples", "profiles", "references",
    "research", "roles", "tests", "tools", "workflows", "templates", "assets",
}
EXCLUDED_DIRECTORIES = {
    "private", "__pycache__", "dist", "build", "node_modules", "venv", "local",
    "local-artifacts", "secrets", "raw-samples", "raw_samples",
}
EXCLUDED_FILENAMES = {
    "personal-samples.json", "raw-samples.json", "raw_samples.json",
    "source-locators.json", "source_locators.json", "voice_evidence.md",
}
PRIVATE_KEYS = {
    "private_manifest", "private_source", "private_sources", "private_source_path",
    "private_source_locator", "private_source_locators", "raw_sample",
    "raw_samples", "chat_id", "chat_ids", "conversation_id", "conversation_ids",
    "thread_id", "thread_ids", "message_id", "message_ids", "source_path",
    "source_paths", "local_source_path", "local_source_paths", "source_locator",
    "source_locators",
}
PUBLIC_PROFILE_POINTER = re.compile(
    r"\A(?:[ \t]*(?:#[^\r\n]*)?\r?\n)*"
    r"schema_version:[ \t]*[0-9]+[ \t]*\r?\n"
    r"profile_path:[ \t]*profiles/[A-Za-z0-9_.-]+\.ya?ml[ \t]*(?:\r?\n)?\Z"
)


def _is_excluded(relative):
    if relative.as_posix() == ".gitignore":
        return False
    parts = relative.parts
    return (
        any(part.startswith(".") or part.casefold() in EXCLUDED_DIRECTORIES for part in parts)
        or relative.name.casefold() in EXCLUDED_FILENAMES
        or relative.suffix.casefold() in {".pyc", ".pyo", ".zip", ".sha256"}
    )


def _public_paths(root):
    paths = []
    for directory, subdirectories, filenames in os.walk(root, topdown=True, followlinks=False):
        parent = Path(directory)
        kept = []
        for name in sorted(subdirectories):
            path = parent / name
            relative = path.relative_to(root)
            if _is_excluded(relative) or relative.parts[0] not in PUBLIC_DIRECTORIES:
                continue
            if path.is_symlink():
                raise ValueError("Refusing public symlink: " + relative.as_posix())
            kept.append(name)
        subdirectories[:] = kept
        for name in sorted(filenames):
            path = parent / name
            relative = path.relative_to(root)
            if _is_excluded(relative):
                continue
            if len(relative.parts) == 1 and name not in PUBLIC_ROOT_FILES:
                continue
            if len(relative.parts) > 1 and relative.parts[0] not in PUBLIC_DIRECTORIES:
                continue
            if path.is_symlink():
                raise ValueError("Refusing public symlink: " + relative.as_posix())
            if any(character in relative.as_posix() for character in "\r\n\\"):
                raise ValueError("Unsafe archive filename: " + repr(relative.as_posix()))
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ValueError("Refusing non-regular public file: " + relative.as_posix())
            paths.append((relative.as_posix(), path))
    return sorted(paths)


def _without_private_metadata(value):
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("Metadata keys must be text to verify private provenance")
        return {
            key: _without_private_metadata(item)
            for key, item in value.items()
            if key.casefold() not in PRIVATE_KEYS
        }
    if isinstance(value, list):
        return [_without_private_metadata(item) for item in value]
    return value


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate metadata keys prevent private provenance validation")
        result[key] = value
    return result


def _validate_yaml_provenance(root_node, yaml):
    active = set()
    checked = set()
    scalar_tags = {
        "tag:yaml.org,2002:" + tag for tag in ("str", "int", "float", "bool", "null")
    }

    def visit(node):
        if node is None or id(node) in checked:
            return
        if id(node) in active:
            raise ValueError("Recursive YAML provenance cannot be safely exported")
        active.add(id(node))
        if isinstance(node, yaml.nodes.MappingNode):
            if node.tag != "tag:yaml.org,2002:map":
                raise ValueError("Unsupported YAML mapping tag prevents provenance validation")
            for key, value in node.value:
                if not isinstance(key, yaml.nodes.ScalarNode) or key.tag != "tag:yaml.org,2002:str":
                    raise ValueError("YAML provenance requires plain text keys")
                if key.value.casefold() in PRIVATE_KEYS:
                    raise ValueError("Private provenance in non-JSON YAML requires manual removal")
                visit(value)
        elif isinstance(node, yaml.nodes.SequenceNode):
            if node.tag != "tag:yaml.org,2002:seq":
                raise ValueError("Unsupported YAML sequence tag prevents provenance validation")
            for item in node.value:
                visit(item)
        elif not isinstance(node, yaml.nodes.ScalarNode) or node.tag not in scalar_tags:
            raise ValueError("Unsupported YAML scalar tag prevents provenance validation")
        active.remove(id(node))
        checked.add(id(node))

    visit(root_node)


def _export_bytes(path, payload=None):
    if payload is None:
        payload = path.read_bytes()
    if path.suffix.casefold() not in {".json", ".yaml", ".yml"}:
        return payload
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Metadata must be UTF-8: " + path.name) from error
    try:
        original = json.loads(text, object_pairs_hook=_unique_json_object)
    except json.JSONDecodeError:
        if path.suffix.casefold() == ".json":
            raise ValueError("Invalid JSON metadata: " + path.name) from None
        try:
            import yaml
        except ImportError:
            if path.name == "voice-profile.yaml" and PUBLIC_PROFILE_POINTER.fullmatch(text):
                return payload
            raise ValueError(
                "PyYAML is required to verify non-JSON YAML provenance: " + path.name
            ) from None
        try:
            root_node = yaml.compose(text, Loader=yaml.SafeLoader)
            _validate_yaml_provenance(root_node, yaml)
        except yaml.YAMLError as error:
            raise ValueError("Invalid YAML metadata: " + path.name) from error
        except RecursionError as error:
            raise ValueError("Recursive YAML provenance cannot be safely exported: " + path.name) from error
        return payload
    sanitized = _without_private_metadata(original)
    if sanitized == original:
        return payload
    return (json.dumps(sanitized, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_package(root, output):
    root = Path(root).resolve()
    output = Path(output).absolute()
    if not root.is_dir():
        raise ValueError("Package root must be a directory")
    if output.suffix.casefold() != ".zip":
        raise ValueError("Output must end in .zip")
    paths = _public_paths(root)
    if not any(name == "SKILL.md" for name, _ in paths):
        raise ValueError("Package requires a regular public SKILL.md")
    records = []
    transformations = []
    for name, path in paths:
        checkout_bytes = path.read_bytes()
        exported_bytes = _export_bytes(path, checkout_bytes)
        records.append((name, exported_bytes))
        if exported_bytes != checkout_bytes:
            transformations.append({
                "path": name,
                "operation": "remove_private_provenance_metadata",
                "checkout_sha256": hashlib.sha256(checkout_bytes).hexdigest(),
                "export_sha256": hashlib.sha256(exported_bytes).hexdigest(),
            })
    freeze_scope = (
        "Evaluation profile-freeze hashes identify checkout profiles before generation. "
        "Export sanitization can change profile bytes; transformations map checkout "
        "digests to export digests without changing the original freeze record. "
        "SHA256SUMS verifies the exported bytes."
    )
    export_manifest = {
        "schema_version": 1,
        "freeze_scope": freeze_scope,
        "transformations": transformations,
    }
    records.append(("EXPORT-MANIFEST.json", (
        json.dumps(export_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")))
    manifest = "".join(
        hashlib.sha256(payload).hexdigest() + "  " + name + "\n"
        for name, payload in records
    ).encode("utf-8")
    records.append(("SHA256SUMS", manifest))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, payload in sorted(records):
            member = zipfile.ZipInfo("write-like-me/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            member.create_system = 3
            member.external_attr = (stat.S_IFREG | 0o644) << 16
            member.compress_type = zipfile.ZIP_STORED
            archive.writestr(member, payload)
    archive_bytes = buffer.getvalue()
    digest = hashlib.sha256(archive_bytes).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".write-like-me-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(archive_bytes)
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    output.with_suffix(output.suffix + ".sha256").write_text(
        digest + "  " + output.name + "\n", encoding="utf-8"
    )
    return {
        "archive": str(output), "sha256": digest, "file_count": len(records),
        "transformed_files": [item["path"] for item in transformations],
        "freeze_scope": freeze_scope,
        "privacy_scope": "Public allowlist; private directories and known provenance fields excluded. Review public prose before sharing.",
        "installed": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = build_package(args.root, args.output)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

