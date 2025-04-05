"""
Documents tab for SPM Edge UI - Manage and view documents
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

class DocumentsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Documents")
        
        # Create components
        self.create_toolbar()
        self.create_documents_view()
        self.create_preview_panel()
        
        # Load initial data
        self.load_dummy_documents()
    
    def create_toolbar(self):
        """Create toolbar with document actions"""
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=20, pady=10)
        
        # Project selection
        ttk.Label(toolbar, text="Project:").pack(side=tk.LEFT, padx=(0, 5))
        self.project_combo = ttk.Combobox(toolbar, width=30)
        self.project_combo.pack(side=tk.LEFT, padx=5)
        
        # Document type filter
        ttk.Label(toolbar, text="Type:").pack(side=tk.LEFT, padx=(15, 5))
        self.type_combo = ttk.Combobox(
            toolbar, 
            width=15,
            values=["All", "PDF", "Word", "Excel", "Text", "JSON"]
        )
        self.type_combo.set("All")
        self.type_combo.pack(side=tk.LEFT, padx=5)
        
        # Status filter
        ttk.Label(toolbar, text="Status:").pack(side=tk.LEFT, padx=(15, 5))
        self.status_combo = ttk.Combobox(
            toolbar, 
            width=15,
            values=["All", "Pending", "Processing", "Completed", "Failed"]
        )
        self.status_combo.set("All")
        self.status_combo.pack(side=tk.LEFT, padx=5)
        
        # Search
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=(15, 5))
        self.search_var = tk.StringVar()
        ttk.Entry(toolbar, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # Actions
        ttk.Button(
            toolbar,
            text="Upload",
            command=self.upload_documents
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_documents
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_documents_view(self):
        """Create documents list view"""
        # Create paned window for document list and preview
        self.doc_paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.doc_paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Document list panel
        doc_panel = ttk.Frame(self.doc_paned)
        self.doc_paned.add(doc_panel, weight=60)
        
        # Create treeview with scrollbar
        columns = ("name", "type", "status", "size", "date")
        self.docs_tree = ttk.Treeview(doc_panel, columns=columns, show="headings")
        
        # Configure columns
        self.docs_tree.heading("name", text="Document Name")
        self.docs_tree.heading("type", text="Type")
        self.docs_tree.heading("status", text="Status")
        self.docs_tree.heading("size", text="Size")
        self.docs_tree.heading("date", text="Date")
        
        self.docs_tree.column("name", width=250)
        self.docs_tree.column("type", width=80)
        self.docs_tree.column("status", width=100)
        self.docs_tree.column("size", width=80)
        self.docs_tree.column("date", width=120)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(doc_panel, orient=tk.VERTICAL, command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack components
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.docs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.docs_tree.bind("<<TreeviewSelect>>", self.on_document_select)
        self.docs_tree.bind("<Double-1>", self.view_document)
    
    def create_preview_panel(self):
        """Create document preview panel"""
        preview_panel = ttk.Frame(self.doc_paned)
        self.doc_paned.add(preview_panel, weight=40)
        
        # Document info header
        self.doc_title_var = tk.StringVar(value="Document Preview")
        ttk.Label(
            preview_panel, 
            textvariable=self.doc_title_var,
            font=("Arial", 12, "bold")
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Document preview notebook (tabs for info, preview, metadata)
        preview_notebook = ttk.Notebook(preview_panel)
        preview_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Info tab
        info_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(info_frame, text="Info")
        
        # Info fields
        info_content = ttk.Frame(info_frame, padding=10)
        info_content.pack(fill=tk.BOTH, expand=True)
        
        info_fields = [
            ("Name:", "doc_name"),
            ("Type:", "doc_type"),
            ("Size:", "doc_size"),
            ("Status:", "doc_status"),
            ("Created:", "doc_created"),
            ("Modified:", "doc_modified"),
            ("Project:", "doc_project"),
            ("Processed:", "doc_processed")
        ]
        
        self.doc_info_vars = {}
        
        for i, (label_text, field_name) in enumerate(info_fields):
            ttk.Label(info_content, text=label_text, font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=5
            )
            
            var = tk.StringVar()
            ttk.Label(info_content, textvariable=var).grid(
                row=i, column=1, sticky=tk.W, padx=5, pady=5
            )
            
            self.doc_info_vars[field_name] = var
        
        # Preview tab
        preview_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(preview_frame, text="Preview")
        
        # Text preview with scrollbars
        preview_container = ttk.Frame(preview_frame, padding=10)
        preview_container.pack(fill=tk.BOTH, expand=True)
        
        self.preview_text = tk.Text(
            preview_container, 
            wrap=tk.WORD, 
            height=20,
            width=40
        )
        preview_v_scroll = ttk.Scrollbar(
            preview_container, 
            orient=tk.VERTICAL, 
            command=self.preview_text.yview
        )
        preview_h_scroll = ttk.Scrollbar(
            preview_container, 
            orient=tk.HORIZONTAL, 
            command=self.preview_text.xview
        )
        
        self.preview_text.configure(
            yscrollcommand=preview_v_scroll.set,
            xscrollcommand=preview_h_scroll.set,
            state=tk.DISABLED
        )
        
        # Pack preview components
        preview_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        preview_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Metadata tab
        metadata_frame = ttk.Frame(preview_notebook)
        preview_notebook.add(metadata_frame, text="Metadata")
        
        # Metadata text with scrollbar
        metadata_container = ttk.Frame(metadata_frame, padding=10)
        metadata_container.pack(fill=tk.BOTH, expand=True)
        
        self.metadata_text = tk.Text(
            metadata_container, 
            wrap=tk.WORD, 
            height=20,
            width=40
        )
        metadata_scroll = ttk.Scrollbar(
            metadata_container, 
            orient=tk.VERTICAL, 
            command=self.metadata_text.yview
        )
        
        self.metadata_text.configure(
            yscrollcommand=metadata_scroll.set,
            state=tk.DISABLED
        )
        
        # Pack metadata components
        metadata_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.metadata_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Document actions
        actions_frame = ttk.Frame(preview_panel)
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            actions_frame,
            text="View",
            command=self.view_document
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Process",
            command=self.process_document
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Delete",
            command=self.delete_document,
            style="Danger.TButton"
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_dummy_documents(self):
        """Load dummy documents for demonstration"""
        # Clear current items
        for item in self.docs_tree.get_children():
            self.docs_tree.delete(item)
        
        # Add dummy documents
        documents = [
            ("SPM Implementation - Comp Plan.pdf", "PDF", "Completed", "1.2 MB", "2024-01-15"),
            ("Quota Model 2024.xlsx", "Excel", "Completed", "458 KB", "2024-01-16"),
            ("Sales Territories.docx", "Word", "Pending", "328 KB", "2024-01-20"),
            ("Performance Report Q1.pdf", "PDF", "Processing", "2.5 MB", "2024-02-05"),
            ("Commission Calculations.json", "JSON", "Completed", "156 KB", "2024-02-10"),
            ("Incentive Rules.txt", "Text", "Failed", "45 KB", "2024-02-15")
        ]
        
        for doc in documents:
            self.docs_tree.insert("", tk.END, values=doc)
    
    def on_document_select(self, event):
        """Handle document selection in the tree"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            return
        
        # Get selected document
        item = selected_items[0]
        values = self.docs_tree.item(item, "values")
        
        # Update document title
        self.doc_title_var.set(values[0])
        
        # Update info fields
        self.doc_info_vars["doc_name"].set(values[0])
        self.doc_info_vars["doc_type"].set(values[1])
        self.doc_info_vars["doc_size"].set(values[3])
        self.doc_info_vars["doc_status"].set(values[2])
        self.doc_info_vars["doc_created"].set(values[4])
        self.doc_info_vars["doc_modified"].set(values[4])
        self.doc_info_vars["doc_project"].set(self.project_combo.get() or "N/A")
        self.doc_info_vars["doc_processed"].set("Yes" if values[2] == "Completed" else "No")
        
        # Update preview
        self.update_document_preview(values[0], values[1])
        
        # Update metadata
        self.update_document_metadata(values[0], values[1], values[2])
    
    def update_document_preview(self, doc_name, doc_type):
        """Update document preview text"""
        # Enable text widget for editing
        self.preview_text.config(state=tk.NORMAL)
        
        # Clear current content
        self.preview_text.delete("1.0", tk.END)
        
        # Add sample preview based on document type
        if doc_type == "PDF":
            preview = f"PDF Document: {doc_name}\n\n"
            preview += "This is a sample preview of a PDF document.\n"
            preview += "In a real implementation, this would show the first few pages of the PDF."
        
        elif doc_type == "Excel":
            preview = f"Excel Spreadsheet: {doc_name}\n\n"
            preview += "Sheet 1: Sales Data\n"
            preview += "------------------------\n"
            preview += "Month    | Revenue  | Quota   | Attainment\n"
            preview += "Jan 2024 | $125,000 | $120,000| 104%\n"
            preview += "Feb 2024 | $118,000 | $120,000| 98%\n"
            preview += "Mar 2024 | $132,000 | $120,000| 110%\n"
        
        elif doc_type == "Word":
            preview = f"Word Document: {doc_name}\n\n"
            preview += "This is a sample preview of a Word document.\n\n"
            preview += "It would show the formatted text content of the document."
        
        elif doc_type == "JSON":
            preview = f"JSON Document: {doc_name}\n\n"
            preview += "{\n"
            preview += '  "plan_name": "Sales Compensation Plan 2024",\n'
            preview += '  "components": [\n'
            preview += '    {\n'
            preview += '      "name": "Base Salary",\n'
            preview += '      "type": "fixed",\n'
            preview += '      "amount": 60000\n'
            preview += '    },\n'
            preview += '    {\n'
            preview += '      "name": "Commission",\n'
            preview += '      "type": "variable",\n'
            preview += '      "rate": 0.05\n'
            preview += '    }\n'
            preview += '  ]\n'
            preview += '}'
        
        else:
            preview = f"Document: {doc_name}\n\n"
            preview += "Preview not available for this document type."
        
        # Insert the preview
        self.preview_text.insert(tk.END, preview)
        
        # Return to read-only state
        self.preview_text.config(state=tk.DISABLED)
    
    def update_document_metadata(self, doc_name, doc_type, status):
        """Update document metadata text"""
        # Enable text widget for editing
        self.metadata_text.config(state=tk.NORMAL)
        
        # Clear current content
        self.metadata_text.delete("1.0", tk.END)
        
        # Add sample metadata based on document type and status
        metadata = f"Metadata for: {doc_name}\n"
        metadata += "------------------------\n\n"
        
        # Common metadata
        metadata += f"File Type: {doc_type}\n"
        metadata += f"Status: {status}\n"
        metadata += f"Last Modified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        metadata += f"Owner: SPM Edge User\n\n"
        
        # Add processing metadata if processed
        if status == "Completed":
            metadata += "Processing Information:\n"
            metadata += "------------------------\n"
            metadata += "Processing Date: 2024-02-15 14:30:00\n"
            metadata += "Processing Model: gpt-4o\n"
            metadata += "Confidence Score: 0.92\n\n"
            
            # Add extracted metadata based on document type
            if doc_type in ["PDF", "Word"]:
                metadata += "Extracted Components:\n"
                metadata += "------------------------\n"
                metadata += "- Base Salary: $60,000\n"
                metadata += "- Commission Rate: 5%\n"
                metadata += "- Quota: $1,200,000\n"
                metadata += "- Payment Frequency: Monthly\n"
        
        # Insert the metadata
        self.metadata_text.insert(tk.END, metadata)
        
        # Return to read-only state
        self.metadata_text.config(state=tk.DISABLED)
    
    def upload_documents(self):
        """Upload new documents"""
        # Get selected project
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project first")
            return
        
        # Open file dialog
        files = filedialog.askopenfilenames(
            title="Select Documents to Upload",
            filetypes=(
                ("All Documents", "*.pdf;*.docx;*.xlsx;*.pptx;*.txt;*.json"), 
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx"),
                ("Excel Spreadsheets", "*.xlsx"),
                ("PowerPoint Presentations", "*.pptx"),
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            )
        )
        
        if not files:
            return
        
        # Add documents to the list
        for file_path in files:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            # Determine file type
            ext = os.path.splitext(file_name)[1].lower()
            if ext == ".pdf":
                file_type = "PDF"
            elif ext in [".docx", ".doc"]:
                file_type = "Word"
            elif ext in [".xlsx", ".xls"]:
                file_type = "Excel"
            elif ext in [".pptx", ".ppt"]:
                file_type = "PowerPoint"
            elif ext == ".txt":
                file_type = "Text"
            elif ext == ".json":
                file_type = "JSON"
            else:
                file_type = "Other"
            
            # Format file size
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
            # Add to tree
            today = datetime.now().strftime("%Y-%m-%d")
            self.docs_tree.insert("", tk.END, values=(file_name, file_type, "Pending", size_str, today))
        
        # Show success message
        messagebox.showinfo("Upload", f"Successfully uploaded {len(files)} files")
    
    def refresh_documents(self):
        """Refresh the documents list"""
        # In a real implementation, you would reload documents from the database
        messagebox.showinfo("Refresh", "Refreshing document list")
        self.load_dummy_documents()
    
    def view_document(self, event=None):
        """View the selected document"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a document to view")
            return
        
        # Get selected document
        item = selected_items[0]
        values = self.docs_tree.item(item, "values")
        
        messagebox.showinfo("View Document", f"Viewing document: {values[0]}")
    
    def process_document(self):
        """Process the selected document"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a document to process")
            return
        
        # Get selected document
        item = selected_items[0]
        values = self.docs_tree.item(item, "values")
        
        # Check if already processed
        if values[2] == "Completed":
            messagebox.showinfo("Info", f"Document '{values[0]}' is already processed")
            return
        
        # Ask for confirmation
        if not messagebox.askyesno("Confirm", f"Process document '{values[0]}'?"):
            return
        
        # Update status to processing
        self.docs_tree.item(item, values=(values[0], values[1], "Processing", values[3], values[4]))
        
        # In a real implementation, you would start the processing job
        # For simulation, we'll use a simple timer
        def complete_processing():
            self.docs_tree.item(item, values=(values[0], values[1], "Completed", values[3], values[4]))
            self.docs_tree.selection_set(item)
            self.on_document_select(None)  # Update preview
            messagebox.showinfo("Processing", f"Document '{values[0]}' processed successfully")
            
        self.app.root.after(2000, complete_processing)
    
    def delete_document(self):
        """Delete the selected document"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a document to delete")
            return
        
        # Get selected document
        item = selected_items[0]
        values = self.docs_tree.item(item, "values")
        
        # Ask for confirmation
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{values[0]}'?"):
            return
        
        # Delete the document
        self.docs_tree.delete(item)
        
        # Clear preview
        self.doc_title_var.set("Document Preview")
        
        for var in self.doc_info_vars.values():
            var.set("")
        
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.config(state=tk.DISABLED)
        
        self.metadata_text.config(state=tk.NORMAL)
        self.metadata_text.delete("1.0", tk.END)
        self.metadata_text.config(state=tk.DISABLED)
        
        # Show success message
        messagebox.showinfo("Delete", f"Document '{values[0]}' deleted successfully")

def create_documents_tab(notebook, app):
    """Create the documents tab"""
    documents_tab = DocumentsTab(notebook, app)
    app.documents_tab = documents_tab
    return documents_tab.frame