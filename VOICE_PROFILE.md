# Personal voice and canon profile

This initial profile is provisional. It models six profile messages in three source groups: four English task prompts (189 whitespace-delimited words) and two likely transcribed Hindi-English study messages. The user confirmed short informal prompts were unassisted on 2026-11-15. Calibration and held-out groups were not used to tune it.

The strongest evidence is for task-oriented directness (3/4 English messages), connected detail (2/4), and a preference for concrete deliverables. A request to test an interpretation against other findings occurs once; a request for intuitive connections occurs once. These small counts support tentative guidance, not a stable personal stylometric signature. Evidence IDs, examples and exact private source spans appear in ignored private/VOICE_EVIDENCE.md. No private source text belongs in the distributable bundle.

The canon supplies long-form craft where personal evidence is missing: concrete mechanism before abstraction, explicit problem decomposition, reader-oriented argument, bounded claims, and candid limitations. These are adopted choices, not proof that the user naturally writes like any named author. The pre-2018 filter applies to individual passages as well as publication dates; quoted or machine-generated examples inside old works must be excluded.

## Four levels

| Level | Personal finding | Application and confidence |
|---|---|---|
| Sentence | Direct requests; informal fragments; long additive chains | Preserve directness. Fix accidental errors. Exact sentence rhythm uncertain because punctuation and transcription are unreliable. |
| Paragraph | Most samples are single prompt paragraphs | No defensible personal paragraph model. Use concept-led canon craft and preserve supplied organization. |
| Reasoning | One question about whether an experiment supports improvement; one request connecting fields | Preserve actual intellectual position; do not infer a psychological disposition. Evidence preference is also an explicit project requirement. |
| Linguistic identity | Hindi-English code-switching exists in two spoken-style prompts | Preserve understandable supplied Indian English. Do not infer a Hindi cause for any English construction or insert stereotyped wording. |

## Register calibration

Professor email, LinkedIn, GitHub, informal, mathematics, speaking, and academic profiles all share factual restraint and direct purpose. Formal prose uses complete sentences and reader-oriented structure. Informal replies remain short. Documentation may use lists; speaking may use questions; academic prose may use passive voice deliberately. Formal style is canon-informed until genuine personal samples exist. Genre settings are in profiles/*.yaml and workflows/*.md.

The human-readable source of truth is profiles/voice-profile.yaml. The root voice-profile.yaml points to it. Overrides supplied for a task take priority. Permanent changes require a reviewable diff and explicit user approval.

