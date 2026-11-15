# Multilingual writing and language-variety support

Reviewed 15 November 2026. This document proposes language-aware behavior and evaluation. It does not claim that this project has validated multilingual rewriting, Indian-English personalization, or fairness across language communities.

## Evidence boundaries

Liang and colleagues identify disparities in a particular English essay comparison. That finding does not measure Indian English, all second-language English writers, Hindi–English writing, or any present-day detector. Linguistic background should not be inferred from a name, nationality, affiliation, spelling, or a score. The study's category labels describe its design and should not become labels for this user. [Liang et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/).

M4 evaluates multiple languages, domains, and generators, but finite benchmark coverage does not establish reliability for a new variety or register. LinCE includes Hindi–English code-switching among its language pairs; its tasks include labeling and sentiment, not preservation of a writer's voice or detection of authorship. It supplies a precedent for treating code-switching as a real evaluation setting, not evidence that this tool handles it correctly. [Wang et al., 2024](https://aclanthology.org/2024.eacl-long.83/), [Aguilar et al., 2020](https://aclanthology.org/2020.lrec-1.223/).

TextSETTR demonstrates selected style dimensions including dialect in its tested setting. That result does not justify substituting one prestigious variety for another or generalizing few-example transfer to every language. [Riley et al., 2021](https://aclanthology.org/2021.acl-long.293/).

## Preserve the writer's chosen language and register

The writer can specify English, another language, or a mixture, including transliterated forms. Language, script, audience, and degree of formality are separate preferences. A Roman-script message can contain Hindi; an English-language academic draft can use Indian-English conventions; a writer can choose different registers for a supervisor, colleague, family member, or publication.

Proposed behavior:

- Preserve the requested language mix and script unless translation or normalization is requested.
- Keep a variety-specific expression when its meaning and audience fit; explain a possible ambiguity rather than silently replacing it.
- Treat spelling conventions, honorifics, politeness forms, discourse particles, and local terms as candidate preferences, not defects by default.
- Offer clarity changes in the chosen register; do not make “more native” a quality objective.
- Keep names, diacritics, references, units, formulae, and code exact when protected. Ask for authoritative transliteration rather than inventing one.
- Keep quoted passages distinguishable from the author's own writing. A quotation is not evidence for an author profile.

These are design choices. They are not measured effects of the reviewed papers. A user preference may change with audience; it should not be treated as a permanent national or linguistic identity.

## Measurement needs explicit assumptions

A whitespace word count is a count of whitespace-separated units. It is not a linguistically validated token count for every language. Sentence boundaries based on periods are also vulnerable to abbreviations, initials, decimal notation, and script-specific punctuation. Character counts can mean Unicode code points or grapheme clusters, which may differ for combining marks and conjuncts. The tool should name the measure it actually computes.

English function-word lists, readability formulae, vocabulary rarity dictionaries, and fixed sentence-length thresholds should not be silently applied to another language. A code-switched sentence may be understandable to its intended reader even when a monolingual dictionary marks many tokens unknown. Do not turn such failures into a fluency, grammar, education, or AI-authorship verdict.

For a local surface auditor, safe fallbacks are raw, clearly defined counts and an explicit “unsupported or unvalidated for this language/register” qualification. Mixed-language segmentation should be inspectable and overridable. Never silently translate text merely to make a measurement available. Unicode normalization, punctuation conversion, and transliteration can change a protected string; preserve the original and disclose any normalization used only for comparison.

## Proposed evaluation strata

| Dimension | Example distinction | Why it matters |
|---|---|---|
| Language and variety | English with declared en-IN preference; Hindi; another user-selected variety | One language label does not specify spelling, politeness, or register |
| Script | Devanagari versus Romanized Hindi | Segmentation and exact preservation behave differently |
| Language mixing | Monolingual English versus Hindi–English code-switching | A monolingual lexicon may mischaracterize valid writing |
| Register | Technical report, formal email, informal message | Appropriate style changes with relationship and task |
| Editing history | Original, translated, spelling-corrected, substantially rewritten | Legitimate assistance creates mixed production histories |
| Text structure | Prose, quotations, citations, mathematics, code | Surface statistics can be driven by protected nonprose spans |

Use only consented, clearly sourced samples. Writers should state their intended audience and judge whether a revision preserves their voice and meaning. Reviewers need competence in the actual language mix and register; a monolingual judge may miss either an error or a valid local expression. Report sample counts and failures separately for each supported stratum. Sparse or absent strata should remain “not evaluated,” not inherit an overall score.

Tests should include negation, modality, honorifics, names, dates, units, discourse particles, and code-switch boundaries. A draft may preserve every number and still change whether the writer is requesting, promising, doubting, or reporting something. Exact-span checks must therefore be followed by semantic review whenever prose changes.

## What remains untested

No private multilingual samples were examined. No translation, tokenization, readability, grammar, preservation, or author-preference benchmark was run in this research task. The reviewed selection contains no direct evaluation of this assistant for Indian-English writing, no general subgroup estimate for Indian writers, and no universal minimum sample size for learning personal voice. Those questions require a new, consented study with appropriate comparators. Until then, language support must describe actual implemented operations and their limits.
