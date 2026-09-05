---
name: cleanup-audit
description: >
  Dead-config and junk audit for this dotfiles repo. Finds leftover window-manager configs that are no
  longer in use, untracked cruft (backup files, caches), tracked build artifacts (__pycache__, logs), and
  orphans not wired into home-manager. Use when asked to "clean up", "prune", "remove dead config", or for
  a periodic repo health check.
---

# Dotfiles Cleanup Audit

Goal: surface (1) configs that belong to WMs/apps no longer used, (2) files that should be untracked,
(3) tracked artifacts that shouldn't be in git. **Report before deleting anything** — this is an audit
skill; only act after the user approves each class of change individually.

## 1. Dead window-manager configs

The current stack is **niri + hyprland**; check which are actually enabled before touching anything:

- `grep -rn 'programs\.\(bspwm\|hyprland\|sway\|qtile\)\?' ~/nixconfig/hosts/*/configuration.nix`
  (also any imported modules) to see what home-manager/NixOS enables. niri may be enabled via a module — search `modules/nixos/desktop*`.
- Candidates known to be likely-dead: entire `.config/bspwm`, `.config/sxhkd` (bspwm's BDK),
  `.config/qtile` + its __pycache__, polybar if waybar is the only bar in use (`ls .config/polybar` vs grep for `exec.*polybar\|waybar` across all WMs' configs).
- Confirm before declaring dead: grep every *active* config for references (e.g. a hyprland autostart launching polybar means it's alive, even if bspwm is not).

## 2. Untracked cruft in the working tree

```bash
git status --porcelain=v1 | grep '^??'   # untracked — scratch notes, *.bak, .migrate.bak files
find . -name '*.bak' -o -name '*-backup-*' -o -name '~' 2>/dev/null
```
Report each hit; do not batch-delete without listing and confirming.

## 3. Tracked artifacts that should be gitignored

The repo currently has NO `.gitignore` and DOES track, e.g.:

- `__pycache__/*.pyc` under `.config/qtile/` (multiple Python versions)
- `.nvimlog`, top-level log/build residue

Proposed fix pattern:
1. Add a minimal root `.gitignore`: `__pycache__/`, `*.pyc`, `*.bak`, `.vscode/settings.local.json`, scratch log files by name.
2. Remove from index without touching disk for things that will keep being regenerated:
   ```bash
   git rm -r --cached .config/qtile/__pycache__
   git add -A && git commit  # split? one logical change per user preference (see .pi/skills/git-commit)
   ```

## 4. Orphan directories not linked from home-manager

```bash
comm -23 <(ls .config/) <(grep -oP '(?<=source.*"dotfilesDir}/\.config/)[a-z0-9_-]+' ~/nixconfig/home/dave/default.nix | sort -u)
```
Anything here is present but not symlinked: either wire it in via the dotfiles-add-app skill or decide to remove. Report both options per hit.

## Reporting format

Summarize by category with a **proposed action line** (delete / gitignore+untrack / wire-in), nothing executed until the user signs off on each bucket. Then hand off execution to `.pi/skills/git-commit` for the commit/push phase — that skill also appends Obsidian session notes per its step 6.
