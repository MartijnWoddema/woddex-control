#!/usr/bin/env bash
set -u

# Script om een nieuwe tmux sessie aan te maken
# Optioneel met meerdere commando's (zoals je start-hakon.sh)

SESSION_NAME="$1"
COMMANDS=()

# Parse optionele commando's
shift 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    COMMANDS+=("$1")
    shift
done

if [ -z "$SESSION_NAME" ]; then
    echo "Gebruik: $0 <session_name> [command1] [command2] ..." >&2
    echo "Voorbeeld: $0 my-session 'npm start' 'npm run watch'" >&2
    exit 1
fi

# Source shared functions als die bestaan
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.scripts-common.sh" ]; then
    source "${SCRIPT_DIR}/.scripts-common.sh"
    
    # Gebruik shared function als er commando's zijn
    if [ ${#COMMANDS[@]} -gt 0 ]; then
        create_tmux_session "$SESSION_NAME" "${COMMANDS[@]}"
    else
        # Simpele sessie zonder commando's
        create_tmux_session "$SESSION_NAME" ""
    fi
    
    exit $?
else
    # Fallback: gebruik basis functionaliteit
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "Sessie '$SESSION_NAME' bestaat al" >&2
        exit 1
    fi
    
    if [ ${#COMMANDS[@]} -gt 0 ]; then
        # Maak sessie met eerste commando
        tmux new-session -d -s "$SESSION_NAME" "${COMMANDS[0]}"
        
        # Voeg extra windows toe voor andere commando's
        for i in "${!COMMANDS[@]}"; do
            if [ $i -gt 0 ] && [ "${COMMANDS[$i]}" != "true" ]; then
                tmux new-window -t "$SESSION_NAME" "${COMMANDS[$i]}"
            fi
        done
    else
        # Maak simpele sessie
        tmux new-session -d -s "$SESSION_NAME"
    fi
    
    if [ $? -eq 0 ]; then
        echo "Sessie '$SESSION_NAME' is aangemaakt"
        exit 0
    else
        echo "Fout bij aanmaken van sessie" >&2
        exit 1
    fi
fi

