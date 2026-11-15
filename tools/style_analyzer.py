"""Local descriptive metrics. No authorship, intelligence or quality inference."""

import argparse
import json
import re
import statistics
import unicodedata
from collections import Counter
from pathlib import Path


def words(text):
    tokens, current = [], []
    for char in text:
        if unicodedata.category(char)[0] in "LNM" or (char in "'-’" and current):
            current.append(char)
        elif current:
            tokens.append("".join(current).strip("'-’"))
            current = []
    if current:
        tokens.append("".join(current).strip("'-’"))
    return [x for x in tokens if x]


def sentences(text):
    protected = re.sub(r"(?<=\d)\.(?=\d)", "\ue000", text)
    protected = re.sub(r"\b(?:Dr|Mr|Mrs|Ms|Prof|Fig|Eq)\.", lambda m: m[0][:-1] + "\ue000", protected)
    return [x.replace("\ue000", ".").strip() for x in re.split(r"[.!?।]+(?:\s+|$)|\n\s*\n", protected) if x.strip()]


def analyze(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    tokens = words(text)
    segments = sentences(text)
    lengths = [len(words(s)) for s in segments if words(s)]
    lower = [w.lower() for w in tokens]
    function_set = {"a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "for", "with", "is", "are", "was", "it", "that", "this", "we", "i"}
    counts = Counter(w for w in lower if w in function_set)
    return {
        "words": len(tokens), "sentences": len(lengths),
        "paragraphs": len([p for p in re.split(r"\n\s*\n", text) if p.strip()]),
        "sentence_words": {"lengths": lengths, "mean": statistics.mean(lengths) if lengths else None,
                           "median": statistics.median(lengths) if lengths else None,
                           "population_stdev": statistics.pstdev(lengths) if lengths else None},
        "type_token_ratio": len(set(lower)) / len(lower) if lower else None,
        "mean_word_characters": statistics.mean(map(len, tokens)) if tokens else None,
        "question_marks": text.count("?"),
        "function_word_counts": dict(sorted(counts.items())),
        "scripts": {"devanagari_characters": sum("\u0900" <= c <= "\u097f" for c in text),
                    "latin_characters": sum("LATIN" in unicodedata.name(c, "") for c in text)},
        "method": "Unicode categories; heuristic sentence boundaries; no syntactic parser or language model",
        "limits": ["Punctuation-poor chat and mixed language distort sentence estimates.",
                   "Type-token ratio depends on length. No target burstiness or quality threshold.",
                   "Passive voice, clause complexity, entropy and perplexity are not estimated."]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.file.read_text(encoding="utf-8")), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
