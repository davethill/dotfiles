---
name: git-commit
description: >
  Git commit-and-push workflow for /home/dave/dotfiles. Use when the user asks to "commit",
  "commit and push", "push changes", or wants the working tree tidied up — checks git status/diff,
  stages relevant changes, writes a descriptive commit message, commits, and pushes to origin.
---

# Git Commit & Push Workflow

Root: `/home/dave/dotfiles` (dotfiles repo; everything lives under `.config/<app>/`).

## Procedure

1. **Inspect first, always** — never stage blindly:
```bash
git status --porcelain=v1
git diff
git diff --staged   # in case something is already staged from before
```

2. **Decide what to stage.** Stage only the files that are part of the change being committed:
```bash
git add <specific-paths>     # preferred, usually .config/<app>/...
# git add -A                # only when every unstaged file genuinely belongs to this commit
```
   - Skip anything that looks accidental (scratch notes, editor swap files, backup/bak files like `*.migrate.bak`, untracked debug output). If unsure whether an untracked file should be committed, ask the user.
   - Never stage credentials, secrets, or local-only config.

3. **Write the commit message.** Conventional-commit style, imperative mood:
   ```
   <type>(<scope>): <summary under ~72 chars>

   Optional body explaining why. Types: feat|fix|refactor|docs|test|chore
   Scope is the app/config area, e.g. niri | hypr | waybar | rofi | kitty (omit if multi-area).
   ```

4. **Commit and push:**
```bash
git commit -m "<message>"          # use a heredoc via $'...' or git commit -F for bodies
git push                           # assumes current branch has an upstream; push -u origin <branch> on new branches
```
   If the push fails due to remote changes, run `git pull --rebase` and re-inspect before retrying — never force-push.

5. **Report back**: show the resulting subjects with `git log -1 --oneline` and confirm push status (`git status`).

6. **Save session notes** — after a successful push (or if there was nothing to commit but real work happened this session), load `.pi/skills/pi-session-notes/SKILL.md` (relative to the repo root) with the read tool and follow its invocation workflow: append today's section to the Obsidian daily file, summarizing what was committed (files touched, why, notable commands/fixes). Use normal prose per that skill. Then finish by printing only the notes path as a final line.

## Rules

- One logical change per commit unless the user asks otherwise; if the diff mixes concerns, split into multiple commits or ask which should go together.
- If there is nothing to commit (clean tree), say so — don't invent a commit.
- Amending/rewriting existing pushed history: stop and confirm with the user first.
