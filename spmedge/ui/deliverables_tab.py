"""
Deliverables tab for SPM Edge UI - Generate project deliverables
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class DeliverablesTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Deliverables")
        
        # Create components
        self.create_header()
        self.create_project_selector()
        self.create_deliverables_grid()
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="Generate Project Deliverables", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Create reports and analysis from processed documents"
        ).pack(anchor=tk.W)
    
    def create_project_selector(self):
        """Create project selection panel"""
        selection_frame = ttk.Frame(self.frame)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(selection_frame, text="Project:").pack(side=tk.LEFT, padx=5)
        self.project_combo = ttk.Combobox(selection_frame, width=30)
        self.project_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            selection_frame,
            text="Load Project Data",
            command=self.load_project_data
        ).pack(side=tk.LEFT, padx=5)
    
    def create_deliverables_grid(self):
        """Create grid of deliverable options"""
        # Deliverables list (card-based UI)
        deliverables_content = ttk.Frame(self.frame)
        deliverables_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Available deliverables
        deliverables = [
            {
                "title": "Executive Summary",
                "description": "High-level overview of all compensation components",
                "icon": "📊",
                "action": self.generate_executive_summary
            },
            {
                "title": "Detailed Analysis",
                "description": "In-depth analysis of compensation plan components",
                "icon": "📈",
                "action": self.generate_detailed_analysis
            },
            {
                "title": "Component Matrix",
                "description": "Matrix view of all compensation components",
                "icon": "🔢",
                "action": self.generate_component_matrix
            },
            {
                "title": "Excel Export",
                "description": "Export all components to Excel spreadsheet",
                "icon": "📑",
                "action": self.export_to_excel
            },
            {
                "title": "Client Presentation",
                "description": "Create PowerPoint presentation for client review",
                "icon": "🎯",
                "action": self.generate_presentation
            },
            {
                "title": "Custom Report",
                "description": "Generate a custom report with selected components",
                "icon": "📝",
                "action": self.generate_custom_report
            }
        ]
        
        # Create a grid layout for deliverable cards
        row_size = 3  # Number of cards per row
        for i, deliverable in enumerate(deliverables):
            row = i // row_size
            col = i % row_size
            
            self.create_deliverable_card(
                deliverables_content,
                deliverable["title"],
                deliverable["description"],
                deliverable["icon"],
                deliverable["action"],
                row, col
            )
            
        # Configure grid
        for i in range(2):  # 2 rows
            deliverables_content.rowconfigure(i, weight=1)
        for i in range(row_size):  # 3 columns
            deliverables_content.columnconfigure(i, weight=1)
    
    def create_deliverable_card(self, parent, title, description, icon, action, row, col):
        """Create a card for a deliverable option"""
        card = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Card header with icon and title
        header = ttk.Frame(card)
        header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Icon (using a label with emoji)
        ttk.Label(
            header,
            text=icon,
            font=("Arial", 24)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Title
        ttk.Label(
            header,
            text=title,
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        # Description
        ttk.Label(
            card,
            text=description,
            wraplength=200
        ).pack(fill=tk.X, padx=10, pady=5)
        
        # Generate button
        ttk.Button(
            card,
            text="Generate",
            command=action
        ).pack(pady=10, padx=10, fill=tk.X)
    
    def load_project_data(self):
        """Load project data for deliverables"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
            
        messagebox.showinfo("Load Project", f"Loading data for project: {project}")
    
    def generate_executive_summary(self):
        """Generate an executive summary report"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            initialfile=f"{project}_Executive_Summary.pdf"
        )
        
        if not file_path:
            return
            
        messagebox.showinfo("Generate Report", f"Generating Executive Summary for project: {project}")
        
        # In a real implementation, you would generate the report here
        # For simulation, we'll just show a message
        self.app.root.after(2000, lambda: messagebox.showinfo(
            "Report Generated", 
            f"Executive Summary generated successfully and saved to:\n{file_path}"
        ))
    

    def generate_detailed_analysis(self):
        """Generate a detailed analysis report"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            initialfile=f"{project}_Detailed_Analysis.pdf"
        )
        
        if not file_path:
            return
            
        messagebox.showinfo("Generate Report", f"Generating Detailed Analysis for project: {project}")
        
        # In a real implementation, you would generate the report here
        # For simulation, we'll just show a message
        self.app.root.after(2000, lambda: messagebox.showinfo(
            "Report Generated", 
            f"Detailed Analysis generated successfully and saved to:\n{file_path}"
        ))
    
    def generate_component_matrix(self):
        """Generate a component matrix"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            initialfile=f"{project}_Component_Matrix.xlsx"
        )
        
        if not file_path:
            return
            
        messagebox.showinfo("Generate Matrix", f"Generating Component Matrix for project: {project}")
        
        # Simulation of processing time
        self.app.root.after(2000, lambda: messagebox.showinfo(
            "Matrix Generated", 
            f"Component Matrix generated successfully and saved to:\n{file_path}"
        ))
    
    def export_to_excel(self):
        """Export components to Excel"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            initialfile=f"{project}_Components_Export.xlsx"
        )
        
        if not file_path:
            return
            
        messagebox.showinfo("Export", f"Exporting components for project: {project}")
        
        # Simulation of processing time
        self.app.root.after(1500, lambda: messagebox.showinfo(
            "Export Complete", 
            f"Components exported successfully to:\n{file_path}"
        ))
    
    def generate_presentation(self):
        """Generate client presentation"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Ask for output location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pptx",
            filetypes=[("PowerPoint Files", "*.pptx"), ("All Files", "*.*")],
            initialfile=f"{project}_Presentation.pptx"
        )
        
        if not file_path:
            return
            
        messagebox.showinfo("Generate Presentation", f"Creating presentation for project: {project}")
        
        # Simulation of processing time
        self.app.root.after(3000, lambda: messagebox.showinfo(
            "Presentation Created", 
            f"Client presentation created successfully and saved to:\n{file_path}"
        ))
    
    def generate_custom_report(self):
        """Generate custom report with selected components"""
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project")
            return
        
        # Create a dialog to select components
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Select Components")
        dialog.geometry("400x500")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Components selection
        ttk.Label(dialog, text="Select components to include:", font=("Arial", 11, "bold")).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        # Sample components - in a real app, these would come from your data model
        components = [
            "Revenue Components", 
            "Bonus Structures", 
            "Quota Models", 
            "Calculation Rules",
            "Performance Metrics",
            "Special Provisions",
            "Clawback Terms",
            "Payment Schedules",
            "Eligibility Rules",
            "Territory Assignments"
        ]
        
        # Create checkboxes for components
        component_vars = []
        for component in components:
            var = tk.BooleanVar(value=False)
            component_vars.append(var)
            ttk.Checkbutton(dialog, text=component, variable=var).pack(pady=2, padx=30, anchor=tk.W)
        
        # Output format selection
        ttk.Label(dialog, text="Output format:", font=("Arial", 11, "bold")).pack(pady=(15, 5), padx=20, anchor=tk.W)
        format_var = tk.StringVar(value="pdf")
        ttk.Radiobutton(dialog, text="PDF Document", variable=format_var, value="pdf").pack(pady=2, padx=30, anchor=tk.W)
        ttk.Radiobutton(dialog, text="Word Document", variable=format_var, value="docx").pack(pady=2, padx=30, anchor=tk.W)
        ttk.Radiobutton(dialog, text="Excel Spreadsheet", variable=format_var, value="xlsx").pack(pady=2, padx=30, anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20, fill=tk.X)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(
            button_frame, 
            text="Generate Report", 
            command=lambda: self._process_custom_report(dialog, project, component_vars, components, format_var.get())
        ).pack(side=tk.RIGHT, padx=10)
    
    def _process_custom_report(self, dialog, project, component_vars, components, format_type):
        """Process the custom report selection"""
        # Get selected components
        selected_components = [components[i] for i, var in enumerate(component_vars) if var.get()]
        
        if not selected_components:
            messagebox.showinfo("Info", "Please select at least one component")
            return
        
        # Close the dialog
        dialog.destroy()
        
        # Ask for output location
        extensions = {
            "pdf": ".pdf",
            "docx": ".docx",
            "xlsx": ".xlsx"
        }
        
        file_types = {
            "pdf": [("PDF Files", "*.pdf")],
            "docx": [("Word Files", "*.docx")],
            "xlsx": [("Excel Files", "*.xlsx")]
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=extensions[format_type],
            filetypes=file_types[format_type] + [("All Files", "*.*")],
            initialfile=f"{project}_Custom_Report{extensions[format_type]}"
        )
        
        if not file_path:
            return
            
        # Start generating the report
        components_str = ", ".join(selected_components)
        messagebox.showinfo(
            "Generate Custom Report", 
            f"Generating custom report for project: {project}\n\nComponents: {components_str}\n\nFormat: {format_type.upper()}"
        )
        
        # Simulation of processing time
        self.app.root.after(2500, lambda: messagebox.showinfo(
            "Report Generated", 
            f"Custom report generated successfully and saved to:\n{file_path}"
        ))