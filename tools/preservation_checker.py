"""Conservative exact-span guard. Changed prose always needs semantic review."""

import argparse
import difflib
import json
import re
from collections import Counter
from pathlib import Path


def _matches(pattern, text, flags=0):
    return [m.group(0) for m in re.finditer(pattern, text, flags)]


def _markdown_links(text):
    links = []
    for start in re.finditer(r"!?\[[^\]\n]*\]\(", text):
        pos, depth = start.end(), 1
        while pos < len(text) and depth:
            if text[pos] == "\\":
                pos += 2
                continue
            depth += (text[pos] == "(") - (text[pos] == ")")
            pos += 1
        links.append(text[start.start():pos])
    links.extend(_matches(r"^\s*\[[^\]\n]+\]:[^\n]+", text, re.M))
    links.extend(_matches(r"\[[^\]\n]*\]\[[^\]\n]*\]", text))
    return links


def _code_spans(text):
    spans, masked = [], list(text)
    lines = text.splitlines(keepends=True)
    pos, active, start = 0, None, 0
    for line in lines:
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*?)(?:\n|$)", line)
        if active is None and marker:
            active, start = marker[1], pos
        elif active is not None:
            close = re.match(r"^ {0,3}([`~]+)[ \t]*(?:\n|$)", line)
            if close and set(close[1]) == {active[0]} and len(close[1]) >= len(active):
                end = pos + len(line)
                spans.append(text[start:end])
                masked[start:end] = " " * (end - start)
                active = None
        pos += len(line)
    if active is not None:
        spans.append(text[start:])
        masked[start:] = " " * (len(text) - start)
    spans.extend(_matches(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", "".join(masked), re.S))
    return spans


def protected(text):
    code = _code_spans(text)
    math = _matches(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$|(?<![\\$])\$(?!\$).*?(?<!\\)\$(?!\$)", text)
    math += _matches(r"(?s)\\\(.*?\\\)|\\\[.*?\\\]", text)
    math += _matches(r"(?s)\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|displaymath|math)\}.*?\\end\{\1\}", text)
    latex = _matches(r"\\(?:[A-Za-z]+\*?)(?:\[[^\]\n]*\])*(?:\{[^{}\n]*(?:\{[^{}\n]*\}[^{}\n]*)*\})*", text)
    citations = _matches(r"\\(?:[Cc]ite\w*|nocite|bibitem)(?:\[[^\]]*\])*(?:\{[^}]*\})+", text)
    references = _matches(r"(?ms)^#{1,6}\s*(?:References|Bibliography)\s*\n.*?(?=^#{1,6}\s|\Z)", text)
    references += _matches(r"(?s)\\begin\{thebibliography\}.*?\\end\{thebibliography\}", text)
    references += _matches(r"(?m)^\s*\\bibitem[^\n]*(?:\n(?!\s*\\bibitem|\s*\\end)[^\n]+)*", text)
    names = _matches(r"\b(?:[A-Z][a-z]+\s+){1,4}[A-Z][a-z]+\b|\b[A-Z]{2,}[A-Z0-9-]*\b", text)
    names += _matches(r"\b(?:Dr|Prof|Mr|Ms|Mrs)\.?\s+[A-Z][\w-]+", text)
    numbers = _matches(r"(?<!\w)[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?(?:%|\b)", text)
    number_words = _matches(r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b", text, re.I)
    urls = [x.rstrip(".,;") for x in _matches(r"https?://[^\s<>\]\"']+", text)]
    anchors = _matches(r"\b(?:not|no|never|neither|without|cannot|can't|may|might|could|must|will|would|should|suggests?|proves?|causes?|correlates?|increas\w*|decreas\w*|significan\w*|insignifican\w*|unreliable|reliable)\b", text, re.I)
    complexity = _matches(r"\b[OΘΩ]\([^\n]*?\)", text)
    evidence_status = _matches(r"\b(?:constructed|hypothetical|toy|planned|historical)\b", text, re.I)
    return {"numbers": numbers, "number_words": [x.lower() for x in number_words], "names": names,
            "math": math, "latex": latex, "citations": citations, "references": references,
            "links": _markdown_links(text), "urls": urls, "code": code, "complexity": complexity,
            "epistemic_anchors": [x.lower() for x in anchors],
            "evidence_status": [x.lower() for x in evidence_status]}


def check(original, revised, locks=None, minimal=False, max_edit_ratio=0.2):
    if not isinstance(original, str) or not isinstance(revised, str):
        raise TypeError("original and revised must be strings")
    if not 0 <= max_edit_ratio <= 1:
        raise ValueError("max_edit_ratio must be between 0 and 1")
    before, after = protected(original), protected(revised)
    violations = []
    for kind in before:
        if before[kind] != after[kind]:
            violations.append({"kind": kind, "removed": list((Counter(before[kind]) - Counter(after[kind])).elements()),
                               "added": list((Counter(after[kind]) - Counter(before[kind])).elements()),
                               "reason": "Protected sequence changed; review exact original and proposed spans."})
    for group, spans in (locks or {}).items():
        if not isinstance(spans, list) or any(not isinstance(s, str) or not s for s in spans):
            raise ValueError("Each lock group must be a list of nonempty strings")
        for span in spans:
            if span not in original:
                raise ValueError(f"Lock is absent from original: {group}")
            if original.count(span) != revised.count(span):
                violations.append({"kind": "explicit_" + group, "span": span, "reason": "Locked occurrence changed"})
    experience = r"\bI\s+(?:led|built|worked|published|visited|discovered|developed|read|met|won)\b"
    if _matches(experience, original, re.I) != _matches(experience, revised, re.I):
        violations.append({"kind": "personal_experience", "reason": "First-person experience changed or added; user evidence required"})
    ratio = 1 - difflib.SequenceMatcher(None, original, revised, autojunk=False).ratio()
    if minimal and ratio > max_edit_ratio:
        violations.append({"kind": "edit_budget", "ratio": ratio, "maximum": max_edit_ratio})
    decision = "veto" if violations else "identical" if original == revised else "review_required"
    return {"decision": decision, "violations": violations, "edit_ratio": ratio,
            "exact_checks_passed": not violations, "changed": original != revised,
            "semantic_verified": False, "grammar_verified": False, "voice_verified": False,
            "manual_checks": ["Meaning, quantifiers, causality, attribution and evidence", "Scientific truth and logical consistency", "Grammar, user voice and genre suitability"],
            "limits": "Exact heuristics can miss entities, context swaps, uncommon LaTeX and paraphrased claims. Changed prose is never automatically cleared. Identical means unchanged, not true or grammatical."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--locks", type=Path, help="JSON object of lock-group names to lists of exact spans")
    parser.add_argument("--minimal", action="store_true")
    parser.add_argument("--max-edit-ratio", type=float, default=0.2)
    args = parser.parse_args()
    result = check(args.original.read_text(encoding="utf-8"), args.revised.read_text(encoding="utf-8"),
                   json.loads(args.locks.read_text()) if args.locks else None, args.minimal, args.max_edit_ratio)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit({"identical": 0, "veto": 2, "review_required": 3}[result["decision"]])


if __name__ == "__main__":
    main()
