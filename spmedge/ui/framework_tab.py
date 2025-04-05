"""
Framework tab for SPM Edge UI - Manage SPM frameworks
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class FrameworkTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Framework")
        
        # Create layout
        self.create_header()
        self.create_toolbar()
        self.create_main_content()
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="SPM Framework Manager", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Manage and edit Sales Performance Management frameworks"
        ).pack(anchor=tk.W)
    
    def create_toolbar(self):
        """Create toolbar with framework actions"""
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=20, pady=5)
        
        # Framework selection
        ttk.Label(toolbar, text="Framework:").pack(side=tk.LEFT, padx=(0, 5))
        self.framework_combo = ttk.Combobox(
            toolbar, 
            width=25,
            values=["SPM Framework", "Client Framework", "Industry Framework"]
        )
        self.framework_combo.set("SPM Framework")
        self.framework_combo.pack(side=tk.LEFT, padx=5)
        
        # Version selection
        ttk.Label(toolbar, text="Version:").pack(side=tk.LEFT, padx=(15, 5))
        self.version_combo = ttk.Combobox(
            toolbar, 
            width=10,
            values=["v1.0", "v1.1", "v2.0"]
        )
        self.version_combo.set("v1.0")
        self.version_combo.pack(side=tk.LEFT, padx=5)
        
        # Actions
        ttk.Button(
            toolbar,
            text="Import",
            command=self.import_framework
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            toolbar,
            text="Export",
            command=self.export_framework
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            toolbar,
            text="New Version",
            command=self.new_version
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_main_content(self):
        """Create main content area with framework editor"""
        # Create paned window for framework components and editor
        paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Framework tree
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=30)
        
        # Framework tree label
        ttk.Label(left_panel, text="Framework Components", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Create treeview for framework components
        tree_frame = ttk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        self.framework_tree = ttk.Treeview(tree_frame, selectmode="browse")
        
        # Configure columns
        self.framework_tree["columns"] = ("type",)
        self.framework_tree.column("#0", width=250, minwidth=150)
        self.framework_tree.column("type", width=100, minwidth=50)
        
        # Configure headings
        self.framework_tree.heading("#0", text="Component", anchor=tk.W)
        self.framework_tree.heading("type", text="Type", anchor=tk.W)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.framework_tree.yview)
        self.framework_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.framework_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.framework_tree.bind("<<TreeviewSelect>>", self.on_component_select)
        
        # Component tree buttons
        tree_buttons = ttk.Frame(left_panel)
        tree_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            tree_buttons,
            text="Add",
            command=self.add_component
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            tree_buttons,
            text="Delete",
            command=self.delete_component,
            style="Danger.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        # Right panel - Component editor
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=70)
        
        # Component editor label
        self.editor_title = tk.StringVar(value="Component Editor")
        ttk.Label(right_panel, textvariable=self.editor_title, font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Create notebook for component editor tabs
        editor_notebook = ttk.Notebook(right_panel)
        editor_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Basic tab
        basic_frame = ttk.Frame(editor_notebook)
        editor_notebook.add(basic_frame, text="Basic")
        
        # Create form fields
        basic_form = ttk.Frame(basic_frame, padding=10)
        basic_form.pack(fill=tk.BOTH, expand=True)
        
        # Basic form fields
        fields = [
            ("Process:", "process"),
            ("Category:", "category"),
            ("Component:", "component"),
            ("Keyword:", "keyword"),
            ("Framework Type:", "framework_type")
        ]
        
        self.component_fields = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(basic_form, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            var = tk.StringVar()
            entry = ttk.Entry(basic_form, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
            
            self.component_fields[field_name] = var
        
        # Definition field (multiline)
        ttk.Label(basic_form, text="Definition:").grid(row=len(fields), column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        
        definition_frame = ttk.Frame(basic_form, borderwidth=1, relief=tk.SUNKEN)
        definition_frame.grid(row=len(fields), column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        self.definition_text = tk.Text(definition_frame, height=8, width=40, wrap=tk.WORD)
        self.definition_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Make definition row expandable
        basic_form.rowconfigure(len(fields), weight=1)
        basic_form.columnconfigure(1, weight=1)
        
        # Advanced tab
        advanced_frame = ttk.Frame(editor_notebook)
        editor_notebook.add(advanced_frame, text="Advanced")
        
        # Create advanced form
        advanced_form = ttk.Frame(advanced_frame, padding=10)
        advanced_form.pack(fill=tk.BOTH, expand=True)
        
        # Advanced form fields
        advanced_fields = [
            ("User Type:", "user_type"),
            ("Complexity Level:", "complexity_level"),
            ("Traceability Code:", "traceability_code")
        ]
        
        for i, (label_text, field_name) in enumerate(advanced_fields):
            ttk.Label(advanced_form, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            var = tk.StringVar()
            entry = ttk.Entry(advanced_form, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
            
            self.component_fields[field_name] = var
        
        # Prompt field (multiline)
        ttk.Label(advanced_form, text="Prompt:").grid(row=len(advanced_fields), column=0, sticky=tk.W+tk.N, padx=5, pady=5)
        
        prompt_frame = ttk.Frame(advanced_form, borderwidth=1, relief=tk.SUNKEN)
        prompt_frame.grid(row=len(advanced_fields), column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        self.prompt_text = tk.Text(prompt_frame, height=8, width=40, wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Make prompt row expandable
        advanced_form.rowconfigure(len(advanced_fields), weight=1)
        advanced_form.columnconfigure(1, weight=1)
        
        # Save button
        save_button = ttk.Button(
            right_panel,
            text="Save Changes",
            command=self.save_component,
            style="Success.TButton"
        )
        save_button.pack(anchor=tk.E, pady=10)
        
        # Load initial framework data
        self.load_dummy_framework_data()
    
    def load_dummy_framework_data(self):
        """Load dummy framework data for demonstration"""
        # Clear existing tree items
        for item in self.framework_tree.get_children():
            self.framework_tree.delete(item)
        
        # Add processes (level 1)
        processes = {
            "incentive_comp": "Incentive Compensation Management",
            "sales_planning": "Sales Planning",
            "territory_mgmt": "Territory Management",
            "quota_mgmt": "Quota Management"
        }
        
        for proc_id, proc_name in processes.items():
            process = self.framework_tree.insert("", tk.END, text=proc_name, values=("Process",), iid=proc_id)
            
            # Add categories for Incentive Compensation only (level 2)
            if proc_id == "incentive_comp":
                categories = {
                    "ic_payouts": "Payouts",
                    "ic_calcs": "Calculations",
                    "ic_rules": "Rules",
                    "ic_provisions": "Provisions"
                }
                
                for cat_id, cat_name in categories.items():
                    category = self.framework_tree.insert(proc_id, tk.END, text=cat_name, values=("Category",), iid=cat_id)
                    
                    # Add components for Payouts only (level 3)
                    if cat_id == "ic_payouts":
                        components = [
                            ("ic_payout_freq", "Payment Frequency", "Component"),
                            ("ic_payout_calc", "Payment Calculation", "Component"),
                            ("ic_payout_rule", "Payment Rules", "Component")
                        ]
                        
                        for comp_id, comp_name, comp_type in components:
                            self.framework_tree.insert(cat_id, tk.END, text=comp_name, values=(comp_type,), iid=comp_id)
    
    def on_component_select(self, event):
        """Handle component selection in the framework tree"""
        selected_items = self.framework_tree.selection()
        if not selected_items:
            return
        
        # Get selected item
        item_id = selected_items[0]
        item_text = self.framework_tree.item(item_id, "text")
        item_type = self.framework_tree.item(item_id, "values")[0]
        
        # Update editor title
        self.editor_title.set(f"{item_type} Editor: {item_text}")
        
        # Clear current fields
        for field_var in self.component_fields.values():
            field_var.set("")
        
        self.definition_text.delete("1.0", tk.END)
        self.prompt_text.delete("1.0", tk.END)
        
        # Set dummy data based on type
        if item_type == "Process":
            self.component_fields["process"].set(item_text)
            self.component_fields["framework_type"].set("SPM")
            self.definition_text.insert("1.0", f"The {item_text} process encompasses all activities related to managing and administering {item_text.lower()}.")
        
        elif item_type == "Category":
            parent_id = self.framework_tree.parent(item_id)
            parent_text = self.framework_tree.item(parent_id, "text")
            
            self.component_fields["process"].set(parent_text)
            self.component_fields["category"].set(item_text)
            self.component_fields["framework_type"].set("SPM")
            self.definition_text.insert("1.0", f"The {item_text} category represents a subset of {parent_text} focused on specific {item_text.lower()} activities.")
        
        elif item_type == "Component":
            parent_id = self.framework_tree.parent(item_id)
            parent_text = self.framework_tree.item(parent_id, "text")
            grand_parent_id = self.framework_tree.parent(parent_id)
            grand_parent_text = self.framework_tree.item(grand_parent_id, "text")
            
            self.component_fields["process"].set(grand_parent_text)
            self.component_fields["category"].set(parent_text)
            self.component_fields["component"].set(item_text)
            self.component_fields["keyword"].set(item_text.lower().replace(" ", "_"))
            self.component_fields["framework_type"].set("SPM")
            self.component_fields["complexity_level"].set("Medium")
            self.component_fields["user_type"].set("Sales Compensation Manager")
            
            self.definition_text.insert("1.0", f"The {item_text} component provides functionality for managing {item_text.lower()} within the {parent_text} category of {grand_parent_text}.")
            
            self.prompt_text.insert("1.0", f"Extract information about {item_text.lower()} from the document, including frequency, calculation methods, and specific rules.")
    
    def add_component(self):
        """Add a new component to the framework"""
        # Get the current selection
        selected_items = self.framework_tree.selection()
        
        # Create a popup for new component
        popup = tk.Toplevel(self.app.root)
        popup.title("Add Component")
        popup.geometry("400x300")
        popup.transient(self.app.root)
        popup.grab_set()
        
        # Create form
        form_frame = ttk.Frame(popup, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Add Framework Component", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        # Component name
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=30).grid(
            row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5
        )
        
        # Component type
        ttk.Label(form_frame, text="Type:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        type_var = tk.StringVar(value="Component")
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, width=30)
        type_combo["values"] = ["Process", "Category", "Component", "Keyword"]
        type_combo.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Parent component
        ttk.Label(form_frame, text="Parent:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        
        parent_var = tk.StringVar()
        if selected_items:
            parent_item = selected_items[0]
            parent_text = self.framework_tree.item(parent_item, "text")
            parent_var.set(parent_text)
        
        ttk.Entry(form_frame, textvariable=parent_var, width=30, state="readonly").grid(
            row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5
        )
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Add Component",
            command=lambda: self.create_component(name_var.get(), type_var.get(), popup),
            style="Success.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def create_component(self, name, comp_type, popup):
        """Create a new component in the framework tree"""
        if not name:
            messagebox.showerror("Error", "Component name is required")
            return
        
        # Get selected parent
        selected_items = self.framework_tree.selection()
        parent_id = "" if not selected_items else selected_items[0]
        
        # Generate a unique ID
        import random
        import string
        comp_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        # Insert the new component
        self.framework_tree.insert(parent_id, tk.END, text=name, values=(comp_type,), iid=comp_id)
        
        # Select the new component
        self.framework_tree.selection_set(comp_id)
        
        # Expand parent if needed
        if parent_id:
            self.framework_tree.item(parent_id, open=True)
        
        # Close popup
        popup.destroy()
        
        # Show success message
        messagebox.showinfo("Success", f"{comp_type} '{name}' created successfully")
    
    def delete_component(self):
        """Delete the selected component"""
        selected_items = self.framework_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a component to delete")
            return
        
        # Get selected item
        item_id = selected_items[0]
        item_text = self.framework_tree.item(item_id, "text")
        item_type = self.framework_tree.item(item_id, "values")[0]
        
        # Check if it has children
        children = self.framework_tree.get_children(item_id)
        
        if children and not messagebox.askyesno(
            "Confirm Delete", 
            f"This {item_type} has {len(children)} child components that will also be deleted.\nAre you sure you want to delete '{item_text}' and all its children?"
        ):
            return
        elif not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the {item_type} '{item_text}'?"):
            return
        
        # Delete the item
        self.framework_tree.delete(item_id)
        
        # Update editor title
        self.editor_title.set("Component Editor")
        
        # Clear fields
        for field_var in self.component_fields.values():
            field_var.set("")
        
        self.definition_text.delete("1.0", tk.END)
        self.prompt_text.delete("1.0", tk.END)
        
        # Show success message
        messagebox.showinfo("Success", f"{item_type} '{item_text}' deleted successfully")
    
    def save_component(self):
        """Save the component changes"""
        selected_items = self.framework_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a component to save")
            return
        
        # Get selected item
        item_id = selected_items[0]
        item_type = self.framework_tree.item(item_id, "values")[0]
        
        # Get the new component name based on type
        if item_type == "Process":
            new_name = self.component_fields["process"].get()
        elif item_type == "Category":
            new_name = self.component_fields["category"].get()
        elif item_type == "Component":
            new_name = self.component_fields["component"].get()
        else:
            new_name = self.component_fields["keyword"].get()
        
        if not new_name:
            messagebox.showerror("Error", f"{item_type} name is required")
            return
        
        # Update the item text
        self.framework_tree.item(item_id, text=new_name)
        
        # Show success message
        messagebox.showinfo("Success", f"{item_type} '{new_name}' saved successfully")
    
    def import_framework(self):
        """Import framework from file"""
        file_path = filedialog.askopenfilename(
            title="Import Framework",
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Show message
        messagebox.showinfo("Import", f"Framework will be imported from: {file_path}")
    
    def export_framework(self):
        """Export framework to file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Framework",
            defaultextension=".json",
            filetypes=[
                ("JSON Files", "*.json"),
                ("Excel Files", "*.xlsx"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Show message
        messagebox.showinfo("Export", f"Framework will be exported to: {file_path}")
    
    def new_version(self):
        """Create a new framework version"""
        # Create a popup for new version
        popup = tk.Toplevel(self.app.root)
        popup.title("New Framework Version")
        popup.geometry("400x200")
        popup.transient(self.app.root)
        popup.grab_set()
        
        # Create form
        form_frame = ttk.Frame(popup, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Create New Framework Version", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        # Current version
        ttk.Label(form_frame, text="Current Version:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        current_var = tk.StringVar(value=self.version_combo.get())
        ttk.Entry(form_frame, textvariable=current_var, width=20, state="readonly").grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5
        )
        
        # New version
        ttk.Label(form_frame, text="New Version:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        new_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=new_var, width=20).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=5
        )
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Create Version",
            command=lambda: self.create_version(new_var.get(), popup),
            style="Success.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def create_version(self, new_version, popup):
            """Create a new framework version"""
            if not new_version:
                messagebox.showerror("Error", "New version is required")
                return
            
            # Add the new version to combobox
            current_values = list(self.version_combo['values'])
            if new_version in current_values:
                messagebox.showerror("Error", f"Version {new_version} already exists")
                return
                
            current_values.append(new_version)
            self.version_combo['values'] = current_values
            self.version_combo.set(new_version)
            
            # Close popup
            popup.destroy()
            
            # Show success message
            messagebox.showinfo("Success", f"Framework version {new_version} created successfully")
    
def create_framework_tab(notebook, app):
    """Create the framework tab"""
    framework_tab = FrameworkTab(notebook, app)
    app.framework_tab = framework_tab
    return framework_tab.frame