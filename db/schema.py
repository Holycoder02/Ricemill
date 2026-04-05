"""
Database schema definitions and table creation for Rice Mill ERP.
"""

from db.connection import get_connection, commit


TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT,
            role TEXT NOT NULL DEFAULT 'Accountant'
        )
    """,
    "mills": """
        CREATE TABLE IF NOT EXISTS mills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "godowns": """
        CREATE TABLE IF NOT EXISTS godowns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mill_id INTEGER,
            total_capacity REAL DEFAULT 0,
            current_stock REAL DEFAULT 0,
            storage_rate REAL DEFAULT 0,
            FOREIGN KEY (mill_id) REFERENCES mills(id)
        )
    """,
    "godown_entries": """
        CREATE TABLE IF NOT EXISTS godown_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            godown_id INTEGER,
            party_id INTEGER,
            product_id INTEGER,
            quantity REAL,
            unit TEXT,
            from_date TEXT,
            to_date TEXT,
            storage_rate REAL,
            total_charges REAL,
            FOREIGN KEY (godown_id) REFERENCES godowns(id),
            FOREIGN KEY (party_id) REFERENCES parties(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """,
    "categories": """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """,
    "parties": """
        CREATE TABLE IF NOT EXISTS parties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'Customer'
        )
    """,
    "purchases": """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_id INTEGER,
            product_id INTEGER,
            quantity REAL,
            unit TEXT,
            rate REAL,
            subtotal REAL,
            gst_percent REAL,
            gst_amount REAL,
            total REAL,
            date TEXT,
            FOREIGN KEY (party_id) REFERENCES parties(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """,
    "sales": """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_id INTEGER,
            product_id INTEGER,
            quantity REAL,
            unit TEXT,
            rate REAL,
            subtotal REAL,
            gst_percent REAL,
            gst_amount REAL,
            total REAL,
            date TEXT,
            FOREIGN KEY (party_id) REFERENCES parties(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """,
    "processing": """
        CREATE TABLE IF NOT EXISTS processing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_no TEXT NOT NULL,
            input_product INTEGER,
            output_product INTEGER,
            quantity REAL,
            unit TEXT,
            date TEXT,
            FOREIGN KEY (input_product) REFERENCES products(id),
            FOREIGN KEY (output_product) REFERENCES products(id)
        )
    """,
    "staff": """
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            payout_type TEXT DEFAULT 'Monthly',
            salary REAL DEFAULT 0
        )
    """,
    "vehicles": """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_no TEXT NOT NULL,
            driver TEXT,
            vehicle_type TEXT DEFAULT 'Truck',
            empty_weight REAL DEFAULT 0,
            loaded_weight REAL DEFAULT 0
        )
    """,
    "company_info": """
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            gst_number TEXT,
            rst_number TEXT,
            contact_number TEXT,
            address TEXT
        )
    """,
    "bank_accounts": """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT NOT NULL,
            account_no TEXT,
            ifsc_code TEXT,
            balance REAL DEFAULT 0
        )
    """,
}


def create_tables():
    """Create all database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    for table_name, create_sql in TABLES.items():
        cursor.execute(create_sql)

    # Add salt column to users if it doesn't exist (migration)
    try:
        cursor.execute("SELECT salt FROM users LIMIT 1")
    except Exception:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN salt TEXT")
        except Exception:
            pass

    commit()


def setup_defaults():
    """Insert default data if tables are empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # Default company info
    cursor.execute("SELECT COUNT(*) FROM company_info")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """INSERT INTO company_info (company_name, gst_number, rst_number, contact_number, address)
               VALUES ('Rice Mill', '', '', '', '')"""
        )

    commit()
