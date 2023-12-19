#!/bin/zsh
entries=$(ls $HOME/Wallpapers)
 
selected=$(printf '%s\n' $entries | rofi -dmenu awk '{print tolower($1)}')
 
case $selected in
        *.jpg|*.png|*.jpeg)
		hyprctl hyprpaper unload all &&
		hyprctl hyprpaper preload $HOME/Wallpapers/$selected &&
		hyprctl hyprpaper wallpaper eDP-1,$HOME/Wallpapers/$selected ;;
esac
