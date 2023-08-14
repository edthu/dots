#!/bin/bash

# Set the directory path
dir="$HOME/Wallpapers"

# Get all image files in the directory
images=$(find "$dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))

# Launch wofi with the images as entries
wofi --show dmenu --allow-images --cache-file /tmp/wofi-cache <<< "$images"

