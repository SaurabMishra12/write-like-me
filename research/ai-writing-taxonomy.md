# Contextual editorial taxonomy

Research checked **2026-11-15**. These 24 patterns are prompts for editorial review, not a classifier, an authorship verdict, a detector-evasion checklist, or a list of forbidden words. The target is writing that says what the author means, supports its claims, fits its audience, and preserves the author's accepted voice. Some competent writing will match every surface feature below.

The [Wikipedia community guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) was opened and read in relevant sections. It identifies itself as an advice page, not policy, and distinguishes observed signals from underlying problems. This taxonomy borrows that caution rather than treating its examples as universal prescriptions. The argument problem often lies in missing evidence, a false relation, or an unexplained decision, not in the token that drew attention.

[UNC's concision guide](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/) explicitly allows deliberate repetition and rhythm. [Google's lists guide](https://developers.google.com/style/lists) gives useful purposes for structured lists. Preserve those choices when they serve this writer and reader. Never reduce the user's voice to a generic anti-AI house style.

## Evidence, confidence, and actions

- **B** means primary editorial/university guidance, **C** a community observation, **H** a historical primary text, **J** our contextual editorial judgment, and **A-scoped** a primary research result limited to its actual domain. These are evidence types, not a ranking of how “AI-like” a sentence is.
- **Detection confidence** below concerns the specified editing issue in the supplied context. It is a qualitative judgment, not a measured probability, score, prevalence estimate, or authorship confidence.
- **Severity** concerns reader burden or factual integrity. It does not measure suspicion. A low-severity preference mismatch can be left alone; an unsupported factual claim requires verification.
- **Warning** means explain the gap and seek evidence or a decision; **edit** means a supported local change that preserves meaning. Do not fill an evidence gap by making the prose sound more plausible.
- All examples and revisions below are **original constructed illustrations**, not quotations, genuine research findings, actual client claims, or pre-2018 excerpts. Any illustrative factual detail must be replaced by verified material before use.

### Limits of empirical evidence

[KOBAK-2025](https://arxiv.org/abs/2406.07016v5) reports aggregate vocabulary shifts in biomedical abstracts. It does not establish that any word diagnoses the origin of an individual sentence. [LIANG-2023](https://arxiv.org/abs/2304.02819v3) reports false classifications for particular detectors and English-writing samples; [ALALI-2026](https://arxiv.org/abs/2602.05769) reports a different result in a Czech setting and different systems. Only their abstracts/metadata were reviewed here, and no findings were replicated. Neither universal bias nor universal accuracy follows. This package has no validated authorship classifier.

### Historical counterexamples and discussion

The codes below keep historical evidence separate from invented examples. A historical discussion establishes that a concern or device existed before 2018; it does not authenticate the exact constructed wording above.

- **H0: not established here.** No exact dated pre-2018 counterpart was verified for that entry. No recent-origin claim is made. The entry remains an editorial concern, not historical proof or authorship evidence.
- **H1: [STRUNK-1920](https://www.gutenberg.org/cache/epub/37134/pg37134-images.html).** The opened edition records 1918/1919/1920 copyrights and discusses specificity, needless wording, paragraphs, parallel form, punctuation, and sentence variety. Its own headings and lists also refute a blanket claim that structured writing is inherently new or machine-produced.
- **H2: [ORWELL-1946](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/).** The essay examines vague, inflated, formulaic prose and stale imagery. These concerns preceded modern language models. Its preferences are situated rhetorical advice, not universal bans.
- **H3: [LINCOLN-1863](https://www.gutenberg.org/files/4/4-h/4-h.htm).** The opened Gettysburg Address transcription supplies clear human counterexamples for triplets, repeated syntax, contrast, and ceremonial elevation. Effective use of a device is possible; its presence alone says nothing about a current writer's authorship.
- **H4: document structure.** H1's headings and parallel lists establish longstanding human use. The current [GOOGLE-LISTS](https://developers.google.com/style/lists) guide demonstrates their practical value. Neither source is offered as an exact historical counterpart for a modern chat-formatting complaint.

## Review patterns

### WL-T01: Prestige vocabulary that carries no extra meaning

**Category:** lexical. **Severity:** Low. **Detection confidence:** Low without the surrounding argument and a voice profile.

Inspect clustered abstract or promotional wording when it obscures the actual action or result. A single word never triggers a rewrite.

**Constructed example:** We leverage a robust framework to delve into the intricate landscape of adoption.

**Context:** Explanatory and professional prose; compare the writer's accepted samples. **False-positive risk:** Technical senses of robust, a literal landscape, deliberate metaphor, disciplinary terminology, and the writer's normal vocabulary.

**Source / evidence grade:** [ORWELL-1946](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/), [KOBAK-2025](https://arxiv.org/abs/2406.07016v5). B/J; A-scoped association only. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H2. No individual listed word is treated as new, forbidden, or uniquely machine-associated.

**Warning versus edit:** Warning first. Edit only when a more precise expression keeps the meaning and matches the user's voice.

**Correction strategy:** We examine why teams adopted the framework. Use this only if it preserves the intended question; otherwise identify the real action first.

### WL-T02: Synonym changes that make one thing look like several

**Category:** lexical / technical documentation. **Severity:** Medium. **Detection confidence:** Medium after checking the product vocabulary; low from tokens alone.

A named component or concept changes labels for surface variety, leaving the reader unsure whether the referent changed.

**Constructed example:** Create a workspace. Open the environment. Rename the project area.

**Context:** Documentation, scientific methods, requirements, reports. **False-positive risk:** Synonyms can signal genuine distinctions or be necessary in literary prose; never collapse them without domain evidence.

**Source / evidence grade:** [GOOGLE-WORDS](https://developers.google.com/style/word-list). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No dated pre-2018 example for this exact technical sequence was verified.

**Warning versus edit:** Warn when referents are uncertain; edit only after identity is established.

**Correction strategy:** If all three refer to the same product entity, use its verified interface name consistently. If they differ, define the difference.

### WL-T03: Indirect identity statements

**Category:** syntactic. **Severity:** Low. **Detection confidence:** Medium for avoidable indirection, never for authorship.

A sentence reaches for an evaluative construction where the reader only needs a definition or identity.

**Constructed example:** The register serves as a testament to the project's commitment to traceability.

**Context:** Definitions, summaries, project documentation. **False-positive risk:** Serves as can describe a real temporary role; metaphor may be part of an intentional voice.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). C/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H2; the historical discussion is about inflated expression, not this exact sentence.

**Warning versus edit:** Optional edit when the direct version preserves the relationship.

**Correction strategy:** The register records the project's sources. Keep an evaluative claim only if the text supports it.

### WL-T04: Commentary appended as if it were analysis

**Category:** syntactic / academic. **Severity:** High when an inference is overstated. **Detection confidence:** Medium; requires study design and evidence context.

A trailing clause interprets an observation without stating the reasoning needed to get there.

**Constructed example:** The two scores differ, highlighting the superiority of the new approach.

**Context:** Results, literature synthesis, business reports. **False-positive risk:** A participial clause can compactly express an inference already established nearby.

**Source / evidence grade:** [UNC-EVIDENCE](https://writingcenter.unc.edu/tips-and-tools/evidence/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No dated pre-2018 instance of this constructed analytical sentence was verified.

**Warning versus edit:** Warning requiring evidence. Do not repair the argument by inventing a mechanism or result.

**Correction strategy:** Report the observed difference. Establish comparability and uncertainty before claiming superiority; if that evidence is missing, leave the interpretation unresolved.

### WL-T05: Actors hidden by nouns and passive constructions

**Category:** syntactic. **Severity:** Medium. **Detection confidence:** Medium; role identity must be known.

The reader cannot tell who must do what, especially in a request or procedure.

**Constructed example:** Completion of the review should be undertaken before publication.

**Context:** Procedures, policy implementation, email requests. **False-positive risk:** Passive voice can correctly foreground a specimen, method, or unknown actor. Nominalizations can name necessary technical concepts.

**Source / evidence grade:** [UNC-CONCISE](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H1.

**Warning versus edit:** Edit only when the actor is known; otherwise flag the responsibility gap. Do not ban passive voice.

**Correction strategy:** The editor should finish the review before publication, if editor is the verified responsible role.

### WL-T06: Transitions that misstate the logic

**Category:** discourse. **Severity:** High for unsupported causation; low for repetition. **Detection confidence:** Medium after reading both claims.

A connective announces addition, contrast, or causation that the surrounding claims do not support.

**Constructed example:** The sample was smaller. Therefore, the method was more accurate.

**Context:** Arguments, scientific explanations, reports. **False-positive risk:** Explicit connectives help readers, language learners, and complex arguments. Repeated moreover is not itself a defect.

**Source / evidence grade:** [UNC-TRANSITIONS](https://writingcenter.unc.edu/tips-and-tools/transitions/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. The logical problem is not assigned a recent origin; no exact pre-2018 sentence is claimed.

**Warning versus edit:** Warning for uncertain logic; edit only after the relationship is determined.

**Correction strategy:** State the actual relationship. If no causal link is established, present the two observations separately.

### WL-T07: Recaps that repeatedly restart the same point

**Category:** discourse / structural. **Severity:** Low. **Detection confidence:** Medium across the full section.

An opening, midsection recap, and conclusion repeat one proposition without adding evidence, implications, or orientation.

**Constructed example:** This section explains backups. Backups matter because they preserve copies. In summary, copies are why backups matter.

**Context:** Short answers, memos, tutorials. **False-positive risk:** Teaching, accessibility, long reports, and executive summaries may require purposeful repetition.

**Source / evidence grade:** [UNC-CONCISE](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H1.

**Warning versus edit:** Optional edit conditioned on length, genre, and the user's preference for recap.

**Correction strategy:** Keep the explanation and any needed recovery detail; remove repeated restatement only if the reader loses no guidance.

### WL-T08: Contrast used as a slogan instead of a distinction

**Category:** rhetorical. **Severity:** Low unless the contrast distorts a claim. **Detection confidence:** Low; the validity of the distinction is semantic.

A repeated 'not X, but Y' frame substitutes a neat opposition for a supported distinction.

**Constructed example:** This is not about storage. It is about trust.

**Context:** Essays, opinion, presentations, marketing. **False-positive risk:** Antithesis is an established human rhetorical device and can express an essential contrast.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [LINCOLN-1863](https://www.gutenberg.org/files/4/4-h/4-h.htm). C/J; H counterexample. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H3.

**Warning versus edit:** Warning only unless the contrast is demonstrably empty or the user asked for plainer phrasing.

**Correction strategy:** Explain the actual storage failure and why it affects trust. Keep the contrast if both sides make the argument more accurate.

### WL-T09: A forced third item or repeated triplet cadence

**Category:** rhetorical / stylistic. **Severity:** Low. **Detection confidence:** Low for cadence; medium for a demonstrable duplicate.

A passage repeatedly groups items into threes, with an irrelevant or overlapping item added to complete the rhythm.

**Constructed example:** The tool improves accuracy, correctness, and being right.

**Context:** Summaries, promotional prose, talks. **False-positive risk:** Triplets aid memory, describe real three-part systems, and occur in historical speeches.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [LINCOLN-1863](https://www.gutenberg.org/files/4/4-h/4-h.htm). C/J; H counterexample. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H3.

**Warning versus edit:** Edit redundant membership, never the number three itself.

**Correction strategy:** Name the distinct supported benefit. Retain three items when there really are three.

### WL-T10: Significance claimed without a defined consequence

**Category:** semantic / rhetorical. **Severity:** Medium. **Detection confidence:** Medium when evidence is absent from the supplied material; absence from all sources is unverified.

A text labels a modest event transformative or historically important without explaining the relevant effect.

**Constructed example:** The new menu marks a pivotal moment in the evolution of collaboration.

**Context:** Biographies, project summaries, promotional copy. **False-positive risk:** Ceremonial speech and advocacy can intentionally use elevated language; some events have documented major effects.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [ORWELL-1946](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/). C/B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H2 and H3.

**Warning versus edit:** Warn about unsupported significance; replace only with supplied concrete facts.

**Correction strategy:** Describe what changed in the menu and the user task it affects. Broader significance needs evidence.

### WL-T11: An unnamed crowd presented as authority

**Category:** semantic / academic. **Severity:** High when authority is central to the argument. **Detection confidence:** Medium; the attribution may exist elsewhere in the document.

Experts, observers, critics, or many people are invoked without enough identity or evidence to assess the claim.

**Constructed example:** Experts agree that this system is the best option.

**Context:** Academic, policy, review, and advice writing. **False-positive risk:** A short summary may legitimately refer back to named sources or a documented consensus.

**Source / evidence grade:** [UNC-EVIDENCE](https://writingcenter.unc.edu/tips-and-tools/evidence/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No exact pre-2018 consensus sentence verified; unsupported authority is an argument issue.

**Warning versus edit:** Evidence warning. Do not generate experts, quotes, organizations, or a consensus.

**Correction strategy:** Identify the relevant experts and their supported positions, or qualify/remove the consensus claim.

### WL-T12: A balanced-sounding paragraph with no discriminating evidence

**Category:** semantic / discourse. **Severity:** Medium. **Detection confidence:** Medium for missing specificity within the supplied scope.

The text lists generic benefits and challenges but gives no basis for a decision or interpretation.

**Constructed example:** The approach has benefits and limitations. Context matters, and future work will help.

**Context:** Discussion, recommendations, reports. **False-positive risk:** A brief signpost or an honest statement of uncertainty can be appropriate; do not manufacture a strong opinion.

**Source / evidence grade:** [UNC-EVIDENCE](https://writingcenter.unc.edu/tips-and-tools/evidence/), [UNC-TRANSITIONS](https://writingcenter.unc.edu/tips-and-tools/transitions/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No verified historical quote is asserted.

**Warning versus edit:** Warning requiring substance, not synonym substitution.

**Correction strategy:** State the actual benefit, relevant limitation, and decision criterion available in the source material; otherwise say what is missing.

### WL-T13: Precision that has no traceable origin

**Category:** semantic / content generation. **Severity:** High. **Detection confidence:** High that provenance is missing from the provided record; truth itself remains unverified.

An exact number, date, quotation, example person, or operational detail appears without provenance.

**Constructed example:** The redesign reduced delays by 37.4%.

**Context:** All factual deliverables. **False-positive risk:** The author may possess measurements not supplied to the editor; lack of a citation does not prove fabrication.

**Source / evidence grade:** [MLA-AI](https://style.mla.org/citing-generative-ai-updated-revised/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No claim that unsupported precision is new, and no exact pre-2018 example verified.

**Warning versus edit:** Warning. Never replace a suspicious value with a plausible invented value.

**Correction strategy:** Keep the value only with a verifiable origin and relevant conditions. Otherwise mark it unverified or omit it with an explicit note.

### WL-T14: Formatting that defeats the requested reading mode

**Category:** structural / stylistic. **Severity:** Low; medium when it prevents usable copying or reading. **Detection confidence:** High when an explicit formatting instruction is contradicted; otherwise low.

Repeated bold spans, nested lists, or one-sentence blocks make an intended conversation hard to follow.

**Constructed example:** Every sentence becomes a bold-labeled bullet even after the user requests continuous prose.

**Context:** Chat, emails, reports, document exports. **False-positive risk:** Headings, emphasis, parallel lists, and accessible chunking may be requested or necessary.

**Source / evidence grade:** [REDDIT-BOLD](https://www.reddit.com/r/ChatGPT/comments/1idkxf4/how_to_stop_chatgpt_from_using_bold_font_too_much/), [REDDIT-FORMAT](https://www.reddit.com/r/ChatGPT/comments/1fkh33c/chatgpt_refuses_to_follow_format_instructions/), [DEV-FORMAT](https://community.openai.com/t/chatgpt-refuses-to-format-responses-correctly/946916), [GOOGLE-LISTS](https://developers.google.com/style/lists). C for reported friction; B/J for contextual correction. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H4.

**Warning versus edit:** Edit when a clear formatting preference or reader task supports it. No universal headings/list/bold ban.

**Correction strategy:** Use the requested prose form; retain lists where genuine choices, steps, or comparisons benefit from them.

### WL-T15: A template forces sections the material cannot support

**Category:** structural / content generation. **Severity:** Low. **Detection confidence:** Medium after checking the required format.

Uniform sections exist because a template expects them, leaving filler in areas with no relevant content.

**Constructed example:** A two-sentence change note is expanded into Background, Benefits, Challenges, Future Outlook, and Conclusion.

**Context:** Reports, technical notes, web copy, generated outlines. **False-positive risk:** Rubrics, regulatory forms, journal templates, or a user request can require fixed sections.

**Source / evidence grade:** [UNC-TRANSITIONS](https://writingcenter.unc.edu/tips-and-tools/transitions/), [GOOGLE-LISTS](https://developers.google.com/style/lists). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H4. Historical sectioning is not evidence for the exact modern template.

**Warning versus edit:** Optional structural edit unless a required format must be preserved.

**Correction strategy:** Keep sections that help the intended reader; omit empty sections or flag missing required content.

### WL-T16: Punctuation clashes with the user's established cadence

**Category:** stylistic. **Severity:** Low. **Detection confidence:** Low without samples and context.

Dense asides, parentheticals, semicolons, or dashes interrupt the particular reading task or differ from accepted samples.

**Constructed example:** A simple request accumulates three parenthetical asides before reaching its verb.

**Context:** Voice-sensitive editing; plain procedural requests. **False-positive risk:** Dashes and other marks are normal human punctuation; literary, academic, and conversational styles use them differently.

**Source / evidence grade:** [UNC-CONCISE](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H1 and H2. No punctuation mark is treated as post-2018 evidence.

**Warning versus edit:** Warning or optional local edit. Never count dashes as an authorship score.

**Correction strategy:** Separate or move the asides when meaning and emphasis survive; keep the punctuation that the writer intentionally uses.

### WL-T17: Uniform sentence fragments flatten the reasoning

**Category:** syntactic / stylistic. **Severity:** Low. **Detection confidence:** Medium for a documented preference mismatch; otherwise low.

A passage breaks connected reasoning into repeated short fragments, losing relationships or producing an unwanted cadence.

**Constructed example:** One result. One answer. One future. The next step. The way forward.

**Context:** Explanatory prose and conversational answers. **False-positive risk:** Fragments suit dialogue, headlines, accessible summaries, advertisements, or the writer's deliberate rhythm.

**Source / evidence grade:** [STRUNK-1920](https://www.gutenberg.org/cache/epub/37134/pg37134-images.html), [REDDIT-BOLD](https://www.reddit.com/r/ChatGPT/comments/1idkxf4/how_to_stop_chatgpt_from_using_bold_font_too_much/). H/B/J; C for user report. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H1.

**Warning versus edit:** Optional edit. Do not impose uniformly long sentences as a supposed human style.

**Correction strategy:** Join connected ideas and vary rhythm where that clarifies their relationship; retain purposeful fragments.

### WL-T18: Assistant conversation leaks into the deliverable

**Category:** stylistic / content generation. **Severity:** Low. **Detection confidence:** High for a standalone document boundary; low for a chat response.

Task acknowledgments or offers to continue remain inside a document meant to stand on its own.

**Constructed example:** Absolutely! Here is your revised report. Let me know if you'd like me to expand it.

**Context:** Reports, emails drafted for sending, articles, slide text. **False-positive risk:** Such phrases are natural in actual correspondence and interactive assistance.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). C/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. These exact contemporary assistant expressions were not checked against pre-2018 texts.

**Warning versus edit:** Edit document-boundary residue when its role is unambiguous; preserve quoted examples.

**Correction strategy:** Remove the wrapper from the report body unless it is a deliberate conversational document.

### WL-T19: Certainty or caution detached from the evidence

**Category:** academic / semantic. **Severity:** High for overclaim; low for verbal clutter. **Detection confidence:** Medium only with access to methods and results.

The text overstates a result or adds so many generic hedges that the actual measured finding disappears.

**Constructed example:** These findings conclusively prove universal effectiveness. / The data may perhaps possibly suggest something.

**Context:** Academic abstracts, results, discussion, research summaries. **False-positive risk:** May and suggests often express necessary epistemic limits; legal and clinical qualifications may be essential.

**Source / evidence grade:** [UNC-EVIDENCE](https://writingcenter.unc.edu/tips-and-tools/evidence/), [UNC-CONCISE](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H2. Historical criticism of vagueness does not settle scientific uncertainty.

**Warning versus edit:** Evidence warning before editing claims; local hedge removal only when certainty is unchanged.

**Correction strategy:** State the supported result and its actual conditions or uncertainty. Preserve domain-required cautious wording.

### WL-T20: A citation is present but does not support the sentence

**Category:** academic. **Severity:** High. **Detection confidence:** High only after direct source inspection; otherwise unverified.

A reference is missing, nonexistent, unrelated, or cited for a stronger claim than the inspected source supports.

**Constructed example:** A general review is cited as proof that this specific intervention succeeded.

**Context:** Papers, literature reviews, technical and professional reports. **False-positive risk:** A citation can be indirect, support a limited subclaim, or follow a field convention; check its intended scope.

**Source / evidence grade:** [MLA-AI](https://style.mla.org/citing-generative-ai-updated-revised/). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. Citation errors are not assigned an AI origin; no dated pre-2018 example audited here.

**Warning versus edit:** Warning requiring source verification. Do not invent a replacement citation, page, DOI, quotation, or author.

**Correction strategy:** Open the original source, check identity and claim support, then narrow the sentence or supply an actually supporting source.

### WL-T21: Email ceremony obscures the actual request

**Category:** email / discourse. **Severity:** Low. **Detection confidence:** Low without recipient and relationship context.

Stacked goodwill and preambles delay the purpose, owner, or deadline of a practical message.

**Constructed example:** I hope this message finds you well. I am writing to kindly reach out regarding the possibility of your reviewing the attached note.

**Context:** Follow-up, request, scheduling, and professional email. **False-positive risk:** Courtesy is culturally variable and may be especially important in a first contact or unequal power relationship.

**Source / evidence grade:** [PURDUE-EMAIL](https://owl.purdue.edu/owl/general_writing/academic_writing/email_etiquette.html). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. Purdue's visible copyright range is not used to claim this exact greeting was verified before 2018.

**Warning versus edit:** Optional edit based on audience and voice, never a universal ban on greetings or politeness.

**Correction strategy:** Could you review the attached note? Add a deadline only when supplied. Retain a greeting and warmth appropriate to the relationship.

### WL-T22: Documentation describes a benefit but omits the task

**Category:** technical documentation / semantic. **Severity:** High if missing detail makes the procedure unreliable. **Detection confidence:** Medium; the task may be specified elsewhere.

A paragraph tells users a capability is powerful or simple but omits the needed action, prerequisite, or expected result.

**Constructed example:** This intuitive configuration unlocks seamless deployment.

**Context:** README files, onboarding, support articles, API guides. **False-positive risk:** An overview may intentionally defer instructions through a useful verified link.

**Source / evidence grade:** [GOOGLE-WORDS](https://developers.google.com/style/word-list), [GOOGLE-LISTS](https://developers.google.com/style/lists). B/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No exact dated pre-2018 task paragraph inspected.

**Warning versus edit:** Warning requiring technical evidence; edit once the procedure is known. Keep code and interface labels exact.

**Correction strategy:** Supply verified settings, commands, prerequisites, and expected output. If unavailable, flag those gaps rather than generating runnable-looking instructions.

### WL-T23: A borrowed voice claims experiences the writer did not supply

**Category:** content generation / semantic. **Severity:** High. **Detection confidence:** High that the experience lacks supplied provenance; its real-world truth remains unknown.

A first-person anecdote, testimonial, feeling, or credential is added to make prose feel human.

**Constructed example:** When I led a team through this crisis, I learned the answer firsthand.

**Context:** Personal statements, opinion pieces, posts, recommendation letters, marketing. **False-positive risk:** The writer may have the experience but not have included it in the materials; fiction can intentionally invent a narrator.

**Source / evidence grade:** [MLA-AI](https://style.mla.org/citing-generative-ai-updated-revised/). J; source supports provenance checking, not this exact anecdote rule. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. No claim that invented personas began with AI; no exact historical anecdote verified.

**Warning versus edit:** Warning. Never manufacture flaws, memories, typos, or personal disclosures to simulate humanity.

**Correction strategy:** Use a supplied authentic experience, label a genuinely hypothetical example, or make the general argument without invented autobiography.

### WL-T24: Unresolved template slots or broken output artifacts

**Category:** content generation / structural. **Severity:** Medium; high if it masquerades as a real source. **Detection confidence:** High for an unresolved literal placeholder; low for intentional examples.

Placeholders, copied prompt directives, malformed references, or incomplete template fields survive into final prose.

**Constructed example:** Dear [RECIPIENT], see SOURCE_URL for the verified result.

**Context:** Email drafts, reports, generated documentation. **False-positive risk:** Templates, teaching examples, code, and quoted prompts often intentionally contain placeholders.

**Source / evidence grade:** [WIKI-AI](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). C/J. The operational rule and example are editorial synthesis; the cited source does not validate this package's detection accuracy.

**Pre-2018 counterexample / discussion:** H0. Exact contemporary placeholder syntax was not historically audited.

**Warning versus edit:** Edit only with known values; otherwise issue a missing-information warning and preserve draft status.

**Correction strategy:** Resolve from supplied information; keep a clearly labelled placeholder in a draft when the required fact is unavailable.

## Applying the taxonomy to an individual writer

Start from representative, user-authorized samples and the task's audience, purpose, register, medium, and factual record. An approved stylistic habit outranks a generic preference in this taxonomy. Preserve deliberate syntax, dialect, cultural politeness, technical terms, quotations, citation content, numbers, code, and proper names. Do not inject personal history or perform artificial “human” errors.

For a review, identify the exact span, the reader/argument consequence, the relevant pattern, the available evidence, and a suggested action. A token match is a candidate for inspection only. If the reason for changing it is merely “AI uses this,” make no edit. For a rewrite, repair local supported problems and recheck meaning, factual certainty, voice, and structure. Track unresolved factual gaps separately from optional style changes.

## Source coverage and limitations

Actually examined: Wikipedia's relevant community-guide sections; two public Reddit threads ([bold](https://www.reddit.com/r/ChatGPT/comments/1idkxf4/how_to_stop_chatgpt_from_using_bold_font_too_much/) and [format requests](https://www.reddit.com/r/ChatGPT/comments/1fkh33c/chatgpt_refuses_to_follow_format_instructions/)); one [developer-community formatting report](https://community.openai.com/t/chatgpt-refuses-to-format-responses-correctly/946916); the linked university/editorial guides; three historical texts; and the three paper abstract/metadata pages.

Reddit and forum reports establish that users have reported particular friction. They do not establish prevalence, a cause, a model-wide property, or a prohibition on formatting. This is a selected source review, not an exhaustive literature search or statistical validation.

**X and LinkedIn were not examined.** No authenticated access to either was used, and no claims are attributed to those platforms. The LOC page attempted for Lincoln returned 403; the opened Gutenberg transcription is the actual historical source. The complete access ledger, grade definitions, reviewed scope, and source-specific limitations are in [editorial-sources.json](editorial-sources.json). Platform documentation has a separate boundary in [platform-support.md](platform-support.md).

