# Independent bounded implementation review

Reviewed 15 November 2026. **The initial review identified four concrete findings; all four are fixed in the independently rechecked cases.** The final rerun passed `93 tests in 1.66s`. Original findings and reproductions remain below as historical evidence, followed by verified fix status. The initial suite had passed `73 tests in 1.14s` while missing these cases.

This was an independent review pass by a separate agent. It was read-only on implementation, tests, instructions, and profiles. Only this report was written in the repository. Synthetic probes and temporary archives were created under `/tmp/wlm-independent-review-kvmbxbdw/`; no private raw samples, private baselines, or guided outputs were opened. The review did not install the skill or test other model hosts.

## Findings

### [P1] Valid YAML forms bypass known-private-metadata exclusion

Location: [tools/build_package.py:108](../../tools/build_package.py), especially the fallback at lines 113–115 and the scanner defined at lines 41–43 in the reviewed snapshot.

If a `.yaml` file is not JSON-compatible, the builder checks its text with a case-sensitive, line-start regular expression and otherwise returns the bytes unchanged. Valid YAML with quoted keys, uppercase keys, or inline flow mappings bypasses that expression. These are alternate serializations of metadata that the JSON branch strips or that the YAML branch intends to reject.

Synthetic fixtures each used a regular `SKILL.md` and `profiles/voice.yaml`. All three produced exit 0 and a ZIP whose actual member bytes contained the sentinel:

```yaml
status: provisional
"source_locator": SYNTHETIC_PRIVATE_SENTINEL
```

```yaml
status: provisional
SOURCE_LOCATOR: SYNTHETIC_PRIVATE_SENTINEL
```

```yaml
status: provisional
evidence: {source_locator: SYNTHETIC_PRIVATE_SENTINEL}
```

Reproduction using the retained synthetic fixture:

```bash
python tools/build_package.py --root /tmp/wlm-independent-review-kvmbxbdw/quoted-key --output /tmp/wlm-independent-review-kvmbxbdw/repro.zip
python -c 'import zipfile; z=zipfile.ZipFile("/tmp/wlm-independent-review-kvmbxbdw/repro.zip"); print(z.read("write-like-me/profiles/voice.yaml").decode())'
```

Observed consequence: `SYNTHETIC_PRIVATE_SENTINEL` exists in the archive, not merely in tool stdout. Source-file hashes remained unchanged. No real private data was used or shown to leak.

Fix direction: safely parse and recursively sanitize supported YAML, or fail closed for YAML that cannot be safely interpreted. A broader line regex alone will remain vulnerable to other YAML syntaxes. Add tests for quoted, flow, nested, and case-varied keys. The documented need to review public prose is appropriate, but does not remove this concrete failure of the builder's known-field handling.

### [P2] Standard Markdown code forms escape the strict code veto

Location: [tools/preservation_checker.py:32](../../tools/preservation_checker.py) and line 33.

The inline regex only recognizes single-backtick delimiters. The fenced-code regex requires a closing delimiter identical in length to the opener. CommonMark permits matching longer inline backtick runs and a closing fence at least as long as its opening fence. [CommonMark code spans](https://spec.commonmark.org/0.31.2/#code-spans), [fenced code blocks](https://spec.commonmark.org/0.31.2/#fenced-code-blocks).

Reproduced input pairs:

- Original `Run ``alpha()``.`; revision `Run ``beta()``.`
- Original string `"```text\nalpha\n````"`; revision `"```text\nbeta\n````"`

Both returned:

```json
{"decision":"review_required","violations":[],"exact_checks_passed":true,"semantic_verified":false}
```

`protected(original)["code"]` was `[]` in both cases. This does **not** create an automatic semantic approval: the conservative changed-prose branch still works. It does defeat the stated hard-veto behavior for changed fenced/inline code and incorrectly reports that exact checks passed for these recognized Markdown constructs.

Fix direction: use a Markdown-aware span extractor or support delimiter-run rules and retain exact original bytes. Add regression cases with alphabetic code changes so an unrelated numeric/name detector cannot make the test pass accidentally.

### [P2] JSON-compatible profile files bypass the mapping check

Location: [tools/engine.py:23](../../tools/engine.py) through line 33.

`_load_yaml` returns `json.loads(text)` immediately. Its `isinstance(value, dict)` validation only runs for the non-JSON YAML branch. A profile containing `[]` is valid JSON and YAML but invalid as a profile mapping; `route()` accepts it and returns `"profile": []` instead of rejecting it.

The synthetic routing fixture had `profiles/voice-profile.yaml` containing `[]`, the other two profiles containing `{}`, and a real workflow file. `route("Write Like Me: Rewrite", fixture)` returned successfully with the list profile. The normal tests only load shipped, well-formed mappings.

Fix direction: parse either format into one variable, then validate the same type and required schema/version fields regardless of serialization. Reject malformed profiles before exposing a task context to a host model.

### [P2] Malformed eligibility metadata silently includes a sample in metrics

Location: [tools/corpus_manager.py:17](../../tools/corpus_manager.py) through line 21, and line 60.

The validator checks required string fields but not optional flags used in eligibility decisions. A confirmed A/profile sample with `"metrics_eligible": "false"` is accepted as valid, then included in quantitative measurements because the string is truthy. JSON `false` behaves differently from the string `"false"`.

The synthetic sample contained `"text": "SYNTHETICMETRICWORD is present."`, with the normal required provenance fields and the string flag. Observed output:

```json
{"validate":{"valid":true,"samples":1,"groups":1,"split_groups":{"g1":"profile"}},"metrics_words":3,"personal_evidence_ids":["A1"]}
```

This is a malformed-input bug, not evidence that any actual stored sample was mishandled. Invalid exclusion/eligibility metadata should be rejected rather than silently becoming an opt-in. The same principle should cover any optional field consumed as a boolean or provenance decision.

Fix direction: enforce boolean types for `metrics_eligible` and `human_authorship_verified`, validate row/container shapes, and test that malformed metadata cannot contribute to a proposed profile.

## Checks that behaved as documented

- All 73 existing pytest cases passed using `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider`.
- A semantic-only reversal with no protected numeric/code spans remained `review_required`, with `semantic_verified: false`, in the guard and engine. Both CLIs exited 3.
- The revision-comparison CLI reported the same review requirement in JSON and assigned no winner. It exited 0; this is report-command behavior rather than a proven bypass of the separate guard. Callers must inspect its JSON and must not treat exit 0 as semantic approval. Propagating guard status would be a useful consistency improvement if it is intended for gating automation.
- The implementation exposes no automatic authorship probability, grammar truth, personal-voice truth, or semantic-equivalence approval.
- Source reads found no network calls in the seven local Python tools. This is source evidence, not a network-monitor trace.
- The instructions consistently separate host-model writing/review from optional mechanical helpers, keep one candidate and shared ledger, and state that platform documentation is not runtime verification.
- Profiles mark sparse personal/formal evidence and distinguish canon craft from a verified imitation of personal formal writing. This review did not independently verify the underlying private evidence.

## Scope, evidence and remaining uncertainty

Read all seven public Python implementation files, all existing tests, `SKILL.md`, the shared protocol and eight role specifications, six workflows, six profiles plus the root profile router, design notes, platform-support notes, and the universal/Codex adapters. The parent supplied graph evidence that this new source was not tracked by the stale, source-empty graph generation. Exact source reads were therefore used as fallback; no completeness claim was derived from empty graph search results.

The adversarial probe driver is `/tmp/wlm_independent_probes.py`; complete captured outputs are `/tmp/wlm-independent-review-kvmbxbdw/results.json`. The temporary artifacts are reproducibility aids, not part of the public distribution. Findings refer to the code inspected and executed in this pass; subsequent parent fixes need their own rerun and should not be inferred from this report.

Known limitations are not counted as bugs: heuristic sentence boundaries, length-sensitive type-token ratios, incomplete proper-name/LaTeX coverage when explicit locks are available, inability to infer scientific truth or personal authenticity, and need for semantic review despite unchanged protected spans. No private-data audit, host installation, model writing experiment, broad language benchmark, performance benchmark, or cross-platform runtime test was performed. Before/after fixture hashes establish that the packaging probes did not mutate their sources; they do not observe network traffic, transient files, child processes, or writes outside the declared fixtures.

The initial recommendation was to withhold a distribution-safety claim until the YAML export issue and the other regressions were addressed. The rerun below supersedes the open-finding status for the reproduced cases; it does not establish universal privacy or complete Markdown/semantic coverage.


## Verified fix status after implementation updates

The same synthetic probes were rerun after the parent reported the package worker complete. The recheck driver `/tmp/wlm_independent_recheck.py` preserves the original inputs and expectations, adding exception capture so intentional rejection can be recorded without aborting the remaining probes. Final captured outputs are `/tmp/wlm-independent-review-4hmkzcnb/results.json`.

| Initial finding | Independently observed final result | Status |
|---|---|---|
| P1 private metadata in quoted, uppercase, or flow YAML | Each export exits 1 with a private-provenance error; no ZIP is created; synthetic source hashes are unchanged | Fixed for all three original reproductions |
| P2 double-backtick inline code and longer closing fence | Both code spans are extracted, the content changes appear under `kind: code`, and the decision is `veto` | Fixed for both original reproductions |
| P2 JSON list accepted as a profile | `ValueError: Profile must be a mapping` | Fixed for original reproduction |
| P2 string eligibility flag accepted and measured | `ValueError: metrics_eligible must be a boolean` | Fixed for original reproduction |

The guard and engine still return `review_required`, exit 3, and `semantic_verified: false` for the synthetic semantic reversal. The comparison tool retains its documented report behavior: exit 0 with the review requirement present in JSON. No automatic semantic approval was introduced by these fixes.

The final full-suite invocation was:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider
```

Observed final result: `93 passed in 1.66s`. This includes the expanded packaging regressions and new evaluation tests. An intermediate run during concurrent implementation had 87 passes and five failures: three evaluation tests had been written before their implementation existed, and two broader YAML cases were still red. All five were green in the final rerun. This report does not erase that intermediate state or treat it as the final implementation result.

The parent reports that the personal/canon profiles stayed frozen while holdout generation proceeded, and that guard hardening was prompted by these independent synthetic failures rather than holdout feedback. This review did not open the holdout text, baseline output, or guided output, and did not independently establish the earlier profile freeze from pre-run hashes. Its confirmed evidence is the synthetic reproductions, observed fixes, and final suite results. No further broadening of review was performed.

**Remaining status:** no unresolved actionable finding among the four reproduced defects. Semantic fidelity, personal voice, grammar, host behavior, and universal privacy remain outside the guarantees of these local checks. The seven original tools were reviewed in depth; the subsequently added benchmark evaluator was included in the passing test run but did not receive a new whole-source review in this bounded task.
