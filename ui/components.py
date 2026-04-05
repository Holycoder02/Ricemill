"""
Reusable UI components for Rice Mill ERP.

These replace the 10+ copy-pasted view/edit/delete functions from the old code
with generic, configurable widgets.
"""

from tkinter import *
from tkinter import ttk, messagebox
from ui.theme import Colors, Fonts, Spacing, apply_theme


# ═══════════════════════════════════════════════
# SCROLLABLE TABLE VIEW
# ═══════════════════════════════════════════════

class DataTableView:
    """
    A reusable data table with search bar, scrollbar, context menu,
    and role-based edit/delete support.

    Replaces ALL the copy-pasted view_mills(), view_godowns(), etc.
    """

    def __init__(self, parent_root, title, columns, data_fn, role="Accountant",
                 on_edit=None, on_delete=None, on_add=None, width=900, height=500,
                 format_row=None):
        """
        Args:
            parent_root: The parent Tk/Toplevel window
            title: Window title
            columns: List of (column_id, column_heading, width) tuples
            data_fn: Callable that returns list of row tuples
            role: User role for permission checks
            on_edit: Callable(row_data) for editing a record
            on_delete: Callable(row_id) for deleting a record
            on_add: Callable() for adding a new record
            format_row: Optional callable(row) -> formatted_values tuple
        """
        self.role = role
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_add = on_add
        self.data_fn = data_fn
        self.format_row = format_row
        self.columns = columns

        self.win = Toplevel(parent_root)
        self.win.title(title)
        self.win.geometry(f"{width}x{height}")
        self.win.configure(bg=Colors.BG_PAGE)
        self.win.minsize(600, 400)
        apply_theme(self.win)

        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        """Build the complete table view UI."""
        # ── Header Bar ──
        header = Frame(self.win, bg=Colors.BG_DARK, height=50)
        header.pack(fill=X)
        header.pack_propagate(False)

        Label(header, text=self.win.title(), font=Fonts.SUBHEADING,
              bg=Colors.BG_DARK, fg=Colors.TEXT_PRIMARY).pack(side=LEFT, padx=Spacing.LG, pady=Spacing.MD)

        # Record count label
        self.count_label = Label(header, text="", font=Fonts.SMALL,
                                  bg=Colors.BG_DARK, fg=Colors.TEXT_SECONDARY)
        self.count_label.pack(side=RIGHT, padx=Spacing.LG)

        # ── Search Bar ──
        search_frame = Frame(self.win, bg=Colors.BG_PAGE, padx=Spacing.LG, pady=Spacing.SM)
        search_frame.pack(fill=X)

        Label(search_frame, text="🔍", font=Fonts.BODY, bg=Colors.BG_PAGE).pack(side=LEFT)
        self.search_var = StringVar()
        self.search_var.trace_add("write", lambda *args: self._filter_data())
        search_entry = Entry(search_frame, textvariable=self.search_var, font=Fonts.INPUT,
                             bg=Colors.INPUT_BG, fg=Colors.INPUT_TEXT, relief=SOLID, bd=1,
                             insertbackground=Colors.INPUT_TEXT)
        search_entry.pack(side=LEFT, fill=X, expand=True, padx=(Spacing.SM, 0), ipady=6)

        # ── Action buttons (top right) ──
        btn_frame = Frame(search_frame, bg=Colors.BG_PAGE)
        btn_frame.pack(side=RIGHT, padx=(Spacing.SM, 0))

        if self.on_add and self.role in ("Admin", "Manager"):
            self._make_button(btn_frame, "＋ Add New", Colors.SUCCESS, self.on_add).pack(side=LEFT, padx=2)

        self._make_button(btn_frame, "⟳ Refresh", Colors.PRIMARY, self.refresh_data).pack(side=LEFT, padx=2)

        # ── Table ──
        table_frame = Frame(self.win, bg=Colors.BG_PAGE, padx=Spacing.LG, pady=Spacing.SM)
        table_frame.pack(fill=BOTH, expand=True)

        col_ids = [c[0] for c in self.columns]
        self.tree = ttk.Treeview(table_frame, columns=col_ids, show="headings", selectmode="browse")

        for col_id, heading, width in self.columns:
            self.tree.heading(col_id, text=heading, anchor=W)
            self.tree.column(col_id, anchor=W, width=width, minwidth=40)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Alternating row colors via tags
        self.tree.tag_configure("even", background=Colors.TABLE_ROW_EVEN)
        self.tree.tag_configure("odd", background=Colors.TABLE_ROW_ODD)

        # ── Context menu / interactions ──
        if self.role == "Admin":
            self.tree.bind("<Double-1>", lambda e: self._edit_selected())
            self.tree.bind("<Button-3>", self._show_context_menu)
            self.tree.bind("<Delete>", lambda e: self._delete_selected())
        elif self.role == "Manager":
            self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        # ── Bottom bar ──
        bottom = Frame(self.win, bg=Colors.BG_PAGE, padx=Spacing.LG, pady=Spacing.MD)
        bottom.pack(fill=X)

        if self.role == "Admin":
            self._make_button(bottom, "✏ Edit", Colors.PRIMARY, self._edit_selected).pack(side=LEFT, padx=4)
            self._make_button(bottom, "🗑 Delete", Colors.DANGER, self._delete_selected).pack(side=LEFT, padx=4)
        elif self.role == "Manager":
            self._make_button(bottom, "✏ Edit", Colors.PRIMARY, self._edit_selected).pack(side=LEFT, padx=4)
            Label(bottom, text="ℹ Manager role — editing only", font=Fonts.TINY,
                  bg=Colors.BG_PAGE, fg=Colors.TEXT_MUTED).pack(side=RIGHT)
        else:
            Label(bottom, text="📖 View Only — requires Admin/Manager access for editing", font=Fonts.SMALL,
                  bg=Colors.BG_PAGE, fg=Colors.TEXT_MUTED).pack(side=LEFT)

    def refresh_data(self):
        """Reload data from the database."""
        self.all_data = self.data_fn()
        self._populate_tree(self.all_data)

    def _populate_tree(self, data):
        """Populate the treeview with data."""
        self.tree.delete(*self.tree.get_children())
        for idx, row in enumerate(data):
            tag = "even" if idx % 2 == 0 else "odd"
            values = self.format_row(row) if self.format_row else row
            self.tree.insert("", END, iid=str(row[0]), values=values, tags=(tag,))
        self.count_label.configure(text=f"{len(data)} records")

    def _filter_data(self):
        """Filter displayed data based on search query."""
        query = self.search_var.get().lower().strip()
        if not query:
            self._populate_tree(self.all_data)
            return

        filtered = []
        for row in self.all_data:
            row_text = " ".join(str(val).lower() for val in row)
            if query in row_text:
                filtered.append(row)
        self._populate_tree(filtered)

    def _get_selected(self):
        """Get the selected row data."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a record first.", parent=self.win)
            return None
        return sel[0]

    def _edit_selected(self):
        """Edit the selected record."""
        if self.on_edit is None:
            return
        row_id = self._get_selected()
        if row_id:
            self.on_edit(row_id, self.win, self.refresh_data)

    def _delete_selected(self):
        """Delete the selected record."""
        if self.on_delete is None or self.role not in ("Admin",):
            return
        row_id = self._get_selected()
        if row_id:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?", parent=self.win):
                self.on_delete(int(row_id))
                self.refresh_data()

    def _show_context_menu(self, event):
        """Show right-click context menu."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = Menu(self.win, tearoff=0, font=Fonts.SMALL,
                        bg=Colors.CARD_BG, fg=Colors.TEXT_DARK)
            menu.add_command(label="✏  Edit", command=self._edit_selected)
            menu.add_separator()
            menu.add_command(label="🗑  Delete", command=self._delete_selected)
            menu.post(event.x_root, event.y_root)

    def _make_button(self, parent, text, color, command):
        """Create a styled button."""
        btn = Button(parent, text=text, command=command, bg=color, fg="white",
                     font=Fonts.BUTTON_SM, relief=FLAT, bd=0, padx=14, pady=6,
                     cursor="hand2", activebackground=color, activeforeground="white")
        return btn


# ═══════════════════════════════════════════════
# FORM DIALOG
# ═══════════════════════════════════════════════

class FormDialog:
    """
    A reusable form dialog for add/edit operations.

    Replaces all the copy-pasted add_mill(), add_product(), etc.
    """

    def __init__(self, parent, title, fields, on_save, initial_values=None,
                 width=420, height=None):
        """
        Args:
            parent: Parent window
            title: Dialog title
            fields: List of field definitions, each a dict with:
                - "label": Display label
                - "key": Field key for the result dict
                - "type": "entry", "combo", "text", "readonly"
                - "options": List of options for combo type
                - "default": Default value
                - "required": Boolean
                - "validate": Optional validation function
            on_save: Callable(values_dict) called when save is clicked
            initial_values: Dict of initial values for editing
        """
        self.parent = parent
        self.on_save = on_save
        self.fields = fields
        self.widgets = {}

        # Calculate height if not specified
        if height is None:
            height = 120 + len(fields) * 70
            height = min(height, 650)

        self.win = Toplevel(parent)
        self.win.title(title)
        self.win.geometry(f"{width}x{height}")
        self.win.configure(bg=Colors.BG_PAGE)
        self.win.resizable(False, True)
        self.win.transient(parent)
        self.win.grab_set()
        apply_theme(self.win)

        self._build_ui(initial_values)

        # Bind Enter key to save
        self.win.bind("<Return>", lambda e: self._handle_save())
        self.win.bind("<Escape>", lambda e: self.win.destroy())

    def _build_ui(self, initial_values):
        """Build the form UI."""
        # Header
        header = Frame(self.win, bg=Colors.BG_DARK, height=45)
        header.pack(fill=X)
        header.pack_propagate(False)
        Label(header, text=self.win.title(), font=Fonts.SUBHEADING,
              bg=Colors.BG_DARK, fg=Colors.TEXT_PRIMARY).pack(side=LEFT, padx=Spacing.LG, pady=Spacing.SM)

        # Scrollable form area
        canvas = Canvas(self.win, bg=Colors.BG_PAGE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.win, orient=VERTICAL, command=canvas.yview)
        form_container = Frame(canvas, bg=Colors.BG_PAGE, padx=Spacing.XL, pady=Spacing.MD)

        form_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_container, anchor="nw", width=self.win.winfo_reqwidth() - 20)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Build fields
        for field in self.fields:
            key = field["key"]
            label_text = field["label"]
            field_type = field.get("type", "entry")
            options = field.get("options", [])
            default = field.get("default", "")
            required = field.get("required", True)

            # Get initial value
            init_val = ""
            if initial_values and key in initial_values:
                init_val = initial_values[key]
            elif default:
                init_val = default

            # Label with required indicator
            label_display = f"{label_text} *" if required else label_text
            Label(form_container, text=label_display, font=Fonts.BODY_BOLD,
                  bg=Colors.BG_PAGE, fg=Colors.TEXT_DARK).pack(anchor=W, pady=(Spacing.SM, 2))

            if field_type == "combo":
                var = StringVar(value=str(init_val))
                widget = ttk.Combobox(form_container, textvariable=var, values=options,
                                       state="readonly", font=Fonts.INPUT)
                widget.pack(fill=X, pady=(0, Spacing.SM), ipady=4)
                self.widgets[key] = var
            elif field_type == "text":
                widget = Text(form_container, font=Fonts.INPUT, height=4,
                              bg=Colors.INPUT_BG, fg=Colors.INPUT_TEXT, relief=SOLID, bd=1,
                              insertbackground=Colors.INPUT_TEXT)
                widget.pack(fill=X, pady=(0, Spacing.SM))
                if init_val:
                    widget.insert("1.0", str(init_val))
                self.widgets[key] = widget
            elif field_type == "readonly":
                var = StringVar(value=str(init_val))
                widget = Entry(form_container, textvariable=var, font=Fonts.INPUT,
                               bg="#E2E8F0", fg=Colors.TEXT_MUTED, relief=SOLID, bd=1,
                               state="readonly")
                widget.pack(fill=X, pady=(0, Spacing.SM), ipady=6)
                self.widgets[key] = var
            else:  # entry
                var = StringVar(value=str(init_val))
                widget = Entry(form_container, textvariable=var, font=Fonts.INPUT,
                               bg=Colors.INPUT_BG, fg=Colors.INPUT_TEXT, relief=SOLID, bd=1,
                               insertbackground=Colors.INPUT_TEXT)
                widget.pack(fill=X, pady=(0, Spacing.SM), ipady=6)
                self.widgets[key] = var

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        if len(self.fields) > 6:
            scrollbar.pack(side=RIGHT, fill=Y)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Button bar
        btn_frame = Frame(self.win, bg=Colors.CARD_BORDER, padx=Spacing.XL, pady=Spacing.MD)
        btn_frame.pack(fill=X, side=BOTTOM)

        Button(btn_frame, text="💾  Save", command=self._handle_save,
               bg=Colors.SUCCESS, fg="white", font=Fonts.BUTTON_SM, relief=FLAT,
               bd=0, padx=20, pady=8, cursor="hand2").pack(side=LEFT, padx=4)
        Button(btn_frame, text="Cancel", command=self.win.destroy,
               bg="#64748B", fg="white", font=Fonts.BUTTON_SM, relief=FLAT,
               bd=0, padx=20, pady=8, cursor="hand2").pack(side=LEFT, padx=4)

    def _handle_save(self):
        """Collect values and validate, then call on_save."""
        values = {}
        for field in self.fields:
            key = field["key"]
            widget = self.widgets[key]

            if isinstance(widget, Text):
                values[key] = widget.get("1.0", END).strip()
            elif isinstance(widget, StringVar):
                values[key] = widget.get().strip()
            else:
                values[key] = str(widget).strip()

            # Required check
            if field.get("required", True) and not values[key]:
                messagebox.showerror("Validation Error",
                                     f"'{field['label']}' is required.",
                                     parent=self.win)
                return

            # Custom validation
            validate = field.get("validate")
            if validate and values[key]:
                if not validate(values[key]):
                    messagebox.showerror("Validation Error",
                                         f"'{field['label']}' has an invalid value.",
                                         parent=self.win)
                    return

        try:
            self.on_save(values)
            self.win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.win)

    def get_values(self):
        """Get current form values as a dict."""
        values = {}
        for field in self.fields:
            key = field["key"]
            widget = self.widgets[key]
            if isinstance(widget, Text):
                values[key] = widget.get("1.0", END).strip()
            elif isinstance(widget, StringVar):
                values[key] = widget.get().strip()
        return values


# ═══════════════════════════════════════════════
# STAT CARD (for dashboard)
# ═══════════════════════════════════════════════

class StatCard:
    """A dashboard statistic card widget."""

    def __init__(self, parent, title, value, icon, color, row=0, col=0):
        self.frame = Frame(parent, bg=Colors.CARD_BG, relief=FLAT, bd=0,
                           highlightbackground=Colors.CARD_BORDER, highlightthickness=1)
        self.frame.grid(row=row, column=col, padx=Spacing.SM, pady=Spacing.SM, sticky="nsew")

        # Color accent bar
        accent = Frame(self.frame, bg=color, height=4)
        accent.pack(fill=X)

        content = Frame(self.frame, bg=Colors.CARD_BG, padx=Spacing.LG, pady=Spacing.MD)
        content.pack(fill=BOTH, expand=True)

        Label(content, text=icon, font=("Segoe UI", 24), bg=Colors.CARD_BG).pack(anchor=W)
        Label(content, text=str(value), font=Fonts.HEADING, bg=Colors.CARD_BG,
              fg=Colors.TEXT_DARK).pack(anchor=W, pady=(4, 0))
        Label(content, text=title, font=Fonts.SMALL, bg=Colors.CARD_BG,
              fg=Colors.TEXT_MUTED).pack(anchor=W)


# ═══════════════════════════════════════════════
# SECTION FRAME (for dashboard)
# ═══════════════════════════════════════════════

class SectionFrame:
    """A collapsible section card for the dashboard."""

    def __init__(self, parent, title, icon, color):
        self.outer = Frame(parent, bg=Colors.CARD_BG, relief=FLAT, bd=0,
                           highlightbackground=Colors.CARD_BORDER, highlightthickness=1)
        self.outer.pack(fill=X, padx=Spacing.XL, pady=Spacing.SM)

        # Section header
        header = Frame(self.outer, bg=color, height=48)
        header.pack(fill=X)
        header.pack_propagate(False)
        Label(header, text=f"{icon}  {title}", font=Fonts.SECTION,
              bg=color, fg="white").pack(anchor=W, padx=Spacing.LG, pady=Spacing.MD)

        # Content area
        self.content = Frame(self.outer, bg=Colors.CARD_BG, padx=Spacing.LG, pady=Spacing.MD)
        self.content.pack(fill=X)

    def add_button_grid(self, buttons, columns=3):
        """
        Add a grid of buttons to the section.

        Args:
            buttons: List of (text, command, color) tuples
            columns: Number of columns in the grid
        """
        for idx, (text, cmd, color) in enumerate(buttons):
            row = idx // columns
            col = idx % columns
            btn = Button(self.content, text=text, command=cmd, bg=color, fg="white",
                         font=Fonts.BUTTON_SM, relief=FLAT, bd=0, padx=12, pady=10,
                         cursor="hand2", activebackground=color, activeforeground="white")
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew", ipady=6)

        for c in range(columns):
            self.content.grid_columnconfigure(c, weight=1)
