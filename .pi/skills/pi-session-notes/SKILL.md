---
name: pi-session-notes
description: >
  Save daily session notes from the current Pi conversation to /home/dave/sync/Obsidian/AI.
  Creates a subfolder named after the active model (derived from PI_MODEL). Files follow
  YYYY-MM-DD.md naming, one file per day, with each session appended as its own section.
  Use when user says "save session notes", "note this in Obsidian", "session notes to
  obsidian", or at end of a substantial work session when the user asks for notes.
---

Save current Pi session notes into the Obsidian vault `AI` folder, next to Claude_Code / Gemini_Code exports.

## Persisted output: normal prose only

These files leave in-session context. Do not use compressed styles (caveman, summaries with dropped articles). Write clear technical prose. Code blocks, commands, and error strings stay exact.

## Placement rule

Root: `/home/dave/sync/Obsidian/AI/`

1. **Model subfolder** — derive folder name from `PI_MODEL` env var (read via `printenv PI_MODEL`, e.g. `hf.co/hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q4_K_M`).
   - Strip provider path prefix (`provider/` or any leading segment before the model ID).
   - Drop revision tag after last colon if present.
   - Sanitize: replace everything outside `[A-Za-z0-9._-]` with `-`, collapse repeats, trim ends. Examples: `Qwen3.8-27B-GGUF`, `claude-opus-4-1`, `gemini-2-5-pro`.
   - Folder = `<Model>/<revision>` if revision present (e.g. `Qwen3.8-27B-GGUF/UD-Q4_K_M`), else just model name. `mkdir -p`.
   **Same session = same folder.** If the user switches models mid-session, append to whichever file the work was written under; when ambiguous pick current derived model and note the switch in the section header frontmatter block of that section if relevant.

## File naming (per day, one file)

File: `<Model Folder>/YYYY-MM-DD.md` — local date via `date +%F`. One file per calendar day. If exists, append new session section; do not rewrite or reorder existing content unless user explicitly asks to fix it.

Filename example: `/home/dave/sync/Obsidian/AI/Qwen3.8-27B-GGUF/UD-Q4_K_M/2026-09-05.md`

## Daily file structure

First time a day's file is created, start with this header (frontmatter mirrors Claude_Code conventions):

```markdown
---
date: 2026-09-05
tags: [session-notes, pi]
model: Qwen3.8-27B-GGUF/UD-Q4_K_M
provider: ollama            # from PI_PROVIDER env var
---

# Session Notes — 2026-09-05
```

`tags:` may grow with topic tags as content justifies (e.g. `nixconfig`, `vault`). Keep model/provider accurate to the session that wrote them; if a single day spans models, add one section per switch and note it in the header line of each appended session.

## Session section format (append this per session)

```markdown
---
# Session HH:MM — <short topic slug in title case>

**Started**: <approx start time + TZ> &nbsp; **Model**: `<PI_MODEL value>` 
**Session ID**: `<PI_SESSION_ID>`

## Summary
<2-5 sentence plain-language recap of what the session accomplished and why it matters. Include host/context if relevant (Big-Nix, Consus, nixconfig repo, etc.).>

## Key Decisions & Findings
- <bullet: decision made + one-line rationale — or discovery worth keeping>
- <only items actually made/found in this conversation; do not invent>

## Work Performed
Group by area, each entry = what changed / what was run. Bullet per meaningful unit (each file edited or command series counts as one bullet, not per line diff):
- `<path>`: <what changed + why>
- ran `<cmd>` — <observed outcome, 1 clause max>

## Commands Worth Keeping
Only include non-obvious commands the user would want to rerun (not routine ls/cd/cat). Code fence bash. If nothing qualifies, omit this section entirely.

## Unresolved / Next Time
Omit if none remain. Otherwise bullets (blocked by X, Y left for Z reason) — one line each.
```

Replace `---` separator block above the H2 title with a real markdown horizontal rule at append time only if it reads as clean in Obsidian; otherwise keep a blank-line separation between sections. Do not literally write `---` separators before H2s (interior `---` produces unwanted thematic-break semantics and frontmatter-like confusion); use just the heading plus one lead-in paragraph instead. The block above is structural guidance, not literal text.

## How to capture facts

Use only what actually happened in this conversation:
- Files read/edited and the why (paths exact, relative to their repo root where obvious — if nixconfig work use repo-relative like `modules/system/samba.nix`; include host name when multiple hosts touched).
- Non-trivial commands + outcome. Skip exploratory one-liners that yielded nothing new.
- Errors observed + how resolved (exact error string, 1-line context of cause).
- User preferences/corrections stated this session (they are durable cross-session facts too — also consider `memory:` tool for those; notes file is a log, memory tool is the retrieval layer).

Do NOT include secrets, tokens, passwords from commands seen in the conversation. Redact inline (`<redacted>`) if you must quote a command containing credentials.

## Invocation workflow (deterministic steps)

1. `printenv PI_MODEL PI_PROVIDER PI_SESSION_ID && date -Iseconds` — note values; derive Model Folder + revision per rule above.
2. `mkdir -p "/home/dave/sync/Obsidian/AI/<Model Folder>"`.
3. If daily file exists: read it (it is short, at most a few KB for one day) and confirm current date/time context matches before appending, to avoid double-writing the same section on retry after partial success — if you see an incomplete trailing `# Session HH` heading from this session started earlier, replace that tail instead of appending twice.
4. Draft the section per format above (normal prose regardless of any active compressed-style skill).
5. Append: use `edit` by matching EOF sentinel if it exists; safest general approach is read full file then `write` entire content + new section, since daily files stay small (few hundred lines max realistically). Prefer edit-with-unique-tail-anchor over whole-file rewrite when the last-line anchor is short and clearly unique to this append.
6. Confirm: print final path only (`/home/dave/sync/Obsidian/AI/<Model Folder>/YYYY-MM-DD.md`), single line, no summary-dump duplication of what you already wrote in the answer — unless user asked for the notes content back too (then show it).

## Boundaries with existing folders

- Do not touch `Claude_Chats`, `Claude_Code`, `Gemini_Chats`, or any pre-existing non-model folders. This skill only writes under its derived Model Folder.
- Different from nixconfig docs: notes capture the *session/decisions/commands*; anything that belongs in repo-local README/docs (e.g. new module usage) still goes there — do NOT copy session-note prose into `~/nixconfig` or flag it as "should be documented" instead of actually writing to both places if user asked for docs too, and when asked write normal full-prose docs there regardless of skill scope.
