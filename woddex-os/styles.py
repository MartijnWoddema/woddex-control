"""
Stylesheet definities voor de Tmux Manager applicatie.
Alle kleuren en styles zijn hier gecentraliseerd.
"""


class ColorScheme:
    """Kleurenschema voor de applicatie."""
    # Achtergrondkleuren
    BACKGROUND = "#242328"
    CARD_BACKGROUND = "#29282d"
    CARD_HOVER = "#302f34"
    CARD_BORDER = "#302f34"
    CARD_BORDER_HOVER = "#403f44"
    
    # Tekstkleuren
    TEXT_PRIMARY = "#f7f8f8"
    TEXT_SECONDARY = "#8a8f98"
    
    # Accentkleuren
    PRIMARY = "#5e6ad2"
    PRIMARY_HOVER = "#6e7ae2"
    SUCCESS = "#2ecc71"
    ERROR = "#ea3734"
    
    # Statuskleuren
    STATUS_ACTIVE = "#2ecc71"
    STATUS_INACTIVE = "#8a8f98"
    
    # Status label kleuren
    STATUS_INFO = "#5e6ad2"
    STATUS_SUCCESS = "#2ecc71"
    STATUS_ERROR = "#ea3734"


class Icons:
    """Unicode iconen voor UI buttons."""
    # Play/Start/Attach iconen - verschillende opties:
    # ▶ (U+25B6) - Black Right-Pointing Triangle (basis)
    # ⏵ (U+23F5) - Black Medium Right-Pointing Triangle (specifiek voor play)
    # ► (U+25BA) - Black Right-Pointing Small Triangle
    PLAY = "⏵"  # Moderne play button (U+23F5)
    ATTACH = "⏵"  # Zelfde symbool voor attach/verbinden
    
    # Stop/Kill iconen:
    # ✕ (U+2715) - Multiplication X (huidig)
    # ✖ (U+2716) - Heavy Multiplication X
    # ⨯ (U+2A2F) - N-Ary Times Operator
    # ⛔ (U+26D4) - No Entry Sign
    # 🛑 (U+1F6D1) - Stop Sign (emoji)
    KILL = "✕"  # Multiplication X (U+2715)
    
    # Status indicator iconen:
    STATUS_ACTIVE = "●"  # Black Circle (U+25CF)
    STATUS_INACTIVE = "○"  # White Circle (U+25CB)


class Styles:
    """Stylesheet strings voor UI componenten."""
    
    @staticmethod
    def get_central_widget() -> str:
        """Stylesheet voor central widget (hoofdachtergrond)."""
        return f"background-color: {ColorScheme.BACKGROUND};"
    
    @staticmethod
    def get_title_label() -> str:
        """Stylesheet voor titel label."""
        return f"color: {ColorScheme.TEXT_PRIMARY}; margin: 10px 15px;"
    
    @staticmethod
    def get_refresh_button() -> str:
        """Stylesheet voor refresh knop."""
        return f"""
            QPushButton {{
                background-color: {ColorScheme.PRIMARY};
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorScheme.PRIMARY_HOVER};
            }}
        """
    
    @staticmethod
    def get_scroll_area() -> str:
        """Stylesheet voor scroll area."""
        return "QScrollArea { border: none; padding: 0px; }"
    
    @staticmethod
    def get_status_label(default_color: str = None) -> str:
        """Stylesheet voor status label."""
        color = default_color or ColorScheme.TEXT_SECONDARY
        return f"""
            color: {color};
            font-size: 10pt;
            padding: 4px;
            margin-top: 5px;
        """
    
    @staticmethod
    def get_status_label_info() -> str:
        """Status label met info kleur."""
        return Styles.get_status_label(ColorScheme.STATUS_INFO)
    
    @staticmethod
    def get_status_label_success() -> str:
        """Status label met success kleur."""
        return Styles.get_status_label(ColorScheme.STATUS_SUCCESS)
    
    @staticmethod
    def get_status_label_error() -> str:
        """Status label met error kleur."""
        return Styles.get_status_label(ColorScheme.STATUS_ERROR)
    
    @staticmethod
    def get_no_apps_label() -> str:
        """Stylesheet voor 'geen apps' label."""
        return f"""
            color: {ColorScheme.TEXT_SECONDARY};
            font-size: 12pt;
            padding: 30px;
            background-color: {ColorScheme.CARD_BACKGROUND};
            border: 1px solid {ColorScheme.CARD_BORDER};
            border-radius: 5px;
        """
    
    @staticmethod
    def get_app_widget() -> str:
        """Stylesheet voor app widget container."""
        return f"""
            QWidget {{
                background-color: {ColorScheme.CARD_BACKGROUND};
                border: 1px solid {ColorScheme.CARD_BORDER};
                border-radius: 8px;
                padding: 0px;
            }}
            QWidget:hover {{
                background-color: {ColorScheme.CARD_HOVER};
                border-color: {ColorScheme.CARD_BORDER_HOVER};
            }}
        """
    
    @staticmethod
    def get_status_indicator(is_active: bool) -> str:
        """Stylesheet voor status indicator (●/○)."""
        color = ColorScheme.STATUS_ACTIVE if is_active else ColorScheme.STATUS_INACTIVE
        return f"""
            font-size: 16px;
            color: {color};
            padding: 0px 8px 0px 0px;
            background-color: transparent;
            border: none;
            text-align: center;
        """
    
    @staticmethod
    def get_name_label() -> str:
        """Stylesheet voor app naam label."""
        return f"""
            font-size: 13pt;
            font-weight: 500;
            color: {ColorScheme.TEXT_PRIMARY};
            padding: 0px;
            border: none;
            background-color: transparent;
        """
    
    @staticmethod
    def get_attach_button() -> str:
        """Stylesheet voor attach/verbinden knop."""
        return f"""
            QToolButton {{
                background-color: transparent;
                color: {ColorScheme.PRIMARY};
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }}
            QToolButton:hover {{
                background-color: {ColorScheme.PRIMARY};
                color: #ffffff;
            }}
        """
    
    @staticmethod
    def get_kill_button() -> str:
        """Stylesheet voor kill/stop knop."""
        return f"""
            QToolButton {{
                background-color: transparent;
                color: {ColorScheme.TEXT_SECONDARY};
                border: none;
                border-radius: 16px;
                font-size: 18px;
                font-weight: bold;
            }}
            QToolButton:hover {{
                background-color: {ColorScheme.ERROR};
                color: #ffffff;
            }}
        """
    
    @staticmethod
    def get_start_button() -> str:
        """Stylesheet voor start knop."""
        return f"""
            QToolButton {{
                background-color: transparent;
                color: {ColorScheme.SUCCESS};
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }}
            QToolButton:hover {{
                background-color: {ColorScheme.SUCCESS};
                color: #ffffff;
            }}
        """
    
    @staticmethod
    def get_separator() -> str:
        """Stylesheet voor separator/HR lijn."""
        return f"""
            QLabel {{
                background-color: {ColorScheme.CARD_BORDER};
                border: none;
                min-height: 1px;
                max-height: 1px;
                margin: 10px 0px;
            }}
        """
    
    @staticmethod
    def get_new_branch_input() -> str:
        """Stylesheet voor new branch input field."""
        return f"""
            QLineEdit {{
                background-color: {ColorScheme.CARD_BACKGROUND};
                color: {ColorScheme.TEXT_PRIMARY};
                border: 1px solid {ColorScheme.CARD_BORDER};
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }}
            QLineEdit:focus {{
                border-color: {ColorScheme.PRIMARY};
            }}
        """
    
    @staticmethod
    def get_new_branch_button() -> str:
        """Stylesheet voor new branch knop."""
        return f"""
            QPushButton {{
                background-color: {ColorScheme.PRIMARY};
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorScheme.PRIMARY_HOVER};
            }}
        """

