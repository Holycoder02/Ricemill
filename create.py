import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

# ==============================
# DATABASE SETUP
# ==============================

conn = sqlite3.connect("rice_mill_erp.db")
cursor = conn.cursor()

def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS godowns(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mill_id INTEGER,
        total_capacity REAL,
        current_stock REAL,
        storage_rate REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS godown_entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        godown_id INTEGER,
        party_id INTEGER,
        product_id INTEGER,
        quantity REAL,
        unit TEXT,
        from_date TEXT,
        to_date TEXT,
        storage_rate REAL,
        total_charges REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parties(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases(
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
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
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
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processing(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        batch_no TEXT,
        input_product INTEGER,
        output_product INTEGER,
        quantity REAL,
        unit TEXT,
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        payout_type TEXT,
        salary REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        driver TEXT,
        vehicle_type TEXT,
        empty_weight REAL,
        loaded_weight REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        gst_number TEXT,
        rst_number TEXT,
        contact_number TEXT,
        address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bank_name TEXT,
        account_no TEXT,
        ifsc_code TEXT,
        balance REAL
    )
    """)

    conn.commit()

create_tables()

# ==============================
# COMPANY & BANK SETUP FUNCTIONS
# ==============================

def setup_company_info():
    # Check if company info exists
    cursor.execute("SELECT * FROM company_info WHERE id=1")
    info = cursor.fetchone()
    
    if not info:
        cursor.execute("""INSERT INTO company_info(id, company_name, gst_number, rst_number, contact_number, address) 
                         VALUES(1, 'Rice Mill', '', '', '', '')""")
        conn.commit()

setup_company_info()

def add_company_info():
    win = Tk()
    win.title("Add Company")
    win.geometry("400x400")
    
    main_frame = Frame(win, padx=20, pady=20)
    main_frame.pack(fill=BOTH, expand=True)
    
    Label(main_frame, text="Company Name:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
    company_name = Entry(main_frame, font=("Arial", 10))
    company_name.pack(fill=X, pady=(0, 10))
    
    Label(main_frame, text="GST Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
    gst_number = Entry(main_frame, font=("Arial", 10))
    gst_number.pack(fill=X, pady=(0, 10))
    
    Label(main_frame, text="RST/Registration Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
    rst_number = Entry(main_frame, font=("Arial", 10))
    rst_number.pack(fill=X, pady=(0, 10))
    
    Label(main_frame, text="Contact Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
    contact = Entry(main_frame, font=("Arial", 10))
    contact.pack(fill=X, pady=(0, 10))
    
    Label(main_frame, text="Mill Address:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
    address = Text(main_frame, font=("Arial", 10), height=4)
    address.pack(fill=BOTH, expand=True, pady=(0, 10))
    
    def save():
        if not all([company_name.get(), gst_number.get(), rst_number.get(), contact.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("""INSERT INTO company_info(company_name, gst_number, rst_number, contact_number, address) VALUES(?,?,?,?,?)""",
                          (company_name.get(), gst_number.get(), rst_number.get(), contact.get(), address.get(1.0, END)))
            conn.commit()
            messagebox.showinfo("Success", "Company Added!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    Button(main_frame, text="Save", command=save, bg="#4CAF50", fg="white", 
           font=("Arial", 10), width=20, padx=10, pady=8).pack()

def view_companies(role="Accountant"):
    win = Tk()
    win.title("View & Edit Companies")
    win.geometry("700x350")
    
    cursor.execute("SELECT * FROM company_info")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Company Name", "GST", "RST", "Contact"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Company Name", anchor=W, width=220)
    tree.column("GST", anchor=W, width=100)
    tree.column("RST", anchor=W, width=100)
    tree.column("Contact", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Company Name", text="Company Name", anchor=W)
    tree.heading("GST", text="GST Number", anchor=W)
    tree.heading("RST", text="RST Number", anchor=W)
    tree.heading("Contact", text="Contact", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_company():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a company")
            return
        
        company_id = selected[0]
        cursor.execute("SELECT * FROM company_info WHERE id=?", (company_id,))
        info = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Company - {info[1]}")
        edit_win.geometry("400x400")
        
        main_frame = Frame(edit_win, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        Label(main_frame, text="Company Name:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
        company_name_edit = Entry(main_frame, font=("Arial", 10))
        company_name_edit.insert(0, info[1])
        company_name_edit.pack(fill=X, pady=(0, 10))
        
        Label(main_frame, text="GST Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
        gst_number_edit = Entry(main_frame, font=("Arial", 10))
        gst_number_edit.insert(0, info[2])
        gst_number_edit.pack(fill=X, pady=(0, 10))
        
        Label(main_frame, text="RST/Registration Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
        rst_number_edit = Entry(main_frame, font=("Arial", 10))
        rst_number_edit.insert(0, info[3])
        rst_number_edit.pack(fill=X, pady=(0, 10))
        
        Label(main_frame, text="Contact Number:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
        contact_edit = Entry(main_frame, font=("Arial", 10))
        contact_edit.insert(0, info[4])
        contact_edit.pack(fill=X, pady=(0, 10))
        
        Label(main_frame, text="Mill Address:", font=("Arial", 10, "bold")).pack(anchor=W, pady=(5, 0))
        address_edit = Text(main_frame, font=("Arial", 10), height=4)
        address_edit.insert(1.0, info[5])
        address_edit.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        def save():
            try:
                cursor.execute("""UPDATE company_info SET company_name=?, gst_number=?, rst_number=?, contact_number=?, address=? WHERE id=?""",
                              (company_name_edit.get(), gst_number_edit.get(), rst_number_edit.get(), contact_edit.get(), address_edit.get(1.0, END), company_id))
                conn.commit()
                messagebox.showinfo("Success", "Company Updated!")
                edit_win.destroy()
                win.destroy()
                view_companies(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this company?"):
                try:
                    cursor.execute("DELETE FROM company_info WHERE id=?", (company_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Company Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_companies(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(main_frame)
        button_frame.pack(fill=X, pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", 
               font=("Arial", 10), width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", 
               font=("Arial", 10), width=10).pack(side=LEFT, padx=5)
    
    if role == "Admin":
        Button(win, text="Edit Selected", command=edit_company, bg="#2196F3", fg="white", 
               font=("Arial", 10), width=25).pack(pady=10)
    else:
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def add_bank_account():
    win = Tk()
    win.title("Add Bank Account")
    win.geometry("350x300")
    
    Label(win, text="Bank Name", font=("Arial", 10, "bold")).pack(pady=5)
    bank_name = Entry(win, font=("Arial", 10))
    bank_name.pack(pady=5, padx=20, fill=X)
    
    Label(win, text="Account Number", font=("Arial", 10, "bold")).pack(pady=5)
    account_no = Entry(win, font=("Arial", 10))
    account_no.pack(pady=5, padx=20, fill=X)
    
    Label(win, text="IFSC Code", font=("Arial", 10, "bold")).pack(pady=5)
    ifsc_code = Entry(win, font=("Arial", 10))
    ifsc_code.pack(pady=5, padx=20, fill=X)
    
    def save():
        if not all([bank_name.get(), account_no.get(), ifsc_code.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("INSERT INTO bank_accounts(bank_name, account_no, ifsc_code, balance) VALUES(?,?,?,?)",
                          (bank_name.get(), account_no.get(), ifsc_code.get(), 0.0))
            conn.commit()
            messagebox.showinfo("Success", "Bank Account Added!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    Button(win, text="Save", command=save, bg="#4CAF50", fg="white", 
           font=("Arial", 10), width=20, padx=10, pady=8).pack(pady=10)
    
    def view_accounts():
        view_bank_accounts()
    
    Button(win, text="View All Bank Accounts", command=view_accounts, bg="#2196F3", fg="white", 
           font=("Arial", 10), width=20, padx=10, pady=8).pack(pady=5)

def view_bank_accounts(role="Accountant"):
    win = Tk()
    win.title("Bank Accounts")
    win.geometry("700x300")
    
    cursor.execute("SELECT * FROM bank_accounts")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Bank Name", "Account No", "IFSC Code"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=50)
    tree.column("Bank Name", anchor=W, width=250)
    tree.column("Account No", anchor=W, width=200)
    tree.column("IFSC Code", anchor=W, width=120)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Bank Name", text="Bank Name", anchor=W)
    tree.heading("Account No", text="Account Number", anchor=W)
    tree.heading("IFSC Code", text="IFSC Code", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def delete_account():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a bank account")
            return
        
        if messagebox.askyesno("Confirm", "Delete this bank account?"):
            try:
                cursor.execute("DELETE FROM bank_accounts WHERE id=?", (selected[0],))
                conn.commit()
                messagebox.showinfo("Success", "Bank Account Deleted!")
                win.destroy()
                view_bank_accounts(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    if role == "Admin":
        Button(win, text="Delete Selected", command=delete_account, bg="#F44336", fg="white", 
               font=("Arial", 10), width=25).pack(pady=10)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for deletion", font=("Arial", 9), fg="#666").pack(pady=10)

# ==============================
# MODULE FUNCTIONS
# ==============================

def add_mill():
    win = Tk()
    win.title("Add Mill")
    win.geometry("300x150")

    Label(win, text="Mill Name").pack(pady=5)
    entry = Entry(win)
    entry.pack(pady=5)

    def save():
        if not entry.get():
            messagebox.showerror("Error", "Mill Name cannot be empty")
            return
        try:
            cursor.execute("INSERT INTO mills(name) VALUES(?)", (entry.get(),))
            conn.commit()
            messagebox.showinfo("Success", "Mill Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def add_godown():
    win = Tk()
    win.title("Add Godown")
    win.geometry("300x250")

    Label(win, text="Godown Name").pack(pady=5)
    name = Entry(win)
    name.pack(pady=5)

    Label(win, text="Mill ID").pack(pady=5)
    mill_id = Entry(win)
    mill_id.pack(pady=5)

    Label(win, text="Total Capacity (in Kg)").pack(pady=5)
    capacity = Entry(win)
    capacity.pack(pady=5)

    Label(win, text="Storage Rate (Per Kg Per Day)").pack(pady=5)
    rate = Entry(win)
    rate.pack(pady=5)

    def save():
        if not all([name.get(), mill_id.get(), capacity.get(), rate.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("INSERT INTO godowns(name,mill_id,total_capacity,current_stock,storage_rate) VALUES(?,?,?,?,?)",
                           (name.get(), int(mill_id.get()), float(capacity.get()), 0.0, float(rate.get())))
            conn.commit()
            messagebox.showinfo("Success", "Godown Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def add_product():
    win = Tk()
    win.title("Add Product")
    win.geometry("300x200")

    Label(win, text="Product Name").pack(pady=5)
    name = Entry(win)
    name.pack(pady=5)

    Label(win, text="Category ID").pack(pady=5)
    cat = Entry(win)
    cat.pack(pady=5)

    def save():
        if not name.get() or not cat.get():
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("INSERT INTO products(name,category_id) VALUES(?,?)",
                           (name.get(), int(cat.get())))
            conn.commit()
            messagebox.showinfo("Success", "Product Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def add_party():
    win = Tk()
    win.title("Add Party")
    win.geometry("300x200")

    Label(win, text="Party Name").pack(pady=5)
    name = Entry(win)
    name.pack(pady=5)

    Label(win, text="Type (Customer/Supplier/Broker)").pack(pady=5)
    ptype = Entry(win)
    ptype.pack(pady=5)

    def save():
        if not name.get() or not ptype.get():
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("INSERT INTO parties(name,type) VALUES(?,?)",
                           (name.get(), ptype.get()))
            conn.commit()
            messagebox.showinfo("Success", "Party Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def purchase_entry():
    win = Tk()
    win.title("Purchase Entry")
    win.geometry("350x450")

    Label(win, text="Party ID").pack(pady=5)
    party = Entry(win)
    party.pack(pady=5)

    Label(win, text="Product ID").pack(pady=5)
    product = Entry(win)
    product.pack(pady=5)

    Label(win, text="Quantity").pack(pady=5)
    qty = Entry(win)
    qty.pack(pady=5)

    Label(win, text="Unit").pack(pady=5)
    unit = StringVar(value="Kg")
    unit_combo = ttk.Combobox(win, textvariable=unit, values=["Ton", "Quintal", "Kg"], state="readonly", width=27)
    unit_combo.pack(pady=5)

    Label(win, text="Rate").pack(pady=5)
    rate = Entry(win)
    rate.pack(pady=5)

    Label(win, text="GST Percentage (%)").pack(pady=5)
    gst_percent = Entry(win)
    gst_percent.insert(0, "18")
    gst_percent.pack(pady=5)

    def save():
        if not all([party.get(), product.get(), qty.get(), rate.get(), gst_percent.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            qty_val = float(qty.get())
            rate_val = float(rate.get())
            gst_val = float(gst_percent.get())
            
            subtotal = qty_val * rate_val
            gst_amount = subtotal * (gst_val / 100)
            total = subtotal + gst_amount
            
            cursor.execute("""
            INSERT INTO purchases(party_id,product_id,quantity,unit,rate,subtotal,gst_percent,gst_amount,total,date)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (int(party.get()), int(product.get()), qty_val, unit.get(), rate_val,
                  subtotal, gst_val, gst_amount, total, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            messagebox.showinfo("Success", f"Purchase Saved\nSubtotal: Rs. {subtotal:.2f}\nGST ({gst_val}%): Rs. {gst_amount:.2f}\nTotal: Rs. {total:.2f}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def sale_entry():
    win = Tk()
    win.title("Sale Entry")
    win.geometry("350x450")

    Label(win, text="Party ID").pack(pady=5)
    party = Entry(win)
    party.pack(pady=5)

    Label(win, text="Product ID").pack(pady=5)
    product = Entry(win)
    product.pack(pady=5)

    Label(win, text="Quantity").pack(pady=5)
    qty = Entry(win)
    qty.pack(pady=5)

    Label(win, text="Unit").pack(pady=5)
    unit = StringVar(value="Kg")
    unit_combo = ttk.Combobox(win, textvariable=unit, values=["Ton", "Quintal", "Kg"], state="readonly", width=27)
    unit_combo.pack(pady=5)

    Label(win, text="Rate").pack(pady=5)
    rate = Entry(win)
    rate.pack(pady=5)

    Label(win, text="GST Percentage (%)").pack(pady=5)
    gst_percent = Entry(win)
    gst_percent.insert(0, "18")
    gst_percent.pack(pady=5)

    def save():
        if not all([party.get(), product.get(), qty.get(), rate.get(), gst_percent.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            qty_val = float(qty.get())
            rate_val = float(rate.get())
            gst_val = float(gst_percent.get())
            
            subtotal = qty_val * rate_val
            gst_amount = subtotal * (gst_val / 100)
            total = subtotal + gst_amount
            
            cursor.execute("""
            INSERT INTO sales(party_id,product_id,quantity,unit,rate,subtotal,gst_percent,gst_amount,total,date)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (int(party.get()), int(product.get()), qty_val, unit.get(), rate_val,
                  subtotal, gst_val, gst_amount, total, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            messagebox.showinfo("Success", f"Sale Saved\nSubtotal: Rs. {subtotal:.2f}\nGST ({gst_val}%): Rs. {gst_amount:.2f}\nTotal: Rs. {total:.2f}")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def processing_entry():
    win = Tk()
    win.title("Processing Batch")
    win.geometry("300x350")

    Label(win, text="Batch No").pack(pady=5)
    batch = Entry(win)
    batch.pack(pady=5)

    Label(win, text="Input Product ID").pack(pady=5)
    inp = Entry(win)
    inp.pack(pady=5)

    Label(win, text="Output Product ID").pack(pady=5)
    out = Entry(win)
    out.pack(pady=5)

    Label(win, text="Quantity").pack(pady=5)
    qty = Entry(win)
    qty.pack(pady=5)

    Label(win, text="Unit").pack(pady=5)
    unit = StringVar(value="Kg")
    unit_combo = ttk.Combobox(win, textvariable=unit, values=["Ton", "Quintal", "Kg"], state="readonly", width=27)
    unit_combo.pack(pady=5)

    def save():
        if not all([batch.get(), inp.get(), out.get(), qty.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("""
            INSERT INTO processing(batch_no,input_product,output_product,quantity,unit,date)
            VALUES(?,?,?,?,?,?)
            """, (batch.get(), int(inp.get()), int(out.get()),
                  float(qty.get()), unit.get(), datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            messagebox.showinfo("Success", "Batch Saved")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def add_staff():
    win = Tk()
    win.title("Add Staff")
    win.geometry("300x250")

    Label(win, text="Name").pack(pady=5)
    name = Entry(win)
    name.pack(pady=5)

    Label(win, text="Payout Type (Monthly/Daily/Contract)").pack(pady=5)
    ptype = Entry(win)
    ptype.pack(pady=5)

    Label(win, text="Salary").pack(pady=5)
    salary = Entry(win)
    salary.pack(pady=5)

    def save():
        if not all([name.get(), ptype.get(), salary.get()]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            cursor.execute("INSERT INTO staff(name,payout_type,salary) VALUES(?,?,?)",
                           (name.get(), ptype.get(), float(salary.get())))
            conn.commit()
            messagebox.showinfo("Success", "Staff Added")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

def add_vehicle():
    win = Tk()
    win.title("Add Vehicle")
    win.geometry("350x420")

    Label(win, text="Vehicle No").pack(pady=5)
    vno = Entry(win)
    vno.pack(pady=5)

    Label(win, text="Driver Name").pack(pady=5)
    driver = Entry(win)
    driver.pack(pady=5)

    Label(win, text="Vehicle Type").pack(pady=5)
    vehicle_type = StringVar(value="Truck")
    type_combo = ttk.Combobox(win, textvariable=vehicle_type, values=["Truck", "Pickup", "Tractor", "6-Wheeler"], state="readonly", width=27)
    type_combo.pack(pady=5)

    Label(win, text="Empty Vehicle Weight (Kg)").pack(pady=5)
    empty_weight = Entry(win)
    empty_weight.pack(pady=5)

    Label(win, text="Loaded Vehicle Weight (Kg)").pack(pady=5)
    loaded_weight = Entry(win)
    loaded_weight.pack(pady=5)

    def save():
        if not vno.get() or not driver.get() or not empty_weight.get() or not loaded_weight.get():
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            empty_wt = float(empty_weight.get())
            loaded_wt = float(loaded_weight.get())
            
            if loaded_wt < empty_wt:
                messagebox.showerror("Error", "Loaded weight must be greater than or equal to empty weight")
                return
            
            cursor.execute("INSERT INTO vehicles(vehicle_no,driver,vehicle_type,empty_weight,loaded_weight) VALUES(?,?,?,?,?)",
                           (vno.get(), driver.get(), vehicle_type.get(), empty_wt, loaded_wt))
            conn.commit()
            messagebox.showinfo("Success", "Vehicle Added")
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Weight must be numeric")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(win, text="Save", command=save).pack(pady=10)

# ==============================
# MAIN DASHBOARD
# ==============================

def view_mills(role="Accountant"):
    win = Tk()
    win.title("View Mills")
    win.geometry("450x350")
    
    cursor.execute("SELECT * FROM mills")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Name"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=50)
    tree.column("Name", anchor=W, width=250)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_mill():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a mill")
            return
        
        mill_id = selected[0]
        cursor.execute("SELECT * FROM mills WHERE id=?", (mill_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Mill - {row[1]}")
        edit_win.geometry("300x150")
        
        Label(edit_win, text="Mill Name").pack(pady=5)
        name = Entry(edit_win)
        name.insert(0, row[1])
        name.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not name.get():
                messagebox.showerror("Error", "Mill name is required")
                return
            try:
                cursor.execute("UPDATE mills SET name=? WHERE id=?",
                              (name.get(), mill_id))
                conn.commit()
                messagebox.showinfo("Success", "Mill Updated!")
                edit_win.destroy()
                win.destroy()
                view_mills(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this mill?"):
                try:
                    cursor.execute("DELETE FROM mills WHERE id=?", (mill_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Mill Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_mills(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_mill)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                mill_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this mill?"):
                    try:
                        cursor.execute("DELETE FROM mills WHERE id=?", (mill_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Mill Deleted!")
                        win.destroy()
                        view_mills(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_mill())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_godowns(role="Accountant"):
    win = Tk()
    win.title("View Godowns")
    win.geometry("850x350")
    
    cursor.execute("SELECT * FROM godowns")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Name", "Mill ID", "Total Capacity", "Current Stock", "Storage Rate"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Name", anchor=W, width=120)
    tree.column("Mill ID", anchor=W, width=60)
    tree.column("Total Capacity", anchor=W, width=120)
    tree.column("Current Stock", anchor=W, width=120)
    tree.column("Storage Rate", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    tree.heading("Mill ID", text="Mill ID", anchor=W)
    tree.heading("Total Capacity", text="Total Capacity (Kg)", anchor=W)
    tree.heading("Current Stock", text="Current Stock (Kg)", anchor=W)
    tree.heading("Storage Rate", text="Rate/Kg/Day", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4], row[5]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_godown():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a godown")
            return
        
        godown_id = selected[0]
        cursor.execute("SELECT * FROM godowns WHERE id=?", (godown_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Godown - {row[1]}")
        edit_win.geometry("350x300")
        
        Label(edit_win, text="Godown Name").pack(pady=5)
        name = Entry(edit_win)
        name.insert(0, row[1])
        name.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Mill ID").pack(pady=5)
        mill_id = Entry(edit_win)
        mill_id.insert(0, row[2])
        mill_id.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Total Capacity (Kg)").pack(pady=5)
        capacity = Entry(edit_win)
        capacity.insert(0, row[3])
        capacity.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Current Stock (Kg)").pack(pady=5)
        stock = Entry(edit_win)
        stock.insert(0, row[4])
        stock.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Storage Rate (Rs/Kg/Day)").pack(pady=5)
        rate = Entry(edit_win)
        rate.insert(0, row[5])
        rate.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not all([name.get(), mill_id.get(), capacity.get(), stock.get(), rate.get()]):
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                cursor.execute("UPDATE godowns SET name=?, mill_id=?, total_capacity=?, current_stock=?, storage_rate=? WHERE id=?",
                              (name.get(), int(mill_id.get()), float(capacity.get()), float(stock.get()), float(rate.get()), godown_id))
                conn.commit()
                messagebox.showinfo("Success", "Godown Updated!")
                edit_win.destroy()
                win.destroy()
                view_godowns(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this godown?"):
                try:
                    cursor.execute("DELETE FROM godowns WHERE id=?", (godown_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Godown Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_godowns(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_godown)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                godown_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this godown?"):
                    try:
                        cursor.execute("DELETE FROM godowns WHERE id=?", (godown_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Godown Deleted!")
                        win.destroy()
                        view_godowns(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_godown())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_godown_entries():
    win = Tk()
    win.title("View Godown Storage Entries")
    win.geometry("1000x350")
    
    cursor.execute("SELECT * FROM godown_entries")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Godown", "Party", "Product", "Qty", "Unit", "From Date", "To Date", "Rate", "Charges"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Godown", anchor=W, width=80)
    tree.column("Party", anchor=W, width=80)
    tree.column("Product", anchor=W, width=80)
    tree.column("Qty", anchor=W, width=60)
    tree.column("Unit", anchor=W, width=50)
    tree.column("From Date", anchor=W, width=80)
    tree.column("To Date", anchor=W, width=80)
    tree.column("Rate", anchor=W, width=60)
    tree.column("Charges", anchor=W, width=80)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Godown", text="Godown ID", anchor=W)
    tree.heading("Party", text="Party ID", anchor=W)
    tree.heading("Product", text="Product ID", anchor=W)
    tree.heading("Qty", text="Qty", anchor=W)
    tree.heading("Unit", text="Unit", anchor=W)
    tree.heading("From Date", text="From Date", anchor=W)
    tree.heading("To Date", text="To Date", anchor=W)
    tree.heading("Rate", text="Rate/Kg/Day", anchor=W)
    tree.heading("Charges", text="Total Charges (Rs.)", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

def view_products(role="Accountant"):
    win = Tk()
    win.title("View Products")
    win.geometry("550x350")
    
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Name", "Category ID"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=50)
    tree.column("Name", anchor=W, width=250)
    tree.column("Category ID", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    tree.heading("Category ID", text="Category ID", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_product():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = selected[0]
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Product - {row[1]}")
        edit_win.geometry("300x200")
        
        Label(edit_win, text="Product Name").pack(pady=5)
        name = Entry(edit_win)
        name.insert(0, row[1])
        name.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Category ID").pack(pady=5)
        cat_id = Entry(edit_win)
        cat_id.insert(0, row[2])
        cat_id.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not name.get() or not cat_id.get():
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                cursor.execute("UPDATE products SET name=?, category_id=? WHERE id=?",
                              (name.get(), int(cat_id.get()), product_id))
                conn.commit()
                messagebox.showinfo("Success", "Product Updated!")
                edit_win.destroy()
                win.destroy()
                view_products(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this product?"):
                try:
                    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Product Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_products(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_product)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                product_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this product?"):
                    try:
                        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Product Deleted!")
                        win.destroy()
                        view_products(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_product())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_parties(role="Accountant"):
    win = Tk()
    win.title("View Parties")
    win.geometry("550x350")
    
    cursor.execute("SELECT * FROM parties")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Name", "Type"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=50)
    tree.column("Name", anchor=W, width=250)
    tree.column("Type", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    tree.heading("Type", text="Type", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_party():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a party")
            return
        
        party_id = selected[0]
        cursor.execute("SELECT * FROM parties WHERE id=?", (party_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Party - {row[1]}")
        edit_win.geometry("300x200")
        
        Label(edit_win, text="Party Name").pack(pady=5)
        name = Entry(edit_win)
        name.insert(0, row[1])
        name.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Party Type (Buyer/Seller)").pack(pady=5)
        party_type = StringVar(value=row[2])
        type_combo = ttk.Combobox(edit_win, textvariable=party_type, values=["Buyer", "Seller"], state="readonly", width=27)
        type_combo.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not name.get():
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                cursor.execute("UPDATE parties SET name=?, type=? WHERE id=?",
                              (name.get(), party_type.get(), party_id))
                conn.commit()
                messagebox.showinfo("Success", "Party Updated!")
                edit_win.destroy()
                win.destroy()
                view_parties(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this party?"):
                try:
                    cursor.execute("DELETE FROM parties WHERE id=?", (party_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Party Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_parties(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_party)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                party_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this party?"):
                    try:
                        cursor.execute("DELETE FROM parties WHERE id=?", (party_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Party Deleted!")
                        win.destroy()
                        view_parties(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_party())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_purchases(role="Accountant"):
    win = Tk()
    win.title("View Purchases")
    win.geometry("1050x400")
    
    cursor.execute("SELECT * FROM purchases")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Party", "Product", "Qty", "Unit", "Rate", "Subtotal", "GST%", "GST Amt", "Total", "Date"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=35)
    tree.column("Party", anchor=W, width=50)
    tree.column("Product", anchor=W, width=60)
    tree.column("Qty", anchor=W, width=50)
    tree.column("Unit", anchor=W, width=50)
    tree.column("Rate", anchor=W, width=50)
    tree.column("Subtotal", anchor=W, width=60)
    tree.column("GST%", anchor=W, width=50)
    tree.column("GST Amt", anchor=W, width=60)
    tree.column("Total", anchor=W, width=60)
    tree.column("Date", anchor=W, width=75)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Party", text="Party", anchor=W)
    tree.heading("Product", text="Product", anchor=W)
    tree.heading("Qty", text="Qty", anchor=W)
    tree.heading("Unit", text="Unit", anchor=W)
    tree.heading("Rate", text="Rate", anchor=W)
    tree.heading("Subtotal", text="Subtotal", anchor=W)
    tree.heading("GST%", text="GST%", anchor=W)
    tree.heading("GST Amt", text="GST Amt", anchor=W)
    tree.heading("Total", text="Total", anchor=W)
    tree.heading("Date", text="Date", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], f"{row[6]:.2f}", f"{row[7]:.2f}", f"{row[8]:.2f}", f"{row[9]:.2f}", row[10]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_purchase():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a purchase record")
            return
        
        purchase_id = selected[0]
        cursor.execute("SELECT * FROM purchases WHERE id=?", (purchase_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Purchase #{purchase_id}")
        edit_win.geometry("350x350")
        
        Label(edit_win, text="Party ID", font=("Arial", 10, "bold")).pack(pady=5)
        party_id = Entry(edit_win)
        party_id.insert(0, row[1])
        party_id.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Product ID", font=("Arial", 10, "bold")).pack(pady=5)
        product_id = Entry(edit_win)
        product_id.insert(0, row[2])
        product_id.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Quantity", font=("Arial", 10, "bold")).pack(pady=5)
        quantity = Entry(edit_win)
        quantity.insert(0, row[3])
        quantity.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Unit", font=("Arial", 10, "bold")).pack(pady=5)
        unit = StringVar(value=row[4])
        unit_combo = ttk.Combobox(edit_win, textvariable=unit, values=["Ton", "Quintal", "Kg"], state="readonly", width=27)
        unit_combo.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Rate", font=("Arial", 10, "bold")).pack(pady=5)
        rate = Entry(edit_win)
        rate.insert(0, row[5])
        rate.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="GST %", font=("Arial", 10, "bold")).pack(pady=5)
        gst_percent = Entry(edit_win)
        gst_percent.insert(0, row[7])
        gst_percent.pack(pady=5, padx=20, fill=X)
        
        def save():
            try:
                qty = float(quantity.get())
                rt = float(rate.get())
                gst_pct = float(gst_percent.get())
                
                subtotal = qty * rt
                gst_amt = subtotal * (gst_pct / 100)
                total = subtotal + gst_amt
                
                cursor.execute("""UPDATE purchases SET party_id=?, product_id=?, quantity=?, unit=?, rate=?, subtotal=?, gst_percent=?, gst_amount=?, total=? WHERE id=?""",
                              (int(party_id.get()), int(product_id.get()), qty, unit.get(), rt, subtotal, gst_pct, gst_amt, total, purchase_id))
                conn.commit()
                messagebox.showinfo("Success", "Purchase Updated!")
                edit_win.destroy()
                win.destroy()
                view_purchases(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this purchase record?"):
                try:
                    cursor.execute("DELETE FROM purchases WHERE id=?", (purchase_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Purchase Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_purchases(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_purchase)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                purchase_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this purchase record?"):
                    try:
                        cursor.execute("DELETE FROM purchases WHERE id=?", (purchase_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Purchase Deleted!")
                        win.destroy()
                        view_purchases(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_purchase())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_sales(role="Accountant"):
    win = Tk()
    win.title("View Sales")
    win.geometry("1050x400")
    
    cursor.execute("SELECT * FROM sales")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Party", "Product", "Qty", "Unit", "Rate", "Subtotal", "GST%", "GST Amt", "Total", "Date"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=35)
    tree.column("Party", anchor=W, width=50)
    tree.column("Product", anchor=W, width=60)
    tree.column("Qty", anchor=W, width=50)
    tree.column("Unit", anchor=W, width=50)
    tree.column("Rate", anchor=W, width=50)
    tree.column("Subtotal", anchor=W, width=60)
    tree.column("GST%", anchor=W, width=50)
    tree.column("GST Amt", anchor=W, width=60)
    tree.column("Total", anchor=W, width=60)
    tree.column("Date", anchor=W, width=75)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Party", text="Party", anchor=W)
    tree.heading("Product", text="Product", anchor=W)
    tree.heading("Qty", text="Qty", anchor=W)
    tree.heading("Unit", text="Unit", anchor=W)
    tree.heading("Rate", text="Rate", anchor=W)
    tree.heading("Subtotal", text="Subtotal", anchor=W)
    tree.heading("GST%", text="GST%", anchor=W)
    tree.heading("GST Amt", text="GST Amt", anchor=W)
    tree.heading("Total", text="Total", anchor=W)
    tree.heading("Date", text="Date", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], f"{row[6]:.2f}", f"{row[7]:.2f}", f"{row[8]:.2f}", f"{row[9]:.2f}", row[10]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_sale():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale record")
            return
        
        sale_id = selected[0]
        cursor.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Sale #{sale_id}")
        edit_win.geometry("350x350")
        
        Label(edit_win, text="Party ID", font=("Arial", 10, "bold")).pack(pady=5)
        party_id = Entry(edit_win)
        party_id.insert(0, row[1])
        party_id.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Product ID", font=("Arial", 10, "bold")).pack(pady=5)
        product_id = Entry(edit_win)
        product_id.insert(0, row[2])
        product_id.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Quantity", font=("Arial", 10, "bold")).pack(pady=5)
        quantity = Entry(edit_win)
        quantity.insert(0, row[3])
        quantity.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Unit", font=("Arial", 10, "bold")).pack(pady=5)
        unit = StringVar(value=row[4])
        unit_combo = ttk.Combobox(edit_win, textvariable=unit, values=["Ton", "Quintal", "Kg"], state="readonly", width=27)
        unit_combo.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Rate", font=("Arial", 10, "bold")).pack(pady=5)
        rate = Entry(edit_win)
        rate.insert(0, row[5])
        rate.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="GST %", font=("Arial", 10, "bold")).pack(pady=5)
        gst_percent = Entry(edit_win)
        gst_percent.insert(0, row[7])
        gst_percent.pack(pady=5, padx=20, fill=X)
        
        def save():
            try:
                qty = float(quantity.get())
                rt = float(rate.get())
                gst_pct = float(gst_percent.get())
                
                subtotal = qty * rt
                gst_amt = subtotal * (gst_pct / 100)
                total = subtotal + gst_amt
                
                cursor.execute("""UPDATE sales SET party_id=?, product_id=?, quantity=?, unit=?, rate=?, subtotal=?, gst_percent=?, gst_amount=?, total=? WHERE id=?""",
                              (int(party_id.get()), int(product_id.get()), qty, unit.get(), rt, subtotal, gst_pct, gst_amt, total, sale_id))
                conn.commit()
                messagebox.showinfo("Success", "Sale Updated!")
                edit_win.destroy()
                win.destroy()
                view_sales(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this sale record?"):
                try:
                    cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Sale Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_sales(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    # Only enable editing for Admin users
    if role == "Admin":
        # Right-click context menu
        def show_context_menu(event):
            selected = tree.selection()
            if selected:
                context_menu = Menu(win, tearoff=0)
                context_menu.add_command(label="✏️  Edit", command=edit_sale)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️   Delete", command=lambda: delete_from_context())
                context_menu.post(event.x_root, event.y_root)
        
        def delete_from_context():
            selected = tree.selection()
            if selected:
                sale_id = selected[0]
                if messagebox.askyesno("Confirm", "Delete this sale record?"):
                    try:
                        cursor.execute("DELETE FROM sales WHERE id=?", (sale_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Sale Deleted!")
                        win.destroy()
                        view_sales(role)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        
        # Double-click to edit
        tree.bind("<Double-1>", lambda e: edit_sale())
        # Right-click for context menu
        tree.bind("<Button-3>", show_context_menu)
    else:
        # Show message for non-admin users
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_processing(role="Accountant"):
    win = Tk()
    win.title("View Processing Batches")
    win.geometry("750x300")
    
    cursor.execute("SELECT * FROM processing")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Batch No", "Input Prod", "Output Prod", "Qty", "Unit", "Date"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Batch No", anchor=W, width=100)
    tree.column("Input Prod", anchor=W, width=100)
    tree.column("Output Prod", anchor=W, width=100)
    tree.column("Qty", anchor=W, width=80)
    tree.column("Unit", anchor=W, width=70)
    tree.column("Date", anchor=W, width=80)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Batch No", text="Batch No", anchor=W)
    tree.heading("Input Prod", text="Input Prod", anchor=W)
    tree.heading("Output Prod", text="Output Prod", anchor=W)
    tree.heading("Qty", text="Qty", anchor=W)
    tree.heading("Unit", text="Unit", anchor=W)
    tree.heading("Date", text="Date", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

def view_staff(role="Accountant"):
    win = Tk()
    win.title("View Staff")
    win.geometry("600x350")
    
    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Name", "Payout Type", "Salary"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Name", anchor=W, width=180)
    tree.column("Payout Type", anchor=W, width=130)
    tree.column("Salary", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    tree.heading("Payout Type", text="Payout Type", anchor=W)
    tree.heading("Salary", text="Salary", anchor=W)
    
    for row in data:
        tree.insert(parent='', index='end', iid=row[0], text='', values=(row[0], row[1], row[2], row[3]))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_staff():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a staff member")
            return
        
        staff_id = selected[0]
        cursor.execute("SELECT * FROM staff WHERE id=?", (staff_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Staff - {row[1]}")
        edit_win.geometry("350x250")
        
        Label(edit_win, text="Staff Name").pack(pady=5)
        name = Entry(edit_win)
        name.insert(0, row[1])
        name.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Payout Type").pack(pady=5)
        payout_type = StringVar(value=row[2])
        payout_combo = ttk.Combobox(edit_win, textvariable=payout_type, values=["Daily", "Weekly", "Monthly"], state="readonly", width=27)
        payout_combo.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Salary").pack(pady=5)
        salary = Entry(edit_win)
        salary.insert(0, row[3])
        salary.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not name.get() or not salary.get():
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                cursor.execute("UPDATE staff SET name=?, payout_type=?, salary=? WHERE id=?",
                              (name.get(), payout_type.get(), float(salary.get()), staff_id))
                conn.commit()
                messagebox.showinfo("Success", "Staff Updated!")
                edit_win.destroy()
                win.destroy()
                view_staff(role)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this staff member?"):
                try:
                    cursor.execute("DELETE FROM staff WHERE id=?", (staff_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Staff Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_staff(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    if role == "Admin":
        Button(win, text="Edit Selected", command=edit_staff, bg="#2196F3", fg="white", width=25).pack(pady=10)
    else:
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

def view_vehicles(role="Accountant"):
    win = Tk()
    win.title("View Vehicles")
    win.geometry("1050x400")
    
    cursor.execute("SELECT * FROM vehicles")
    data = cursor.fetchall()
    
    tree = ttk.Treeview(win, columns=("ID", "Vehicle No", "Driver", "Type", "Empty Weight (Kg)", "Loaded Weight (Kg)", "Payload (Kg)"), height=15)
    tree.column("#0", width=0, stretch=NO)
    tree.column("ID", anchor=W, width=40)
    tree.column("Vehicle No", anchor=W, width=90)
    tree.column("Driver", anchor=W, width=110)
    tree.column("Type", anchor=W, width=90)
    tree.column("Empty Weight (Kg)", anchor=W, width=120)
    tree.column("Loaded Weight (Kg)", anchor=W, width=120)
    tree.column("Payload (Kg)", anchor=W, width=100)
    
    tree.heading("#0", text="", anchor=W)
    tree.heading("ID", text="ID", anchor=W)
    tree.heading("Vehicle No", text="Vehicle No", anchor=W)
    tree.heading("Driver", text="Driver", anchor=W)
    tree.heading("Type", text="Type", anchor=W)
    tree.heading("Empty Weight (Kg)", text="Empty Weight (Kg)", anchor=W)
    tree.heading("Loaded Weight (Kg)", text="Loaded Weight (Kg)", anchor=W)
    tree.heading("Payload (Kg)", text="Payload (Kg)", anchor=W)
    
    for row in data:
        vehicle_id, vehicle_no, driver, vehicle_type, empty_wt, loaded_wt = row[0], row[1], row[2], row[3], row[4], row[5]
        payload = loaded_wt - empty_wt if empty_wt and loaded_wt else 0
        tree.insert(parent='', index='end', iid=vehicle_id, text='', values=(vehicle_id, vehicle_no, driver, vehicle_type, empty_wt, loaded_wt, f"{payload:.2f}"))
    
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def edit_vehicle():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a vehicle")
            return
        
        vehicle_id = selected[0]
        cursor.execute("SELECT * FROM vehicles WHERE id=?", (vehicle_id,))
        row = cursor.fetchone()
        
        edit_win = Tk()
        edit_win.title(f"Edit Vehicle - {row[1]}")
        edit_win.geometry("350x420")
        
        Label(edit_win, text="Vehicle No").pack(pady=5)
        vno = Entry(edit_win)
        vno.insert(0, row[1])
        vno.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Driver Name").pack(pady=5)
        driver = Entry(edit_win)
        driver.insert(0, row[2])
        driver.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Vehicle Type").pack(pady=5)
        vehicle_type = StringVar(value=row[3])
        type_combo = ttk.Combobox(edit_win, textvariable=vehicle_type, values=["Truck", "Pickup", "Tractor", "6-Wheeler"], state="readonly", width=27)
        type_combo.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Empty Vehicle Weight (Kg)").pack(pady=5)
        empty_weight = Entry(edit_win)
        empty_weight.insert(0, row[4])
        empty_weight.pack(pady=5, padx=20, fill=X)
        
        Label(edit_win, text="Loaded Vehicle Weight (Kg)").pack(pady=5)
        loaded_weight = Entry(edit_win)
        loaded_weight.insert(0, row[5])
        loaded_weight.pack(pady=5, padx=20, fill=X)
        
        def save():
            if not all([vno.get(), driver.get(), empty_weight.get(), loaded_weight.get()]):
                messagebox.showerror("Error", "All fields are required")
                return
            try:
                empty_wt = float(empty_weight.get())
                loaded_wt = float(loaded_weight.get())
                
                if loaded_wt < empty_wt:
                    messagebox.showerror("Error", "Loaded weight must be >= empty weight")
                    return
                
                cursor.execute("UPDATE vehicles SET vehicle_no=?, driver=?, vehicle_type=?, empty_weight=?, loaded_weight=? WHERE id=?",
                              (vno.get(), driver.get(), vehicle_type.get(), empty_wt, loaded_wt, vehicle_id))
                conn.commit()
                messagebox.showinfo("Success", "Vehicle Updated!")
                edit_win.destroy()
                win.destroy()
                view_vehicles(role)
            except ValueError:
                messagebox.showerror("Error", "Weight must be numeric")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm", "Delete this vehicle?"):
                try:
                    cursor.execute("DELETE FROM vehicles WHERE id=?", (vehicle_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Vehicle Deleted!")
                    edit_win.destroy()
                    win.destroy()
                    view_vehicles(role)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        button_frame = Frame(edit_win)
        button_frame.pack(pady=10)
        Button(button_frame, text="Save", command=save, bg="#4CAF50", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete, bg="#F44336", fg="white", width=10).pack(side=LEFT, padx=5)
    
    if role == "Admin":
        Button(win, text="Edit Selected", command=edit_vehicle, bg="#2196F3", fg="white", width=25).pack(pady=10)
    else:
        Label(win, text="📖 View Only Mode - Admin privileges required for editing", font=("Arial", 9), fg="#666").pack(pady=10)

# ==============================
# INVOICE GENERATION
# ==============================

def generate_sale_invoice():
    win = Tk()
    win.title("Generate Sale Invoice")
    win.geometry("500x250")
    win.resizable(False, False)
    
    # Header
    header_frame = Frame(win, bg="#FF5722", height=60)
    header_frame.pack(fill=X)
    Label(header_frame, text="SALE INVOICE GENERATOR", font=("Arial", 14, "bold"), bg="#FF5722", fg="white").pack(pady=10)
    
    # Main frame
    main_frame = Frame(win, padx=30, pady=30)
    main_frame.pack()
    
    Label(main_frame, text="Enter Sale ID:", font=("Arial", 11, "bold")).pack(anchor=W, pady=(10, 5))
    sale_id = Entry(main_frame, font=("Arial", 11), width=30)
    sale_id.pack(pady=5)
    sale_id.focus()
    
    def create_invoice():
        try:
            sid = int(sale_id.get())
            cursor.execute("SELECT * FROM sales WHERE id=?", (sid,))
            sale = cursor.fetchone()
            
            if not sale:
                messagebox.showerror("Error", "Sale ID not found")
                return
            
            cursor.execute("SELECT name FROM parties WHERE id=?", (sale[1],))
            party = cursor.fetchone()
            
            cursor.execute("SELECT name FROM products WHERE id=?", (sale[2],))
            product = cursor.fetchone()
            
            # Get company info
            cursor.execute("SELECT * FROM company_info WHERE id=1")
            company = cursor.fetchone()
            
            # Get bank accounts
            cursor.execute("SELECT * FROM bank_accounts")
            banks = cursor.fetchall()
            
            # Create invoice window
            inv_win = Tk()
            inv_win.title(f"Sale Invoice #{sid}")
            inv_win.geometry("850x750")
            inv_win.resizable(True, True)
            
            # Header
            inv_header = Frame(inv_win, bg="#FF5722", height=80)
            inv_header.pack(fill=X)
            Label(inv_header, text="RICE MILL ERP", font=("Arial", 18, "bold"), bg="#FF5722", fg="white").pack(pady=5)
            Label(inv_header, text="SALE INVOICE", font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=5)
            
            # Content frame with scrollbar
            content_frame = Frame(inv_win)
            content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # Build bank details string
            bank_details = ""
            if banks:
                bank_details = "\nBANK DETAILS FOR PAYMENT\n" + "="*70 + "\n"
                for bank in banks:
                    bank_details += f"Bank Name:             {bank[1]}\n"
                    bank_details += f"Account Number:        {bank[2]}\n"
                    bank_details += f"IFSC Code:             {bank[3]}\n\n"
            
            # Invoice details
            details_text = f"""
{'RICE MILL ERP - SALE INVOICE':^70}

FROM (OUR DETAILS)
{'='*70}

Mill Name:             {company[1] if company else 'Rice Mill'}
GST Number:            {company[2] if company else 'N/A'}
Registration Number:   {company[3] if company else 'N/A'}
Contact Number:        {company[4] if company else 'N/A'}
Address:               {company[5] if company else 'N/A'}

INVOICE DETAILS
{'='*70}

Invoice Number:        {sale[0]}
Date:                  {sale[10]}

BILL TO (CUSTOMER DETAILS)
{'='*70}

Customer Name:         {party[0] if party else 'N/A'}
Customer Type:         Customer

PRODUCT INFORMATION
{'='*70}

Product Name:          {product[0] if product else 'N/A'}
Quantity:              {sale[3]} {sale[4]}
Rate Per Unit:         Rs. {sale[5]:.2f}

BILLING SUMMARY
{'='*70}

Subtotal Amount:       Rs. {sale[6]:.2f}
GST ({sale[7]:.1f}%):              Rs. {sale[8]:.2f}
                       {'─'*70}
TOTAL AMOUNT:          Rs. {sale[9]:.2f}
                       {'='*70}
{bank_details}

NOTES
{'='*70}

- Prices are inclusive of taxes where applicable
- Payment due within 30 days
- Please verify all details before payment
- For queries, contact us at {company[4] if company else 'N/A'}

Thank you for your business!
"""
            
            text_widget = Text(content_frame, wrap=WORD, font=("Courier", 9), 
                             bg="white", fg="#333", padx=15, pady=15, 
                             relief=RAISED, bd=1, height=28)
            text_widget.pack(fill=BOTH, expand=True)
            text_widget.insert(1.0, details_text)
            text_widget.config(state=DISABLED)
            
            # Button frame
            button_frame = Frame(inv_win, bg="#F5F5F5", height=60)
            button_frame.pack(fill=X, side=BOTTOM)
            
            button_inner = Frame(button_frame, bg="#F5F5F5")
            button_inner.pack(pady=10)
            
            def save_invoice():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile=f"Sale_Invoice_{sid}.txt"
                )
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(details_text)
                    messagebox.showinfo("Success", "Invoice saved successfully!")
            
            def print_invoice():
                messagebox.showinfo("Print", "Print functionality:\n\n1. Use Ctrl+P in this window\nor\n2. File > Print in your system")
            
            Button(button_inner, text="Save Invoice", command=save_invoice, 
                   bg="#4CAF50", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            Button(button_inner, text="Print", command=print_invoice, 
                   bg="#2196F3", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            Button(button_inner, text="Close", command=inv_win.destroy, 
                   bg="#757575", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            
            win.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Sale ID")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Buttons
    button_frame = Frame(win)
    button_frame.pack(pady=20)
    
    Button(button_frame, text="Generate Invoice", command=create_invoice, 
           bg="#FF5722", fg="white", font=("Arial", 11, "bold"), 
           width=20, padx=10, pady=10).pack()

def generate_purchase_invoice():
    win = Tk()
    win.title("Generate Purchase Invoice")
    win.geometry("500x250")
    win.resizable(False, False)
    
    # Header
    header_frame = Frame(win, bg="#FF5722", height=60)
    header_frame.pack(fill=X)
    Label(header_frame, text="PURCHASE INVOICE GENERATOR", font=("Arial", 14, "bold"), bg="#FF5722", fg="white").pack(pady=10)
    
    # Main frame
    main_frame = Frame(win, padx=30, pady=30)
    main_frame.pack()
    
    Label(main_frame, text="Enter Purchase ID:", font=("Arial", 11, "bold")).pack(anchor=W, pady=(10, 5))
    purchase_id = Entry(main_frame, font=("Arial", 11), width=30)
    purchase_id.pack(pady=5)
    purchase_id.focus()
    
    def create_invoice():
        try:
            pid = int(purchase_id.get())
            cursor.execute("SELECT * FROM purchases WHERE id=?", (pid,))
            purchase = cursor.fetchone()
            
            if not purchase:
                messagebox.showerror("Error", "Purchase ID not found")
                return
            
            cursor.execute("SELECT name FROM parties WHERE id=?", (purchase[1],))
            party = cursor.fetchone()
            
            cursor.execute("SELECT name FROM products WHERE id=?", (purchase[2],))
            product = cursor.fetchone()
            
            # Get company info
            cursor.execute("SELECT * FROM company_info WHERE id=1")
            company = cursor.fetchone()
            
            # Get bank accounts
            cursor.execute("SELECT * FROM bank_accounts")
            banks = cursor.fetchall()
            
            # Create invoice window
            inv_win = Tk()
            inv_win.title(f"Purchase Invoice #{pid}")
            inv_win.geometry("850x750")
            inv_win.resizable(True, True)
            
            # Header
            inv_header = Frame(inv_win, bg="#FF5722", height=80)
            inv_header.pack(fill=X)
            Label(inv_header, text="RICE MILL ERP", font=("Arial", 18, "bold"), bg="#FF5722", fg="white").pack(pady=5)
            Label(inv_header, text="PURCHASE INVOICE", font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=5)
            
            # Content frame
            content_frame = Frame(inv_win)
            content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            # Build bank details string
            bank_details = ""
            if banks:
                bank_details = "\nOUR BANK DETAILS FOR PAYMENT\n" + "="*70 + "\n"
                for bank in banks:
                    bank_details += f"Bank Name:             {bank[1]}\n"
                    bank_details += f"Account Number:        {bank[2]}\n"
                    bank_details += f"IFSC Code:             {bank[3]}\n\n"
            
            # Invoice details
            details_text = f"""
{'RICE MILL ERP - PURCHASE INVOICE':^70}

FROM (OUR DETAILS)
{'='*70}

Mill Name:             {company[1] if company else 'Rice Mill'}
GST Number:            {company[2] if company else 'N/A'}
Registration Number:   {company[3] if company else 'N/A'}
Contact Number:        {company[4] if company else 'N/A'}
Address:               {company[5] if company else 'N/A'}

INVOICE DETAILS
{'='*70}

Invoice Number:        {purchase[0]}
Date:                  {purchase[10]}

BILL FROM (VENDOR DETAILS)
{'='*70}

Vendor Name:           {party[0] if party else 'N/A'}
Vendor Type:           Supplier

PRODUCT INFORMATION
{'='*70}

Product Name:          {product[0] if product else 'N/A'}
Quantity:              {purchase[3]} {purchase[4]}
Rate Per Unit:         Rs. {purchase[5]:.2f}

BILLING SUMMARY
{'='*70}

Subtotal Amount:       Rs. {purchase[6]:.2f}
GST ({purchase[7]:.1f}%):              Rs. {purchase[8]:.2f}
                       {'─'*70}
TOTAL AMOUNT:          Rs. {purchase[9]:.2f}
                       {'='*70}
{bank_details}

NOTES
{'='*70}

- Prices are inclusive of taxes where applicable
- Payment due within 30 days
- Please verify all details before payment
- For queries, contact us at {company[4] if company else 'N/A'}

Thank you for your supply!
"""
            
            text_widget = Text(content_frame, wrap=WORD, font=("Courier", 9), 
                             bg="white", fg="#333", padx=15, pady=15, 
                             relief=RAISED, bd=1, height=28)
            text_widget.pack(fill=BOTH, expand=True)
            text_widget.insert(1.0, details_text)
            text_widget.config(state=DISABLED)
            
            # Button frame
            button_frame = Frame(inv_win, bg="#F5F5F5", height=60)
            button_frame.pack(fill=X, side=BOTTOM)
            
            button_inner = Frame(button_frame, bg="#F5F5F5")
            button_inner.pack(pady=10)
            
            def save_invoice():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile=f"Purchase_Invoice_{pid}.txt"
                )
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(details_text)
                    messagebox.showinfo("Success", "Invoice saved successfully!")
            
            def print_invoice():
                messagebox.showinfo("Print", "Print functionality:\n\n1. Use Ctrl+P in this window\nor\n2. File > Print in your system")
            
            Button(button_inner, text="Save Invoice", command=save_invoice, 
                   bg="#4CAF50", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            Button(button_inner, text="Print", command=print_invoice, 
                   bg="#2196F3", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            Button(button_inner, text="Close", command=inv_win.destroy, 
                   bg="#757575", fg="white", font=("Arial", 10), width=12, padx=10).pack(side=LEFT, padx=5)
            
            win.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Purchase ID")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Buttons
    button_frame = Frame(win)
    button_frame.pack(pady=20)
    
    Button(button_frame, text="Generate Invoice", command=create_invoice, 
           bg="#FF5722", fg="white", font=("Arial", 11, "bold"), 
           width=20, padx=10, pady=10).pack()

def main_dashboard(role):
    dashboard = Tk()
    dashboard.title("Rice Mill ERP - Dashboard")
    dashboard.geometry("1200x800")
    dashboard.config(bg="#F8FAFC")
    dashboard.state("zoomed")  # Maximize on Windows

    # Header with gradient effect
    header = Frame(dashboard, bg="#0F172A", height=100)
    header.pack(fill=X)
    header.pack_propagate(False)
    
    # Left side of header - Title
    left_header = Frame(header, bg="#0F172A")
    left_header.pack(side=LEFT, fill=BOTH, expand=True, padx=30, pady=15)
    
    Label(left_header, text="🌾 Rice Mill ERP", font=("Arial", 28, "bold"), bg="#0F172A", fg="white").pack(anchor=W)
    Label(left_header, text=f"Welcome, {role}!", font=("Arial", 12), bg="#0F172A", fg="#CBD5E1").pack(anchor=W, pady=(5, 0))
    
    # Right side of header - Info
    right_header = Frame(header, bg="#0F172A")
    right_header.pack(side=RIGHT, fill=Y, padx=30)
    
    from datetime import datetime
    current_time = datetime.now().strftime("%A, %B %d, %Y")
    Label(right_header, text=current_time, font=("Arial", 10), bg="#0F172A", fg="#94A3B8").pack(anchor=E, pady=(5, 0))
    Label(right_header, text=f"Role: {role}", font=("Arial", 11, "bold"), bg="#0F172A", fg="#60A5FA").pack(anchor=E, pady=(8, 0))

    # Main scrollable area
    canvas = Canvas(dashboard, bg="#F8FAFC", highlightthickness=0)
    scrollbar = ttk.Scrollbar(dashboard, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#F8FAFC")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Helper function to create modern section cards
    def create_section(title, icon, color):
        section = Frame(scrollable_frame, bg="white", relief=FLAT, bd=0)
        section.pack(fill=X, padx=20, pady=15)
        
        # Section header
        header_frame = Frame(section, bg=color, height=50)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)
        
        Label(header_frame, text=f"{icon} {title}", font=("Arial", 13, "bold"), 
              bg=color, fg="white").pack(anchor=W, padx=20, pady=12)
        
        # Content frame
        content = Frame(section, bg="#FFFFFF", padx=20, pady=15)
        content.pack(fill=X)
        
        return content
    
    # ADD DATA Section with grid layout
    add_content = create_section("📝 ADD DATA", "📝", "#3B82F6")
    
    # Create grid for add buttons (3 columns)
    buttons_data_add = [
        ("Add Mill", add_mill, "#4CAF50"),
        ("Add Godown", add_godown, "#4CAF50"),
        ("Add Product", add_product, "#4CAF50"),
        ("Add Party", add_party, "#4CAF50"),
        ("Purchase Entry", purchase_entry, "#2196F3"),
        ("Sale Entry", sale_entry, "#2196F3"),
        ("Add Staff", add_staff, "#9C27B0"),
        ("Add Vehicle", add_vehicle, "#9C27B0"),
        ("Processing Batch", processing_entry, "#FF9800"),
    ]
    
    for idx, (text, cmd, color) in enumerate(buttons_data_add):
        row = idx // 3
        col = idx % 3
        btn = Button(add_content, text=text, command=cmd, bg=color, fg="white", font=("Arial", 10, "bold"),
                     relief=FLAT, bd=0, padx=15, pady=10, cursor="hand2", activebackground=color, activeforeground="white")
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew", ipady=8)
    
    add_content.grid_columnconfigure(0, weight=1)
    add_content.grid_columnconfigure(1, weight=1)
    add_content.grid_columnconfigure(2, weight=1)
    
    # VIEW DATA Section with grid layout
    view_content = create_section("👁️ VIEW DATA", "👁️", "#8B5CF6")
    
    buttons_data_view = [
        ("View Mills", lambda r=role: view_mills(r), "#607D8B"),
        ("View Godowns", lambda r=role: view_godowns(r), "#607D8B"),
        ("View Products", lambda r=role: view_products(r), "#607D8B"),
        ("View Parties", lambda r=role: view_parties(r), "#607D8B"),
        ("View Purchases", lambda r=role: view_purchases(r), "#607D8B"),
        ("View Sales", lambda r=role: view_sales(r), "#607D8B"),
        ("View Staff", lambda r=role: view_staff(r), "#607D8B"),
        ("View Vehicles", lambda r=role: view_vehicles(r), "#607D8B"),
        ("View Processing", lambda r=role: view_processing(r), "#607D8B"),
    ]
    
    for idx, (text, cmd, color) in enumerate(buttons_data_view):
        row = idx // 3
        col = idx % 3
        btn = Button(view_content, text=text, command=cmd, bg=color, fg="white", font=("Arial", 10, "bold"),
                     relief=FLAT, bd=0, padx=15, pady=10, cursor="hand2", activebackground=color, activeforeground="white")
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew", ipady=8)
    
    view_content.grid_columnconfigure(0, weight=1)
    view_content.grid_columnconfigure(1, weight=1)
    view_content.grid_columnconfigure(2, weight=1)
    
    # INVOICES Section
    invoice_content = create_section("📄 INVOICES & REPORTS", "📄", "#EC4899")
    
    Button(invoice_content, text="Generate Sale Invoice", command=generate_sale_invoice, 
           bg="#FF5722", fg="white", font=("Arial", 10, "bold"), relief=FLAT, bd=0, 
           padx=15, pady=12, cursor="hand2", activebackground="#E64A19", activeforeground="white").pack(fill=X, pady=6)
    Button(invoice_content, text="Generate Purchase Invoice", command=generate_purchase_invoice, 
           bg="#FF5722", fg="white", font=("Arial", 10, "bold"), relief=FLAT, bd=0, 
           padx=15, pady=12, cursor="hand2", activebackground="#E64A19", activeforeground="white").pack(fill=X, pady=6)
    
    # SETTINGS Section  
    settings_content = create_section("⚙️ SETTINGS & CONFIGURATION", "⚙️", "#14B8A6")
    
    buttons_data_settings = [
        ("Add Company", add_company_info, "#673AB7"),
        ("View/Edit Companies", lambda r=role: view_companies(r), "#673AB7"),
        ("Add Bank Account", add_bank_account, "#673AB7"),
        ("View Bank Accounts", lambda r=role: view_bank_accounts(r), "#673AB7"),
    ]
    
    for idx, (text, cmd, color) in enumerate(buttons_data_settings):
        row = idx // 2
        col = idx % 2
        btn = Button(settings_content, text=text, command=cmd, bg=color, fg="white", font=("Arial", 10, "bold"),
                     relief=FLAT, bd=0, padx=15, pady=10, cursor="hand2", activebackground=color, activeforeground="white")
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew", ipady=8)
    
    settings_content.grid_columnconfigure(0, weight=1)
    settings_content.grid_columnconfigure(1, weight=1)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Bind mouse wheel to scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    dashboard.mainloop()

# ==============================
# LOGIN SYSTEM
# ==============================

def login():
    username = user_entry.get()
    password = pass_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password")
        return

    cursor.execute("SELECT role FROM users WHERE username=? AND password=?",
                   (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful")
        login_window.destroy()
        main_dashboard(result[0])
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# ==============================
# DEFAULT USERS (ADMIN & ACCOUNTANT)
# ==============================

cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users(username,password,role) VALUES('admin','admin','Admin')")
    conn.commit()

cursor.execute("SELECT * FROM users WHERE username='accountant'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users(username,password,role) VALUES('accountant','accountant','Accountant')")
    conn.commit()

# ==============================
# MODERN LOGIN WINDOW
# ==============================

login_window = Tk()
login_window.title("Rice Mill ERP - Login")
login_window.geometry("500x600")
login_window.resizable(False, False)

# Background gradient effect using frames
bg_frame = Frame(login_window, bg="#1E3A8A")
bg_frame.pack(fill=BOTH, expand=True)

# Top header section
header = Frame(bg_frame, bg="#2563EB", height=180)
header.pack(fill=X)
header.pack_propagate(False)

# Logo/Title area
Label(header, text="🌾", font=("Arial", 60), bg="#2563EB", fg="white").pack(pady=(20, 10))
Label(header, text="RICE MILL ERP", font=("Arial", 26, "bold"), bg="#2563EB", fg="white").pack()
Label(header, text="Enterprise Resource Planning System", font=("Arial", 10), bg="#2563EB", fg="#E0E7FF").pack(pady=(5, 0))

# Login form section
form_frame = Frame(bg_frame, bg="#1E3A8A")
form_frame.pack(fill=BOTH, expand=True, padx=40, pady=30)

# Username section
Label(form_frame, text="Username", font=("Arial", 11, "bold"), bg="#1E3A8A", fg="white").pack(anchor=W, pady=(20, 5))
user_entry = Entry(form_frame, font=("Arial", 12), bg="#FFFFFF", fg="#1E3A8A", relief=FLAT, bd=0)
user_entry.pack(fill=X, ipady=12, pady=(0, 15))

# Password section
Label(form_frame, text="Password", font=("Arial", 11, "bold"), bg="#1E3A8A", fg="white").pack(anchor=W, pady=(0, 5))
pass_entry = Entry(form_frame, font=("Arial", 12), bg="#FFFFFF", fg="#1E3A8A", show="*", relief=FLAT, bd=0)
pass_entry.pack(fill=X, ipady=12, pady=(0, 10))

# Demo credentials info
demo_frame = Frame(form_frame, bg="#1E40AF", relief=FLAT)
demo_frame.pack(fill=X, pady=(0, 20))
Label(demo_frame, text="Demo Credentials: admin / admin  |  accountant / accountant", font=("Arial", 8), bg="#1E40AF", fg="#E0E7FF").pack(pady=8)

# Login button
login_btn = Button(form_frame, text="LOGIN", command=login, bg="#3B82F6", fg="white", font=("Arial", 12, "bold"), 
                   relief=FLAT, bd=0, padx=20, pady=12, cursor="hand2", activebackground="#2563EB", activeforeground="white")
login_btn.pack(fill=X, pady=(10, 0))

login_window.mainloop()
