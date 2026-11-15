# Write Like Me

A local, portable writing skill that preserves the user's ideas and factual claims while applying a provisional personal voice profile and selected pre-2018 explanatory craft. It combines host-model drafting/review with deterministic Python diagnostics. It is not a detector, a trained personalized model, or an automatic guarantee of semantic fidelity.

## Use it now

In a file-capable assistant, point to this bundle's `SKILL.md` and make the request, for example:

> Use the Write Like Me skill in this folder. Write Like Me: Minimal. Edit the attached draft and preserve all factual claims, equations and citations.

The host model does the writing. The Python tools audit it locally and return a diff or veto. They do not call an API, send an email, upload samples, or generate prose on their own. An unchanged clear draft is a valid result.

Supported requests: Email, Academic, Blog, Speak, Audit, Rewrite, Explain, Compare, Learn, Minimal; equivalent natural requests also work. Documentation/GitHub and LinkedIn have distinct register guidance. Conversational prefixes do not automatically register ten native slash commands in every host.

## Installation

Use the public ZIP built under `dist/`, not a recursive copy of the working checkout. It excludes the local private corpus. Extract to a temporary directory, inspect `SHA256SUMS` and `EXPORT-MANIFEST.json`, and copy the extracted `write-like-me` folder to one chosen destination. Do not overwrite an existing same-named skill; select a separate project or reconcile it explicitly.

| Host | Current documented project destination | Guide |
|---|---|---|
| Codex | `.agents/skills/write-like-me/` | [Codex](adapters/codex.md) |
| Claude Code | `.claude/skills/write-like-me/` | [Claude Code](adapters/claude-code.md) |
| Google Antigravity | `.agents/skills/write-like-me/` | [Antigravity](adapters/antigravity.md) |
| ChatGPT / Custom GPT | Use the instruction/knowledge adapter or the supported native skill route for the actual product | [ChatGPT](adapters/chatgpt.md) |
| Other assistants | Load the shared instructions and active profile/workflow | [Universal](adapters/universal.md) |

Paths and capabilities were checked against current official documentation on 15 November 2026. These instructions have not been executed in the target products. See the [source-linked support matrix](research/platform-support.md) for version-sensitive differences, user-level locations and remaining checks. This project does not install or publish itself.

## Python tools

Python 3.10+; core shipped profiles are JSON-compatible YAML, so runtime scripts use the standard library. Optional PyYAML is needed for arbitrary human-edited YAML and robust non-JSON YAML packaging. Packaging fails closed on unsupported metadata. Pytest is a development dependency; it was available in the execution environment.

Run from the extracted skill directory:

```bash
python tools/engine.py context 'Write Like Me: Academic'
python tools/style_analyzer.py draft.md
python tools/writing_auditor.py draft.md --genre academic
python tools/preservation_checker.py original.md proposed.md --minimal
python tools/compare_revisions.py original.md proposed.md --genre academic
python tools/engine.py review original.md proposed.md --genre academic
```

For custom entities, terms and exact scientific statements, supply `--locks locks.json` to the checker or engine review. Example lock file:

```json
{"names":["Dr Rao"],"terms":["numpy"],"claims":["The comparison does not establish causation."]}
```

The declared spans must occur in the original. Exit codes for preservation/engine review are **0** unchanged, **2** veto, **3** changed prose requiring semantic review; operational/invalid-input errors are nonzero. A clean exact-span report cannot establish that a number still refers to the same method or that a citation supports its claim. The guardian checks common numerical, citation/reference, LaTeX/math, name, code, complexity and polarity forms; explicit locks and semantic review cover the rest. Conservative anchor checks can also flag legitimate paraphrases.

The auditor emits contextual warnings, with no edits, banned-word authorship score or “AI probability.” A word such as “delve” alone triggers nothing. Lists can be useful in documentation. Sentence boundaries, word counts, function words and variation are descriptive heuristics, especially unreliable in punctuation-poor or bilingual chat. Grammar and voice authenticity are explicitly unverified by code.

## Personal evidence and control

The user confirmed short informal prompts are unassisted. The initial profile uses six selected messages in three source groups: four English prompts totaling 189 whitespace-delimited words and two likely transcribed Hindi-English messages. Two calibration messages and one held-out message belong to separate groups. Formal email, LinkedIn and academic cadence remain unverified. Canon craft is an adopted preference, not the user's historical voice or a named author's impersonation.

The editable source of truth is [profiles/voice-profile.yaml](profiles/voice-profile.yaml); the root YAML points to it. [VOICE_PROFILE.md](VOICE_PROFILE.md), [patterns](WRITING_PATTERNS.md), [constructed examples](WRITING_EXAMPLES.md), and [confidence report](STYLE_CONFIDENCE_REPORT.md) explain the evidence and limits. Actual personal excerpts remain in ignored local `private/VOICE_EVIDENCE.md` and never ship. Public canon excerpts retain attribution and copyright limits.

Only confirmed A evidence informs personal voice; verified pre-2018 human P passages inform craft. B informs editing preferences, C/D acceptance/rejection preferences, and E is quarantined. Pre-2018 material may itself contain generated examples. See the [provenance audit](research/provenance-audit.md) and [canon study](research/pre2018-canon-study.md).

To learn from new authorized local samples:

```bash
python tools/corpus_manager.py local-corpus.json
python tools/corpus_manager.py local-corpus.json --proposal proposed-observations.yaml --current-profile profiles/voice-profile.yaml
```

Each sample declares `id`, `category`, `authorship_confidence`, `source_group`, `split` (`profile`, `calibration`, `heldout`), `genre`, and `text`. Optional `metrics_eligible` must be Boolean. P also needs an original year before 2018, an HTTPS source, and `human_authorship_verified: true` to be admitted to a proposal. These are declarations requiring real source review; schema validation does not authenticate authorship. Keep all samples from one source group in one split. B/C/D/E are never promoted into personal evidence.

Set `excluded_ids` in the corpus to revoke samples. Set `evidence.excluded_ids` in the active profile to suppress dependent learned patterns and mark aggregate personal counts stale until recomputation. Rule overrides can be edited directly or supplied for a task. The proposal command creates a new file exclusively, never applies a change, and refuses the permanent profile filename. Show the diff and obtain explicit user approval before replacing a permanent profile. A proposal of surface observations is not an automatic psychological or long-form style inference.

## Research, roles and evaluation

- [Research review](research/literature-review.md): 21 published sources, with [machine-readable methods/findings/limits](research/papers.json) and [BibTeX](research/references.bib).
- [Canon study](research/pre2018-canon-study.md): 24 source records, 15 supported craft principles, all requested core authors, selected-passage/full-book access distinctions.
- [Taxonomy](research/ai-writing-taxonomy.md): 24 contextual editorial checks, source quality, false positives, historical counterexamples and correction policy.
- [Eight review roles](agents/protocol.md): one shared identity and argument ledger, one composed draft, factual-guardian veto. Roles may be separate agents or explicitly labeled passes; a specification is not evidence of actual independent execution.
- [Benchmark protocol](evaluation/benchmark.md), [evaluation report](evaluation/evaluation-report.md), and [independent code review](evaluation/results/independent-review.md).

Replay software checks and saved-output diagnostics:

```bash
python -m pytest -q
python tools/evaluate_benchmark.py --output /tmp/write-like-me-replay
python tools/build_package.py --output dist/write-like-me.zip
```

The saved pilot includes B/C/D outputs on seven public constructed tasks, plus private A/B/C/D cases on one personal and two canon holdouts. Surface checks and model judgments do not establish superior authorship quality, personal authenticity or multi-agent advantage. Human/author blind ratings and runtime integration tests remain unexecuted. Details and negative findings are retained in the report; raw private cases are excluded from export.

The public builder uses deterministic ZIP entries, excludes private/config/cache directories, rejects symlinks and unsafe metadata, and emits internal checksums plus a ZIP checksum. `EXPORT-MANIFEST.json` explains sanitized-profile transformations: pre-generation freeze hashes describe original checkout bytes; exported hashes describe distributed bytes. The builder is not a general secret scanner; review any newly added public prose before sharing. No files were published in this task.

## Roadmap

1. Add confirmed unassisted samples in missing formal genres; keep topic/time/source-disjoint holdouts and user exclusions.
2. Run blinded author and reader comparisons across all eight dimensions, with sufficient independent documents and repeated fixed model settings. Include no-profile and mismatched-profile ablations.
3. Freeze all instructions and tool code before a fresh confirmatory benchmark. Measure conservative false positives and review burden as well as factual drift.
4. Install in explicitly chosen test projects and verify discovery, invocation, reference loading, privacy and actual writing on each target platform/version.
5. Consider deeper parsing or semantic-review assistance only after demonstrating a need; retain evidence, uncertainty and the user's final control.

Original code and documentation are MIT licensed. Third-party excerpts and private writing are excluded from that grant; see [LICENSE](LICENSE).
