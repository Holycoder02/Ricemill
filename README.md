# 🌾 Rice Mill ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed specifically for rice mill operations. Built with Python, Tkinter, and SQLite — featuring a modern UI, role-based access control, and complete inventory management.

## Features

- **🔐 Secure Authentication** — PBKDF2-HMAC-SHA256 password hashing with per-user salts
- **👥 Role-Based Access** — Admin, Manager, and Accountant roles with granular permissions
- **🏭 Mill Management** — Track and manage multiple rice mills
- **🏢 Godown Management** — Monitor storage facilities with capacity tracking and stock updates
- **📦 Product & Category** — Full product catalog with category organization
- **👤 Party Management** — Manage customers, suppliers, and brokers
- **📥 Purchase & Sale Tracking** — Complete transaction management with GST calculation
- **⚙️ Processing Batches** — Track rice processing from raw to finished products
- **👷 Staff Management** — Employee records with flexible payout types
- **🚛 Vehicle Management** — Fleet tracking with weight/payload calculations
- **📄 Invoice Generation** — Professional invoices with company letterhead and bank details
- **🏦 Banking** — Bank account management for payment tracking
- **🔍 Search & Filter** — Real-time search across all data tables
- **📊 Dashboard Stats** — Live statistics cards with key business metrics

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (batch scripts optimized for Windows)
- **RAM**: Minimum 2GB
- **Storage**: 500MB for application and database

## Installation

### Option 1: Quick Setup (Recommended)

1. Ensure Python is installed and added to your system PATH
2. Run the setup script:
   ```bash
   setup_all.bat
   ```

### Option 2: Manual Setup

1. Install Python from [python.org](https://www.python.org)

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Default Login Credentials

| Role       | Username     | Password  |
|------------|-------------|-----------|
| Admin      | `admin`     | `admin123`|
| Accountant | `accountant`| `acc123`  |
| Manager    | `manager`   | `mgr123`  |

> **Note:** Passwords are hashed on first run. Change them after initial setup.

## Building Standalone Executable

```bash
build_app.bat
```

The built executable will be located in `dist/RiceMill ERP.exe`

## Project Structure

```
Ricemill/
├── app.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
│
├── db/                       # Database layer
│   ├── __init__.py
│   ├── connection.py         # Connection manager with WAL mode
│   ├── schema.py             # Table definitions & migrations
│   └── models.py             # CRUD operations for all tables
│
├── auth/                     # Authentication & security
│   ├── __init__.py
│   └── password.py           # PBKDF2 hashing & verification
│
├── ui/                       # User interface
│   ├── __init__.py
│   ├── theme.py              # Colors, fonts, styling system
│   ├── components.py         # Reusable widgets (DataTable, FormDialog)
│   ├── login.py              # Login window
│   ├── dashboard.py          # Main dashboard & all form handlers
│   └── invoice.py            # Invoice generation
│
├── utils/                    # Utilities
│   ├── __init__.py
│   ├── validators.py         # Input validation (GST, phone, IFSC)
│   └── formatters.py         # Currency & weight formatting
│
├── build_app.bat             # Build executable script
├── setup_all.bat             # Complete setup script
├── create_shortcut.bat       # Desktop shortcut creation
├── generate_summary.py       # PDF report generation
└── README.md                 # This file
```

## User Roles & Permissions

| Feature              | Admin | Manager | Accountant |
|---------------------|-------|---------|------------|
| View all data       | ✅    | ✅      | ✅         |
| Add records         | ✅    | ✅      | ✅         |
| Edit records        | ✅    | ✅      | ❌         |
| Delete records      | ✅    | ❌      | ❌         |
| Company settings    | ✅    | ❌      | ❌         |
| Generate invoices   | ✅    | ✅      | ✅         |

## Technology Stack

| Technology   | Purpose                        |
|-------------|--------------------------------|
| Python 3.x  | Core programming language      |
| Tkinter     | GUI framework (ttk themed)     |
| SQLite3     | Embedded database (WAL mode)   |
| PyInstaller | Executable packaging           |
| ReportLab   | PDF report generation          |

## Troubleshooting

### Python Not Found
- Install Python from [python.org](https://www.python.org)
- Ensure "Add Python to PATH" is checked during installation

### Database Errors
- The app auto-creates the database on first run
- Delete `rice_mill_erp.db` to reset to a fresh database
- Ensure the app has write permissions in its directory

### GUI Not Displaying
- Tkinter is included with standard Python installations on Windows
- If missing, reinstall Python with the "tcl/tk" option checked

## License

MIT License — See LICENSE file for details.

## Version History

- **v2.0** — Complete architecture overhaul
  - Modular codebase (db/, auth/, ui/, utils/ packages)
  - Secure password hashing (PBKDF2-HMAC-SHA256)
  - Manager role with edit-only permissions
  - Category management UI
  - Godown entry creation
  - Search/filter on all data tables
  - Scrollbars on all tables
  - Names displayed instead of raw IDs
  - Real print functionality
  - Dashboard statistics cards
  - Input validation (GST, phone, IFSC)
  - Indian currency formatting (₹)
  - Exit/logout confirmation dialogs
  - Fixed party & staff type inconsistencies
  - Fixed GST field mapping in edit forms
  - Proper Toplevel windows (no ghost windows)

- **v1.0** — Initial release
  - Basic ERP functionality
  - User management
  - Mill and godown management

---

**Last Updated**: April 2026
