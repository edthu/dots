#!/bin/zsh
wallpaper_dir=$HOME/Wallpapers
entries=$(ls $wallpaper_dir)
 
selected=$(printf '%s\n' $entries | wofi --show dmenu awk '{print tolower($1)}')
 
case $selected in
        *.jpg|*.png|*.jpeg)
		swaybg -i $wallpaper_dir/$selected -m fill
esac
