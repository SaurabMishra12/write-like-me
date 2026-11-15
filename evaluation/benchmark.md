# Benchmark and reproducibility protocol

The benchmark separates genuine source passages from constructed engineering tasks. No constructed text is called human ground truth. No commercial detector is used.

## Data and conditions

| Set | Source and split | Conditions available | What it can establish |
|---|---|---|---|
| Personal | One confirmed unassisted informal message from a held-out chat group; private | A original, B ordinary generation, C generic polishing of B, D skill-guided | A bounded revision case, with a source ambiguity requiring user review |
| Canon | Two short verified pre-2018 passages from whole documents excluded from profile construction; manifest in examples/pre2018-benchmarks | A/B/C/D | Bounded preservation/register cases; author overlap and likely model-pretraining exposure remain |
| Public engineering | Seven explicitly constructed tasks: email, academic, blog/math explanation, speaking, documentation, LinkedIn, informal | B/C/D; A unavailable | Controlled supplied-fact and restraint checks, not genuine personal style similarity |

Category A (authorship provenance) and condition A (original source) are different fields. A canon passage is category P but condition A. Benchmark IDs beginning B-CANON mean benchmark, not condition B.

Nine personal messages were selected in five source groups: six profile, two calibration, one held-out. Entire groups remain disjoint. Calibration is reserved for inspecting metric behavior and does not tune the profile. Canon holdouts are document-disjoint, not author-disjoint. The profile-building corpus is far too small to recover formal writing identity.

## Generation actually recorded

Two isolated generator contexts were invoked in this session. One received only task requests/facts/originals to produce B, then this prompt to produce C: “Polish this writing to sound more natural and human while preserving its meaning.” A separate generator received the skill and relevant profiles/workflows to produce D, with single-model labeled review passes. It did not see B/C. The Research Analyst role was not needed for fixture drafting; seven editorial roles were recorded, not eight independently invoked agents. Each context used the inherited model and host defaults; the backend revision, temperature, sampling seed and training data were not controllable or known. No API costs or historical credentials were used.

This is one output per condition/task. It is not a repeated-seed model comparison or a test of multi-agent benefit. B/C and D differ in instruction/context access, not just a single isolated component. Do not infer causality or superiority from this pilot.

Profile hashes were frozen before generation in results/profile-freeze.json; guided results also record instruction hashes. The tools were hardened during independent review using synthetic bug reproductions, without updating profiles or tuning against held-out feedback. Thus the strongest predeclared freeze concerns the style profiles/instructions, not a fully immutable runtime. Final tool hashes and exact code remain in the release for replay. A future confirmatory experiment should freeze all code before unseen task selection.

## Eight dimensions

Use 0 (fails), 1 (partly meets; explain), 2 (meets in this task), or null (insufficient evidence). Every non-null judgment needs a concrete note. Keep dimensions separate; no aggregate “human score.”

1. Voice and canon similarity: distinguish personal voice from adopted craft. Without suitable original personal writing, personal similarity is unassessed. Canon craft fit can be judged as an editorial interpretation.
2. Meaning preservation: unchanged intent, assumptions, qualification and stance. Drafting tasks use the supplied fact ledger; no original prose equivalence claim is possible.
3. Factual integrity: correct names, values, associations, dates, units, citations, equations and code. Any changed truth or unsupported claim is a hard failure.
4. Naturalness: coherent, usable prose without forced narrative or artificial imperfection. This is a reader judgment, not an authorship label.
5. Clarity: a reader can follow the mechanism/request without a missing referent or step.
6. Argument quality: claims follow reasons/evidence; limitations and counterclaims retain their scope.
7. Genre suitability: the appropriate register, structure and useful level of detail for the task.
8. Edit restraint: changes serve the request; only score revision tasks where an original exists. Drafting has no edit-distance baseline.

## Blinding and replay

Run `python tools/evaluate_benchmark.py --output /tmp/write-like-me-replay` to regenerate surface diagnostics, a packet with candidate labels, and a separate method key. Seed 17 determines label order only, not model generation. A reviewer must read only blind-packet.json until recording ratings. Decoding the key comes afterward. Model-judge opinions need their own provenance and remain separate from pending human/author judgments.

Exact span-presence, word counts, sentence heuristics and edit ratios are diagnostics. No surface match certifies scientific truth, meaning, grammar, authorship or voice. On original revisions run the preservation checker; exit 3 means review is still required, not failure or success in writing quality. Do not repair held-out outputs after seeing failures. Save negative cases and test future rule changes on fresh holdouts.

Private inputs/outputs remain under private/. Public reports may include case counts, hashes and unresolved review status, never private source text. No professor email, LinkedIn post or academic paragraph has been verified as the user's unassisted writing; the missing genuine-human genre cells stay missing. Full human-blind evaluation and cross-platform runtime checks remain future work.
