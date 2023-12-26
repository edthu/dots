#!/bin/bash
#


entries="Log_Out Lock Reboot Shutdown"

selected=$(printf '%s\n' $entries | wofi --show dmenu --conf=$HOME/.config/wofi/power_menu_config --style=$HOME/.config/wofi/power_menu_style.css awk '{print tolower($1)}')

case $selected in
	Log_Out)
		pkill -SIGKILL -u eax ;;
	Reboot)
		reboot ;;
	Shutdown)
		systemctl poweroff ;;
    Lock)
		playerctl pause &&
		swaylock -F -C $HOME/.config/swaylock/config ;;
esac
