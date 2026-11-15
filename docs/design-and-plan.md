# Design and execution plan

The supplied ten-phase brief authorizes research, implementation, and evaluation. Implementation follows the completed source audit and research files. Alternatives considered: a monolithic prompt is cheap but difficult to audit; a hosted training service adds data movement and unapproved inference costs. Use a local Agent Skills bundle with a host-model editorial workflow and deterministic audit helpers.

## Boundaries

The Python code measures visible surface properties and exact preservation. It cannot prove semantic equivalence, scientific truth, grammaticality, or personal authenticity. Modified prose needs explicit semantic review; exact token matches cannot clear that review. The factual guardian vetoes detected changes to protected content. Role specifications form one shared ledger and one writer, never eight competing rewrites.

## Execution tasks

1. Research: separate A/P from B/C/D/E, record access and genre gaps, verify canon and scholarly findings. Freeze profiles before held-out evaluation.
2. Tests before implementation: numbers/dates/names/math/citations/code/negation, minimal-edit threshold, Unicode and empty input, false-positive word cases, provenance and group leakage.
3. Tools: implement style metrics, contextual editorial audit, preservation check, revision comparison; local corpus validation/profile proposal; route and review CLI. Each command emits JSON and nonzero error status where appropriate, never silently edits source.
4. Instructions: progressive-loading SKILL.md, eight review roles, six genre workflows, five adapters, source-linked platform notes, human-editable profile.
5. Evaluation: genuine held-out A/P and separate synthetic engineering fixtures; generate B ordinary, C generic polish, D skill-assisted with recorded provenance; blind comparison protocol and measured preservation. Report missing human/independent platform evaluation explicitly.
6. Distribution: exclude private samples and secrets, validate frontmatter and local links, run pytest and CLI examples, produce checksum manifest and a portable ZIP.

## Review focus

- A changed conclusion can preserve all numbers: any changed prose remains review-required.
- Protected forms include Markdown references, multiline LaTeX, dollar escapes, URLs and code fences.
- Sentence starts are not reliable proper-name detection: explicit protected spans are supported and name detection remains qualified.
- Never learn the personal profile from AI-written briefs, constructed examples or held-out tasks.
- No observed dialect marker licenses invented Hindi transfer or grammatical errors.

No global installation or external publishing is performed by building this repository. Runtime support outside this host is documented, not claimed tested.

