#!/bin/zsh
wallpaper_dir=$1
monitor=$2
option=$3
entries=$(ls $wallpaper_dir)
 
selected=$(printf '%s\n' $entries | wofi --show dmenu awk '{print tolower($1)}')
 
case $selected in
        *.jpg|*.png|*.jpeg)
		swaybg -o $monitor -i $wallpaper_dir/$selected -m $option ;;
esac
