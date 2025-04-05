"""
Projects tab for SPM Edge UI - Create and manage projects
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import uuid
from datetime import datetime

class ProjectsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Projects")
        
        # Get database connection from app
        self.db_manager = app.db_manager
        
        # Basic project fields
        self.project_id_var = tk.StringVar()
        self.project_name_var = tk.StringVar()
        self.project_code_var = tk.StringVar()
        self.client_id_var = tk.IntVar()
        self.client_display_var = tk.StringVar()
        self.project_type_var = tk.StringVar()
        self.domain_var = tk.StringVar(value="SPM")
        self.description_var = tk.StringVar()
        self.status_var = tk.StringVar(value="active")
        
        # New RFP and industry fields
        self.rfp_number_var = tk.StringVar()
        self.business_unit_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.budget_var = tk.StringVar()
        self.estimated_hours_var = tk.StringVar()
        self.project_manager_var = tk.StringVar()
        self.technical_lead_var = tk.StringVar()
        self.source_var = tk.StringVar()
        
        # Date fields
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.kickoff_date_var = tk.StringVar()
        self.go_live_date_var = tk.StringVar()
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the UI components"""
        # Split view - Project list on left, details on right
        paned_window = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Project list
        left_panel = ttk.Frame(paned_window)
        paned_window.add(left_panel, weight=1)
        
        # Create project list with scrollbar
        list_frame = ttk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header and controls
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame, 
            text="Projects", 
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        # New project button
        ttk.Button(
            header_frame,
            text="+ New Project",
            command=self.new_project
        ).pack(side=tk.RIGHT)
        
        # Filter/search
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=20)
        filter_entry.pack(side=tk.LEFT, padx=5)
        filter_entry.bind("<KeyRelease>", self.filter_projects)
        
        status_frame = ttk.Frame(filter_frame)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(
            status_frame, 
            text="All", 
            variable=self.status_filter_var, 
            value="all",
            command=self.filter_projects
        ).pack(side=tk.LEFT)
        
        ttk.Radiobutton(
            status_frame, 
            text="Active", 
            variable=self.status_filter_var, 
            value="active",
            command=self.filter_projects
        ).pack(side=tk.LEFT)
        
        ttk.Radiobutton(
            status_frame, 
            text="Completed", 
            variable=self.status_filter_var, 
            value="completed",
            command=self.filter_projects
        ).pack(side=tk.LEFT)
        
        # Project list with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("name", "code", "type", "client", "status")
        self.project_tree = ttk.Treeview(
            list_container, 
            columns=columns,
            show="headings",
            selectmode="browse",
            height=20,
            yscrollcommand=scrollbar.set
        )
        
        # Define headings
        self.project_tree.heading("name", text="Name")
        self.project_tree.heading("code", text="Code")
        self.project_tree.heading("type", text="Type")
        self.project_tree.heading("client", text="Client")
        self.project_tree.heading("status", text="Status")
        
        # Define columns
        self.project_tree.column("name", width=200)
        self.project_tree.column("code", width=80)
        self.project_tree.column("type", width=100)
        self.project_tree.column("client", width=150)
        self.project_tree.column("status", width=80)
        
        self.project_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.project_tree.yview)
        
        # Bind selection event
        self.project_tree.bind("<<TreeviewSelect>>", self.on_project_select)
        
        # Right panel - Project details with notebook for tabs
        right_panel = ttk.Frame(paned_window)
        paned_window.add(right_panel, weight=2)
        
        # Project details notebook
        self.details_notebook = ttk.Notebook(right_panel)
        self.details_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Basic Info Tab
        basic_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(basic_frame, text="Basic Info")
        
        # Create a form with labels and fields
        form_frame = ttk.Frame(basic_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Project ID (hidden)
        self.project_id_label = ttk.Label(form_frame, text="ID:", foreground="gray")
        self.project_id_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            form_frame, 
            textvariable=self.project_id_var, 
            state="readonly",
            width=36
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Project Name
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            form_frame, 
            textvariable=self.project_name_var, 
            width=40
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Project Code
        ttk.Label(form_frame, text="Code:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            form_frame, 
            textvariable=self.project_code_var, 
            width=20
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Client
        ttk.Label(form_frame, text="Client:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        client_frame = ttk.Frame(form_frame)
        client_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.client_combo = ttk.Combobox(client_frame, textvariable=self.client_display_var, width=30)
        self.client_combo.pack(side=tk.LEFT)
        self.client_combo.bind("<<ComboboxSelected>>", self.on_client_selected)
        
        ttk.Button(
            client_frame,
            text="Details",
            command=self.show_client_details,
            width=8
        ).pack(side=tk.LEFT, padx=5)
        
        # Project Type
        ttk.Label(form_frame, text="Project Type:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.type_combo = ttk.Combobox(form_frame, textvariable=self.project_type_var, width=30)
        self.type_combo["values"] = ["Implementation", "Configuration", "Migration", "Upgrade", "Consulting", "Support"]
        self.type_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Domain
        ttk.Label(form_frame, text="Domain:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.domain_combo = ttk.Combobox(form_frame, textvariable=self.domain_var, width=20)
        self.domain_combo["values"] = ["SPM", "CPQ", "CLM", "ICM", "TPM", "CRM", "Other"]
        self.domain_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # RFP Number
        ttk.Label(form_frame, text="RFP Number:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            form_frame, 
            textvariable=self.rfp_number_var, 
            width=20
        ).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Business Unit
        ttk.Label(form_frame, text="Business Unit:").grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            form_frame, 
            textvariable=self.business_unit_var, 
            width=30
        ).grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=8, column=0, sticky=tk.W, pady=5)
        
        self.priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var, width=15)
        self.priority_combo["values"] = ["High", "Medium", "Low"]
        self.priority_combo.grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Status
        ttk.Label(form_frame, text="Status:").grid(row=9, column=0, sticky=tk.W, pady=5)
        
        status_frame = ttk.Frame(form_frame)
        status_frame.grid(row=9, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            status_frame, 
            text="Active", 
            variable=self.status_var, 
            value="active"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            status_frame, 
            text="Completed", 
            variable=self.status_var, 
            value="completed"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            status_frame, 
            text="On Hold", 
            variable=self.status_var, 
            value="on_hold"
        ).pack(side=tk.LEFT)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=10, column=0, sticky=tk.NW, pady=5)
        
        self.description_text = tk.Text(form_frame, height=4, width=40, wrap=tk.WORD)
        self.description_text.grid(row=10, column=1, sticky=tk.W, pady=5)
        
        # Details Tab
        details_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(details_frame, text="Project Details")
        
        details_form = ttk.Frame(details_frame)
        details_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Budget
        ttk.Label(details_form, text="Budget:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            details_form, 
            textvariable=self.budget_var, 
            width=15
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Estimated Hours
        ttk.Label(details_form, text="Estimated Hours:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            details_form, 
            textvariable=self.estimated_hours_var, 
            width=10
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Project Manager
        ttk.Label(details_form, text="Project Manager:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            details_form, 
            textvariable=self.project_manager_var, 
            width=30
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Technical Lead
        ttk.Label(details_form, text="Technical Lead:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            details_form, 
            textvariable=self.technical_lead_var, 
            width=30
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Source
        ttk.Label(details_form, text="Source:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            details_form, 
            textvariable=self.source_var, 
            width=30
        ).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Dates Tab
        dates_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(dates_frame, text="Dates")
        
        dates_form = ttk.Frame(dates_frame)
        dates_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Start Date
        ttk.Label(dates_form, text="Start Date:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            dates_form, 
            textvariable=self.start_date_var, 
            width=15
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # End Date
        ttk.Label(dates_form, text="End Date:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            dates_form, 
            textvariable=self.end_date_var, 
            width=15
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Kickoff Date
        ttk.Label(dates_form, text="Kickoff Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            dates_form, 
            textvariable=self.kickoff_date_var, 
            width=15
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Go Live Date
        ttk.Label(dates_form, text="Go Live Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(
            dates_form, 
            textvariable=self.go_live_date_var, 
            width=15
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Success Criteria Tab
        success_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(success_frame, text="Success & Risks")
        
        success_form = ttk.Frame(success_frame)
        success_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Success Criteria
        ttk.Label(success_form, text="Success Criteria:").grid(row=0, column=0, sticky=tk.NW, pady=5)
        
        self.success_criteria_text = tk.Text(success_form, height=5, width=50, wrap=tk.WORD)
        self.success_criteria_text.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Risks
        ttk.Label(success_form, text="Risks:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        
        self.risks_text = tk.Text(success_form, height=5, width=50, wrap=tk.WORD)
        self.risks_text.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(right_panel)
        buttons_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Button(
            buttons_frame,
            text="Save",
            command=self.save_project
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Delete",
            command=self.delete_project
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Clear",
            command=self.clear_form
        ).pack(side=tk.RIGHT, padx=5)
    
    def on_client_selected(self, event):
        """Handle client selection from dropdown"""
        # This is a stub - will be implemented when database is connected
        messagebox.showinfo("Info", "Client selection will be available when database is connected")
    
    def show_client_details(self):
        """Show client details dialog"""
        # This is a stub - will be implemented when database is connected
        messagebox.showinfo("Info", "Client details will be available when database is connected")
    
    def load_projects(self):
        """Load projects from database"""
        # This is a stub - demo function until database is connected
        try:
            # Clear existing items
            for item in self.project_tree.get_children():
                self.project_tree.delete(item)
            
            # Add some demo data
            demo_projects = [
                ("p1", "SPM Implementation", "SPM01", "Implementation", "Acme Corp", "active"),
                ("p2", "Sales Comp Migration", "SPM02", "Migration", "Global Inc", "completed"),
                ("p3", "ICM Configuration", "ICM01", "Configuration", "Tech Solutions", "on_hold")
            ]
            
            # Insert projects into tree
            for project in demo_projects:
                self.project_tree.insert("", tk.END, iid=project[0], values=(
                    project[1],  # name
                    project[2],  # code
                    project[3],  # project_type
                    project[4],  # client_name
                    project[5]   # status
                ), tags=(project[5],))
            
            # Apply conditional formatting
            self.project_tree.tag_configure("completed", foreground="gray")
            self.project_tree.tag_configure("on_hold", foreground="orange")
            
            # Update status bar
            self.app.update_status("Loaded demo projects", "Projects: 3", "Demo Mode")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {e}")
    
    def new_project(self):
        """Create a new project"""
        self.clear_form()
        # Generate a new UUID
        self.project_id_var.set(str(uuid.uuid4()))
        # Set default values
        self.domain_var.set("SPM")
        self.status_var.set("active")
        # Set current date as start date
        self.start_date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def on_project_select(self, event):
        """Handle project selection in tree view"""
        selected_id = self.project_tree.selection()
        if not selected_id:
            return
            
        project_id = selected_id[0]
        values = self.project_tree.item(project_id, "values")
        
        # Fill in basic form fields with selected project values
        self.project_id_var.set(project_id)
        self.project_name_var.set(values[0])
        self.project_code_var.set(values[1])
        self.project_type_var.set(values[2])
        self.client_display_var.set(values[3])
        self.status_var.set(values[4])
        
        # For demo purposes, set some sample data for other fields
        self.domain_var.set("SPM" if "SPM" in values[0] else "ICM")
        self.rfp_number_var.set(f"RFP-{values[1]}")
        self.business_unit_var.set("Sales")
        self.priority_var.set("Medium")
        self.budget_var.set("$100,000")
        self.estimated_hours_var.set("500")
        self.project_manager_var.set("John Smith")
        self.technical_lead_var.set("Jane Doe")
        self.start_date_var.set("2024-01-01")
        self.end_date_var.set("2024-06-30")
        
        # Set text fields
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", f"This is a {values[2]} project for {values[3]}.")
        
        self.success_criteria_text.delete("1.0", tk.END)
        self.success_criteria_text.insert("1.0", "1. Successful deployment\n2. User adoption\n3. Performance targets met")
        
        self.risks_text.delete("1.0", tk.END)
        self.risks_text.insert("1.0", "1. Resource constraints\n2. Timeline challenges\n3. Data quality issues")
    
    def save_project(self):
        """Save project to database"""
        # Validate required fields
        project_name = self.project_name_var.get().strip()
        project_code = self.project_code_var.get().strip()
        project_type = self.project_type_var.get()
        
        if not project_name:
            messagebox.showwarning("Validation Error", "Project name is required")
            return
            
        if not project_code:
            messagebox.showwarning("Validation Error", "Project code is required")
            return
            
        if not project_type:
            messagebox.showwarning("Validation Error", "Project type is required")
            return
        
        # Get form values
        project_id = self.project_id_var.get()
        domain = self.domain_var.get()
        description = self.description_text.get("1.0", tk.END).strip()
        status = self.status_var.get()
        
        # In a real app, we would save to database here
        # For demo purposes, update the treeview
        try:
            # Update treeview with new values
            if project_id and project_id in self.project_tree.get_children():
                # Update existing project
                self.project_tree.item(project_id, values=(
                    project_name,
                    project_code,
                    project_type,
                    self.client_display_var.get(),
                    status
                ), tags=(status,))
                
                messagebox.showinfo("Success", "Project updated successfully!")
            else:
                # Add new project
                new_id = project_id if project_id else f"p{len(self.project_tree.get_children())+1}"
                self.project_tree.insert("", tk.END, iid=new_id, values=(
                    project_name,
                    project_code,
                    project_type,
                    self.client_display_var.get(),
                    status
                ), tags=(status,))
                
                # Set the project ID
                self.project_id_var.set(new_id)
                
                messagebox.showinfo("Success", "Project created successfully!")
            
            # Update status bar
            count = len(self.project_tree.get_children())
            self.app.update_status("Project saved", f"Projects: {count}", "Demo Mode")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {e}")
    
    def delete_project(self):
        """Delete the current project"""
        project_id = self.project_id_var.get()
        if not project_id or project_id not in self.project_tree.get_children():
            messagebox.showinfo("Info", "No project selected")
            return
            
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this project?"):
            return
            
        try:
            # In a real app, we would delete from database here
            # For demo purposes, just remove from treeview
            self.project_tree.delete(project_id)
            
            messagebox.showinfo("Success", "Project deleted successfully!")
            
            # Clear form 
            self.clear_form()
            
            # Update status bar
            count = len(self.project_tree.get_children())
            self.app.update_status("Project deleted", f"Projects: {count}", "Demo Mode")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete project: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.project_id_var.set("")
        self.project_name_var.set("")
        self.project_code_var.set("")
        self.client_display_var.set("")
        self.project_type_var.set("")
        self.domain_var.set("SPM")
        self.rfp_number_var.set("")
        self.business_unit_var.set("")
        self.priority_var.set("Medium")
        self.budget_var.set("")
        self.estimated_hours_var.set("")
        self.project_manager_var.set("")
        self.technical_lead_var.set("")
        self.source_var.set("")
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.kickoff_date_var.set("")
        self.go_live_date_var.set("")
        self.status_var.set("active")
        
        # Clear text widgets
        self.description_text.delete("1.0", tk.END)
        self.success_criteria_text.delete("1.0", tk.END)
        self.risks_text.delete("1.0", tk.END)
    
    def filter_projects(self, event=None):
        """Filter projects based on search text and status"""
        search_text = self.filter_var.get().lower()
        status_filter = self.status_filter_var.get()
        
        # For demo mode, we'll reload and filter the demo data
        try:
            # Clear existing items
            for item in self.project_tree.get_children():
                self.project_tree.delete(item)
            
            # Add demo data
            demo_projects = [
                ("p1", "SPM Implementation", "SPM01", "Implementation", "Acme Corp", "active"),
                ("p2", "Sales Comp Migration", "SPM02", "Migration", "Global Inc", "completed"),
                ("p3", "ICM Configuration", "ICM01", "Configuration", "Tech Solutions", "on_hold")
            ]
            
            # Filter and insert projects
            for project in demo_projects:
                # Check if project matches filter criteria
                status_match = (status_filter == "all") or (project[5] == status_filter)
                
                search_match = not search_text or any(
                    search_text in str(value).lower() 
                    for value in project[1:5]
                )
                
                if status_match and search_match:
                    self.project_tree.insert("", tk.END, iid=project[0], values=(
                        project[1],  # name
                        project[2],  # code
                        project[3],  # project_type
                        project[4],  # client_name
                        project[5]   # status
                    ), tags=(project[5],))
            
            # Apply conditional formatting
            self.project_tree.tag_configure("completed", foreground="gray")
            self.project_tree.tag_configure("on_hold", foreground="orange")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter projects: {e}")