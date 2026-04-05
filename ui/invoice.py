"""
Invoice generation for Rice Mill ERP.

Generates sale and purchase invoices with company letterhead,
bank details, and save/print functionality.
"""

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from ui.theme import Colors, Fonts, Spacing, apply_theme
from db import models
from utils.formatters import format_currency
import os
import tempfile


def _build_invoice_text(invoice_type, record, party_name, product_name, company, banks):
    """Build the invoice text content."""
    type_label = "SALE" if invoice_type == "sale" else "PURCHASE"
    bill_label = "BILL TO (CUSTOMER)" if invoice_type == "sale" else "BILL FROM (VENDOR)"
    party_label = "Customer" if invoice_type == "sale" else "Supplier"

    bank_section = ""
    if banks:
        bank_section = "\nBANK DETAILS FOR PAYMENT\n" + "=" * 65 + "\n"
        for bank in banks:
            bank_section += f"  Bank Name:        {bank[1]}\n"
            bank_section += f"  Account Number:   {bank[2]}\n"
            bank_section += f"  IFSC Code:        {bank[3]}\n\n"

    text = f"""
{'=' * 65}
{'RICE MILL ERP — ' + type_label + ' INVOICE':^65}
{'=' * 65}

FROM (OUR DETAILS)
{'─' * 65}
  Mill Name:           {company[1] if company else 'Rice Mill'}
  GST Number:          {company[2] if company else 'N/A'}
  Registration No:     {company[3] if company else 'N/A'}
  Contact:             {company[4] if company else 'N/A'}
  Address:             {company[5].strip() if company and company[5] else 'N/A'}

INVOICE DETAILS
{'─' * 65}
  Invoice Number:      #{record[0]}
  Date:                {record[10]}

{bill_label}
{'─' * 65}
  Name:                {party_name}
  Type:                {party_label}

PRODUCT INFORMATION
{'─' * 65}
  Product:             {product_name}
  Quantity:            {record[3]:,.2f} {record[4]}
  Rate Per Unit:       {format_currency(record[5])}

BILLING SUMMARY
{'─' * 65}
  Subtotal:            {format_currency(record[6])}
  GST ({record[7]:.1f}%):           {format_currency(record[8])}
                       {'─' * 35}
  TOTAL AMOUNT:        {format_currency(record[9])}
{'=' * 65}
{bank_section}
NOTES
{'─' * 65}
  • Prices are inclusive of taxes where applicable
  • Payment due within 30 days
  • For queries, contact: {company[4] if company else 'N/A'}

  Thank you for your {'business' if invoice_type == 'sale' else 'supply'}!
{'=' * 65}
"""
    return text


def _open_invoice_dialog(parent, invoice_type):
    """Open a dialog to generate an invoice by ID."""
    type_label = "Sale" if invoice_type == "sale" else "Purchase"

    win = Toplevel(parent)
    win.title(f"Generate {type_label} Invoice")
    win.geometry("480x260")
    win.resizable(False, False)
    win.configure(bg=Colors.BG_PAGE)
    win.transient(parent)
    win.grab_set()
    apply_theme(win)

    # Header
    header = Frame(win, bg=Colors.DANGER if invoice_type == "sale" else Colors.ORANGE, height=55)
    header.pack(fill=X)
    header.pack_propagate(False)
    Label(header, text=f"📄  {type_label.upper()} INVOICE GENERATOR", font=Fonts.SUBHEADING,
          bg=header.cget("bg"), fg="white").pack(anchor=W, padx=Spacing.LG, pady=Spacing.MD)

    # Form
    form = Frame(win, bg=Colors.BG_PAGE, padx=Spacing.XXL, pady=Spacing.XL)
    form.pack(fill=BOTH, expand=True)

    Label(form, text=f"Enter {type_label} ID:", font=Fonts.BODY_BOLD,
          bg=Colors.BG_PAGE, fg=Colors.TEXT_DARK).pack(anchor=W, pady=(0, 4))
    id_entry = Entry(form, font=Fonts.INPUT, bg=Colors.INPUT_BG, fg=Colors.INPUT_TEXT,
                      relief=SOLID, bd=1, insertbackground=Colors.INPUT_TEXT)
    id_entry.pack(fill=X, ipady=8, pady=(0, Spacing.LG))
    id_entry.focus_set()

    def generate():
        try:
            record_id = int(id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", f"Please enter a valid {type_label} ID.", parent=win)
            return

        # Fetch record
        if invoice_type == "sale":
            record = models.get_sale(record_id)
        else:
            record = models.get_purchase(record_id)

        if not record:
            messagebox.showerror("Error", f"{type_label} #{record_id} not found.", parent=win)
            return

        party_names = models.get_party_names()
        product_names = models.get_product_names()
        party_name = party_names.get(record[1], "N/A")
        product_name = product_names.get(record[2], "N/A")
        company = models.get_default_company()
        banks = models.get_all_bank_accounts()

        invoice_text = _build_invoice_text(invoice_type, record, party_name,
                                            product_name, company, banks)

        # Show invoice window
        _show_invoice_window(parent, win, invoice_type, record_id, invoice_text)

    # Buttons
    btn_frame = Frame(form, bg=Colors.BG_PAGE)
    btn_frame.pack(fill=X)
    Button(btn_frame, text="Generate Invoice", command=generate,
           bg=Colors.DANGER if invoice_type == "sale" else Colors.ORANGE,
           fg="white", font=Fonts.BUTTON, relief=FLAT, bd=0, padx=20, pady=10,
           cursor="hand2").pack(fill=X)

    win.bind("<Return>", lambda e: generate())


def _show_invoice_window(parent, prompt_win, invoice_type, record_id, invoice_text):
    """Display the generated invoice."""
    type_label = "Sale" if invoice_type == "sale" else "Purchase"
    header_color = Colors.DANGER if invoice_type == "sale" else Colors.ORANGE

    prompt_win.destroy()

    inv_win = Toplevel(parent)
    inv_win.title(f"{type_label} Invoice #{record_id}")
    inv_win.geometry("780x700")
    inv_win.configure(bg=Colors.BG_PAGE)
    apply_theme(inv_win)

    # Header
    header = Frame(inv_win, bg=header_color, height=70)
    header.pack(fill=X)
    header.pack_propagate(False)

    Label(header, text="🌾  RICE MILL ERP", font=Fonts.HEADING,
          bg=header_color, fg="white").pack(anchor=W, padx=Spacing.LG, pady=(12, 0))
    Label(header, text=f"{type_label.upper()} INVOICE", font=Fonts.BODY,
          bg=header_color, fg="#FFE0E0").pack(anchor=W, padx=Spacing.LG)

    # Invoice content
    content = Frame(inv_win, bg=Colors.BG_PAGE, padx=Spacing.XL, pady=Spacing.MD)
    content.pack(fill=BOTH, expand=True)

    text_widget = Text(content, wrap=WORD, font=Fonts.MONO,
                        bg="white", fg="#1E293B", padx=20, pady=20,
                        relief=SOLID, bd=1, insertbackground="#1E293B")
    text_widget.pack(fill=BOTH, expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(text_widget, orient=VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_widget.insert("1.0", invoice_text)
    text_widget.config(state=DISABLED)

    # Button bar
    btn_bar = Frame(inv_win, bg=Colors.CARD_BORDER, padx=Spacing.XL, pady=Spacing.MD)
    btn_bar.pack(fill=X, side=BOTTOM)

    def save_invoice():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{type_label}_Invoice_{record_id}.txt",
            parent=inv_win
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(invoice_text)
            messagebox.showinfo("Saved", f"Invoice saved to:\n{file_path}", parent=inv_win)

    def print_invoice():
        """Save to temp file and open system print dialog."""
        try:
            tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
            tmp.write(invoice_text)
            tmp.close()
            os.startfile(tmp.name, "print")
        except Exception:
            messagebox.showinfo("Print", "To print, save the invoice first then open it with your text editor.",
                                parent=inv_win)

    Button(btn_bar, text="💾  Save", command=save_invoice,
           bg=Colors.SUCCESS, fg="white", font=Fonts.BUTTON_SM, relief=FLAT,
           bd=0, padx=16, pady=8, cursor="hand2").pack(side=LEFT, padx=4)
    Button(btn_bar, text="🖨  Print", command=print_invoice,
           bg=Colors.PRIMARY, fg="white", font=Fonts.BUTTON_SM, relief=FLAT,
           bd=0, padx=16, pady=8, cursor="hand2").pack(side=LEFT, padx=4)
    Button(btn_bar, text="Close", command=inv_win.destroy,
           bg="#64748B", fg="white", font=Fonts.BUTTON_SM, relief=FLAT,
           bd=0, padx=16, pady=8, cursor="hand2").pack(side=RIGHT, padx=4)


# ── Public API ──

def open_sale_invoice(parent):
    """Open the sale invoice generation dialog."""
    _open_invoice_dialog(parent, "sale")


def open_purchase_invoice(parent):
    """Open the purchase invoice generation dialog."""
    _open_invoice_dialog(parent, "purchase")
