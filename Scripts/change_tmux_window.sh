#!/bin/bash

switch_window() {
    local window_number=$1
    if tmux has-session 2>/dev/null; then
        tmux select-window -t :$window_number
    else
        echo "No tmux session found. Starting a new session..."
        tmux new-session -d
        tmux select-window -t :$window_number
        tmux attach-session -d
    fi
}

case "$1" in
    1) switch_window 1 ;;
    2) switch_window 2 ;;
    3) switch_window 3 ;;
    *) echo "Usage: $0 {1|2|3}" ;;
esac
