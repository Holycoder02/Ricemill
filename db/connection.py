"""
Database connection manager for Rice Mill ERP.

Provides a singleton connection with proper cleanup via atexit.
"""

import sqlite3
import atexit
import os

_conn = None
_cursor = None

DB_NAME = "rice_mill_erp.db"


def _get_db_path():
    """Get the database path relative to the app's directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DB_NAME)


def get_connection():
    """Get or create the singleton database connection."""
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(_get_db_path())
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
    return _conn


def get_cursor():
    """Get a cursor from the singleton connection."""
    global _cursor
    if _cursor is None:
        _cursor = get_connection().cursor()
    return _cursor


def commit():
    """Commit the current transaction."""
    conn = get_connection()
    conn.commit()


def close_connection():
    """Close the database connection cleanly."""
    global _conn, _cursor
    if _conn is not None:
        try:
            _conn.commit()
            _conn.close()
        except Exception:
            pass
        _conn = None
        _cursor = None


# Register cleanup on app exit
atexit.register(close_connection)
