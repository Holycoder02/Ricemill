"""
Rice Mill ERP — Application Entry Point

A comprehensive Enterprise Resource Planning system designed
specifically for rice mill operations.

Usage:
    python app.py
"""

import sys
import os

# Ensure the app directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Initialize the database, set up default users, and launch the login window."""

    # ── Step 1: Initialize database ──
    from db.schema import create_tables, setup_defaults
    create_tables()
    setup_defaults()

    # ── Step 2: Set up default users (with hashed passwords) ──
    from auth.password import setup_default_users
    migrated = setup_default_users()
    if migrated > 0:
        print(f"[Info] Migrated {migrated} plain-text password(s) to hashed format.")

    # ── Step 3: Launch login window ──
    from ui.login import LoginWindow
    from ui.dashboard import Dashboard

    def on_login_success(role):
        """Called when user successfully logs in."""
        dashboard = Dashboard(role)
        dashboard.run()

    login = LoginWindow(on_login_success=on_login_success)
    login.run()


if __name__ == "__main__":
    main()
