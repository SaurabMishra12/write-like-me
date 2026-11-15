# Claude Code adapter

Documentation checked 2026-11-15; runtime installation and invocation remain unexecuted.

Copy the **extracted public release folder** to `<project>/.claude/skills/write-like-me/`, preserving `SKILL.md` and all relative references. Copy a release rather than a raw working checkout containing ignored private samples. Inspect an existing destination before any replacement.

The [official Claude Code guide](https://code.claude.com/docs/en/skills) documents project `.claude/skills` and personal `~/.claude/skills`. No global installation is performed here. Invoke explicitly:

```text
/write-like-me
Revise the supplied paragraph using the approved academic profile.
Preserve citations, equations, uncertainty, and the strength of the conclusion.
Identify unresolved evidence gaps without inventing fixes.
```

Follow [SKILL.md](../SKILL.md). Keep one draft and shared review ledger; use the role descriptions as perspectives even when no subagent feature is available. Claude-specific frontmatter controls are optional adapter concerns and should not replace the portable standard fields.

Verify discovery and actual reference access in the installed host, then exercise an ordinary task and a protected-content task. Local tool permission and availability depend on host settings; an installed folder does not establish that checks ran. Do not upload `private/` or alter the permanent profile without the workflow's evidence review and explicit user approval. Use [the universal adapter](universal.md) when filesystem skills are unavailable.

