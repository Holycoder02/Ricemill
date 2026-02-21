from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create PDF
pdf_path = "Ricemill_ERP_Summary.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=0.75*inch, leftMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Story to contain the platypus flowable objects
story = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2e5c8a'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    leading=12
)

# Title
story.append(Paragraph("RICE MILL ERP SYSTEM", title_style))
story.append(Paragraph("Project Summary & Technical Documentation", styles['Heading3']))
story.append(Spacer(1, 0.3*inch))

# Document Metadata
meta_data = [
    ['Project Name:', 'Rice Mill ERP System'],
    ['Generated:', datetime.now().strftime("%B %d, %Y")],
    ['Type:', 'Enterprise Resource Planning Application'],
    ['Platform:', 'Windows Desktop Application'],
    ['Technology:', 'Python, Tkinter, SQLite3']
]
meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
meta_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
]))
story.append(meta_table)
story.append(Spacer(1, 0.3*inch))

# Overview
story.append(Paragraph("PROJECT OVERVIEW", heading_style))
overview_text = """The Rice Mill ERP System is a comprehensive enterprise resource planning application designed 
specifically for rice milling operations. It provides integrated management of multiple facilities, inventory, 
financial transactions, and operational workflows. Built with Python and Tkinter, it offers a user-friendly 
desktop interface with robust SQLite database backend."""
story.append(Paragraph(overview_text, body_style))
story.append(Spacer(1, 0.2*inch))

# Key Features
story.append(Paragraph("KEY FEATURES", heading_style))

features = [
    "User Management - Role-based access control and authentication",
    "Multi-Location Support - Manage multiple rice mills and godowns (storage facilities)",
    "Inventory Management - Track storage capacity, stock levels, and movement history",
    "Financial Management - Bank account setup and account payable/receivable tracking",
    "Party Management - Manage suppliers, customers, and business partners",
    "Product Management - Catalog rice products and varieties",
    "Godown Operations - Monitor storage facilities, capacity utilization, and storage rates",
    "Entry Logging - Track all godown entries with timestamps and party information",
    "Reports & Analytics - Generate business reports and performance metrics",
]

for i, feature in enumerate(features, 1):
    story.append(Paragraph(f"<b>{i}. {feature}</b>", body_style))

story.append(Spacer(1, 0.2*inch))

# Database Structure
story.append(Paragraph("DATABASE ARCHITECTURE", heading_style))
db_text = """The system uses SQLite3 for data persistence with the following core tables:"""
story.append(Paragraph(db_text, body_style))

db_tables = [
    ['Table Name', 'Purpose'],
    ['users', 'Store user accounts and authentication credentials'],
    ['mills', 'Store rice mill location information'],
    ['godowns', 'Track storage facilities and capacity'],
    ['godown_entries', 'Log all inventory transactions and movements'],
    ['companies', 'Financial entity and business information'],
    ['bank_accounts', 'Bank account details and financial records'],
    ['products', 'Rice product catalog and specifications'],
    ['parties', 'Supplier and customer information'],
    ['accounts_payable', 'Outstanding payments to suppliers'],
    ['accounts_receivable', 'Outstanding payments from customers'],
]

table_obj = Table(db_tables, colWidths=[2*inch, 3.5*inch])
table_obj.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5fa')])
]))
story.append(table_obj)
story.append(Spacer(1, 0.2*inch))

# Core Modules
story.append(Paragraph("CORE MODULES", heading_style))

modules_text = """
<b>1. Company Management:</b> Setup and maintain company information with bank accounts and financial details.<br/>
<br/>
<b>2. Mill Management:</b> Register and manage multiple rice milling facilities across different locations.<br/>
<br/>
<b>3. Godown Management:</b> Control storage facility operations including capacity tracking, stock monitoring, and storage charges.<br/>
<br/>
<b>4. Product Catalog:</b> Maintain a comprehensive list of rice products with specifications and pricing.<br/>
<br/>
<b>5. Party Management:</b> Manage supplier and customer information for procurement and sales activities.<br/>
<br/>
<b>6. Financial Module:</b> Track accounts payable and receivable with reporting capabilities.<br/>
<br/>
<b>7. Transaction Logging:</b> Record all godown entries with complete audit trails including timestamps, parties, products, and quantities.
"""
story.append(Paragraph(modules_text, body_style))
story.append(Spacer(1, 0.2*inch))

# Installation & Deployment
story.append(PageBreak())
story.append(Paragraph("INSTALLATION & DEPLOYMENT", heading_style))

install_text = """The project includes automated setup scripts for easy deployment on Windows systems:"""
story.append(Paragraph(install_text, body_style))

scripts = [
    ['Script', 'Description'],
    ['build_app.bat', 'Builds executable using PyInstaller; automates dependency checking and compilation'],
    ['create_shortcut.bat', 'Creates desktop shortcut for easy application launch'],
    ['setup_all.bat', 'Master setup script that orchestrates build and shortcut creation'],
]

scripts_table = Table(scripts, colWidths=[2*inch, 3.5*inch])
scripts_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5fa')])
]))
story.append(scripts_table)
story.append(Spacer(1, 0.2*inch))

# Technical Stack
story.append(Paragraph("TECHNICAL STACK", heading_style))

tech_stack = [
    ['Technology', 'Version', 'Purpose'],
    ['Python', '3.x', 'Core programming language'],
    ['Tkinter', 'Built-in', 'GUI framework for desktop interface'],
    ['SQLite3', 'Embedded', 'Local database management'],
    ['PyInstaller', 'Latest', 'Executable packaging and distribution'],
]

tech_table = Table(tech_stack, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f5fa')])
]))
story.append(tech_table)
story.append(Spacer(1, 0.2*inch))

# User Roles
story.append(Paragraph("USER ROLES & PERMISSIONS", heading_style))

roles_text = """The system supports role-based access control to ensure data integrity and appropriate user privileges:
<br/>
<b>• Accountant:</b> Full access to financial records, accounts payable/receivable, and company information.<br/>
<b>• Manager:</b> Access to inventory, godown operations, and operational reports.<br/>
<b>• Admin:</b> Complete system access including user management, configuration, and all operational modules.
"""
story.append(Paragraph(roles_text, body_style))
story.append(Spacer(1, 0.2*inch))

# System Requirements
story.append(Paragraph("SYSTEM REQUIREMENTS", heading_style))

requirements_text = """
<b>Minimum Requirements:</b><br/>
• Operating System: Windows 7 or later<br/>
• Processor: Intel Core 2 Duo or equivalent<br/>
• RAM: 2 GB minimum<br/>
• Storage: 500 MB free disk space<br/>
• Display: 1024x768 resolution minimum<br/>
<br/>
<b>Recommended Specifications:</b><br/>
• Operating System: Windows 10 or Windows 11<br/>
• Processor: Intel Core i5 or higher<br/>
• RAM: 4 GB or more<br/>
• Storage: 1 GB free disk space<br/>
• Display: 1280x1024 or higher
"""
story.append(Paragraph(requirements_text, body_style))
story.append(Spacer(1, 0.2*inch))

# Getting Started
story.append(Paragraph("GETTING STARTED", heading_style))

getting_started_text = """
<b>Step 1:</b> Run setup_all.bat from the project directory<br/>
<b>Step 2:</b> The script validates Python installation and installs required packages<br/>
<b>Step 3:</b> Application is compiled into a standalone executable<br/>
<b>Step 4:</b> Optional: Create desktop shortcut for quick access<br/>
<b>Step 5:</b> Launch the application and create admin user account<br/>
<b>Step 6:</b> Configure company information and mill locations<br/>
<b>Step 7:</b> Begin operational activities and data entry<br/>
"""
story.append(Paragraph(getting_started_text, body_style))
story.append(Spacer(1, 0.3*inch))

# Footer
story.append(Spacer(1, 0.2*inch))
footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.grey,
    alignment=TA_CENTER
)
story.append(Paragraph("_______________________________________________________________", footer_style))
story.append(Paragraph(f"Rice Mill ERP System | Project Summary | {datetime.now().strftime('%B %d, %Y')}", footer_style))

# Build PDF
doc.build(story)
print(f"✓ PDF Summary created successfully: {pdf_path}")
print(f"✓ Location: {pdf_path}")
