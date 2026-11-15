"""Route host-model writing tasks and enforce a local factual-guardian veto."""

import argparse
import json
import re
from pathlib import Path

from compare_revisions import compare
from preservation_checker import check
from writing_auditor import audit

ROOT = Path(__file__).resolve().parents[1]
MODES = {"email": "email", "academic": "academic", "blog": "blog", "speak": "speaking", "explain": "blog",
         "minimal": "general", "compare": "general", "learn": "general", "audit": "general", "rewrite": "general"}
WORKFLOWS = {"email": "professor-email.md", "academic": "academic-paper.md", "blog": "research-blog.md",
             "speaking": "speaking-script.md", "technical": "technical-writing.md", "general": "general-writing.md"}
PROFILES = {"email": "email-profile.yaml", "academic": "academic-profile.yaml", "blog": "blog-speaker-profile.yaml",
            "speaking": "blog-speaker-profile.yaml", "technical": "general-profile.yaml", "general": "general-profile.yaml"}


def _load_yaml(path):
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("This edited YAML needs PyYAML; shipped profiles use JSON-compatible YAML") from exc
        value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("Profile must be a mapping")
    return value


def route(request, root=ROOT, genre=None):
    root = Path(root)
    explicit = re.search(r"(?i)write like me\s*:\s*(\w+)", request)
    mode = explicit[1].lower() if explicit else "rewrite"
    if mode not in MODES:
        raise ValueError("Unknown Write Like Me mode: " + mode)
    if genre is None:
        genre = MODES[mode]
        if not explicit:
            lower = request.lower()
            for keys, value in [(("email", "professor", "internship"), "email"), (("academic", "paper", "manuscript"), "academic"),
                                (("presentation", "speaking", "talk script"), "speaking"), (("readme", "documentation", "github"), "technical"),
                                (("blog", "explain"), "blog")]:
                if any(key in lower for key in keys):
                    genre = value
                    break
    if genre in {"informal", "linkedin"}:
        genre = "general"
    if genre not in WORKFLOWS:
        raise ValueError("Unknown genre")
    paths = ["profiles/voice-profile.yaml", "profiles/pre2018-canon-profile.yaml", "profiles/" + PROFILES[genre], "workflows/" + WORKFLOWS[genre]]
    profile = _load_yaml(root / paths[0])
    evidence = profile.get("evidence", {})
    exclusions = list(profile.get("excluded_ids", [])) + list(evidence.get("excluded_ids", []))
    if any(not isinstance(item, str) for item in exclusions):
        raise ValueError("excluded_ids must contain strings")
    if exclusions:
        excluded = set(exclusions)
        patterns = profile.get("personal_patterns", [])
        profile["excluded_pattern_ids"] = [p["id"] for p in patterns if excluded.intersection(p.get("evidence_ids", []))]
        profile["personal_patterns"] = [p for p in patterns if not excluded.intersection(p.get("evidence_ids", []))]
        profile["evidence"]["category_A"] = {"status": "recompute_required_after_exclusion"}
    return {"mode": mode, "genre": genre, "loaded_files": paths,
            "profile": profile, "canon": _load_yaml(root / paths[1]),
            "genre_profile": _load_yaml(root / paths[2]), "workflow_text": (root / paths[3]).read_text(encoding="utf-8"),
            "host_model_required": True, "writes_or_sends": False}


def review(original, candidate, root=ROOT, genre="general", locks=None, minimal=False):
    guardian = check(original, candidate, locks=locks, minimal=minimal)
    status = {"veto": "blocked", "review_required": "review_required", "identical": "unchanged"}[guardian["decision"]]
    return {"delivery_status": status, "guardian": guardian,
            "candidate_text": None if status == "blocked" else candidate,
            "audit": audit(candidate, genre),
            "required_review": "Check the argument and every changed claim against the original. A host-model review or user approval must be recorded separately; this CLI never clears changed semantics."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    context = sub.add_parser("context", help="Load only the active task's profiles and workflow")
    context.add_argument("request")
    context.add_argument("--genre", choices=list(WORKFLOWS))
    reviewer = sub.add_parser("review", help="Check a host-model proposal; never rewrite automatically")
    reviewer.add_argument("original", type=Path)
    reviewer.add_argument("candidate", type=Path)
    reviewer.add_argument("--genre", default="general", choices=list(WORKFLOWS))
    reviewer.add_argument("--minimal", action="store_true")
    reviewer.add_argument("--locks", type=Path)
    args = parser.parse_args()
    if args.action == "context":
        result = route(args.request, genre=args.genre)
        code = 0
    else:
        result = review(args.original.read_text(encoding="utf-8"), args.candidate.read_text(encoding="utf-8"), genre=args.genre,
                        locks=json.loads(args.locks.read_text()) if args.locks else None, minimal=args.minimal)
        code = {"blocked": 2, "review_required": 3, "unchanged": 0}[result["delivery_status"]]
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
