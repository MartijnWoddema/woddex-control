#!/bin/bash
# Shared functions voor tmux scripts
# Gebaseerd op je eigen workflow

# Kleuren voor output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Print een header
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BLUE}$1${RESET}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
}

# Kill processen op opgegeven poorten
kill_ports() {
    local ports=("$@")
    if [ ${#ports[@]} -eq 0 ]; then
        return 0
    fi
    
    for port in "${ports[@]}"; do
        local pid=$(lsof -ti:"$port" 2>/dev/null)
        if [ -n "$pid" ]; then
            echo -e "${YELLOW}🔌 Killing proces op poort $port (PID: $pid)${RESET}"
            kill -9 "$pid" 2>/dev/null
        fi
    done
}

# Maak een tmux sessie aan met meerdere commando's
# Gebruik: create_tmux_session "session_name" "command1" "command2" ...
create_tmux_session() {
    local session_name="$1"
    shift
    
    if [ -z "$session_name" ]; then
        echo -e "${RED}❌ Geen sessienaam opgegeven${RESET}" >&2
        return 1
    fi
    
    # Controleer of sessie al bestaat
    if tmux has-session -t "$session_name" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Sessie '$session_name' bestaat al${RESET}"
        return 0
    fi
    
    # Maak nieuwe sessie met eerste commando
    local first_cmd="$1"
    shift
    
    if [ -n "$first_cmd" ]; then
        tmux new-session -d -s "$session_name" -n "main" "$first_cmd"
    else
        tmux new-session -d -s "$session_name"
    fi
    
    # Voeg extra windows/panes toe voor resterende commando's
    local window_num=1
    for cmd in "$@"; do
        if [ "$cmd" != "true" ]; then
            tmux new-window -t "$session_name" -n "cmd$window_num" "$cmd"
            window_num=$((window_num + 1))
        fi
    done
    
    # Focus op eerste window
    tmux select-window -t "$session_name:0"
    
    echo -e "${GREEN}✅ Tmux sessie '$session_name' aangemaakt${RESET}"
    return 0
}

# Kill een tmux sessie
kill_tmux_session() {
    local session_name="$1"
    
    if [ -z "$session_name" ]; then
        echo -e "${RED}❌ Geen sessienaam opgegeven${RESET}" >&2
        return 1
    fi
    
    if tmux has-session -t "$session_name" 2>/dev/null; then
        echo -e "${YELLOW}🧱 Killing tmux sessie '$session_name'${RESET}"
        tmux kill-session -t "$session_name"
        echo -e "${GREEN}✅ Sessie '$session_name' beëindigd${RESET}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Sessie '$session_name' bestaat niet${RESET}"
        return 0
    fi
}

# Cleanup zombie processen (Angular Console, Nx watchers, etc.)
cleanup_zombie_processes() {
    echo -e "${YELLOW}🧹 Cleaning up zombie processen...${RESET}"
    
    # Kill Angular dev server processen
    pkill -f "ng serve" 2>/dev/null
    pkill -f "nx serve" 2>/dev/null
    pkill -f "nx run.*:serve" 2>/dev/null
    
    # Kill node watchers
    pkill -f "node.*watch" 2>/dev/null
    
    echo -e "${GREEN}✅ Cleanup voltooid${RESET}"
}

