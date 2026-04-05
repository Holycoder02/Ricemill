"""
Modern login window for Rice Mill ERP.
"""

from tkinter import *
from tkinter import messagebox
from ui.theme import Colors, Fonts, Spacing, apply_theme
from db.models import get_user_by_username
from auth.password import verify_password


class LoginWindow:
    """Premium login window with modern styling."""

    def __init__(self, on_login_success):
        """
        Args:
            on_login_success: Callable(role) invoked after successful login
        """
        self.on_login_success = on_login_success

        self.root = Tk()
        self.root.title("Rice Mill ERP — Login")
        self.root.geometry("520x640")
        self.root.resizable(False, False)
        self.root.configure(bg=Colors.PRIMARY_DARK)
        apply_theme(self.root)

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 260
        y = (self.root.winfo_screenheight() // 2) - 320
        self.root.geometry(f"520x640+{x}+{y}")

        self._build_ui()

    def _build_ui(self):
        """Build the login window UI."""
        # ── Outer container ──
        outer = Frame(self.root, bg=Colors.PRIMARY_DARK)
        outer.pack(fill=BOTH, expand=True)

        # ── Top Branding Section ──
        brand_frame = Frame(outer, bg=Colors.PRIMARY, height=200)
        brand_frame.pack(fill=X)
        brand_frame.pack_propagate(False)

        # Decorative top bar
        Frame(brand_frame, bg=Colors.SUCCESS, height=4).pack(fill=X)

        brand_inner = Frame(brand_frame, bg=Colors.PRIMARY)
        brand_inner.pack(expand=True)

        Label(brand_inner, text="🌾", font=("Segoe UI", 52),
              bg=Colors.PRIMARY, fg="white").pack(pady=(10, 5))
        Label(brand_inner, text="RICE MILL ERP", font=("Segoe UI", 28, "bold"),
              bg=Colors.PRIMARY, fg="white").pack()
        Label(brand_inner, text="Enterprise Resource Planning System",
              font=Fonts.SMALL, bg=Colors.PRIMARY, fg="#BFDBFE").pack(pady=(4, 0))

        # ── Login Form Card ──
        card_frame = Frame(outer, bg=Colors.PRIMARY_DARK, padx=40, pady=20)
        card_frame.pack(fill=BOTH, expand=True)

        # Card with subtle border
        card = Frame(card_frame, bg=Colors.BG_MEDIUM, relief=FLAT, bd=0,
                     highlightbackground="#334155", highlightthickness=1)
        card.pack(fill=BOTH, expand=True)

        form_inner = Frame(card, bg=Colors.BG_MEDIUM, padx=30, pady=25)
        form_inner.pack(fill=BOTH, expand=True)

        # Sign In label
        Label(form_inner, text="Sign In", font=Fonts.HEADING,
              bg=Colors.BG_MEDIUM, fg=Colors.TEXT_PRIMARY).pack(anchor=W, pady=(0, 5))
        Label(form_inner, text="Enter your credentials to continue",
              font=Fonts.SMALL, bg=Colors.BG_MEDIUM, fg=Colors.TEXT_SECONDARY).pack(anchor=W, pady=(0, 20))

        # Username field
        Label(form_inner, text="Username", font=Fonts.BODY_BOLD,
              bg=Colors.BG_MEDIUM, fg=Colors.TEXT_PRIMARY).pack(anchor=W, pady=(0, 4))
        self.user_entry = Entry(form_inner, font=Fonts.INPUT, bg="#1E293B",
                                fg=Colors.TEXT_PRIMARY, relief=SOLID, bd=1,
                                insertbackground=Colors.TEXT_PRIMARY,
                                highlightcolor=Colors.PRIMARY, highlightthickness=1)
        self.user_entry.pack(fill=X, ipady=10, pady=(0, 16))
        self.user_entry.focus_set()

        # Password field
        Label(form_inner, text="Password", font=Fonts.BODY_BOLD,
              bg=Colors.BG_MEDIUM, fg=Colors.TEXT_PRIMARY).pack(anchor=W, pady=(0, 4))
        self.pass_entry = Entry(form_inner, font=Fonts.INPUT, bg="#1E293B",
                                fg=Colors.TEXT_PRIMARY, show="●", relief=SOLID, bd=1,
                                insertbackground=Colors.TEXT_PRIMARY,
                                highlightcolor=Colors.PRIMARY, highlightthickness=1)
        self.pass_entry.pack(fill=X, ipady=10, pady=(0, 8))

        # Show password toggle
        self.show_pw_var = BooleanVar(value=False)
        show_pw_check = Checkbutton(form_inner, text="Show password", variable=self.show_pw_var,
                                     command=self._toggle_password,
                                     bg=Colors.BG_MEDIUM, fg=Colors.TEXT_SECONDARY,
                                     selectcolor=Colors.BG_MEDIUM, activebackground=Colors.BG_MEDIUM,
                                     activeforeground=Colors.TEXT_SECONDARY,
                                     font=Fonts.TINY, cursor="hand2")
        show_pw_check.pack(anchor=W, pady=(0, 20))

        # Login button
        self.login_btn = Button(form_inner, text="LOGIN", command=self._handle_login,
                                bg=Colors.PRIMARY, fg="white", font=Fonts.BUTTON,
                                relief=FLAT, bd=0, padx=20, pady=12, cursor="hand2",
                                activebackground=Colors.PRIMARY_HOVER, activeforeground="white")
        self.login_btn.pack(fill=X, ipady=4)

        # Subtle hint
        hint_frame = Frame(form_inner, bg=Colors.BG_LIGHT, relief=FLAT)
        hint_frame.pack(fill=X, pady=(16, 0))
        Label(hint_frame, text="Default: admin / admin123  |  accountant / acc123  |  manager / mgr123",
              font=("Segoe UI", 8), bg=Colors.BG_LIGHT, fg=Colors.TEXT_SECONDARY).pack(pady=6)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._handle_login())

    def _toggle_password(self):
        """Toggle password visibility."""
        if self.show_pw_var.get():
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="●")

    def _handle_login(self):
        """Process login attempt."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.",
                                parent=self.root)
            return

        # Look up user
        user = get_user_by_username(username)
        if user is None:
            messagebox.showerror("Login Failed", "Invalid username or password.",
                                parent=self.root)
            return

        user_id, db_username, db_password, role, salt = user

        # Verify password
        if salt:
            # Hashed password
            if not verify_password(password, db_password, salt):
                messagebox.showerror("Login Failed", "Invalid username or password.",
                                    parent=self.root)
                return
        else:
            # Legacy plain-text password (pre-migration)
            if password != db_password:
                messagebox.showerror("Login Failed", "Invalid username or password.",
                                    parent=self.root)
                return

        # Success!
        self.root.destroy()
        self.on_login_success(role)

    def run(self):
        """Start the login window mainloop."""
        self.root.mainloop()
