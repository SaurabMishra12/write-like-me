# Executed evaluation and remaining limits

Date: 15 November 2026. Release: skill 0.1.1; initial personal profile 0.1.0. The repository is a working host-model skill with local audit tools. The results below establish bounded software behavior and a small saved-output pilot. They do not establish authentic personal authorship or superior writing quality.

## Executed evidence

| Check | Actual outcome | Evidence |
|---|---|---|
| Automated regression suite | 97 passed in the current suite | results/pytest.xml; final command is `python -m pytest -q --junitxml=evaluation/results/pytest.xml` |
| Skill frontmatter | Bundled skill validator passes after conservative metadata adjustment | SKILL.md; results/release-metadata-change.json |
| Local CLI behavior | Real-file style/audit/compare/context/review commands tested; unchanged=0, veto=2, semantic review=3 | tests/test_cli.py; preservation/engine reports |
| Independent implementation review | Four reproduced issues fixed and independently rechecked; later engineering additions separately tested | results/independent-review.md |
| Public drafting pilot | Seven constructed tasks × B/C/D = 21 generated outputs | test-cases/tasks.json; results/baselines.json; results/guided.json |
| Genuine held-out pilot | One personal and two pre-2018 canon source cases; A/B/C/D = 12 rows, of which 9 are generated revisions | results/heldout-summary.json; raw inputs/outputs are private |
| Blinded model rubric | 21 candidates reviewed with method key unseen; no human/author judgments | results/blind-model-review.json; results/blind-packet.json; results/blind-key.json |
| Profile integrity | All six pre-generation profile hashes unchanged | results/profile-freeze.json |

There are **30 generated pilot texts**: 21 public and 9 private, plus 3 genuine source originals. Two additional calibration messages were analyzed locally without tuning the profile. The public seven-task set has no genuine-human A condition; its missing human-reference cells are not filled with fabricated text.

## What the pilot found

Every public B/C/D output contains all declared required spans: 0 missing-span cases in each condition. This establishes literal presence only. It does not establish correct attribution, complete meaning, citation support or writing quality. All three conditions return the clear informal message unchanged. Their identical result is a successful restraint case and supplies no ranking evidence.

The blind model judge found four full ties (academic, blog, speaking and informal). It preferred C/D over a repeated request in B's email, and B/C over D on documentation and the hypothetical professional post under its stricter supplied-facts-only interpretation. No task supplied evidence to score personal voice similarity, so those 21 ratings are null. Most drafting tasks also lack an edit-restraint baseline.

The two concerns against D are retained:

1. The professional post omitted its explicit constructed-scenario qualification. Read in isolation, it could be mistaken for a real first-person experience.
2. The documentation said the command had not been run for that documentation. The blind judge lacked a supplied execution record and treated this as an unsupported provenance assertion. The drafting agent's own process knowledge may support a narrowly scoped statement, so this remains an interpretive disagreement requiring human judgment, not a confirmed scientific factual error.

The guided generator reported its own semantic review before the blind judge raised these concerns. That disagreement demonstrates why same-model self-review is insufficient. The comparison does **not** show that the skill generally improves writing, outperforms generic polishing, or gains from independent multi-agent review. Only one output per condition/task was generated with host defaults; there is no controlled repeated-seed experiment or statistical significance claim.

## Genuine holdouts and conservative false positives

The three condition-A originals remain identical. Among six B/C revisions, four trigger conservative vetoes; two require semantic review. All three D revisions require semantic review. None has automatic semantic verification. These are tool decisions, not counts of genuine factual errors or evidence that D is more faithful.

At least one canon veto includes the word “one” used as a pronoun, which the generic number-word guard treats as a protected numeral. Polarity markers can likewise differ in harmless paraphrases. This is a false-positive limitation that remains visible. The local private source also contains an ambiguous phrase about table presentation; D flags its interpretation for user review. No author has confirmed that interpretation. Do not report any of these as approved personal-voice matches.

Whole chat groups and canon documents were held out from profile construction. Canon authors overlap with the craft library, and pretraining exposure is unknown. A curator necessarily inspected source excerpts. The sparse, short passages do not represent complete formal genres or independent authors.

## Revision after the public pilot

The original pilot outputs are immutable evidence. Following its constructed-context issue, release 0.1.1 explicitly preserves hypothetical/toy/constructed/planned/historical status when dropping it could imply actual experience or an achieved/current result. It also requires an execution-status statement to name its evidence and scope. The guard has a conservative evidence-status veto with three new synthetic red-to-green regression cases. See results/post-pilot-revision.json.

This amendment is based on public constructed cases, not private/canon holdout feedback. No full comparative pilot was regenerated to make the result look better. A separate fresh two-task forward-test is recorded in results/evidence-status-forward-test.json; it is a focused behavior test, not a new superiority study. The release profile remains unchanged. Both fresh outputs preserved the hypothetical/planned framing or scoped process status; exact checks remained review-required. A no/not paraphrase caused an initial conservative veto and a local wording revision, retained in the forward-test log. This is additional evidence of review burden, not proof of semantic validation.

The original generation snapshot used 0.1.0 instructions. Independent synthetic review also hardened code/metadata handling concurrently. The later frontmatter compatibility-field move and 0.1.1 behavioral amendment are recorded separately. Therefore this is not a confirmatory experiment on a completely frozen runtime. Use new holdouts after freezing all code for a confirmatory study.

## Software findings and repairs

The independent reviewer reproduced private-metadata leakage through valid YAML forms, missed Markdown code delimiters, acceptance of nonmapping profile JSON, and string-valued metrics eligibility. These cases were observed failing before repair and independently rechecked after repair. Packaging regression tests additionally cover duplicate metadata keys, unsafe tags, missing agent exports, symlinks, deterministic bytes, internal/sidecar hashes and a safe root .gitignore. Source files are not mutated by export.

The guardian protects common forms and explicit locks; it does not parse every language, bibliography or LaTeX construct. A changed meaning with preserved tokens remains review-required rather than being certified. Grammar and personal voice are never automatically declared verified. Passing tests establish the named cases, not universal protection.

## Privacy, portability and reproduction

Private samples, source IDs and raw held-out outputs live under private/, mode 0700 with files 0600, and are excluded from distribution. Personal source content was not put in public search queries. Public model outputs use constructed facts; source originals are not invented. No historical credentials were used. No publication, global installation, or model training occurred.

The release builder creates deterministic ZIP bytes for unchanged sources, includes per-member SHA256SUMS and an archive checksum, and records checkout-to-export sanitization in EXPORT-MANIFEST.json. A final two-build equality and member-hash check accompanies handoff. The source profile freeze describes original checkout bytes; export hashes describe sanitized distributed bytes. These are deliberately different provenance scopes.

Replay `python -m pytest -q` and `python tools/evaluate_benchmark.py --output /tmp/write-like-me-replay`. Replay computes diagnostics from recorded model outputs; it does not regenerate model calls. Private raw cases are available only in this local workspace, so recipients of the public archive can reproduce public diagnostics and software tests but not the private-source experiment.

## Still unexecuted

- Blind author/human reader ratings, including genuine personal-voice judgments.
- Confirmed unassisted professor emails, LinkedIn posts, academic paragraphs and long technical prose, with representative holdouts.
- Native discovery/invocation/reference-loading and actual writing tests on ChatGPT/Custom GPT, Codex, Claude Code and Antigravity installations.
- Repeated controlled-model experiments, no-profile/mismatched-profile ablations, agreement estimates and a multi-agent-versus-single-review ablation.
- Universal semantic, grammatical, scientific-truth or dialect-fairness validation. The literature review and test suite do not supply these missing results.

The next priority is better consented genre evidence and blinded author judgments, followed by explicit platform runtime tests. Increasing surface-metric conformity or lowering a detector score is not an evaluation objective.
