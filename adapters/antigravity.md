# Google Antigravity adapter

Documentation checked 2026-11-15; App, CLI, and IDE runtime behavior remain unexecuted.

For a project, copy the **extracted public release folder** to `<project>/.agents/skills/write-like-me/`. Keep the whole reference tree and check an existing destination before replacing it. Do not copy the raw working tree or private samples.

The current [official skills guide](https://antigravity.google/docs/skills) uses `.agents/skills` by default and retains legacy `.agent/skills` compatibility. Its common global location is `~/.gemini/config/skills/`; additional CLI/legacy paths differ by surface. This repository performs no global installation.

The App documents explicit slash invocation and the CLI converts skills into commands. For example:

```text
/write-like-me
Turn the supplied notes into technical documentation for this audience.
Use only verified commands and settings; flag missing procedural details.
Preserve all code, names, units, and factual conditions.
```

Follow [SKILL.md](../SKILL.md), its chosen workflow, and the relevant profile. A description-based match does not demonstrate that the intended references were read. Verify the active skill and one task requiring a protected span in the installed version. Do not imply Python helpers ran when the host lacks tool access. If loading differs in the installed release, use [the universal text adapter](universal.md) and consult [platform support notes](../research/platform-support.md).

