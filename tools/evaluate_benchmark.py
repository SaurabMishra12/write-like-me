"""Recompute public fixture diagnostics and a blinded review packet from saved outputs."""

import argparse
import hashlib
import json
import random
from pathlib import Path

from preservation_checker import check
from style_analyzer import analyze
from writing_auditor import audit


def _conditions(tasks, baselines, guided):
    task_ids = [t["id"] for t in tasks]
    if len(set(task_ids)) != len(task_ids):
        raise ValueError("duplicate task IDs")
    maps = []
    for rows in (baselines, guided):
        ids = [r["task_id"] for r in rows]
        if len(set(ids)) != len(ids) or set(ids) != set(task_ids):
            raise ValueError("generation task IDs must match all tasks exactly")
        maps.append({r["task_id"]: r for r in rows})
    result = {}
    for task in tasks:
        tid = task["id"]
        candidates = {"B": maps[0][tid]["condition_B"], "C": maps[0][tid]["condition_C"], "D": maps[1][tid]["condition_D"]}
        if any(not isinstance(s, str) or not s.strip() for s in candidates.values()):
            raise ValueError("all generated task texts must be nonempty strings")
        result[tid] = candidates
    return result


def evaluate(tasks, baselines, guided):
    conditions = _conditions(tasks, baselines, guided)
    rows = []
    for task in tasks:
        for condition, candidate in conditions[task["id"]].items():
            metrics = analyze(candidate)
            original = task.get("original")
            rows.append({"task_id": task["id"], "condition": condition,
                         "words": metrics["words"], "sentences": metrics["sentences"],
                         "sentence_words_mean": metrics["sentence_words"]["mean"],
                         "missing_required_spans": [span for span in task.get("locks", []) if span not in candidate],
                         "editorial_findings": len(audit(candidate, task["genre"])["findings"]),
                         "preservation": check(original, candidate) if original is not None else None,
                         "candidate_sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                         "semantic_verified": False, "voice_similarity_score": None})
    return {"schema_version": 1, "task_count": len(tasks), "generated_text_count": len(rows), "rows": rows,
            "evaluation_scope": "Saved-output surface diagnostics only; no generation calls, human ratings or semantic certification.",
            "limits": ["Public fixtures are constructed, without genuine-human condition A.",
                       "Lock presence cannot establish truth, correct association, or completeness.",
                       "Lower word counts and fewer warnings are not proof of better writing."]}


def blind_packet(tasks, baselines, guided, seed=17):
    conditions = _conditions(tasks, baselines, guided)
    rng, items, key = random.Random(seed), [], {}
    for task in tasks:
        order = list(conditions[task["id"]])
        rng.shuffle(order)
        candidates, mapping = [], {}
        for index, condition in enumerate(order, 1):
            label = "candidate-" + str(index)
            candidates.append({"label": label, "text": conditions[task["id"]][condition]})
            mapping[label] = condition
        items.append({"task_id": task["id"], "genre": task["genre"], "request": task["request"],
                      "facts": task.get("facts", ""), "candidates": candidates})
        key[task["id"]] = mapping
    return {"schema_version": 1, "seed": seed, "tasks": items,
            "instructions": "Judge independently before opening the key. Use null when a dimension lacks evidence; do not infer personal voice from synthetic facts."}, key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root
    tasks = json.loads((root / "evaluation/test-cases/tasks.json").read_text())["tasks"]
    baselines = json.loads((root / "evaluation/results/baselines.json").read_text())["outputs"]
    guided = json.loads((root / "evaluation/results/guided.json").read_text())["outputs"]
    diagnostics = evaluate(tasks, baselines, guided)
    packet, key = blind_packet(tasks, baselines, guided)
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, value in [("surface-results.json", diagnostics), ("blind-packet.json", packet), ("blind-key.json", key)]:
        (args.output / filename).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"tasks": diagnostics["task_count"], "outputs": diagnostics["generated_text_count"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
