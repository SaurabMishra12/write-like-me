# ChatGPT and Custom GPT adapter

Documentation checked 2026-11-15; no GPT created, uploads made, or retrieval/runtime checks executed.

## Manual conversation route

Use the [universal instruction and task block](universal.md). Paste the approved derived profile and relevant task material into the conversation, or attach a small public reference selection if the selected experience supports it. Do not upload the private corpus, local source locators, account identifiers, or the raw working repository.

[Official OpenAI guidance](https://learn.chatgpt.com/docs/use-chatgpt) recommends supplying context that changes the result. Prefer `SKILL.md`, the relevant profile, the selected workflow, and only the role/reference text needed for that task. State missing file/tool access honestly; do not pretend a model executed local scripts.

## Custom GPT route

The [official comparison](https://learn.chatgpt.com/docs/migrate-custom-gpts) distinguishes behavioral **instructions**, uploaded **knowledge**, and enabled capabilities. If explicitly creating a GPT:

1. Put the universal instruction plus the operative workflow rules in its Instructions field.
2. Add only the approved public derived profile and a small relevant reference set as Knowledge. Keep instructions that must govern behavior in Instructions rather than trusting retrieval.
3. Select the GPT explicitly and test it on familiar work. Ask it to identify the profile and relevant rule it used, then verify the actual result.
4. Test protected quotations, numbers, negation, and conclusions; inspect whether changed prose retains meaning.

Uploads have file-count, file-size, processing, and context constraints, and successful upload does not guarantee every passage is retrieved. **Numeric Custom GPT upload limits were not established by the official pages reviewed here.** Check the current builder and account documentation before choosing files; do not apply unrelated API upload limits to a GPT. If required material does not fit or cannot be retrieved, narrow the reference set, paste the relevant section directly, or use the local workflow. No “upload the ZIP and everything works” claim is made.

Current [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) also describes native ChatGPT skills and plugin distribution on supported surfaces. This manual adapter is a separate route; uploading `SKILL.md` as knowledge is not demonstrated to install a native skill. No plugin publication, native skill installation, private corpus transfer, or universal account availability is implied.

