#!/bin/bash
# Script om te verbinden met een tmux sessie in de juiste terminal emulator

SESSION_NAME="$1"

if [ -z "$SESSION_NAME" ]; then
    echo "Gebruik: $0 <session_name>" >&2
    exit 1
fi

# Controleer of sessie bestaat
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Sessie '$SESSION_NAME' bestaat niet" >&2
    exit 1
fi

# Detecteer terminal emulator (prioriteit: kitty > alacritty > foot > gnome-terminal > xterm)
if command -v kitty &> /dev/null; then
    kitty tmux attach-session -t "$SESSION_NAME" &
elif command -v alacritty &> /dev/null; then
    alacritty -e tmux attach-session -t "$SESSION_NAME" &
elif command -v foot &> /dev/null; then
    foot tmux attach-session -t "$SESSION_NAME" &
elif command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- tmux attach-session -t "$SESSION_NAME" &
elif command -v xterm &> /dev/null; then
    xterm -e tmux attach-session -t "$SESSION_NAME" &
else
    # Fallback: gebruik standaard terminal
    tmux attach-session -t "$SESSION_NAME"
fi

exit 0

