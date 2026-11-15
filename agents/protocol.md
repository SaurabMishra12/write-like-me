# Shared editorial protocol

One coordinator owns the draft and one frozen voice profile. Use a shared ledger with intent, audience, purpose, immutable facts, original claim spans, evidence sources, uncertainty and desired reader action. All roles receive that ledger and only relevant source excerpts. Private data stays local unless the user authorizes a particular model transfer.

The Voice Analyst, Researcher and Audience Analyst may inspect independently. Authenticity review establishes the argument ledger. Structural and Language Editors propose local patches. The coordinator composes one candidate, then the Factual Guardian checks exact spans and semantics. The Final Auditor evaluates only that candidate with the seven reports. A veto blocks delivery; the coordinator reverts the offending patch and reruns affected reviews. No role can “improve” a result, claim, equation or experience.

Report schema (JSON):

```json
{"role":"factual-guardian","profile_version":"0.1.0","issues":[{"severity":"veto","original_span":"...","candidate_span":"...","claim_id":"claim-1","reason":"...","evidence_source":"...","confidence":"high"}],"proposed_patches":[],"unresolved_checks":[],"rewrite_performed":false}
```

Use severity advisory, review or veto. Empty issues mean none detected in the stated scope, not proof of truth. Missing inputs remain in unresolved_checks. Never fabricate issue evidence, a passed review, user approval, or independent-agent execution. An audit log records actual role invocations/review mode, draft hashes, rule version, tool results, decisions and unresolved risks without copying secrets. The local engine returns review_required on changed prose; a real semantic reviewer must separately compare the meaning before accepting the proposal. For high-stakes conclusions, the user reviews every truth-affecting change.

