#!/usr/bin/env bash

NOTE_FILE="$HOME/notes/scratchpad.md"

scratch_win=$(niri msg --json windows | jq -r '.[] | select(.app_id == "scratchpad") | "\(.id) \(.is_focused)"' 2>/dev/null | head -n1)

if [ -z "$scratch_win" ]; then
    alacritty --class scratchpad -e nvim "$NOTE_FILE" &
else
    win_id=$(echo "$scratch_win" | awk '{print $1}')
    is_focused=$(echo "$scratch_win" | awk '{print $2}')
    if [ "$is_focused" = "true" ]; then
        niri msg action close-window --id "$win_id"
    else
        niri msg action focus-window --id "$win_id"
    fi
fi
