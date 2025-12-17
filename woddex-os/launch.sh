#!/bin/bash
# Launcher script voor de Tmux Sessie Manager

# Ga naar de applicatie directory
cd ~/dev/apps/woddex-os || exit 1

# Activeer de virtual environment als die bestaat
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Gebruik python3 expliciet
PYTHON_CMD=$(which python3 2>/dev/null || which python 2>/dev/null)

if [ -z "$PYTHON_CMD" ]; then
    notify-send "Tmux Manager" "Python niet gevonden!" -u critical 2>/dev/null || true
    exit 1
fi

# Controleer of PySide6 geïnstalleerd is
if ! $PYTHON_CMD -c "import PySide6" 2>/dev/null; then
    notify-send "Tmux Manager" "PySide6 niet geïnstalleerd!\nInstalleer met: pip install PySide6" -u critical 2>/dev/null || true
    exit 1
fi

# Start de applicatie (in achtergrond zodat Hyprland niet blokkeert)
$PYTHON_CMD main.py &
