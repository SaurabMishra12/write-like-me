"""Contextual editorial warnings, never an AI-authorship detector or auto-rewriter."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from style_analyzer import analyze, sentences, words


def audit(text, genre="general"):
    findings = []

    def add(pattern, evidence, recommendation, confidence="medium", severity="advisory", taxonomy=None):
        findings.append({"pattern": pattern, "evidence": evidence, "recommendation": recommendation,
                         "confidence": confidence, "severity": severity, "action": "review_in_context",
                         "false_positive_risk": "Human writers also use this form; preserve it when it serves the task.",
                         "taxonomy_reference": taxonomy})

    segments = sentences(text)
    transitions = [s for s in segments if re.match(r"(?i)^(furthermore|moreover|additionally|in addition)\b", s)]
    if len(transitions) >= 3 and len(transitions) / max(1, len(segments)) >= 0.5:
        add("mechanical_transitions", transitions, "Check the actual relation between claims; remove only redundant scaffolding.")
    normalized = [re.sub(r"(?i)^(furthermore|moreover|additionally),?\s*", "", s).strip().lower() for s in segments]
    repeated = [s for s, n in Counter(normalized).items() if n >= 3 and len(words(s)) >= 3]
    if repeated:
        add("repeated_proposition", repeated, "Check whether repetition teaches or merely restates an unchanged point.")
    lines = [line for line in text.splitlines() if line.strip()]
    lists = [line for line in lines if re.match(r"\s*(?:[-*+] |\d+[.)] )", line)]
    if genre not in {"technical", "documentation"} and len(lists) >= 4 and len(lists) / max(1, len(lines)) > 0.6:
        add("list_density", lists, "Use connected prose if reasoning depends on links between items; keep real parallel items.", "low")
    headings = [line for line in lines if re.match(r"^#{1,6}\s", line)]
    if len(headings) >= 4 and len(words(text)) < 150 and genre != "technical":
        add("overfragmentation", headings, "Check whether headings split a single short argument into fragments.", "low")
    if genre == "email" and re.search(r"(?i)hope this (?:email|message) finds you well", text):
        add("generic_email_opening", "Conventional wellbeing opener", "Use the specific reason for contact if the opener adds no relationship context.", "medium")
    if genre == "academic" and re.search(r"(?i)\b(?:first ever|groundbreaking|revolutionary)\b", text) and not re.search(r"\\cite|https?://|\[[0-9]+\]", text):
        add("unsupported_significance", "Strong novelty wording without a local citation marker", "Inspect actual evidence and prior work; do not invent a gap or replace the scientific claim automatically.", "low", "needs_evidence")
    contrasts = _contrast_matches(text)
    if len(contrasts) >= 2:
        add("repeated_formulaic_contrast", contrasts, "Retain genuine distinctions and remove redundant contrast framing.", "low")
    return {"genre": genre, "findings": findings, "metrics": analyze(text),
            "authorship_inference": "not_performed", "automatic_edits": [],
            "unassessed": ["Claim support in external sources", "Semantic truth", "Grammar", "Personal voice authenticity"],
            "limits": "Only a subset of the qualitative taxonomy is implemented as surface diagnostics. Missing warnings do not certify quality."}


def _contrast_matches(text):
    return [m[0] for m in re.finditer(r"(?is)not (?:just|only)\b.{0,100}?\bbut\b", text)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--genre", default="general", choices=["general", "informal", "academic", "email", "blog", "speaking", "technical", "linkedin"])
    args = parser.parse_args()
    print(json.dumps(audit(args.file.read_text(encoding="utf-8"), args.genre), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
