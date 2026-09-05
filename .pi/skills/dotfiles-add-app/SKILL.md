---
name: dotfiles-add-app
description: >
  Workflow for adding a new application's config to this repo and wiring it into home-manager. Use when asked to "add X" / "track another app", or when an existing .config dir is modified but never shows up on disk because no symlink line exists yet.
---

# Dotfiles add-app workflow

Root: `/home/dave/dotfiles` (content) + `~/nixconfig/home/dave/default.nix` (links). Two halves required: the config files must exist here, AND a matching home.file entry in nixconfig must reference them — one without the other does nothing.

## Steps

1. Check whether it already exists / is symlinked somewhere else, e.g.:
   bash: grep -n 'dotfiles' ~/nixconfig/home/dave/default.nix | grep <app>
   If present, skip ahead and just mention what's there.
2. mkdir .config/<app> (or copy the app's default config in if it needs one).
3. Create/seed the actual config file(s) — start from the app's documented defaults, don't invent keys.
4. In ~/nixconfig/home/dave/default.nix, inside home.file, add (alphabetically next to the others):
   \`\`\`nix
   ".config/<app>".source = config.lib.file.mkOutOfStoreSymlink "${dotfilesDir}/.config/<app>";
   \`\`\`
5. Rebuild: home-manager rebuild --flake ~/nixconfig#dave@Big-Nix  (confirm the correct attr path with the user first if unsure; osConfig/Big-Nix host name is used for other multi-host branching there).
6. Verify: readlink ~/.config/<app> points at /home/dave/dotfiles/.config/<app>, and run the app's basic startup once to catch syntax errors immediately while we can still fix them cheaply.

## Gotchas

- Symlinking a directory that also holds user-generated runtime state (e.g. a cache dir) will get blown away on rollback/rebuild — check the app docs; if it has a data dir, only symlink the config subfile, not the whole folder, or exclude via home.file subpath instead of .source.
- Do NOT add the mkOutOfStoreSymlink for apps that are purely package-managed with no own dotfiles (e.g. some programs keep all state in XDG_DATA_HOME); ask first if unclear which bucket an app is in before creating a link.
