"""
Dashboard tab for SPM Edge UI
"""
import tkinter as tk
from tkinter import ttk

def create_dashboard_card(parent, title, status, button_text, button_command, row, col):
    """Create a dashboard summary card"""
    card_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
    card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
    # Card title
    ttk.Label(
        card_frame,
        text=title,
        font=("Arial", 14, "bold"),
        anchor="center"
    ).pack(pady=(15, 5), fill=tk.X)
    
    # Card content
    content_frame = ttk.Frame(card_frame)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    
    ttk.Label(
        content_frame,
        text=status,
        font=("Arial", 12),
        anchor="center"
    ).pack(fill=tk.BOTH, expand=True)
    
    # Card action button
    ttk.Button(
        card_frame,
        text=button_text,
        command=button_command
    ).pack(pady=(5, 15), padx=15, fill=tk.X)


def create_dashboard_tab(notebook, app):
    """Create the dashboard tab with overview and recent activity"""
    dashboard_frame = ttk.Frame(notebook)
    notebook.add(dashboard_frame, text="Dashboard")
    
    # Header with welcome message
    header_frame = ttk.Frame(dashboard_frame)
    header_frame.pack(fill=tk.X, padx=20, pady=20)
    
    ttk.Label(
        header_frame, 
        text="SPM Edge - AI Document Processor", 
        font=("Arial", 18, "bold")
    ).pack(anchor=tk.W)
    
    ttk.Label(
        header_frame, 
        text="Process and analyze sales performance management documents with AI",
        font=("Arial", 12)
    ).pack(anchor=tk.W)
    
    # Main dashboard content (2x2 grid)
    dashboard_content = ttk.Frame(dashboard_frame)
    dashboard_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Configure grid
    for i in range(2):
        dashboard_content.columnconfigure(i, weight=1)
        dashboard_content.rowconfigure(i, weight=1)
    
    # Summary cards
    create_dashboard_card(
        dashboard_content, 
        "Projects", 
        "0 active projects", 
        "Create New Project",
        app.new_project,
        0, 0
    )
    
    create_dashboard_card(
        dashboard_content, 
        "Documents", 
        "0 documents processed", 
        "Upload Documents",
        app.import_documents,
        0, 1
    )
    
    create_dashboard_card(
        dashboard_content, 
        "Pipeline Status", 
        "Ready to process", 
        "Run Pipeline",
        app.run_pipeline,
        1, 0
    )
    
    create_dashboard_card(
        dashboard_content, 
        "Deliverables", 
        "0 reports generated", 
        "Generate Reports",
        lambda: notebook.select(6),  # Select the Deliverables tab
        1, 1
    )
    
    return dashboard_frame