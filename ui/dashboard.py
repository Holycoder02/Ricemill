"""
Main dashboard for Rice Mill ERP.

Contains the dashboard layout, stat cards, and all form/view handlers that
wire up the generic components to specific database operations.
"""

from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from ui.theme import Colors, Fonts, Spacing, BUTTON_THEMES, apply_theme
from ui.components import DataTableView, FormDialog, StatCard, SectionFrame
from ui.invoice import open_sale_invoice, open_purchase_invoice
from db import models
from utils.validators import is_positive_number, is_non_negative_number, safe_float, safe_int
from utils.formatters import format_currency


# ═══════════════════════════════════════════════════════
# FORM HANDLERS (Add / Edit for each module)
# ═══════════════════════════════════════════════════════

def _open_add_mill(parent):
    FormDialog(parent, "Add Mill", [
        {"label": "Mill Name", "key": "name", "type": "entry", "required": True},
    ], lambda v: models.add_mill(v["name"]))


def _open_edit_mill(mill_id, parent, refresh):
    row = models.get_mill(int(mill_id))
    if not row:
        return
    FormDialog(parent, f"Edit Mill — {row[1]}", [
        {"label": "Mill Name", "key": "name", "type": "entry", "required": True},
    ], lambda v: (models.update_mill(int(mill_id), v["name"]), refresh()),
        initial_values={"name": row[1]})


def _open_add_category(parent):
    FormDialog(parent, "Add Category", [
        {"label": "Category Name", "key": "name", "type": "entry", "required": True},
    ], lambda v: models.add_category(v["name"]))


def _open_edit_category(cat_id, parent, refresh):
    row = models.get_category(int(cat_id))
    if not row:
        return
    FormDialog(parent, f"Edit Category — {row[1]}", [
        {"label": "Category Name", "key": "name", "type": "entry", "required": True},
    ], lambda v: (models.update_category(int(cat_id), v["name"]), refresh()),
        initial_values={"name": row[1]})


def _open_add_godown(parent):
    mill_names = models.get_mill_names()
    mill_options = [f"{mid}: {name}" for mid, name in mill_names.items()]
    FormDialog(parent, "Add Godown", [
        {"label": "Godown Name", "key": "name", "type": "entry", "required": True},
        {"label": "Mill", "key": "mill", "type": "combo", "options": mill_options, "required": True},
        {"label": "Total Capacity (Kg)", "key": "capacity", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "Storage Rate (₹/Kg/Day)", "key": "rate", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_godown(
        v["name"], int(v["mill"].split(":")[0]),
        safe_float(v["capacity"]), safe_float(v["rate"])
    ))


def _open_edit_godown(godown_id, parent, refresh):
    row = models.get_godown(int(godown_id))
    if not row:
        return
    mill_names = models.get_mill_names()
    mill_options = [f"{mid}: {name}" for mid, name in mill_names.items()]
    current_mill = f"{row[2]}: {mill_names.get(row[2], 'N/A')}"
    FormDialog(parent, f"Edit Godown — {row[1]}", [
        {"label": "Godown Name", "key": "name", "type": "entry", "required": True},
        {"label": "Mill", "key": "mill", "type": "combo", "options": mill_options, "required": True,
         "default": current_mill},
        {"label": "Total Capacity (Kg)", "key": "capacity", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "Current Stock (Kg)", "key": "stock", "type": "entry", "required": True,
         "validate": is_non_negative_number},
        {"label": "Storage Rate (₹/Kg/Day)", "key": "rate", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: (models.update_godown(
        int(godown_id), v["name"], int(v["mill"].split(":")[0]),
        safe_float(v["capacity"]), safe_float(v["stock"]), safe_float(v["rate"])
    ), refresh()),
        initial_values={"name": row[1], "mill": current_mill,
                         "capacity": row[3], "stock": row[4], "rate": row[5]})


def _open_add_product(parent):
    cat_names = models.get_category_names()
    cat_options = [f"{cid}: {name}" for cid, name in cat_names.items()]
    if not cat_options:
        cat_options = ["(No categories — add one first)"]
    FormDialog(parent, "Add Product", [
        {"label": "Product Name", "key": "name", "type": "entry", "required": True},
        {"label": "Category", "key": "category", "type": "combo", "options": cat_options, "required": True},
    ], lambda v: models.add_product(v["name"], safe_int(v["category"].split(":")[0])))


def _open_edit_product(product_id, parent, refresh):
    row = models.get_product(int(product_id))
    if not row:
        return
    cat_names = models.get_category_names()
    cat_options = [f"{cid}: {name}" for cid, name in cat_names.items()]
    current_cat = f"{row[2]}: {cat_names.get(row[2], 'N/A')}"
    FormDialog(parent, f"Edit Product — {row[1]}", [
        {"label": "Product Name", "key": "name", "type": "entry", "required": True},
        {"label": "Category", "key": "category", "type": "combo", "options": cat_options, "required": True,
         "default": current_cat},
    ], lambda v: (models.update_product(int(product_id), v["name"],
                                          safe_int(v["category"].split(":")[0])), refresh()),
        initial_values={"name": row[1], "category": current_cat})


def _open_add_party(parent):
    FormDialog(parent, "Add Party", [
        {"label": "Party Name", "key": "name", "type": "entry", "required": True},
        {"label": "Type", "key": "type", "type": "combo",
         "options": models.PARTY_TYPES, "default": "Customer", "required": True},
    ], lambda v: models.add_party(v["name"], v["type"]))


def _open_edit_party(party_id, parent, refresh):
    row = models.get_party(int(party_id))
    if not row:
        return
    FormDialog(parent, f"Edit Party — {row[1]}", [
        {"label": "Party Name", "key": "name", "type": "entry", "required": True},
        {"label": "Type", "key": "type", "type": "combo",
         "options": models.PARTY_TYPES, "default": row[2], "required": True},
    ], lambda v: (models.update_party(int(party_id), v["name"], v["type"]), refresh()),
        initial_values={"name": row[1], "type": row[2]})


def _open_purchase_entry(parent):
    party_names = models.get_party_names()
    product_names = models.get_product_names()
    party_options = [f"{pid}: {name}" for pid, name in party_names.items()]
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    from utils.formatters import WEIGHT_UNITS
    FormDialog(parent, "Purchase Entry", [
        {"label": "Party", "key": "party", "type": "combo", "options": party_options, "required": True},
        {"label": "Product", "key": "product", "type": "combo", "options": product_options, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": "Kg", "required": True},
        {"label": "Rate (₹ per unit)", "key": "rate", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "GST %", "key": "gst", "type": "entry", "default": "18", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_purchase(
        safe_int(v["party"].split(":")[0]), safe_int(v["product"].split(":")[0]),
        safe_float(v["qty"]), v["unit"], safe_float(v["rate"]), safe_float(v["gst"])
    ))


def _open_edit_purchase(purchase_id, parent, refresh):
    row = models.get_purchase(int(purchase_id))
    if not row:
        return
    party_names = models.get_party_names()
    product_names = models.get_product_names()
    party_options = [f"{pid}: {name}" for pid, name in party_names.items()]
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    current_party = f"{row[1]}: {party_names.get(row[1], 'N/A')}"
    current_product = f"{row[2]}: {product_names.get(row[2], 'N/A')}"
    from utils.formatters import WEIGHT_UNITS
    FormDialog(parent, f"Edit Purchase #{purchase_id}", [
        {"label": "Party", "key": "party", "type": "combo", "options": party_options,
         "default": current_party, "required": True},
        {"label": "Product", "key": "product", "type": "combo", "options": product_options,
         "default": current_product, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": row[4], "required": True},
        {"label": "Rate (₹ per unit)", "key": "rate", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "GST %", "key": "gst", "type": "entry", "required": True, "validate": is_non_negative_number},
    ], lambda v: (models.update_purchase(
        int(purchase_id), safe_int(v["party"].split(":")[0]), safe_int(v["product"].split(":")[0]),
        safe_float(v["qty"]), v["unit"], safe_float(v["rate"]), safe_float(v["gst"])
    ), refresh()),
        initial_values={"party": current_party, "product": current_product,
                         "qty": row[3], "unit": row[4], "rate": row[5], "gst": row[7]})


def _open_sale_entry(parent):
    party_names = models.get_party_names()
    product_names = models.get_product_names()
    party_options = [f"{pid}: {name}" for pid, name in party_names.items()]
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    from utils.formatters import WEIGHT_UNITS
    FormDialog(parent, "Sale Entry", [
        {"label": "Party", "key": "party", "type": "combo", "options": party_options, "required": True},
        {"label": "Product", "key": "product", "type": "combo", "options": product_options, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": "Kg", "required": True},
        {"label": "Rate (₹ per unit)", "key": "rate", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "GST %", "key": "gst", "type": "entry", "default": "18", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_sale(
        safe_int(v["party"].split(":")[0]), safe_int(v["product"].split(":")[0]),
        safe_float(v["qty"]), v["unit"], safe_float(v["rate"]), safe_float(v["gst"])
    ))


def _open_edit_sale(sale_id, parent, refresh):
    row = models.get_sale(int(sale_id))
    if not row:
        return
    party_names = models.get_party_names()
    product_names = models.get_product_names()
    party_options = [f"{pid}: {name}" for pid, name in party_names.items()]
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    current_party = f"{row[1]}: {party_names.get(row[1], 'N/A')}"
    current_product = f"{row[2]}: {product_names.get(row[2], 'N/A')}"
    from utils.formatters import WEIGHT_UNITS
    FormDialog(parent, f"Edit Sale #{sale_id}", [
        {"label": "Party", "key": "party", "type": "combo", "options": party_options,
         "default": current_party, "required": True},
        {"label": "Product", "key": "product", "type": "combo", "options": product_options,
         "default": current_product, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": row[4], "required": True},
        {"label": "Rate (₹ per unit)", "key": "rate", "type": "entry", "required": True,
         "validate": is_positive_number},
        {"label": "GST %", "key": "gst", "type": "entry", "required": True, "validate": is_non_negative_number},
    ], lambda v: (models.update_sale(
        int(sale_id), safe_int(v["party"].split(":")[0]), safe_int(v["product"].split(":")[0]),
        safe_float(v["qty"]), v["unit"], safe_float(v["rate"]), safe_float(v["gst"])
    ), refresh()),
        initial_values={"party": current_party, "product": current_product,
                         "qty": row[3], "unit": row[4], "rate": row[5], "gst": row[7]})


def _open_processing_entry(parent):
    product_names = models.get_product_names()
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    from utils.formatters import WEIGHT_UNITS
    FormDialog(parent, "Processing Batch", [
        {"label": "Batch No", "key": "batch", "type": "entry", "required": True},
        {"label": "Input Product", "key": "input", "type": "combo", "options": product_options, "required": True},
        {"label": "Output Product", "key": "output", "type": "combo", "options": product_options, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": "Kg", "required": True},
    ], lambda v: models.add_processing(
        v["batch"], safe_int(v["input"].split(":")[0]), safe_int(v["output"].split(":")[0]),
        safe_float(v["qty"]), v["unit"]
    ))


def _open_add_staff(parent):
    FormDialog(parent, "Add Staff", [
        {"label": "Name", "key": "name", "type": "entry", "required": True},
        {"label": "Payout Type", "key": "payout", "type": "combo",
         "options": models.PAYOUT_TYPES, "default": "Monthly", "required": True},
        {"label": "Salary (₹)", "key": "salary", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_staff_member(v["name"], v["payout"], safe_float(v["salary"])))


def _open_edit_staff(staff_id, parent, refresh):
    row = models.get_staff_member(int(staff_id))
    if not row:
        return
    FormDialog(parent, f"Edit Staff — {row[1]}", [
        {"label": "Name", "key": "name", "type": "entry", "required": True},
        {"label": "Payout Type", "key": "payout", "type": "combo",
         "options": models.PAYOUT_TYPES, "default": row[2], "required": True},
        {"label": "Salary (₹)", "key": "salary", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: (models.update_staff_member(int(staff_id), v["name"], v["payout"],
                                               safe_float(v["salary"])), refresh()),
        initial_values={"name": row[1], "payout": row[2], "salary": row[3]})


def _open_add_vehicle(parent):
    FormDialog(parent, "Add Vehicle", [
        {"label": "Vehicle No", "key": "vno", "type": "entry", "required": True},
        {"label": "Driver Name", "key": "driver", "type": "entry", "required": True},
        {"label": "Vehicle Type", "key": "type", "type": "combo",
         "options": models.VEHICLE_TYPES, "default": "Truck", "required": True},
        {"label": "Empty Weight (Kg)", "key": "empty", "type": "entry", "required": True,
         "validate": is_non_negative_number},
        {"label": "Loaded Weight (Kg)", "key": "loaded", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_vehicle(
        v["vno"], v["driver"], v["type"], safe_float(v["empty"]), safe_float(v["loaded"])
    ))


def _open_edit_vehicle(vehicle_id, parent, refresh):
    row = models.get_vehicle(int(vehicle_id))
    if not row:
        return
    FormDialog(parent, f"Edit Vehicle — {row[1]}", [
        {"label": "Vehicle No", "key": "vno", "type": "entry", "required": True},
        {"label": "Driver Name", "key": "driver", "type": "entry", "required": True},
        {"label": "Vehicle Type", "key": "type", "type": "combo",
         "options": models.VEHICLE_TYPES, "default": row[3], "required": True},
        {"label": "Empty Weight (Kg)", "key": "empty", "type": "entry", "required": True,
         "validate": is_non_negative_number},
        {"label": "Loaded Weight (Kg)", "key": "loaded", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: (models.update_vehicle(int(vehicle_id), v["vno"], v["driver"], v["type"],
                                          safe_float(v["empty"]), safe_float(v["loaded"])), refresh()),
        initial_values={"vno": row[1], "driver": row[2], "type": row[3],
                         "empty": row[4], "loaded": row[5]})


def _open_add_godown_entry(parent):
    godown_names = models.get_godown_names()
    party_names = models.get_party_names()
    product_names = models.get_product_names()
    godown_options = [f"{gid}: {name}" for gid, name in godown_names.items()]
    party_options = [f"{pid}: {name}" for pid, name in party_names.items()]
    product_options = [f"{pid}: {name}" for pid, name in product_names.items()]
    from utils.formatters import WEIGHT_UNITS
    today = datetime.now().strftime("%Y-%m-%d")
    FormDialog(parent, "Add Godown Entry", [
        {"label": "Godown", "key": "godown", "type": "combo", "options": godown_options, "required": True},
        {"label": "Party", "key": "party", "type": "combo", "options": party_options, "required": True},
        {"label": "Product", "key": "product", "type": "combo", "options": product_options, "required": True},
        {"label": "Quantity", "key": "qty", "type": "entry", "required": True, "validate": is_positive_number},
        {"label": "Unit", "key": "unit", "type": "combo", "options": WEIGHT_UNITS, "default": "Kg", "required": True},
        {"label": "From Date (YYYY-MM-DD)", "key": "from_date", "type": "entry", "default": today, "required": True},
        {"label": "To Date (YYYY-MM-DD)", "key": "to_date", "type": "entry", "required": False},
        {"label": "Storage Rate (₹/Kg/Day)", "key": "rate", "type": "entry", "required": True,
         "validate": is_non_negative_number},
    ], lambda v: models.add_godown_entry(
        safe_int(v["godown"].split(":")[0]), safe_int(v["party"].split(":")[0]),
        safe_int(v["product"].split(":")[0]), safe_float(v["qty"]), v["unit"],
        v["from_date"], v.get("to_date", ""), safe_float(v["rate"]),
        0.0  # total_charges computed later or manually
    ))


def _open_add_company(parent):
    FormDialog(parent, "Add Company", [
        {"label": "Company Name", "key": "name", "type": "entry", "required": True},
        {"label": "GST Number", "key": "gst", "type": "entry", "required": False},
        {"label": "RST / Registration No", "key": "rst", "type": "entry", "required": False},
        {"label": "Contact Number", "key": "contact", "type": "entry", "required": False},
        {"label": "Address", "key": "address", "type": "text", "required": False},
    ], lambda v: models.add_company(v["name"], v["gst"], v["rst"], v["contact"], v["address"]))


def _open_edit_company(company_id, parent, refresh):
    row = models.get_company(int(company_id))
    if not row:
        return
    FormDialog(parent, f"Edit Company — {row[1]}", [
        {"label": "Company Name", "key": "name", "type": "entry", "required": True},
        {"label": "GST Number", "key": "gst", "type": "entry", "required": False},
        {"label": "RST / Registration No", "key": "rst", "type": "entry", "required": False},
        {"label": "Contact Number", "key": "contact", "type": "entry", "required": False},
        {"label": "Address", "key": "address", "type": "text", "required": False},
    ], lambda v: (models.update_company(int(company_id), v["name"], v["gst"], v["rst"],
                                          v["contact"], v["address"]), refresh()),
        initial_values={"name": row[1], "gst": row[2], "rst": row[3],
                         "contact": row[4], "address": row[5]})


def _open_add_bank(parent):
    FormDialog(parent, "Add Bank Account", [
        {"label": "Bank Name", "key": "bank", "type": "entry", "required": True},
        {"label": "Account Number", "key": "account", "type": "entry", "required": True},
        {"label": "IFSC Code", "key": "ifsc", "type": "entry", "required": True},
    ], lambda v: models.add_bank_account(v["bank"], v["account"], v["ifsc"]))


# ═══════════════════════════════════════════════════════
# VIEW HANDLERS (open DataTableView with proper columns)
# ═══════════════════════════════════════════════════════

def _view_mills(dashboard, role):
    DataTableView(dashboard, "View Mills",
                  [("id", "ID", 50), ("name", "Name", 300)],
                  models.get_all_mills, role,
                  on_edit=_open_edit_mill, on_delete=models.delete_mill,
                  on_add=lambda: _open_add_mill(dashboard), width=500, height=450)


def _view_categories(dashboard, role):
    DataTableView(dashboard, "View Categories",
                  [("id", "ID", 50), ("name", "Name", 300)],
                  models.get_all_categories, role,
                  on_edit=_open_edit_category, on_delete=models.delete_category,
                  on_add=lambda: _open_add_category(dashboard), width=500, height=450)


def _view_godowns(dashboard, role):
    mill_names = models.get_mill_names()

    def fmt(row):
        return (row[0], row[1], mill_names.get(row[2], f"#{row[2]}"),
                f"{row[3]:,.2f}", f"{row[4]:,.2f}", f"₹ {row[5]:.2f}")

    DataTableView(dashboard, "View Godowns",
                  [("id", "ID", 40), ("name", "Name", 140), ("mill", "Mill", 120),
                   ("capacity", "Capacity (Kg)", 120), ("stock", "Current Stock (Kg)", 130),
                   ("rate", "Rate/Kg/Day", 100)],
                  models.get_all_godowns, role,
                  on_edit=_open_edit_godown, on_delete=models.delete_godown,
                  on_add=lambda: _open_add_godown(dashboard), width=750, format_row=fmt)


def _view_godown_entries(dashboard, role):
    godown_names = models.get_godown_names()
    party_names = models.get_party_names()
    product_names = models.get_product_names()

    def fmt(row):
        return (row[0], godown_names.get(row[1], f"#{row[1]}"),
                party_names.get(row[2], f"#{row[2]}"),
                product_names.get(row[3], f"#{row[3]}"),
                f"{row[4]:,.2f}", row[5], row[6], row[7] or "—",
                f"₹ {row[8]:.2f}" if row[8] else "—",
                format_currency(row[9]) if row[9] else "—")

    DataTableView(dashboard, "View Godown Entries",
                  [("id", "ID", 40), ("godown", "Godown", 100), ("party", "Party", 100),
                   ("product", "Product", 100), ("qty", "Qty", 70), ("unit", "Unit", 50),
                   ("from", "From Date", 90), ("to", "To Date", 90),
                   ("rate", "Rate/Kg/Day", 90), ("charges", "Total Charges", 100)],
                  models.get_all_godown_entries, role,
                  on_delete=models.delete_godown_entry,
                  on_add=lambda: _open_add_godown_entry(dashboard),
                  width=1000, format_row=fmt)


def _view_products(dashboard, role):
    cat_names = models.get_category_names()

    def fmt(row):
        return (row[0], row[1], cat_names.get(row[2], f"#{row[2]}"))

    DataTableView(dashboard, "View Products",
                  [("id", "ID", 50), ("name", "Name", 250), ("category", "Category", 150)],
                  models.get_all_products, role,
                  on_edit=_open_edit_product, on_delete=models.delete_product,
                  on_add=lambda: _open_add_product(dashboard), width=550, format_row=fmt)


def _view_parties(dashboard, role):
    DataTableView(dashboard, "View Parties",
                  [("id", "ID", 50), ("name", "Name", 250), ("type", "Type", 120)],
                  models.get_all_parties, role,
                  on_edit=_open_edit_party, on_delete=models.delete_party,
                  on_add=lambda: _open_add_party(dashboard), width=500)


def _view_purchases(dashboard, role):
    party_names = models.get_party_names()
    product_names = models.get_product_names()

    def fmt(row):
        return (row[0], party_names.get(row[1], f"#{row[1]}"),
                product_names.get(row[2], f"#{row[2]}"),
                f"{row[3]:,.2f}", row[4], f"₹ {row[5]:,.2f}",
                format_currency(row[6]), f"{row[7]:.1f}%",
                format_currency(row[8]), format_currency(row[9]), row[10])

    DataTableView(dashboard, "View Purchases",
                  [("id", "ID", 35), ("party", "Party", 100), ("product", "Product", 100),
                   ("qty", "Qty", 60), ("unit", "Unit", 50), ("rate", "Rate", 80),
                   ("subtotal", "Subtotal", 90), ("gst", "GST%", 55),
                   ("gst_amt", "GST Amt", 85), ("total", "Total", 100), ("date", "Date", 85)],
                  models.get_all_purchases, role,
                  on_edit=_open_edit_purchase, on_delete=models.delete_purchase,
                  width=1050, format_row=fmt)


def _view_sales(dashboard, role):
    party_names = models.get_party_names()
    product_names = models.get_product_names()

    def fmt(row):
        return (row[0], party_names.get(row[1], f"#{row[1]}"),
                product_names.get(row[2], f"#{row[2]}"),
                f"{row[3]:,.2f}", row[4], f"₹ {row[5]:,.2f}",
                format_currency(row[6]), f"{row[7]:.1f}%",
                format_currency(row[8]), format_currency(row[9]), row[10])

    DataTableView(dashboard, "View Sales",
                  [("id", "ID", 35), ("party", "Party", 100), ("product", "Product", 100),
                   ("qty", "Qty", 60), ("unit", "Unit", 50), ("rate", "Rate", 80),
                   ("subtotal", "Subtotal", 90), ("gst", "GST%", 55),
                   ("gst_amt", "GST Amt", 85), ("total", "Total", 100), ("date", "Date", 85)],
                  models.get_all_sales, role,
                  on_edit=_open_edit_sale, on_delete=models.delete_sale,
                  width=1050, format_row=fmt)


def _view_processing(dashboard, role):
    product_names = models.get_product_names()

    def fmt(row):
        return (row[0], row[1],
                product_names.get(row[2], f"#{row[2]}"),
                product_names.get(row[3], f"#{row[3]}"),
                f"{row[4]:,.2f}", row[5], row[6])

    DataTableView(dashboard, "View Processing Batches",
                  [("id", "ID", 40), ("batch", "Batch No", 100),
                   ("input", "Input Product", 130), ("output", "Output Product", 130),
                   ("qty", "Qty", 80), ("unit", "Unit", 60), ("date", "Date", 90)],
                  models.get_all_processing, role,
                  on_delete=models.delete_processing,
                  width=750, format_row=fmt)


def _view_staff(dashboard, role):
    def fmt(row):
        return (row[0], row[1], row[2], format_currency(row[3]))

    DataTableView(dashboard, "View Staff",
                  [("id", "ID", 40), ("name", "Name", 200),
                   ("payout", "Payout Type", 120), ("salary", "Salary", 120)],
                  models.get_all_staff, role,
                  on_edit=_open_edit_staff, on_delete=models.delete_staff_member,
                  on_add=lambda: _open_add_staff(dashboard), width=550, format_row=fmt)


def _view_vehicles(dashboard, role):
    def fmt(row):
        payload = (row[5] - row[4]) if row[4] and row[5] else 0
        return (row[0], row[1], row[2], row[3],
                f"{row[4]:,.2f}", f"{row[5]:,.2f}", f"{payload:,.2f}")

    DataTableView(dashboard, "View Vehicles",
                  [("id", "ID", 40), ("vno", "Vehicle No", 100), ("driver", "Driver", 120),
                   ("type", "Type", 80), ("empty", "Empty Wt (Kg)", 110),
                   ("loaded", "Loaded Wt (Kg)", 110), ("payload", "Payload (Kg)", 100)],
                  models.get_all_vehicles, role,
                  on_edit=_open_edit_vehicle, on_delete=models.delete_vehicle,
                  on_add=lambda: _open_add_vehicle(dashboard), width=750, format_row=fmt)


def _view_companies(dashboard, role):
    DataTableView(dashboard, "View Companies",
                  [("id", "ID", 40), ("name", "Company Name", 200),
                   ("gst", "GST Number", 160), ("rst", "RST Number", 120),
                   ("contact", "Contact", 120)],
                  models.get_all_companies, role,
                  on_edit=_open_edit_company, on_delete=models.delete_company,
                  on_add=lambda: _open_add_company(dashboard), width=750)


def _view_bank_accounts(dashboard, role):
    DataTableView(dashboard, "View Bank Accounts",
                  [("id", "ID", 40), ("bank", "Bank Name", 200),
                   ("account", "Account No", 200), ("ifsc", "IFSC Code", 130)],
                  models.get_all_bank_accounts, role,
                  on_delete=models.delete_bank_account,
                  on_add=lambda: _open_add_bank(dashboard), width=650)


# ═══════════════════════════════════════════════════════
# MAIN DASHBOARD CLASS
# ═══════════════════════════════════════════════════════

class Dashboard:
    """The main application dashboard."""

    def __init__(self, role):
        self.role = role

        self.root = Tk()
        self.root.title("Rice Mill ERP — Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg=Colors.BG_PAGE)
        self.root.state("zoomed")
        apply_theme(self.root)

        # Confirm before closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

    def _build_ui(self):
        """Build the complete dashboard UI."""

        # ── HEADER ──
        header = Frame(self.root, bg=Colors.BG_DARK, height=90)
        header.pack(fill=X)
        header.pack_propagate(False)

        left = Frame(header, bg=Colors.BG_DARK)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=Spacing.XXL, pady=Spacing.MD)

        Label(left, text="🌾  Rice Mill ERP", font=Fonts.TITLE,
              bg=Colors.BG_DARK, fg=Colors.TEXT_PRIMARY).pack(anchor=W)
        Label(left, text=f"Logged in as {self.role}", font=Fonts.SMALL,
              bg=Colors.BG_DARK, fg=Colors.TEXT_SECONDARY).pack(anchor=W, pady=(2, 0))

        right = Frame(header, bg=Colors.BG_DARK)
        right.pack(side=RIGHT, fill=Y, padx=Spacing.XXL)

        now = datetime.now()
        Label(right, text=now.strftime("%A, %B %d, %Y"), font=Fonts.SMALL,
              bg=Colors.BG_DARK, fg=Colors.TEXT_SECONDARY).pack(anchor=E, pady=(12, 0))
        Label(right, text=f"Role: {self.role}", font=Fonts.BODY_BOLD,
              bg=Colors.BG_DARK, fg=Colors.TEXT_ACCENT).pack(anchor=E, pady=(4, 0))

        # Logout button
        Button(right, text="🚪 Logout", command=self._logout,
               bg=Colors.DANGER, fg="white", font=Fonts.BUTTON_SM,
               relief=FLAT, bd=0, padx=14, pady=4, cursor="hand2").pack(anchor=E, pady=(6, 0))

        # ── SCROLLABLE CONTENT ──
        canvas = Canvas(self.root, bg=Colors.BG_PAGE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=canvas.yview)
        self.scroll_frame = Frame(canvas, bg=Colors.BG_PAGE)

        self.scroll_frame.bind("<Configure>",
                                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ── STATS CARDS ──
        self._build_stats()

        # ── ACTION SECTIONS ──
        self._build_add_section()
        self._build_view_section()
        self._build_invoice_section()
        self._build_settings_section()

    def _build_stats(self):
        """Build the dashboard statistics cards."""
        stats = models.get_dashboard_stats()

        stats_frame = Frame(self.scroll_frame, bg=Colors.BG_PAGE, padx=Spacing.XL, pady=Spacing.MD)
        stats_frame.pack(fill=X)

        cards = [
            ("Mills", stats.get("mills", 0), "🏭", Colors.PRIMARY),
            ("Godowns", stats.get("godowns", 0), "🏢", Colors.SECONDARY),
            ("Products", stats.get("products", 0), "📦", Colors.SUCCESS),
            ("Parties", stats.get("parties", 0), "👥", Colors.WARNING),
            ("Purchases", format_currency(stats.get("total_purchases", 0)), "📥", Colors.DANGER),
            ("Sales", format_currency(stats.get("total_sales", 0)), "📤", Colors.PRIMARY),
            ("Staff", stats.get("staff", 0), "👷", Colors.TEAL),
            ("Vehicles", stats.get("vehicles", 0), "🚛", Colors.ORANGE),
        ]

        for idx, (title, value, icon, color) in enumerate(cards):
            StatCard(stats_frame, title, value, icon, color, row=idx // 4, col=idx % 4)

        for c in range(4):
            stats_frame.grid_columnconfigure(c, weight=1)

    def _build_add_section(self):
        """Build the Add Data section."""
        d = self.root
        sec = SectionFrame(self.scroll_frame, "ADD DATA", "📝", Colors.PRIMARY)
        sec.add_button_grid([
            ("Add Mill", lambda: _open_add_mill(d), BUTTON_THEMES["add"]),
            ("Add Godown", lambda: _open_add_godown(d), BUTTON_THEMES["add"]),
            ("Add Category", lambda: _open_add_category(d), BUTTON_THEMES["add"]),
            ("Add Product", lambda: _open_add_product(d), BUTTON_THEMES["add"]),
            ("Add Party", lambda: _open_add_party(d), BUTTON_THEMES["add"]),
            ("Add Staff", lambda: _open_add_staff(d), BUTTON_THEMES["staff"]),
            ("Add Vehicle", lambda: _open_add_vehicle(d), BUTTON_THEMES["staff"]),
            ("Purchase Entry", lambda: _open_purchase_entry(d), BUTTON_THEMES["transaction"]),
            ("Sale Entry", lambda: _open_sale_entry(d), BUTTON_THEMES["transaction"]),
            ("Processing Batch", lambda: _open_processing_entry(d), BUTTON_THEMES["processing"]),
            ("Godown Entry", lambda: _open_add_godown_entry(d), BUTTON_THEMES["transaction"]),
        ])

    def _build_view_section(self):
        """Build the View Data section."""
        r = self.role
        d = self.root
        sec = SectionFrame(self.scroll_frame, "VIEW DATA", "📊", Colors.SECONDARY)
        sec.add_button_grid([
            ("View Mills", lambda: _view_mills(d, r), BUTTON_THEMES["view"]),
            ("View Godowns", lambda: _view_godowns(d, r), BUTTON_THEMES["view"]),
            ("View Godown Entries", lambda: _view_godown_entries(d, r), BUTTON_THEMES["view"]),
            ("View Categories", lambda: _view_categories(d, r), BUTTON_THEMES["view"]),
            ("View Products", lambda: _view_products(d, r), BUTTON_THEMES["view"]),
            ("View Parties", lambda: _view_parties(d, r), BUTTON_THEMES["view"]),
            ("View Purchases", lambda: _view_purchases(d, r), BUTTON_THEMES["view"]),
            ("View Sales", lambda: _view_sales(d, r), BUTTON_THEMES["view"]),
            ("View Processing", lambda: _view_processing(d, r), BUTTON_THEMES["view"]),
            ("View Staff", lambda: _view_staff(d, r), BUTTON_THEMES["view"]),
            ("View Vehicles", lambda: _view_vehicles(d, r), BUTTON_THEMES["view"]),
        ])

    def _build_invoice_section(self):
        """Build the Invoices & Reports section."""
        d = self.root
        sec = SectionFrame(self.scroll_frame, "INVOICES & REPORTS", "📄", Colors.PINK)
        sec.add_button_grid([
            ("Generate Sale Invoice", lambda: open_sale_invoice(d), BUTTON_THEMES["invoice"]),
            ("Generate Purchase Invoice", lambda: open_purchase_invoice(d), BUTTON_THEMES["invoice"]),
        ], columns=2)

    def _build_settings_section(self):
        """Build the Settings section."""
        r = self.role
        d = self.root
        sec = SectionFrame(self.scroll_frame, "SETTINGS & CONFIGURATION", "⚙️", Colors.TEAL)
        sec.add_button_grid([
            ("Add Company", lambda: _open_add_company(d), BUTTON_THEMES["settings"]),
            ("View/Edit Companies", lambda: _view_companies(d, r), BUTTON_THEMES["settings"]),
            ("Add Bank Account", lambda: _open_add_bank(d), BUTTON_THEMES["settings"]),
            ("View Bank Accounts", lambda: _view_bank_accounts(d, r), BUTTON_THEMES["settings"]),
        ], columns=2)

    def _logout(self):
        """Log out and return to login screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.root.destroy()
            # Re-launch login
            from ui.login import LoginWindow
            login = LoginWindow(on_login_success=lambda role: Dashboard(role).run())
            login.run()

    def _on_close(self):
        """Handle window close with confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit Rice Mill ERP?",
                                parent=self.root):
            self.root.destroy()

    def run(self):
        """Start the dashboard mainloop."""
        self.root.mainloop()
