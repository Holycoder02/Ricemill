# Rice Mill ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed specifically for rice mill operations. This application provides tools for managing mills, storage facilities (godowns), inventory, and operational workflows.

## Features

- **User Management**: Role-based access control for different user types
- **Mill Management**: Track and manage multiple rice mills
- **Godown Management**: Monitor storage facilities with capacity tracking
- **Inventory Tracking**: Real-time stock management and movement tracking
- **Database Storage**: SQLite database for reliable data persistence
- **Desktop Application**: User-friendly Tkinter GUI interface

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows (batch scripts optimized for Windows)
- **RAM**: Minimum 2GB
- **Storage**: 500MB for application and database

## Installation

### Option 1: Quick Setup (Recommended)

1. Ensure Python is installed and added to your system PATH
2. Run the setup script:
```bash
setup_all.bat
```

This script will:
- Build the executable application
- Create a desktop shortcut for easy access

### Option 2: Manual Setup

1. Install Python from [python.org](https://www.python.org)

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application directly:
```bash
python create.py
```

## Building Standalone Executable

To create a standalone executable that doesn't require Python to be installed:

```bash
build_app.bat
```

The built executable will be located in the `dist` folder as `RiceMill ERP.exe`

## Project Structure

```
Ricemill/
├── create.py                 # Main application file
├── generate_summary.py       # Report generation utility
├── RiceMill ERP.spec         # PyInstaller configuration
├── rice_mill_erp.db          # SQLite database file
├── build_app.bat             # Build executable script
├── setup_all.bat             # Complete setup script
├── create_shortcut.bat       # Desktop shortcut creation
└── README.md                 # This file
```

## Usage

### First Time Setup

1. Run `setup_all.bat` or directly execute `python create.py`
2. Create a user account with appropriate role
3. Configure your mills and storage facilities
4. Begin tracking inventory and operations

### Daily Operations

- Log in with your credentials
- Access mill and godown management features
- Track inventory movements
- Generate reports as needed

## Database

The application uses SQLite for data storage. Database file: `rice_mill_erp.db`

Database tables include:
- **users**: User accounts and authentication
- **mills**: Rice mill information
- **godowns**: Storage facility details with capacity tracking
- **godown_entries**: Inventory movement records
- And other operational tables

## Troubleshooting

### Python Not Found Error
- Ensure Python is installed from [python.org](https://www.python.org)
- Add Python to your system PATH

### Database Errors
- Check that the application has write permissions in the application directory
- Ensure the database file is not corrupted
- Delete `rice_mill_erp.db` to start with a fresh database

### GUI Not Displaying
- Verify that Tkinter is included with your Python installation
- On Windows, Tkinter is typically included by default

## Development

This project uses:
- **Python**: Application logic
- **Tkinter**: GUI framework
- **SQLite3**: Database management
- **PyInstaller**: Executable packaging

## License

[Add your license information here]

## Support

For issues, feature requests, or contributions, please contact the development team.

## Version History

- **v1.0**: Initial release with core ERP functionality
  - User management
  - Mill and godown management
  - Basic inventory tracking

---

**Last Updated**: April 2026
