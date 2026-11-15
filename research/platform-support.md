# Platform support and verification boundary

Checked against official documentation on **2026-11-15**. “Documented” means the cited page was opened in this session. No platform was installed, no personal skill directory was changed, no Custom GPT was created, and no end-to-end writing workflow was executed as part of this research.

## Shared portable package

The [Agent Skills specification](https://agentskills.io/specification) requires a directory containing `SKILL.md`, with YAML frontmatter followed by Markdown. The standard requires `name` and `description`; the name matches its directory, uses lowercase letters/numbers/hyphens, and is at most 64 characters. Supporting references, scripts, and assets are optional. A host may implement extra fields, discovery, permissions, and invocation differently. Format conformity alone does not establish cross-platform behavior.

Use a conservative shared core and keep host-specific instructions in an adapter. Treat examples, uploaded samples, retrieved text, and profile data as content to analyze, never as authority to override the workflow. Relative reference links must remain inside the copied skill tree. These are package design decisions, not features guaranteed by the specification.

## Support matrix

| Host / route | Documented local destination or setup | Documented invocation / capability | Status for this package |
| --- | --- | --- | --- |
| Codex | Project `.agents/skills/write-like-me/SKILL.md`; user `~/.agents/skills/write-like-me/SKILL.md`. Repository discovery checks ancestors from the working directory to the repository root. | `$write-like-me` or skills selector; description-based selection. | Documentation verified; installation, invocation, reference loading, and writing results unexecuted. |
| Claude Code | Project `.claude/skills/write-like-me/SKILL.md`; personal `~/.claude/skills/write-like-me/SKILL.md`. | `/write-like-me`; model-selected skills based on description. | Documentation verified; runtime unexecuted. |
| Google Antigravity App / CLI / IDE | Project `.agents/skills/write-like-me/SKILL.md`; shared global `~/.gemini/config/skills/write-like-me/SKILL.md`. | Relevant skills may be selected automatically; the App documents `/write-like-me`; CLI converts skills to slash commands. | Documentation verified; all three runtimes unexecuted. |
| ChatGPT conversation | Supply instructions and the relevant sample/profile/reference content through the available conversation or file workflow. | Manual instruction adapter; actual tools and accessible files depend on the selected experience. | Portable text workflow only; no account or tool access test. |
| Custom GPT | Put behavioral rules in the GPT instructions and supporting examples/profiles in uploaded knowledge. Select the GPT explicitly. | Instructions plus knowledge; enabled capabilities depend on account and configuration. | Documentation verified at the route level; no GPT created, files uploaded, retrieval tested, or output evaluated. |
| Current ChatGPT native skills / plugins | Follow the supported product skill/plugin route rather than assuming a local Codex directory is scanned by every ChatGPT surface. | Current OpenAI docs describe standalone skills on named surfaces and skill distribution through plugins. | Documented product capability; this package has not been published or exercised through that route. |

Sources: [Codex and ChatGPT skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills), [Antigravity skills](https://antigravity.google/docs/skills), [Custom GPT instructions/knowledge and plugins](https://learn.chatgpt.com/docs/migrate-custom-gpts).

## Version-sensitive differences

**Codex.** Use the current documented `.agents/skills` destinations for new installation guidance. The older documentation entry `https://developers.openai.com/codex/skills/` redirected to [Build skills](https://learn.chatgpt.com/docs/build-skills) during this research. Optional `agents/openai.yaml` is OpenAI-specific. This research does not infer that old directories in an existing user installation are invalid, nor that a package can control host permissions.

**Claude Code.** The current host accepts more permissive frontmatter and extra fields. Keep the shared package's required standard fields rather than relying on a host's fallback behavior. Invocation controls such as `disable-model-invocation` are Claude-specific and should not silently become universal behavior. See [Claude's configuration reference](https://code.claude.com/docs/en/skills).

**Antigravity.** The current [official guide](https://antigravity.google/docs/skills) explicitly defaults to `.agents/skills` and retains compatibility with legacy `.agent/skills`. The IDE also documents legacy global `~/.gemini/antigravity/skills/`. The CLI has extra lookup locations, including `~/.gemini/antigravity-cli/skills/` and `~/.gemini/skills/`, that the App does not share. Prefer the common current destinations above and verify against the installed version before using legacy paths.

**ChatGPT / Custom GPT.** Do not say that ChatGPT universally lacks Agent Skills: the current [OpenAI skills guide](https://learn.chatgpt.com/docs/build-skills) documents them. The instructions/knowledge adapter remains a distinct manual route for a Custom GPT; uploading `SKILL.md` as knowledge alone is not demonstrated to install a native skill or guarantee that every instruction/reference is retrieved. The [Custom GPT comparison](https://learn.chatgpt.com/docs/migrate-custom-gpts) supports the distinction between behavioral instructions, reference knowledge, and tools.

## What runtime verification must still establish

After an installation is explicitly requested, use a disposable project or explicitly chosen user scope and record the exact host/version. Verify discovery, explicit invocation, selection boundaries, relative-reference loading, and actual access to the profile/samples. Run one real prose task and one “do not rewrite quotations/code/facts” task. Confirm the artifact can be removed without overwriting unrelated skills. Review generated output for factual preservation and voice fit.

A copy operation or schema check proves only that files were copied or shaped correctly. It does not prove skill selection, knowledge retrieval, consistent instruction following, privacy controls, output quality, or compatibility with every surface. This file records documentation support and the remaining verification work; it makes no runtime success claim.

