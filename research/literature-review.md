# Evidence review for Write Like Me

Reviewed 15 November 2026. This is a targeted review of 21 published papers from 2009–2025, not a systematic review or a claim to cover the latest literature. It supports a local writing assistant that describes surface patterns, helps users specify their voice, and protects meaning during revision. No private writing samples, model outputs, or detector services were tested for this review.

The machine-readable register in [papers.json](papers.json) records every paper's complete verified author list, published title, year, venue, publication status, official URL, DOI where verified, research question, method, finding, limitation, project implication, and access evidence. [references.bib](references.bib) is generated from the same records. Findings below concern the cited studies; proposed controls are project decisions inferred from that evidence, not validated outcomes of this application.

## What the evidence supports

### A writing profile is a conditional description

Authorship attribution and personalization answer different questions. A classifier distinguishing a fixed set of candidate authors does not establish that a generated paragraph represents a person's voice. Stamatatos surveys the importance of representations and evaluation settings; Kestemont explains why conspicuous vocabulary alone is an unstable basis for attribution. Their work motivates transparent feature descriptions and careful comparison populations. It does not authorize an identity score. [Stamatatos, 2009](https://onlinelibrary.wiley.com/doi/abs/10.1002/asi.21001), [Kestemont, 2014](https://aclanthology.org/W14-0908/).

For this project, a profile should distinguish preferences explicitly stated by the writer from tendencies observed in supplied examples. Each observation needs its source genre, date or period when available, text amount, and uncertainty. An academic abstract and an informal message should not silently become a single target. Without supplied samples, the assistant can follow a brief but cannot claim to have learned the author's voice. These are proposed controls, not numerical thresholds established by the cited papers.

### Style change competes with preserving content

Style-transfer research commonly isolates attributes such as sentiment or formality. Mir and colleagues evaluate transfer strength, content preservation, and naturalness separately and find tradeoffs. Jin and colleagues survey a broader range of attributes and data settings. TextSETTR demonstrates exemplar-conditioned changes in selected dimensions, which makes it a useful precedent for explicit, limited restyling; it is not evidence that a few examples recover a person's complete voice. [Mir et al., 2019](https://aclanthology.org/N19-1049/), [Jin et al., 2022](https://aclanthology.org/2022.cl-1.6/), [Riley et al., 2021](https://aclanthology.org/2021.acl-long.293/).

The project should therefore specify both the desired change and what must survive it. Exact preservation of numbers, citations, names, mathematics, and code is a useful mechanical guard. It cannot establish that an unchanged number still has the same denominator, that a citation still supports its adjacent claim, or that an association has not become a causal statement. Changed prose always requires semantic review, including negation, uncertainty, scope, attribution, conditions, and the strength of conclusions. A surface checker should report its checks and unresolved questions, never convert them into an automatic fidelity verdict.

### Personalization should retain author control

CoAuthor captures writing as an interaction process rather than just a final string. LaMP evaluates retrieval from user profiles on personalized language tasks. Together they motivate relevant examples, draft comparison, and review decisions. They do not establish that this project's retrieval, privacy behavior, or voice fidelity works. [Lee et al., 2022](https://doi.org/10.1145/3491102.3502030), [Salemi et al., 2024](https://aclanthology.org/2024.acl-long.399/).

Use consented, relevant examples with provenance. Keep quotations and third-party text separate from the author's examples. Preserve the source draft and show proposed changes for acceptance. Logging every keystroke is not required: CoAuthor's research data collection is a precedent for studying interaction, not permission to collect the user's private history. Storage, retrieval, and optional model transmission need explicit, inspectable boundaries.

### Repeated model phrasing has several possible causes

Kirk and colleagues find lower output diversity after RLHF than SFT in their tested models and tasks, alongside better generalization. Holtzman and colleagues show that decoding choices affect repetition and quality in open-ended generation. These are bounded empirical mechanisms, not evidence that every aligned model, every genre, or every repeated phrase has the same cause. [Kirk et al., 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/5a68d05006d5b05dd9463dd9c0219db0-Paper-Conference.pdf), [Holtzman et al., 2020](https://pubs.cs.uct.ac.za/1407/1/the_curious_case_of_neural_text_degeneration.pdf).

DPO provides a simpler objective for optimizing pairwise preferences. Its original paper does not establish a generic-prose effect. Sharma and colleagues identify situations where preference judgments reward agreement at the expense of truth; their study does not isolate DPO. Therefore, the system should match presentation preferences without adopting false premises or strengthening claims to please the user. Fine-tuning is optional future work, not a necessary first implementation step. [Rafailov et al., 2023](https://proceedings.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html), [Sharma et al., 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/0105f7972202c1d4fb817da9f21a9663-Paper-Conference.pdf).

### Lexical trends do not justify a banned-word list

Kobak and colleagues analyze changes in biomedical abstract vocabulary at corpus scale. They explicitly state that the analysis cannot identify individual abstracts processed by an LLM, and discuss direct assistance versus diffusion of vocabulary into human writing. A word can be appropriate scientific terminology, part of the author's ordinary vocabulary, or a quoted passage. Removing a marker word can damage precision while establishing nothing about provenance. [Kobak et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/).

The local auditor may describe repetition or ask whether a phrase contributes meaning. It should not label ordinary words as evidence of AI use. Revisions should have a reason grounded in the writer's intent, audience, and examples.

### Detection and evaluation require separate treatment

DetectGPT and Fast-DetectGPT show that statistical discrimination can work in defined settings. Bias, distribution shift, editing, and mixed-origin studies show why this cannot become a universal authorship verdict. Details and source boundaries are in [detector-limitations.md](detector-limitations.md). A low score is not proof of human authorship, and a high score is not proof of misconduct. Detector reduction should not be the writing objective. [DetectGPT](https://proceedings.mlr.press/v202/mitchell23a.html), [Fast-DetectGPT](https://proceedings.iclr.cc/paper_files/paper/2024/file/6b8c6f846c3575e1d1ad496abea28826-Paper-Conference.pdf).

LLM judges can assist comparison, but the original MT-Bench/Arena study documents position, verbosity, self-enhancement, and reasoning limitations. A judge's preference is not an independent factual audit. Author review, blinded ordering, stable rubrics, and direct checking of protected claims remain necessary. [Zheng et al., 2023](https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).

## Evidence-to-control map

| Evidence or boundary | Proposed control | Verification still needed |
|---|---|---|
| Style depends on task and comparison corpus | Genre-specific profiles; observation provenance; no identity score | Held-out, cross-topic author judgments |
| Style/content/fluency can trade off | Separate rubrics; exact-span checks; semantic review for every changed prose draft | Paired revisions with known content constraints |
| Retrieval can support personalization | Retrieve only consented examples relevant to the requested genre | No-profile and mismatched-profile ablations |
| Preferences can favor agreement | Preserve factual corrections, caveats, and uncertainty despite tone changes | Tests with false premises and conflicting author preferences |
| Diversity depends on training and decoding | Record settings; inspect variation across prompts and users | Repeated runs at fixed settings; quality-conditioned diversity |
| Corpus marker vocabulary is not individual attribution | No banned-word detector; phrase edits require editorial reasons | Writer judgments of appropriateness |
| Detectors can fail under shift or editing | No authorship percentage or detector-evasion objective | Any optional future detector study needs a separate protocol |
| Language and code-switching coverage is finite | Preserve requested variety/script; mark unsupported measurements | Language/register-specific evaluation with competent reviewers |
| Judge scores have biases | Blind/randomize pairs; separate voice, readability, and fidelity | Agreement and disagreement analysis against author review |

These controls describe intended behavior. Their presence in a document or test name does not establish that they are implemented or empirically effective.

## Proposed evaluation, not completed experiments

Create a consented evaluation set split by document, topic, and time before deriving profiles. Keep the target draft and near duplicates out of retrieved examples. Compare an unchanged-source baseline, a generic revision, a brief-only revision, and a profile-conditioned revision using the same underlying model and decoding settings. A mismatched-profile condition can test whether a method meaningfully uses the correct profile; it should use consented test identities or clearly synthetic fixtures rather than another person's private writing.

The author should judge whether outputs fit the requested voice and genre. A second competent reader should examine meaning, evidence, and readability using a rubric that does not identify the method. Keep disagreement visible. Report per-document outcomes and sample counts, not just a pooled mean. For sufficient independent authors/documents, confidence intervals or paired analyses should reflect that clustering; multiple drafts from one source are not independent authors.

Measure protected-span retention, factual/semantic drift, unsupported additions, citation-claim alignment, and review burden alongside style preference. Surface changes are diagnostics; neither matching sentence lengths nor matching function-word frequencies is the goal itself. Record failures where prose sounds appropriate but changes the claim. No such experiment has been executed in this literature task.

## Coverage and unresolved questions

Searches used targeted titles/authors and topic combinations across official proceedings and publishers; the query families are recorded in the JSON. There was no preregistration, exhaustive database export, independent dual screening, formal risk-of-bias score, or quantitative synthesis. A survey or position paper is identified as such. All 21 selected records refer to published peer-reviewed venues; historical preprints are not counted separately. The collection is deliberately selective and contains no claim of current vendor performance.

Access was also uneven. Stamatatos was checked at the publisher abstract/record level. Most ACL records were checked through official metadata and abstracts; key method or limitation claims were checked in accessible primary PDFs/full text. The TMLR listing confirms Sadasivan's 2025 publication, and its accepted primary PDF was available through web-indexed extraction while the live canonical OpenReview page challenged the browser. The JSON records these distinctions rather than implying every appendix was read.

Important gaps remain: authentic-voice evaluation with sparse samples; long-term drift in a person's own writing; distinguishing voice from topic or coauthor/editor influence; meaning preservation beyond protected spans; multilingual and Indian-English personalization; fairness under legitimate language assistance; memorization or private-detail leakage from examples; and whether users can efficiently inspect and correct a profile. See [multilingual-writing.md](multilingual-writing.md) for language-specific scope limits. None is resolved by a successful static check or a plausible demonstration.
