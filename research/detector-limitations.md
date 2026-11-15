# AI-text detection: what the evidence permits

Reviewed 15 November 2026. These notes concern published research settings, not a current ranking of commercial services. Write Like Me should describe and revise writing; it should not issue authorship verdicts, estimate a percentage written by AI, or optimize drafts to lower a detector score.

## Distinguish three questions

1. **Statistical resemblance:** does a passage have features associated with one evaluated generator or dataset?
2. **Production history:** who drafted, translated, edited, or selected each part?
3. **Permitted assistance:** what does the relevant author, venue, or assessment allow?

A text-only score does not answer all three. A percentage attached to a classifier need not be a calibrated posterior probability, a token fraction, or a measure of the writer's contribution. Ground truth in a benchmark is a label assigned by its data-generation protocol. Real workflows may combine human drafting, spelling correction, translation, generation, and substantial human revision.

## Positive detector results have a scope

DetectGPT scores probability curvature using model probabilities and perturbed text. Fast-DetectGPT uses conditional sampling/scoring and evaluates surrogate-model settings as well. Their positive benchmark results are evidence that discrimination is possible under stated conditions. They do not establish performance on this user's genre, language, model, or editing history. AUROC summarizes ranking across thresholds; it does not specify a deployment false-positive rate or prove an individual origin. [Mitchell et al., 2023](https://proceedings.mlr.press/v202/mitchell23a.html), [Bao et al., 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/6b8c6f846c3575e1d1ad496abea28826-Paper-Conference.pdf).

Fast-DetectGPT's headline relative improvement uses the remaining AUROC gap to 1 as its denominator. It must not be rewritten as a percentage-point improvement in accuracy. Its reported speed comparison is also tied to a specified benchmark and hardware. This project has not run that implementation.

## Failure modes and boundaries

| Source | Observed issue | What cannot be inferred |
|---|---|---|
| [Liang et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/) | Large false-positive disparity between the evaluated TOEFL and US school-essay cohorts | A causal estimate for all language learners; a measured Indian-English result; performance of every later detector |
| [Weber-Wulff et al., 2023](https://link.springer.com/article/10.1007/s40979-023-00146-z) | Errors across the tested tools and degradation under transformations | A present-day product ranking or proof that no detector can discriminate |
| [Wang et al., 2024](https://aclanthology.org/2024.eacl-long.83/) | Difficult generalization to unseen domains and generators in M4 | Equal reliability or equal error rates across all languages/registers |
| [Sadasivan et al., 2025](https://openreview.net/forum?id=OOgsAZdFOt) | Vulnerability of tested detector families to editing attacks; conditional theoretical limits | A claim that every possible detector always performs at chance |
| [Saha and Feizi, 2025](https://aclanthology.org/2025.findings-acl.1303/) | Detectors often flag minimal AI polishing and poorly separate involvement levels | A scientifically valid division of any document into percentages of human and AI authorship |

The Liang comparison uses different essay sources and student populations. It raises a serious empirical fairness concern while leaving population, task, age, and proficiency effects entangled. Calling ordinary or predictable English suspicious can penalize legitimate writing. The remedy is not to make every writer adopt a supposedly native style or manufacture linguistic errors.

The Sadasivan result bounds discrimination through the total-variation distance between the specified human and model text distributions. If those distributions coincide, a content-only classifier has no distributional signal separating them. The premise is about defined distributions, not a measurement that all current model outputs coincide with all human text. Its empirical attacks likewise concern the evaluated systems. Neither this theorem nor attack robustness should be turned into a detector-evasion recipe.

## Prevalence changes the meaning of a flag

Consider a hypothetical, explicitly assumed population: 1% of documents belong to a defined generated class; a detector has 90% sensitivity and a 5% false-positive rate on that exact population. Among 10,000 documents, it flags 90 generated and 495 other documents, so only 90/585, about 15.4%, of flags belong to that generated class. These are illustrative arithmetic, not measured performance of any named service.

In notation, with prevalence π, sensitivity s, and false-positive rate f:

`P(class | flag) = sπ / (sπ + f(1 − π))`.

This requires well-defined classes and stable rates. Mixed writing, changing models, and population shift can invalidate those assumptions. A service's displayed score should never be substituted for these quantities without documentation and validation.

## Local surface auditing is a different task

Counts of repeated phrases, sentence lengths, punctuation, headings, or lexical patterns can help the author inspect a draft. They are observations about that draft. They should be labeled with their definitions and limitations, with no calibration claim and no threshold that declares a text human or AI. Short text, quotations, equations, references, code, tables, and script-dependent tokenization can distort such counts.

A strict preservation guard should protect declared spans and flag changes to numbers, names, citations, mathematical expressions, and code. Passing those checks does not establish semantic fidelity. A qualifier can disappear, an argument can reverse, an unchanged quantity can acquire a different referent, and a citation can move onto an unsupported claim. Changed prose requires semantic review. The guard should return mechanical results and a review requirement, not “verified meaning.”

Keep source drafts, revision diffs, author decisions, and optional disclosure notes when the author wants them. Such records can describe this tool's process; they are not tamper-proof proof of every preceding action. Do not transmit private text to external detectors without specific authorization. No detector call or detector benchmark was performed for these artifacts.

## Conditions for a future detector study

A separate study would need a defined use, dated detector versions, documented source models, held-out human and generated documents, realistic edited/mixed conditions, language/register strata, threshold selection on separate validation data, sensitivity at declared false-positive rates, uncertainty, and a report of coverage gaps. It must avoid pooling copies or multiple variants of the same document as independent evidence. A useful benchmark result would still support a population-level operating claim, not certainty about one writer.

The present project does not need a detector to offer useful editorial assistance. Relevant quality outcomes are preserved meaning and evidence, appropriate voice and register, readability, and author control.
