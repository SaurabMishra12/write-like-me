# Technical documentation and GitHub

Load general-profile.yaml and shared profiles. Exact utility takes priority over ornamental personal voice.

1. Identify the user task, supported environment, prerequisites, exact command/API, expected output and known failure. A README edit must not imply execution that has not occurred.
2. Protect fenced/inline code, flags, paths, API signatures, complexity, version requirements and actual behavior. Use explicit locks for identifiers the heuristic guard cannot recognize.
3. Put the actionable instruction near the relevant context. Lists are appropriate for procedures and parallel options. Give failure recovery based on actual behavior; do not invent functionality, installation tests or compatibility.
4. Remove repeated commentary if it contributes no condition or warning. Keep details needed to reproduce the operation, even if they lengthen the section.
5. Compare code and commands byte-for-byte, then semantically inspect the surrounding behavior claims. If an execution check was not run, say so.

Acceptance: following the documented instruction has a defined intended consequence, and the writing edit changes no executable content or promised behavior.

Example failure test: editing --seed 7 to --seed 8 for a smoother example. Veto.

