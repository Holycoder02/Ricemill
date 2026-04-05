"""Database package for Rice Mill ERP."""

from db.connection import get_connection, get_cursor, close_connection
from db.schema import create_tables, setup_defaults
