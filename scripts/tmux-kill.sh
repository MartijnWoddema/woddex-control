#!/usr/bin/env bash
set -u

# Script om een tmux sessie te beëindigen
# Optioneel met poort killing en cleanup

SESSION_NAME="$1"
PORTS=()

# Parse optionele poorten (--ports 4200 8000 of --ports=4200,8000)
shift 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --ports)
            shift
            while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                PORTS+=("$1")
                shift
            done
            ;;
        --ports=*)
            IFS=',' read -ra PORT_ARRAY <<< "${1#*=}"
            PORTS+=("${PORT_ARRAY[@]}")
            shift
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$SESSION_NAME" ]; then
    echo "Gebruik: $0 <session_name> [--ports port1 port2 ...]" >&2
    exit 1
fi

# Source shared functions als die bestaan
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.scripts-common.sh" ]; then
    source "${SCRIPT_DIR}/.scripts-common.sh"
    
    # Gebruik shared functions
    if [ ${#PORTS[@]} -gt 0 ]; then
        kill_ports "${PORTS[@]}"
    fi
    
    kill_tmux_session "$SESSION_NAME"
    
    # Optioneel: cleanup zombie processen
    # cleanup_zombie_processes
    
    exit 0
else
    # Fallback: gebruik basis functionaliteit
    if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo "Sessie '$SESSION_NAME' bestaat niet" >&2
        exit 1
    fi
    
    tmux kill-session -t "$SESSION_NAME"
    
    if [ $? -eq 0 ]; then
        echo "Sessie '$SESSION_NAME' is beëindigd"
        exit 0
    else
        echo "Fout bij beëindigen van sessie '$SESSION_NAME'" >&2
        exit 1
    fi
fi

