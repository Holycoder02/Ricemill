"""
Centralized theme system for Rice Mill ERP.

Defines all colors, fonts, spacing, and ttk styles used across the app.
"""

from tkinter import ttk


# ═══════════════════════════════════════════════
# COLOR PALETTE
# ═══════════════════════════════════════════════

class Colors:
    """Modern dark theme color palette."""

    # Primary backgrounds
    BG_DARK = "#0F172A"         # Deepest background (header, sidebar)
    BG_MEDIUM = "#1E293B"       # Cards, panels
    BG_LIGHT = "#334155"        # Elevated surfaces
    BG_PAGE = "#F1F5F9"         # Main page background

    # Accent colors
    PRIMARY = "#3B82F6"         # Blue — primary actions
    PRIMARY_HOVER = "#2563EB"
    PRIMARY_DARK = "#1E40AF"

    SECONDARY = "#8B5CF6"       # Purple — secondary actions
    SECONDARY_HOVER = "#7C3AED"

    SUCCESS = "#10B981"         # Green — success, save
    SUCCESS_HOVER = "#059669"

    WARNING = "#F59E0B"         # Amber — warnings
    WARNING_HOVER = "#D97706"

    DANGER = "#EF4444"          # Red — delete, errors
    DANGER_HOVER = "#DC2626"

    INFO = "#06B6D4"            # Cyan — info
    INFO_HOVER = "#0891B2"

    TEAL = "#14B8A6"            # Teal — settings
    ORANGE = "#F97316"          # Orange — processing
    PINK = "#EC4899"            # Pink — invoices

    # Text colors
    TEXT_PRIMARY = "#F8FAFC"    # Bright white text on dark
    TEXT_SECONDARY = "#94A3B8"  # Muted text
    TEXT_ACCENT = "#60A5FA"     # Link/accent text
    TEXT_DARK = "#1E293B"       # Dark text on light bg
    TEXT_MUTED = "#64748B"      # Subtle dark text

    # Surface colors for cards on light bg
    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#E2E8F0"
    CARD_SHADOW = "#CBD5E1"

    # Input fields
    INPUT_BG = "#FFFFFF"
    INPUT_BORDER = "#CBD5E1"
    INPUT_FOCUS = "#3B82F6"
    INPUT_TEXT = "#1E293B"

    # Table
    TABLE_HEADER = "#1E293B"
    TABLE_ROW_EVEN = "#FFFFFF"
    TABLE_ROW_ODD = "#F8FAFC"
    TABLE_SELECT = "#DBEAFE"
    TABLE_BORDER = "#E2E8F0"


# ═══════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════

class Fonts:
    """Font definitions."""

    FAMILY = "Segoe UI"
    FAMILY_MONO = "Consolas"

    # Sizes
    TITLE = (FAMILY, 28, "bold")
    HEADING = (FAMILY, 18, "bold")
    SUBHEADING = (FAMILY, 14, "bold")
    SECTION = (FAMILY, 13, "bold")
    BODY = (FAMILY, 11)
    BODY_BOLD = (FAMILY, 11, "bold")
    SMALL = (FAMILY, 10)
    SMALL_BOLD = (FAMILY, 10, "bold")
    TINY = (FAMILY, 9)
    BUTTON = (FAMILY, 11, "bold")
    BUTTON_SM = (FAMILY, 10, "bold")
    INPUT = (FAMILY, 11)
    MONO = (FAMILY_MONO, 10)


# ═══════════════════════════════════════════════
# SPACING
# ═══════════════════════════════════════════════

class Spacing:
    """Consistent spacing values."""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 30
    SECTION = 40


# ═══════════════════════════════════════════════
# SECTION COLORS (for dashboard cards)
# ═══════════════════════════════════════════════

SECTION_THEMES = {
    "add": {"bg": Colors.PRIMARY, "icon": "📝", "label": "ADD DATA"},
    "view": {"bg": Colors.SECONDARY, "icon": "📊", "label": "VIEW DATA"},
    "invoice": {"bg": Colors.PINK, "icon": "📄", "label": "INVOICES & REPORTS"},
    "settings": {"bg": Colors.TEAL, "icon": "⚙️", "label": "SETTINGS & CONFIGURATION"},
}

# Button color schemes for different action types
BUTTON_THEMES = {
    "add": Colors.SUCCESS,
    "transaction": Colors.PRIMARY,
    "staff": Colors.SECONDARY,
    "processing": Colors.ORANGE,
    "view": "#475569",
    "invoice": Colors.DANGER,
    "settings": "#7C3AED",
    "save": Colors.SUCCESS,
    "delete": Colors.DANGER,
    "edit": Colors.PRIMARY,
    "cancel": "#64748B",
}


# ═══════════════════════════════════════════════
# TTK STYLE CONFIGURATION
# ═══════════════════════════════════════════════

def apply_theme(root):
    """Apply the modern theme to a Tk root window."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # Treeview styling
    style.configure("Treeview",
                     background=Colors.CARD_BG,
                     foreground=Colors.TEXT_DARK,
                     fieldbackground=Colors.CARD_BG,
                     font=Fonts.BODY,
                     rowheight=32,
                     borderwidth=0)
    style.configure("Treeview.Heading",
                     background=Colors.TABLE_HEADER,
                     foreground=Colors.TEXT_PRIMARY,
                     font=Fonts.BODY_BOLD,
                     borderwidth=0,
                     relief="flat")
    style.map("Treeview",
              background=[("selected", Colors.TABLE_SELECT)],
              foreground=[("selected", Colors.TEXT_DARK)])
    style.map("Treeview.Heading",
              background=[("active", Colors.BG_LIGHT)])

    # Scrollbar styling
    style.configure("Vertical.TScrollbar",
                     background=Colors.CARD_BORDER,
                     troughcolor=Colors.BG_PAGE,
                     borderwidth=0,
                     arrowsize=14)

    # Combobox styling
    style.configure("TCombobox",
                     fieldbackground=Colors.INPUT_BG,
                     background=Colors.INPUT_BG,
                     foreground=Colors.INPUT_TEXT,
                     font=Fonts.INPUT,
                     padding=8)
    style.map("TCombobox",
              fieldbackground=[("readonly", Colors.INPUT_BG)])

    # Entry styling
    style.configure("TEntry",
                     fieldbackground=Colors.INPUT_BG,
                     foreground=Colors.INPUT_TEXT,
                     font=Fonts.INPUT,
                     padding=8)

    # Label styling
    style.configure("TLabel",
                     font=Fonts.BODY)

    return style
