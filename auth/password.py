"""
Password hashing and verification for Rice Mill ERP.

Uses PBKDF2-HMAC-SHA256 with per-user salt for secure password storage.
"""

import hashlib
import os
import binascii
from db.connection import get_connection, commit


def generate_salt():
    """Generate a random 32-byte salt."""
    return binascii.hexlify(os.urandom(32)).decode('utf-8')


def hash_password(password, salt=None):
    """
    Hash a password with PBKDF2-HMAC-SHA256.

    Returns (hash, salt) tuple.
    """
    if salt is None:
        salt = generate_salt()
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100_000
    )
    return binascii.hexlify(pw_hash).decode('utf-8'), salt


def verify_password(password, stored_hash, salt):
    """Verify a password against a stored hash and salt."""
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == stored_hash


def migrate_plain_text_passwords():
    """
    One-time migration: hash any plain-text passwords in the database.

    Detects plain-text by checking if the salt column is NULL or empty.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password, salt FROM users WHERE salt IS NULL OR salt = ''")
    users = cursor.fetchall()

    for user_id, username, plain_password, _ in users:
        pw_hash, salt = hash_password(plain_password)
        cursor.execute("UPDATE users SET password=?, salt=? WHERE id=?",
                       (pw_hash, salt, user_id))

    if users:
        commit()

    return len(users)


def setup_default_users():
    """Create default admin, accountant, and manager users if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    defaults = [
        ("admin", "admin123", "Admin"),
        ("accountant", "acc123", "Accountant"),
        ("manager", "mgr123", "Manager"),
    ]

    for username, password, role in defaults:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
        if cursor.fetchone()[0] == 0:
            pw_hash, salt = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, role, salt) VALUES (?,?,?,?)",
                (username, pw_hash, role, salt)
            )

    commit()

    # Migrate any existing plain-text passwords
    migrated = migrate_plain_text_passwords()
    return migrated
