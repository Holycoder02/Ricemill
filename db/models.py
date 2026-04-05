"""
Data access layer for Rice Mill ERP.

All CRUD operations for every table live here.
Returns plain tuples from the database — the UI layer handles display.
"""

from db.connection import get_connection, commit
from datetime import datetime


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────

def get_user_by_credentials(username, password_hash):
    """Get user by username and hashed password."""
    cur = get_connection().cursor()
    cur.execute("SELECT id, username, role, salt FROM users WHERE username=? AND password=?",
                (username, password_hash))
    return cur.fetchone()


def get_user_by_username(username):
    """Get user by username."""
    cur = get_connection().cursor()
    cur.execute("SELECT id, username, password, role, salt FROM users WHERE username=?", (username,))
    return cur.fetchone()


def create_user(username, password_hash, role, salt):
    """Create a new user."""
    cur = get_connection().cursor()
    cur.execute("INSERT INTO users (username, password, role, salt) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, salt))
    commit()


def update_user_password(user_id, password_hash, salt):
    """Update a user's password."""
    cur = get_connection().cursor()
    cur.execute("UPDATE users SET password=?, salt=? WHERE id=?", (password_hash, salt, user_id))
    commit()


def user_exists(username):
    """Check if a username already exists."""
    cur = get_connection().cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    return cur.fetchone()[0] > 0


# ─────────────────────────────────────────────
# GENERIC CRUD HELPERS
# ─────────────────────────────────────────────

def _fetch_all(table):
    """Fetch all rows from a table."""
    cur = get_connection().cursor()
    cur.execute(f"SELECT * FROM {table}")
    return cur.fetchall()


def _fetch_by_id(table, row_id):
    """Fetch a single row by ID."""
    cur = get_connection().cursor()
    cur.execute(f"SELECT * FROM {table} WHERE id=?", (row_id,))
    return cur.fetchone()


def _delete_by_id(table, row_id):
    """Delete a row by ID."""
    cur = get_connection().cursor()
    cur.execute(f"DELETE FROM {table} WHERE id=?", (row_id,))
    commit()


def _get_name_by_id(table, row_id):
    """Get the name field of a record by ID."""
    cur = get_connection().cursor()
    cur.execute(f"SELECT name FROM {table} WHERE id=?", (row_id,))
    result = cur.fetchone()
    return result[0] if result else "N/A"


def _get_names_dict(table):
    """Get a dict of {id: name} for a table."""
    cur = get_connection().cursor()
    cur.execute(f"SELECT id, name FROM {table}")
    return {row[0]: row[1] for row in cur.fetchall()}


# ─────────────────────────────────────────────
# MILLS
# ─────────────────────────────────────────────

def get_all_mills():
    return _fetch_all("mills")

def get_mill(mill_id):
    return _fetch_by_id("mills", mill_id)

def get_mill_names():
    return _get_names_dict("mills")

def add_mill(name):
    cur = get_connection().cursor()
    cur.execute("INSERT INTO mills (name) VALUES (?)", (name,))
    commit()

def update_mill(mill_id, name):
    cur = get_connection().cursor()
    cur.execute("UPDATE mills SET name=? WHERE id=?", (name, mill_id))
    commit()

def delete_mill(mill_id):
    _delete_by_id("mills", mill_id)


# ─────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────

def get_all_categories():
    return _fetch_all("categories")

def get_category(cat_id):
    return _fetch_by_id("categories", cat_id)

def get_category_names():
    return _get_names_dict("categories")

def add_category(name):
    cur = get_connection().cursor()
    cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    commit()

def update_category(cat_id, name):
    cur = get_connection().cursor()
    cur.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id))
    commit()

def delete_category(cat_id):
    _delete_by_id("categories", cat_id)


# ─────────────────────────────────────────────
# GODOWNS
# ─────────────────────────────────────────────

def get_all_godowns():
    return _fetch_all("godowns")

def get_godown(godown_id):
    return _fetch_by_id("godowns", godown_id)

def get_godown_names():
    return _get_names_dict("godowns")

def add_godown(name, mill_id, total_capacity, storage_rate):
    cur = get_connection().cursor()
    cur.execute(
        "INSERT INTO godowns (name, mill_id, total_capacity, current_stock, storage_rate) VALUES (?,?,?,?,?)",
        (name, mill_id, total_capacity, 0.0, storage_rate)
    )
    commit()

def update_godown(godown_id, name, mill_id, total_capacity, current_stock, storage_rate):
    cur = get_connection().cursor()
    cur.execute(
        "UPDATE godowns SET name=?, mill_id=?, total_capacity=?, current_stock=?, storage_rate=? WHERE id=?",
        (name, mill_id, total_capacity, current_stock, storage_rate, godown_id)
    )
    commit()

def update_godown_stock(godown_id, quantity_change):
    """Add or subtract stock from a godown."""
    cur = get_connection().cursor()
    cur.execute("UPDATE godowns SET current_stock = current_stock + ? WHERE id=?",
                (quantity_change, godown_id))
    commit()

def delete_godown(godown_id):
    _delete_by_id("godowns", godown_id)


# ─────────────────────────────────────────────
# GODOWN ENTRIES
# ─────────────────────────────────────────────

def get_all_godown_entries():
    return _fetch_all("godown_entries")

def get_godown_entry(entry_id):
    return _fetch_by_id("godown_entries", entry_id)

def add_godown_entry(godown_id, party_id, product_id, quantity, unit, from_date, to_date, storage_rate, total_charges):
    cur = get_connection().cursor()
    cur.execute(
        """INSERT INTO godown_entries (godown_id, party_id, product_id, quantity, unit, from_date, to_date, storage_rate, total_charges)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (godown_id, party_id, product_id, quantity, unit, from_date, to_date, storage_rate, total_charges)
    )
    # Update godown stock
    update_godown_stock(godown_id, quantity)
    commit()

def delete_godown_entry(entry_id):
    # Get entry details first to reverse stock change
    entry = get_godown_entry(entry_id)
    if entry:
        update_godown_stock(entry[1], -entry[4])  # Reverse the quantity
    _delete_by_id("godown_entries", entry_id)


# ─────────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────────

def get_all_products():
    return _fetch_all("products")

def get_product(product_id):
    return _fetch_by_id("products", product_id)

def get_product_names():
    return _get_names_dict("products")

def add_product(name, category_id):
    cur = get_connection().cursor()
    cur.execute("INSERT INTO products (name, category_id) VALUES (?,?)", (name, category_id))
    commit()

def update_product(product_id, name, category_id):
    cur = get_connection().cursor()
    cur.execute("UPDATE products SET name=?, category_id=? WHERE id=?", (name, category_id, product_id))
    commit()

def delete_product(product_id):
    _delete_by_id("products", product_id)


# ─────────────────────────────────────────────
# PARTIES
# ─────────────────────────────────────────────

PARTY_TYPES = ["Customer", "Supplier", "Broker"]

def get_all_parties():
    return _fetch_all("parties")

def get_party(party_id):
    return _fetch_by_id("parties", party_id)

def get_party_names():
    return _get_names_dict("parties")

def add_party(name, party_type):
    cur = get_connection().cursor()
    cur.execute("INSERT INTO parties (name, type) VALUES (?,?)", (name, party_type))
    commit()

def update_party(party_id, name, party_type):
    cur = get_connection().cursor()
    cur.execute("UPDATE parties SET name=?, type=? WHERE id=?", (name, party_type, party_id))
    commit()

def delete_party(party_id):
    _delete_by_id("parties", party_id)


# ─────────────────────────────────────────────
# PURCHASES
# ─────────────────────────────────────────────

def get_all_purchases():
    return _fetch_all("purchases")

def get_purchase(purchase_id):
    return _fetch_by_id("purchases", purchase_id)

def add_purchase(party_id, product_id, quantity, unit, rate, gst_percent):
    subtotal = quantity * rate
    gst_amount = subtotal * (gst_percent / 100)
    total = subtotal + gst_amount
    cur = get_connection().cursor()
    cur.execute(
        """INSERT INTO purchases (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total, date)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total,
         datetime.now().strftime("%Y-%m-%d"))
    )
    commit()

def update_purchase(purchase_id, party_id, product_id, quantity, unit, rate, gst_percent):
    subtotal = quantity * rate
    gst_amount = subtotal * (gst_percent / 100)
    total = subtotal + gst_amount
    cur = get_connection().cursor()
    cur.execute(
        """UPDATE purchases SET party_id=?, product_id=?, quantity=?, unit=?, rate=?,
           subtotal=?, gst_percent=?, gst_amount=?, total=? WHERE id=?""",
        (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total, purchase_id)
    )
    commit()

def delete_purchase(purchase_id):
    _delete_by_id("purchases", purchase_id)


# ─────────────────────────────────────────────
# SALES
# ─────────────────────────────────────────────

def get_all_sales():
    return _fetch_all("sales")

def get_sale(sale_id):
    return _fetch_by_id("sales", sale_id)

def add_sale(party_id, product_id, quantity, unit, rate, gst_percent):
    subtotal = quantity * rate
    gst_amount = subtotal * (gst_percent / 100)
    total = subtotal + gst_amount
    cur = get_connection().cursor()
    cur.execute(
        """INSERT INTO sales (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total, date)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total,
         datetime.now().strftime("%Y-%m-%d"))
    )
    commit()

def update_sale(sale_id, party_id, product_id, quantity, unit, rate, gst_percent):
    subtotal = quantity * rate
    gst_amount = subtotal * (gst_percent / 100)
    total = subtotal + gst_amount
    cur = get_connection().cursor()
    cur.execute(
        """UPDATE sales SET party_id=?, product_id=?, quantity=?, unit=?, rate=?,
           subtotal=?, gst_percent=?, gst_amount=?, total=? WHERE id=?""",
        (party_id, product_id, quantity, unit, rate, subtotal, gst_percent, gst_amount, total, sale_id)
    )
    commit()

def delete_sale(sale_id):
    _delete_by_id("sales", sale_id)


# ─────────────────────────────────────────────
# PROCESSING
# ─────────────────────────────────────────────

def get_all_processing():
    return _fetch_all("processing")

def get_processing(proc_id):
    return _fetch_by_id("processing", proc_id)

def add_processing(batch_no, input_product, output_product, quantity, unit):
    cur = get_connection().cursor()
    cur.execute(
        """INSERT INTO processing (batch_no, input_product, output_product, quantity, unit, date)
           VALUES (?,?,?,?,?,?)""",
        (batch_no, input_product, output_product, quantity, unit,
         datetime.now().strftime("%Y-%m-%d"))
    )
    commit()

def update_processing(proc_id, batch_no, input_product, output_product, quantity, unit):
    cur = get_connection().cursor()
    cur.execute(
        """UPDATE processing SET batch_no=?, input_product=?, output_product=?, quantity=?, unit=? WHERE id=?""",
        (batch_no, input_product, output_product, quantity, unit, proc_id)
    )
    commit()

def delete_processing(proc_id):
    _delete_by_id("processing", proc_id)


# ─────────────────────────────────────────────
# STAFF
# ─────────────────────────────────────────────

PAYOUT_TYPES = ["Daily", "Weekly", "Monthly", "Contract"]

def get_all_staff():
    return _fetch_all("staff")

def get_staff_member(staff_id):
    return _fetch_by_id("staff", staff_id)

def add_staff_member(name, payout_type, salary):
    cur = get_connection().cursor()
    cur.execute("INSERT INTO staff (name, payout_type, salary) VALUES (?,?,?)",
                (name, payout_type, salary))
    commit()

def update_staff_member(staff_id, name, payout_type, salary):
    cur = get_connection().cursor()
    cur.execute("UPDATE staff SET name=?, payout_type=?, salary=? WHERE id=?",
                (name, payout_type, salary, staff_id))
    commit()

def delete_staff_member(staff_id):
    _delete_by_id("staff", staff_id)


# ─────────────────────────────────────────────
# VEHICLES
# ─────────────────────────────────────────────

VEHICLE_TYPES = ["Truck", "Pickup", "Tractor", "6-Wheeler"]

def get_all_vehicles():
    return _fetch_all("vehicles")

def get_vehicle(vehicle_id):
    return _fetch_by_id("vehicles", vehicle_id)

def add_vehicle(vehicle_no, driver, vehicle_type, empty_weight, loaded_weight):
    cur = get_connection().cursor()
    cur.execute(
        "INSERT INTO vehicles (vehicle_no, driver, vehicle_type, empty_weight, loaded_weight) VALUES (?,?,?,?,?)",
        (vehicle_no, driver, vehicle_type, empty_weight, loaded_weight)
    )
    commit()

def update_vehicle(vehicle_id, vehicle_no, driver, vehicle_type, empty_weight, loaded_weight):
    cur = get_connection().cursor()
    cur.execute(
        "UPDATE vehicles SET vehicle_no=?, driver=?, vehicle_type=?, empty_weight=?, loaded_weight=? WHERE id=?",
        (vehicle_no, driver, vehicle_type, empty_weight, loaded_weight, vehicle_id)
    )
    commit()

def delete_vehicle(vehicle_id):
    _delete_by_id("vehicles", vehicle_id)


# ─────────────────────────────────────────────
# COMPANY INFO
# ─────────────────────────────────────────────

def get_all_companies():
    return _fetch_all("company_info")

def get_company(company_id):
    return _fetch_by_id("company_info", company_id)

def get_default_company():
    """Get the first company (default)."""
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM company_info WHERE id=1")
    return cur.fetchone()

def add_company(company_name, gst_number, rst_number, contact_number, address):
    cur = get_connection().cursor()
    cur.execute(
        """INSERT INTO company_info (company_name, gst_number, rst_number, contact_number, address)
           VALUES (?,?,?,?,?)""",
        (company_name, gst_number, rst_number, contact_number, address)
    )
    commit()

def update_company(company_id, company_name, gst_number, rst_number, contact_number, address):
    cur = get_connection().cursor()
    cur.execute(
        """UPDATE company_info SET company_name=?, gst_number=?, rst_number=?, contact_number=?, address=? WHERE id=?""",
        (company_name, gst_number, rst_number, contact_number, address, company_id)
    )
    commit()

def delete_company(company_id):
    _delete_by_id("company_info", company_id)


# ─────────────────────────────────────────────
# BANK ACCOUNTS
# ─────────────────────────────────────────────

def get_all_bank_accounts():
    return _fetch_all("bank_accounts")

def get_bank_account(account_id):
    return _fetch_by_id("bank_accounts", account_id)

def add_bank_account(bank_name, account_no, ifsc_code):
    cur = get_connection().cursor()
    cur.execute(
        "INSERT INTO bank_accounts (bank_name, account_no, ifsc_code, balance) VALUES (?,?,?,?)",
        (bank_name, account_no, ifsc_code, 0.0)
    )
    commit()

def delete_bank_account(account_id):
    _delete_by_id("bank_accounts", account_id)


# ─────────────────────────────────────────────
# DASHBOARD STATS
# ─────────────────────────────────────────────

def get_dashboard_stats():
    """Get counts for the dashboard summary cards."""
    cur = get_connection().cursor()
    stats = {}
    for table in ["mills", "godowns", "products", "parties", "purchases", "sales", "staff", "vehicles"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cur.fetchone()[0]

    # Total purchase and sale amounts
    cur.execute("SELECT COALESCE(SUM(total), 0) FROM purchases")
    stats["total_purchases"] = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(total), 0) FROM sales")
    stats["total_sales"] = cur.fetchone()[0]

    return stats
