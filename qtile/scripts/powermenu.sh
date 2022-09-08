#! /bin/sh

chosen=$(printf "  Power Off\n  Restart\n  Lock" | rofi -dmenu -i -theme-str '@import "~/.config/qtile/scripts/power.rasi"')

case "$chosen" in
	" ") poweroff ;;
	" ") reboot ;;
	"") slock ;;
	*) exit 1 ;;
esac
