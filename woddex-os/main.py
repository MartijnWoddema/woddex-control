#!/usr/bin/env python3

import sys
import subprocess
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QToolButton,
    QHBoxLayout,
    QScrollArea,
    QMessageBox,
    QLineEdit,
    QInputDialog,
)
from PySide6.QtCore import Qt, QEvent, QPoint, QTimer, QSize
from PySide6.QtGui import QFont, QMouseEvent, QIcon
from PySide6.QtWidgets import QStyle
from styles import Styles, ColorScheme, Icons


class MainWindow(QMainWindow):
    APPS = [
        {
            "name": "hakon",
            "ports": [3000, 8010],
            "commands": [
                "cd ~/dev/nea && nx run hakon-app:serve",
                "cd ~/dev/nea && nx run hakon-backend:serve",
            ],
            "depends_on": "avicii",
        },
        {
            "name": "hakon-enq",
            "ports": [4211, 3011],
            "commands": [
                "cd ~/dev/nea && nx run hakon-enq-app:serve",
                "cd ~/dev/nea && nx run hakon-enq-backend:serve",
            ],
        },
        {
            "name": "avicii",
            "ports": [4200, 8000],
            "commands": [
                "cd ~/dev/nea && nx run avicii-app:serve",
                "cd ~/dev/nea && nx run avicii-backend:serve",
            ],
        },
        {
            "name": "avicii-enq",
            "ports": [4201, 3001],
            "commands": [
                "cd ~/dev/nea && nx run avicii-enq-app:serve",
                "cd ~/dev/nea && nx run avicii-enq-backend:serve",
            ],
        },
        {
            "name": "alice",
            "ports": [4220, 8001, 3020],
            "commands": [
                "cd ~/dev/nea && nx run alice-app:serve",
                "cd ~/dev/nea && nx run alice-backend:serve",
                "cd ~/dev/nea && nx run alice-v2-backend:serve"
            ],
        }
    ]
    
    def __init__(self):
        super().__init__()
        self.app_widgets = {}
        self.init_ui()
        self.refresh_apps()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        central_widget.setStyleSheet(Styles.get_central_widget())
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self.title_label = QLabel("Tmux Sessie Manager")
        title_font = QFont("Montserrat", 16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(Styles.get_title_label())
        main_layout.addWidget(self.title_label)
        
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        
        refresh_button = QPushButton("🔄 Vernieuwen")
        refresh_button.setFlat(False)
        refresh_button.setStyleSheet(Styles.get_refresh_button())
        refresh_button.clicked.connect(self.refresh_apps)
        refresh_layout.addWidget(refresh_button)
        refresh_layout.addStretch()
        main_layout.addLayout(refresh_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.get_scroll_area())
        
        self.apps_container = QWidget()
        self.apps_layout = QVBoxLayout()
        self.apps_layout.setSpacing(4)
        self.apps_container.setLayout(self.apps_layout)
        scroll_area.setWidget(self.apps_container)
        main_layout.addWidget(scroll_area)
        
        # Separator tussen apps en new branch sectie
        separator = QLabel()
        separator.setStyleSheet(Styles.get_separator())
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # New Branch sectie
        new_branch_layout = QHBoxLayout()
        new_branch_layout.setContentsMargins(10, 5, 10, 5)
        
        new_branch_label = QLabel("New Branch:")
        new_branch_label.setStyleSheet(f"color: {ColorScheme.TEXT_PRIMARY}; font-size: 11pt;")
        new_branch_layout.addWidget(new_branch_label)
        
        self.new_branch_input = QLineEdit()
        self.new_branch_input.setPlaceholderText("branch-naam")
        self.new_branch_input.setStyleSheet(Styles.get_new_branch_input())
        self.new_branch_input.returnPressed.connect(self.create_new_branch)
        new_branch_layout.addWidget(self.new_branch_input)
        
        new_branch_button = QPushButton("New Branch")
        new_branch_button.setStyleSheet(Styles.get_new_branch_button())
        new_branch_button.clicked.connect(self.create_new_branch)
        new_branch_layout.addWidget(new_branch_button)
        
        main_layout.addLayout(new_branch_layout)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(Styles.get_status_label())
        main_layout.addWidget(self.status_label)
        
        self.setWindowTitle("Tmux Sessie Manager")
        self.setGeometry(100, 100, 700, 600)
        
        self.setWindowFlags(
            Qt.Dialog | 
            Qt.WindowTitleHint | 
            Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint
        )
        
    def is_session_active(self, session_name):
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", session_name],
                capture_output=True,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def kill_ports(self, ports):
        for port in ports:
            try:
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0 and result.stdout.strip():
                    pid = result.stdout.strip().split('\n')[0]
                    subprocess.run(
                        ["kill", "-9", pid],
                        capture_output=True,
                        check=False
                    )
            except Exception:
                pass
    
    def refresh_apps(self):
        """Ververs de lijst met apps."""
        # Verwijder alle bestaande widgets uit de layout
        while self.apps_layout.count():
            item = self.apps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear de dictionary
        self.app_widgets.clear()
        
        if not self.APPS:
            no_apps_label = QLabel("Geen apps geconfigureerd")
            no_apps_label.setStyleSheet(Styles.get_no_apps_label())
            no_apps_label.setAlignment(Qt.AlignCenter)
            self.apps_layout.addWidget(no_apps_label)
        else:
            # Toon alle apps
            for app in self.APPS:
                self.add_app_widget(app)
        
        # Voeg stretch toe aan het einde (maar alleen één keer)
        self.apps_layout.addStretch()
    
    def add_app_widget(self, app):
        """Voegt een widget toe voor een app."""
        app_name = app["name"]
        
        # Check of app actief is (alleen volledige app, niet alleen backend)
        is_active = self.is_session_active(app_name)
        
        # Container widget voor elke app (compact, met hover-highlight)
        app_widget = QWidget()
        app_layout = QHBoxLayout()
        app_layout.setContentsMargins(12, 8, 12, 8)  # Compactere padding
        app_widget.setLayout(app_layout)
        app_widget.setStyleSheet(Styles.get_app_widget())
        
        # Status indicator (groen bolletje als actief)
        status_label = QLabel(Icons.STATUS_ACTIVE if is_active else Icons.STATUS_INACTIVE)
        status_label.setStyleSheet(Styles.get_status_indicator(is_active))
        status_label.setToolTip("Actief" if is_active else "Niet actief")
        app_layout.addWidget(status_label)
        
        # App naam label (plain text, geen borders)
        name_label = QLabel(app_name)
        name_label.setStyleSheet(Styles.get_name_label())
        app_layout.addWidget(name_label)
        
        app_layout.addStretch()
        
        if is_active:
            # Als actief: toon attach en kill knoppen
            # Verbinden knop
            attach_button = QToolButton()
            attach_button.setText(Icons.ATTACH)
            attach_button.setFixedSize(32, 32)
            attach_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
            attach_button.setAutoRaise(True)
            attach_button.setToolTip("Verbinden met sessie")
            attach_button.setStyleSheet(Styles.get_attach_button())
            attach_button.clicked.connect(lambda checked, name=app_name: self.attach_session(name))
            app_layout.addWidget(attach_button)
            
            # Spacing tussen knoppen
            app_layout.addSpacing(8)
            
            # Kill knop
            kill_button = QToolButton()
            kill_button.setText(Icons.KILL)
            kill_button.setFixedSize(32, 32)
            kill_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
            kill_button.setAutoRaise(True)
            kill_button.setToolTip("Stop app")
            kill_button.setStyleSheet(Styles.get_kill_button())
            kill_button.clicked.connect(lambda checked, app_data=app: self.kill_app(app_data))
            app_layout.addWidget(kill_button)
        else:
            # Als niet actief: alleen start knop
            start_button = QToolButton()
            start_button.setText(Icons.PLAY)
            start_button.setFixedSize(32, 32)
            start_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
            start_button.setAutoRaise(True)
            start_button.setToolTip("Start app")
            start_button.setStyleSheet(Styles.get_start_button())
            start_button.clicked.connect(lambda checked, app_data=app: self.start_app(app_data))
            app_layout.addWidget(start_button)
        
        # Voeg toe aan layout
        self.apps_layout.addWidget(app_widget)
        self.app_widgets[app_name] = app_widget

    def detect_terminal_emulator(self):
        """Detecteert welke terminal emulator beschikbaar is."""
        terminals = [
            ("kitty", ["kitty", "tmux", "attach-session", "-t"]),
            ("alacritty", ["alacritty", "-e", "tmux", "attach-session", "-t"]),
            ("foot", ["foot", "tmux", "attach-session", "-t"]),
            ("gnome-terminal", ["gnome-terminal", "--", "tmux", "attach-session", "-t"]),
            ("xterm", ["xterm", "-e", "tmux", "attach-session", "-t"]),
        ]
        
        for name, cmd in terminals:
            if shutil.which(name):
                return cmd
        return None
    
    def attach_session(self, session_name):
        """Voegt zich toe aan een tmux sessie."""
        try:
            # Controleer of sessie bestaat
            result = subprocess.run(
                ["tmux", "has-session", "-t", session_name],
                capture_output=True,
                check=False
            )
            if result.returncode != 0:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Sessie '{session_name}' bestaat niet"
                )
                return
            
            # Detecteer terminal emulator
            terminal_cmd = self.detect_terminal_emulator()
            
            if terminal_cmd:
                # Start terminal met tmux attach
                cmd = terminal_cmd + [session_name]
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            else:
                # Fallback: direct tmux attach (als terminal niet beschikbaar)
                subprocess.Popen(
                    ["tmux", "attach-session", "-t", session_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            self.status_label.setText(f"Verbonden met: {session_name}")
            self.status_label.setStyleSheet(Styles.get_status_label_info())
            # Sluit venster na korte delay
            QTimer.singleShot(300, self.close)
        except Exception as e:
            QMessageBox.warning(
                self,
                "Fout",
                f"Kon niet verbinden met sessie '{session_name}':\n{str(e)}"
            )
            self.status_label.setText("Fout bij verbinden")
    
    def extract_project_dir(self, command):
        """Haal project directory uit commando (cd ~/dev/nea && ... -> ~/dev/nea)."""
        # Zoek naar cd commando in het begin
        if "cd " in command and " && " in command:
            parts = command.split(" && ", 1)
            cd_part = parts[0].strip()
            if cd_part.startswith("cd "):
                # Haal directory uit "cd ~/dev/nea"
                dir_part = cd_part[3:].strip().strip('"').strip("'")
                return dir_part
        return None
    
    def find_app_by_name(self, app_name):
        """Vind een app configuratie op basis van naam."""
        for app in self.APPS:
            if app["name"] == app_name:
                return app
        return None
    
    def _create_tmux_session(self, session_name, commands, project_dir=None):
        """Helper functie om een tmux sessie te maken met commando's in panes."""
        # Filter "true" commando's eruit
        valid_commands = [cmd for cmd in commands if cmd != "true"]
        if not valid_commands:
            return False
        
        # Haal project directory op uit eerste commando als niet gegeven
        if not project_dir:
            project_dir = self.extract_project_dir(valid_commands[0])
        if not project_dir:
            project_dir = "~"
        project_dir_expanded = str(Path(project_dir).expanduser())
        
        # Maak nieuwe lege tmux sessie
        result = subprocess.run(
            ["tmux", "new-session", "-d", "-s", session_name],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            return False
        
        # Eerste pane: cd + eerste commando
        first_cmd = valid_commands[0]
        if "cd " in first_cmd and " && " in first_cmd:
            first_cmd = first_cmd.split(" && ", 1)[1]
        
        subprocess.run(["tmux", "send-keys", "-t", session_name, f"cd \"{project_dir_expanded}\""], capture_output=True, check=False)
        subprocess.run(["tmux", "send-keys", "-t", session_name, "C-m"], capture_output=True, check=False)
        subprocess.run(["tmux", "send-keys", "-t", session_name, first_cmd], capture_output=True, check=False)
        subprocess.run(["tmux", "send-keys", "-t", session_name, "C-m"], capture_output=True, check=False)
        
        # Voeg extra panes toe voor resterende commando's (naast elkaar)
        for cmd in valid_commands[1:]:
            subprocess.run(["tmux", "split-window", "-h", "-t", session_name], capture_output=True, check=False)
            if "cd " in cmd and " && " in cmd:
                cmd = cmd.split(" && ", 1)[1]
            subprocess.run(["tmux", "send-keys", "-t", session_name, f"cd \"{project_dir_expanded}\""], capture_output=True, check=False)
            subprocess.run(["tmux", "send-keys", "-t", session_name, "C-m"], capture_output=True, check=False)
            subprocess.run(["tmux", "send-keys", "-t", session_name, cmd], capture_output=True, check=False)
            subprocess.run(["tmux", "send-keys", "-t", session_name, "C-m"], capture_output=True, check=False)
        
        # Zet layout op even-horizontal
        subprocess.run(["tmux", "select-layout", "-t", session_name, "even-horizontal"], capture_output=True, check=False)
        return True
    
    def start_dependency(self, dependency_app_name):
        """Start een dependency (volledige app). Maakt sessie met naam app_name-backend."""
        dep_app = self.find_app_by_name(dependency_app_name)
        if not dep_app:
            return False
        
        commands = dep_app.get("commands", [])
        if not commands:
            return False
        
        # Sessie naam is app naam + "-backend"
        dependency_session_name = f"{dependency_app_name}-backend"
        return self._create_tmux_session(dependency_session_name, commands)
    
    def start_app(self, app):
        """Start een app met tmux sessie en commando's in panes naast elkaar."""
        app_name = app["name"]
        commands = app.get("commands", [])
        depends_on = app.get("depends_on")
        
        try:
            # Check eerst of er een backend-only sessie draait (gemaakt door dependency)
            # Stop die automatisch als die bestaat, zodat we de volledige app kunnen starten
            backend_session_name = f"{app_name}-backend"
            if self.is_session_active(backend_session_name):
                # Stop de backend-only sessie automatisch
                subprocess.run(
                    ["tmux", "kill-session", "-t", backend_session_name],
                    capture_output=True,
                    check=False
                )
            
            # Controleer nu of de volledige app al actief is
            if self.is_session_active(app_name):
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"App '{app_name}' is al actief"
                )
                return
            
            # Check of er dependencies zijn die we moeten starten
            # (bijv. hakon starten die afhankelijk is van avicii)
            if depends_on:
                dependency_session_name_for_check = f"{depends_on}-backend"
                if not self.is_session_active(dependency_session_name_for_check):
                    # Start de dependency (alleen backend)
                    if not self.start_dependency(depends_on):
                        QMessageBox.warning(
                            self,
                            "Fout",
                            f"Kon dependency '{depends_on}' niet starten"
                        )
                        return
            
            if not commands:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Geen commando's geconfigureerd voor '{app_name}'"
                )
                return
            
            # Filter "true" commando's eruit
            valid_commands = [cmd for cmd in commands if cmd != "true"]
            if not valid_commands:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Geen geldige commando's voor '{app_name}'"
                )
                return
            
            # Haal project directory op uit eerste commando
            project_dir = self.extract_project_dir(valid_commands[0])
            if not project_dir:
                project_dir = "~"  # Fallback
            
            # Expand ~ naar volledig pad
            project_dir_expanded = str(Path(project_dir).expanduser())
            
            # Maak nieuwe lege tmux sessie
            result = subprocess.run(
                ["tmux", "new-session", "-d", "-s", app_name],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() or result.stdout.strip()
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Kon app '{app_name}' niet starten:\n{error_msg}"
                )
                return
            
            # Eerste pane: cd + eerste commando
            first_cmd = valid_commands[0]
            # Verwijder cd deel uit commando als het erin zit
            if "cd " in first_cmd and " && " in first_cmd:
                first_cmd = first_cmd.split(" && ", 1)[1]
            
            subprocess.run(
                ["tmux", "send-keys", "-t", app_name, f"cd \"{project_dir_expanded}\""],
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["tmux", "send-keys", "-t", app_name, "C-m"],
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["tmux", "send-keys", "-t", app_name, first_cmd],
                capture_output=True,
                check=False
            )
            subprocess.run(
                ["tmux", "send-keys", "-t", app_name, "C-m"],
                capture_output=True,
                check=False
            )
            
            # Voeg extra panes toe voor resterende commando's (naast elkaar)
            for cmd in valid_commands[1:]:
                # Split window horizontaal
                subprocess.run(
                    ["tmux", "split-window", "-h", "-t", app_name],
                    capture_output=True,
                    check=False
                )
                
                # Verwijder cd deel uit commando als het erin zit
                if "cd " in cmd and " && " in cmd:
                    cmd = cmd.split(" && ", 1)[1]
                
                # Stuur commando's naar nieuwe pane
                subprocess.run(
                    ["tmux", "send-keys", "-t", app_name, f"cd \"{project_dir_expanded}\""],
                    capture_output=True,
                    check=False
                )
                subprocess.run(
                    ["tmux", "send-keys", "-t", app_name, "C-m"],
                    capture_output=True,
                    check=False
                )
                subprocess.run(
                    ["tmux", "send-keys", "-t", app_name, cmd],
                    capture_output=True,
                    check=False
                )
                subprocess.run(
                    ["tmux", "send-keys", "-t", app_name, "C-m"],
                    capture_output=True,
                    check=False
                )
            
            # Zet layout op even-horizontal (werkt voor 2 of 3 panes)
            subprocess.run(
                ["tmux", "select-layout", "-t", app_name, "even-horizontal"],
                capture_output=True,
                check=False
            )
            
            self.status_label.setText(f"App '{app_name}' gestart")
            self.status_label.setStyleSheet(Styles.get_status_label_success())
            self.refresh_apps()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Fout",
                f"Fout bij starten van app '{app_name}':\n{str(e)}"
            )
    
    def kill_app(self, app):
        """Beëindigt een app: kill poorten en kill tmux sessie."""
        app_name = app["name"]
        ports = app.get("ports", [])
        depends_on = app.get("depends_on")
        
        reply = QMessageBox.question(
            self,
            "Bevestig beëindiging",
            f"App '{app_name}' wordt gestopt.\nLopende processen stoppen.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Kill poorten
                if ports:
                    self.kill_ports(ports)
                
                # Kill tmux sessie
                if self.is_session_active(app_name):
                    result = subprocess.run(
                        ["tmux", "kill-session", "-t", app_name],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if result.returncode != 0:
                        error_msg = result.stderr.strip() or result.stdout.strip()
                        QMessageBox.warning(
                            self,
                            "Fout",
                            f"Kon sessie '{app_name}' niet beëindigen:\n{error_msg}"
                        )
                        return
                
                # Kill dependency backend sessie ook als die bestaat
                if depends_on:
                    dependency_session_name = f"{depends_on}-backend"
                    if self.is_session_active(dependency_session_name):
                        subprocess.run(
                            ["tmux", "kill-session", "-t", dependency_session_name],
                            capture_output=True,
                            check=False
                        )
                
                self.status_label.setText(f"App '{app_name}' gestopt")
                self.status_label.setStyleSheet(Styles.get_status_label_error())
                self.refresh_apps()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Fout bij stoppen van app '{app_name}':\n{str(e)}"
                )
    
    def create_new_branch(self, retry_count=0):
        """Maakt een nieuwe git branch aan en PR volgens het newbranch.sh script."""
        branch_name = self.new_branch_input.text().strip()
        
        if not branch_name:
            QMessageBox.warning(
                self,
                "Fout",
                "Geef een branch naam op"
            )
            return
        
        project_dir = Path("/home/woddex/dev/nea").expanduser()
        
        if not project_dir.exists():
            QMessageBox.warning(
                self,
                "Fout",
                f"Directory bestaat niet: {project_dir}"
            )
            return
        
        try:
            # Checkout develop (alleen als we niet retryen)
            if retry_count == 0:
                result = subprocess.run(
                    ["git", "checkout", "develop"],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    QMessageBox.warning(
                        self,
                        "Fout",
                        f"Kon niet checkout develop:\n{result.stderr}"
                    )
                    return
                
                # Pull origin develop
                result = subprocess.run(
                    ["git", "pull", "origin", "develop"],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    QMessageBox.warning(
                        self,
                        "Fout",
                        f"Kon niet pull origin develop:\n{result.stderr}"
                    )
                    return
                
                # Checkout nieuwe branch
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    QMessageBox.warning(
                        self,
                        "Fout",
                        f"Kon niet branch '{branch_name}' aanmaken:\n{result.stderr}"
                    )
                    return
            
            # Check voor staged changes
            result = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=str(project_dir),
                capture_output=True,
                check=False
            )
            has_staged_changes = result.returncode != 0
            
            if has_staged_changes:
                # Vraag commit message
                commit_message, ok = QInputDialog.getText(
                    self,
                    "Commit Message",
                    "Staged changes gevonden. Geef een commit message op:",
                    text="Update"
                )
                
                if not ok:
                    # Gebruiker heeft geannuleerd
                    return
                
                if not commit_message or not commit_message.strip():
                    commit_message = "Update"
                
                # Commit
                result = subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    QMessageBox.warning(
                        self,
                        "Fout",
                        f"Kon niet committen:\n{result.stderr}"
                    )
                    return
            else:
                # Geen staged changes, vraag bevestiging voor empty commit
                reply = QMessageBox.question(
                    self,
                    "Bevestiging",
                    "Geen staged changes gevonden.\n\nWeet je zeker dat je een lege commit wilt aanmaken?\n\n(Druk 'Nee' om opnieuw te controleren na het stagen van changes)",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.No:
                    # Gebruiker zegt nee, probeer opnieuw (met maximum retries)
                    if retry_count < 2:
                        self.create_new_branch(retry_count + 1)
                    else:
                        QMessageBox.information(
                            self,
                            "Geannuleerd",
                            "Branch aanmaken geannuleerd."
                        )
                    return
                
                # Maak empty commit
                result = subprocess.run(
                    ["git", "commit", "--allow-empty", "-m", "Empty commit to trigger PR"],
                    cwd=str(project_dir),
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode != 0:
                    QMessageBox.warning(
                        self,
                        "Fout",
                        f"Kon niet empty commit aanmaken:\n{result.stderr}"
                    )
                    return
            
            # Push branch
            result = subprocess.run(
                ["git", "push", "--set-upstream", "origin", branch_name],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Kon niet branch pushen:\n{result.stderr}"
                )
                return
            
            # Maak PR aan met gh
            result = subprocess.run(
                [
                    "gh", "pr", "create",
                    "--repo", "onderzoekdoen-nl/nea",
                    "--title", branch_name,
                    "--body", "",
                    "--base", "develop",
                    "--head", branch_name
                ],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                QMessageBox.warning(
                    self,
                    "Fout",
                    f"Kon PR niet aanmaken:\n{result.stderr}\n\nBranch is wel aangemaakt en gepusht."
                )
                self.status_label.setText(f"Branch '{branch_name}' aangemaakt, maar PR mislukt")
                self.status_label.setStyleSheet(Styles.get_status_label_error())
            else:
                self.status_label.setText(f"Branch en PR aangemaakt: {branch_name}")
                self.status_label.setStyleSheet(Styles.get_status_label_success())
                self.new_branch_input.clear()
        
        except Exception as e:
            QMessageBox.warning(
                self,
                "Fout",
                f"Fout bij aanmaken branch:\n{str(e)}"
            )
            self.status_label.setText("Fout bij aanmaken branch")
            self.status_label.setStyleSheet(Styles.get_status_label_error())


def main():
    """Hoofdfunctie die de applicatie start."""
    app = QApplication(sys.argv)
    
    # High-DPI fixes voor Hyprland / Wayland (anti-aliased rendering)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Stel Roboto font in als standaard font voor de hele applicatie
    roboto_font = QFont("Roboto", 10)
    app.setFont(roboto_font)
    
    # Stel applicatie naam in voor window manager herkenning
    app.setApplicationName("Tmux Manager")
    app.setApplicationDisplayName("Tmux Manager")
    app.setOrganizationName("Woddex")
    
    # Stijl voor de hele applicatie
    app.setStyle("Fusion")
    
    # Hoofdvenster maken en tonen
    window = MainWindow()
    
    # Stel expliciet window class in voor Hyprland/X11 herkenning
    # Dit zorgt ervoor dat de window manager de applicatie correct kan identificeren
    window.setObjectName("TmuxManager")
    
    # Centreer het venster op het scherm
    screen = app.primaryScreen().geometry()
    window_geometry = window.frameGeometry()
    window_geometry.moveCenter(screen.center())
    window.move(window_geometry.topLeft())
    
    window.show()
    
    # Event loop starten
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


