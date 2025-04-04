import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

class AssetAnalyzerModule:
    """Asset Analyzer module for compensation plan analysis"""
    
    def __init__(self, parent_frame, colors):
        self.parent_frame = parent_frame
        self.colors = colors
        self.data = None
        self.comp_plans = {}
        
    def create_ui(self):
        """Create the Asset Analyzer UI"""
        # Clean the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.upload_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        self.visualization_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.upload_tab, text="Upload & Configure")
        self.notebook.add(self.analysis_tab, text="Analysis")
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.notebook.add(self.report_tab, text="Report")
        
        # Setup each tab
        self.setup_upload_tab()
        self.setup_analysis_tab()
        self.setup_visualization_tab()
        self.setup_report_tab()
    
    def setup_upload_tab(self):
        """Setup the upload and configuration tab"""
        # File upload section
        upload_frame = ttk.LabelFrame(self.upload_tab, text="Upload Compensation Plan Files")
        upload_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(upload_frame, text="Select compensation plan files to analyze:").pack(anchor=tk.W, padx=10, pady=5)
        
        buttons_frame = ttk.Frame(upload_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(buttons_frame, text="Upload Files", command=self.upload_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Upload Folder", command=self.upload_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear All", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # Files list
        files_frame = ttk.Frame(upload_frame)
        files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(files_frame, text="Uploaded Files:").pack(anchor=tk.W)
        
        # Treeview for files
        columns = ("Filename", "Type", "Size", "Status")
        self.files_tree = ttk.Treeview(files_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.files_tree.heading(col, text=col)
        
        self.files_tree.column("Filename", width=250)
        self.files_tree.column("Type", width=100)
        self.files_tree.column("Size", width=100)
        self.files_tree.column("Status", width=150)
        
        self.files_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Configuration section
        config_frame = ttk.LabelFrame(self.upload_tab, text="Analysis Configuration")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Two-column layout
        left_config = ttk.Frame(config_frame)
        left_config.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_config = ttk.Frame(config_frame)
        right_config.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column - Basic settings
        ttk.Label(left_config, text="Analysis Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.analysis_type = ttk.Combobox(left_config, values=[
            "Comprehensive", 
            "Structure Analysis", 
            "Metrics Comparison",
            "Performance Simulation"
        ])
        self.analysis_type.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.analysis_type.current(0)
        
        ttk.Label(left_config, text="Role Focus:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.role_focus = ttk.Combobox(left_config, values=[
            "All Roles",
            "Sales Representatives", 
            "Sales Managers",
            "Channel Partners",
            "Executives"
        ])
        self.role_focus.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.role_focus.current(0)
        
        ttk.Label(left_config, text="Industry Benchmark:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.industry = ttk.Combobox(left_config, values=[
            "Technology", 
            "Financial Services", 
            "Healthcare",
            "Manufacturing",
            "Retail",
            "Custom..."
        ])
        self.industry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Right column - Advanced settings
        ttk.Label(right_config, text="Compensation Elements:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.comp_elements_frame = ttk.Frame(right_config)
        self.comp_elements_frame.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.base_var = tk.BooleanVar(value=True)
        self.bonus_var = tk.BooleanVar(value=True)
        self.commission_var = tk.BooleanVar(value=True)
        self.equity_var = tk.BooleanVar(value=False)
        self.benefits_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(self.comp_elements_frame, text="Base Salary", variable=self.base_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.comp_elements_frame, text="Bonus", variable=self.bonus_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.comp_elements_frame, text="Commission", variable=self.commission_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.comp_elements_frame, text="Equity", variable=self.equity_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.comp_elements_frame, text="Benefits", variable=self.benefits_var).pack(anchor=tk.W)
        
        ttk.Label(right_config, text="AI Analysis Level:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ai_level = ttk.Scale(right_config, from_=1, to=5, orient=tk.HORIZONTAL, length=150)
        self.ai_level.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.ai_level.set(3)
        
        ttk.Label(right_config, text="Report Detail:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.report_detail = ttk.Combobox(right_config, values=["Executive Summary", "Standard", "Detailed"])
        self.report_detail.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        self.report_detail.current(1)
        
        # Action buttons
        buttons_frame = ttk.Frame(config_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="Start Analysis", command=self.start_analysis).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Save Configuration").pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Load Configuration").pack(side=tk.RIGHT, padx=5)
    
    def setup_analysis_tab(self):
        """Setup the analysis results tab"""
        # Placeholder for the full implementation
        ttk.Label(self.analysis_tab, text="Analysis Results", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(self.analysis_tab, text="This tab would display analysis results including:\n" +
                                      "- Compensation plan structure\n" +
                                      "- Metrics and benchmarks\n" +
                                      "- Issues and recommendations\n" +
                                      "- AI-powered insights").pack()
    
    def setup_visualization_tab(self):
        """Setup the visualization results tab"""
        # Placeholder for the full implementation
        ttk.Label(self.visualization_tab, text="Visualization", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(self.visualization_tab, text="This tab would display interactive visualizations including:\n" +
                                       "- Pay mix distribution charts\n" +
                                       "- Performance curves\n" +
                                       "- Comparative analysis\n" +
                                       "- Scenario modeling").pack()
    
    def setup_report_tab(self):
        """Setup the report generation tab"""
        # Placeholder for the full implementation
        ttk.Label(self.report_tab, text="Report Generation", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(self.report_tab, text="This tab would allow report generation with:\n" +
                                  "- Customizable report sections\n" +
                                  "- Multiple export formats\n" +
                                  "- Presentation-ready outputs\n" +
                                  "- Executive summaries and detailed analysis").pack()
    
    def upload_files(self):
        """Upload files for analysis"""
        file_paths = filedialog.askopenfilenames(
            title="Select Compensation Plan Files",
            filetypes=(
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            )
        )
        
        for file_path in file_paths:
            if file_path:
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_path)[1]
                file_size = os.path.getsize(file_path) / 1024  # size in KB
                
                # Determine file type
                if file_ext.lower() in ['.xlsx', '.xls']:
                    file_type = "Excel"
                elif file_ext.lower() == '.csv':
                    file_type = "CSV"
                elif file_ext.lower() == '.pdf':
                    file_type = "PDF"
                else:
                    file_type = "Unknown"
                
                # Insert into tree
                self.files_tree.insert("", tk.END, values=(
                    file_name,
                    file_type,
                    f"{file_size:.1f} KB",
                    "Ready for processing"
                ))
                
                # Store file reference
                self.comp_plans[file_name] = {
                    'path': file_path,
                    'type': file_type,
                    'processed': False
                }
    
    def upload_folder(self):
        """Upload a folder of files for analysis"""
        folder_path = filedialog.askdirectory(title="Select Folder with Compensation Plans")
        
        if folder_path:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # Skip directories
                if os.path.isdir(file_path):
                    continue
                    
                file_ext = os.path.splitext(file_path)[1]
                file_size = os.path.getsize(file_path) / 1024  # size in KB
                
                # Only process certain file types
                if file_ext.lower() in ['.xlsx', '.xls', '.csv', '.pdf']:
                    # Determine file type
                    if file_ext.lower() in ['.xlsx', '.xls']:
                        file_type = "Excel"
                    elif file_ext.lower() == '.csv':
                        file_type = "CSV"
                    elif file_ext.lower() == '.pdf':
                        file_type = "PDF"
                    else:
                        file_type = "Unknown"
                    
                    # Insert into tree
                    self.files_tree.insert("", tk.END, values=(
                        file_name,
                        file_type,
                        f"{file_size:.1f} KB",
                        "Ready for processing"
                    ))
                    
                    # Store file reference
                    self.comp_plans[file_name] = {
                        'path': file_path,
                        'type': file_type,
                        'processed': False
                    }
    
    def clear_files(self):
        """Clear all uploaded files"""
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        self.comp_plans = {}
    
    def start_analysis(self):
        """Start the analysis process"""
        # Check if we have files to analyze
        if not self.comp_plans:
            messagebox.showwarning("No Files", "Please upload files to analyze first.")
            return
            
        # Update file status in the UI
        for item in self.files_tree.get_children():
            self.files_tree.set(item, "Status", "Processing...")
            
        # In a real implementation, we would process files here
        # For now, just simulate processing with a delay
        self.parent_frame.after(2000, self.update_analysis_status)
        
        # Switch to the Analysis tab
        self.notebook.select(1)
    
    def update_analysis_status(self):
        """Update status after analysis (simulation)"""
        # Update file status
        for item in self.files_tree.get_children():
            self.files_tree.set(item, "Status", "Processed")
            file_name = self.files_tree.item(item, "values")[0]
            if file_name in self.comp_plans:
                self.comp_plans[file_name]['processed'] = True
        
        # Show a completion message
        messagebox.showinfo("Analysis Complete", 
                          "All compensation plans have been analyzed. View the results in the Analysis tab.")