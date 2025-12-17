# PySide6 GUI Applicatie - Tmux Sessie Manager

Een moderne Python GUI-applicatie voor het beheren van tmux sessies, gemaakt met PySide6 (Qt for Python).

## Vereisten

- Python 3.8 of hoger
- PySide6
- tmux (moet geïnstalleerd zijn en beschikbaar in PATH)

## Installatie

Installeer de benodigde dependencies:

```bash
# Als je een virtual environment gebruikt (aanbevolen):
source .venv/bin/activate
pip install -r requirements.txt

# Of zonder virtual environment:
pip3 install -r requirements.txt
# of
python3 -m pip install -r requirements.txt
```

Zorg ervoor dat tmux geïnstalleerd is:

```bash
# Op Arch Linux
sudo pacman -S tmux

# Op Ubuntu/Debian
sudo apt-get install tmux

# Op macOS
brew install tmux
```

## Gebruik

Start de applicatie met:

```bash
# Met virtual environment (aanbevolen):
source .venv/bin/activate
python main.py

# Of zonder virtual environment:
python3 main.py

# Of gebruik het launcher script (activeert automatisch de venv):
./launch.sh
```

### Hyprland Keybinding en Dialog Venster

Voeg deze regels toe aan je `~/.config/hypr/hyprland.conf` om de applicatie te starten met `$modC + E` als floating dialog:

```conf
# Keybinding
bind = $modC, E, exec, ~/dev/apps/woddex-os/launch.sh

# Window rules: open als floating dialog venster
windowrulev2 = float, class:^(Tmux Manager|tmux.*manager.*)$
windowrulev2 = size 700 600, class:^(Tmux Manager|tmux.*manager.*)$
windowrulev2 = center, class:^(Tmux Manager|tmux.*manager.*)$
windowrulev2 = animation popin, class:^(Tmux Manager|tmux.*manager.*)$
```

**Belangrijk:** Als de window rules niet werken, vind dan de juiste window class naam:

1. Start de applicatie
2. Open een terminal en voer uit: `hyprctl clients | grep -A 10 "Tmux"`
3. Zoek naar `class:` in de output
4. Pas de window rules aan met de gevonden class naam

Zie `hyprland-config-example.conf` voor een volledige voorbeeldconfiguratie met alternatieve methodes.

## Functies

- **Tmux Sessie Overzicht**: Toont alle actieve tmux sessies
- **Join/Attach**: Voeg je toe aan een bestaande sessie met één klik
- **Termineer**: Stop een sessie met bevestiging
- **Nieuwe Sessie**: Maak een nieuwe tmux sessie aan (met of zonder naam)
- **Vernieuwen**: Update de lijst met sessies
- Moderne GUI met PySide6/QtWidgets
- Gescheiden UI en logica via MainWindow-klasse
- QVBoxLayout voor moderne layout structuur
- Volledig geschreven in pure Python (geen .ui bestanden)

## Gebruiksinstructies

1. **Sessies bekijken**: Bij het opstarten worden alle actieve tmux sessies automatisch getoond
2. **Joinen**: Klik op de "🔗 Join" knop naast een sessie om je eraan te verbinden
3. **Termineren**: Klik op de "❌ Termineer" knop om een sessie te stoppen (met bevestiging)
4. **Nieuwe sessie**: Voer optioneel een naam in en klik op "➕ Nieuwe Sessie"
5. **Vernieuwen**: Klik op "🔄 Vernieuwen" om de lijst bij te werken

## Structuur

- `main.py` - Hoofdbestand met de applicatie code
- `launch.sh` - Launcher script voor de applicatie
- `requirements.txt` - Python dependencies
- `hyprland-config-example.conf` - Voorbeeld Hyprland configuratie
- `README.md` - Deze documentatie
