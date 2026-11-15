"""Validate a local provenance corpus and propose, never install, profile observations."""

import argparse
import difflib
import json
from pathlib import Path

from style_analyzer import analyze


def validate(corpus):
    rows = corpus.get("samples", [])
    if not isinstance(rows, list):
        raise ValueError("samples must be a list")
    ids, groups = set(), {}
    for row in rows:
        required = {"id", "category", "split", "source_group", "genre", "authorship_confidence", "text"}
        if not required <= row.keys():
            raise ValueError("sample is missing required provenance fields")
        if not all(isinstance(row[k], str) and row[k].strip() for k in required):
            raise ValueError("provenance fields and text must be nonempty strings")
        if "metrics_eligible" in row and type(row["metrics_eligible"]) is not bool:
            raise ValueError("metrics_eligible must be a boolean")
        if row["id"] in ids:
            raise ValueError("duplicate sample id")
        ids.add(row["id"])
        if row["category"] not in {"A", "P", "B", "C", "D", "E"}:
            raise ValueError("unknown provenance category")
        if row["split"] not in {"profile", "calibration", "heldout"}:
            raise ValueError("unknown split")
        group = row["source_group"]
        if group in groups and groups[group] != row["split"]:
            raise ValueError("source group leaks across split boundaries")
        groups[group] = row["split"]
        if row["category"] == "P":
            year = row.get("original_year")
            if type(year) is not int or year >= 2018 or year < 1:
                raise ValueError("P requires a verified original year before 2018")
            if not str(row.get("source_url", "")).startswith("https://"):
                raise ValueError("P requires a source URL")
    excluded = corpus.get("excluded_ids", [])
    if not isinstance(excluded, list) or not set(excluded) <= ids:
        raise ValueError("excluded_ids must refer to existing sample IDs")
    return {"valid": True, "samples": len(rows), "groups": len(groups), "split_groups": groups,
            "validation_scope": "Schema and declared split boundaries only; authorship is not independently verified."}


def propose_profile(corpus):
    validate(corpus)
    excluded = set(corpus.get("excluded_ids", []))
    personal, canon, quarantined = [], [], []
    for row in corpus.get("samples", []):
        if row["id"] in excluded or row["split"] != "profile":
            continue
        confidence = row["authorship_confidence"]
        confirmed = confidence in {"high", "confirmed", "high_user_confirmed_short_prompts"}
        if row["category"] == "A" and confirmed:
            personal.append(row)
        elif row["category"] == "P" and row.get("human_authorship_verified") is True:
            canon.append(row)
        else:
            quarantined.append(row["id"])
    measured = [row for row in personal if row.get("metrics_eligible", True)]
    return {"schema_version": 1, "status": "proposal_requires_explicit_user_approval",
            "personal_evidence_ids": [r["id"] for r in personal], "canon_evidence_ids": [r["id"] for r in canon],
            "quarantined_ids": quarantined, "excluded_ids": sorted(excluded),
            "personal_surface_metrics": analyze("\n\n".join(r["text"] for r in measured)),
            "warning": "Metrics are proposed observations, not style prescriptions. This function does not modify a permanent profile or infer psychological traits."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--proposal", type=Path, help="Create a new proposal file exclusively; never overwrite an existing file")
    parser.add_argument("--current-profile", type=Path, help="Print a reviewable comparison; does not apply it")
    args = parser.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    if args.proposal:
        if args.proposal.name == "voice-profile.yaml":
            parser.error("Choose a proposal filename; permanent profiles cannot be replaced")
        proposal = json.dumps(propose_profile(corpus), indent=2, ensure_ascii=False) + "\n"
        with args.proposal.open("x", encoding="utf-8") as stream:
            stream.write(proposal)
        if args.current_profile:
            print("\n".join(difflib.unified_diff(args.current_profile.read_text().splitlines(), proposal.splitlines(),
                                              fromfile="current-profile", tofile="proposal", lineterm="")))
        else:
            print(json.dumps({"proposal": str(args.proposal), "applied": False}))
    else:
        print(json.dumps(validate(corpus), indent=2))


if __name__ == "__main__":
    main()
