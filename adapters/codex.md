# Codex adapter

Documentation checked 2026-11-15; runtime installation and invocation remain unexecuted.

For project use, copy the **extracted public release folder** to `<project>/.agents/skills/write-like-me/`. Keep `SKILL.md` at that directory's root and retain its relative references. Do not copy the working repository wholesale: it may contain ignored private samples. Do not merge over an existing skill without reviewing the differences.

Current [official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills) lists repository `.agents/skills` and user `~/.agents/skills` locations. This repository has not installed either. Prefer project scope when explicitly installing for one project.

Invoke with a task such as:

```text
$write-like-me
Minimally edit the supplied email for the stated recipient.
Use the approved email profile; preserve every factual claim and quoted span.
Return the email, then unresolved factual questions only.
```

Read [SKILL.md](../SKILL.md) and follow its relevant workflow. Use local helpers only for the checks they implement; never call a preservation report semantic proof. Keep `private/` out of the installed release, file uploads, version control, and prompts unless specific sharing is separately authorized.

Before relying on an installation, verify discovery, explicit invocation, relative-reference loading, one normal task, and one protected-content task in the installed version. Selection based on a description can vary. The [universal text adapter](universal.md) works when native skill loading is unavailable.

