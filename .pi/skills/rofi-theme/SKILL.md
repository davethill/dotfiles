---
name: rofi-theme
description: >
  Guide for restyling the ddevault-style Rofi collection in .config/rofi. Explains the layering
  of @import (base → colors.rasi → styles), how scripts randomize themes, and which file to edit
  for applets / launchers / powermenu / drun. Use when asked to theme, recolor, or debug rofi output.
---

# Rofi theming (.config/rofi)

This tree is a **ddevault (Aditya Shakya)-style** collection. Every menu type works the same way; only paths differ.

## Anatomy of one menu directory

```
.config/rofi/<menu>/                    # powermenu | applets/applets | launchers/slate …
├── launcher.sh / powermenu.sh / style.sh   # entry script: picks theme + color, calls rofi
├── <layout>.rasi                         # layouts (card_square.rasi, row_circle.rasi, …)
└── styles/ (or styles/<theme>/…)
    ├── colors.rasi                       # THE color switch — one @import line at top
    └── <scheme>.rasi                     # one file per palette (@define color * definitions)
```

**Layering rule:** a layout `.rasi` `@import`s its own theme file which `@import`s
`styles/colors.rasi`; `colors.rasi` in turn `@import`s the actual scheme. To recolor anything,
**edit the one line at the top of `styles/colors.rasi` for that menu**, e.g.:

```rasi
/* @import "dark.rasi" */  →  @import "material-dark/teal.rasi"
```

Available schemes are listed in each `colors.rasi` header (material-{light,dark}/<color> plus
adapta, arc, gruvbox, nordic, berry, gotham, …). Menu-local palettes override the shared ones —
there is no global theme for rofi.

## Entry scripts do two randomizations

- `theme="card_square"` (hardcoded default) + a commented-out block that randomly picks layouts.
- A live block: `sed -i 's/@import .*/@import "<random style>/' styles/colors.rasi` — i.e. **scripts rewrite colors.rasi at runtime**. If the user complains "colors keep changing", this is why; comment out those lines to freeze a palette (the scripts say so in their headers).

## Which file drives what

| Want to change | Edit |
|---|---|
| Colors of one menu | that menu's `styles/colors.rasi` @import line, or the scheme rasi it points at |
| Layout/geometry of one menu invocation | variable + `.rasi` layout in its script dir (e.g. powermenu.sh) |
| Dropped-down app launcher (`rofi -show drun`) | `config.rasi` (+ `launchers/…` only if a custom launcher script is used; currently hyprland `Mod+D` and niri use plain `-show drun`, so themes from the `launchers/*` scripts do NOT apply there) |
| Global basics (icons, icon theme) | `.config/rofi/config.rasi` (`icon-theme: "Papirus"`) |

## Verification loop (no GUI needed in a headless shell)

```bash
# catch rasi syntax errors early:
rofi -dump-config --theme .config/rofi/powermenu/styles/colors.rasi >/dev/null; echo $?
# quick sanity render of an actual menu without picking anything:
rofi -theme .config/rofi/powermenu/card_square.rasi -show run    # then Esc
```

The GUI must be running where rofi is invoked; when testing from this agent, prefer `rofi -dump-config` validation and tell the user to hit their keybind.

## Gotchas ddevault trees keep biting people with

- Rasi has **no namespacing** — duplicate selector definitions across imported files silently overwrite each other (last import wins). Keep edits within the scheme file, don't add selectors in colors.rasi.
- Emoji-style glyphs assume a Nerd/Powerline font configured for rofi; missing icons = wrong/absent font (check `font` in the theme or config.rasi).
- Old per-applet configs (`.config/rofi/applets/configs/{circle,rounded,square}/*.rasi`) are dead weight if only the top-level applet themes ship current — verify with the launcher's theme variable before editing them.
