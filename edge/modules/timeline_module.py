import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger("timeline_module")

class TimelineModule:
    """Timeline management module for the KPMG Edge application"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        
    def show_project_timeline(self, project_id):
        """Show the timeline for a specific project"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Load project from database if available
        project = None
        if self.db_manager and self.db_manager.is_connected():
            project = self.db_manager.get_project_by_id(project_id)
        else:
            # This is just a placeholder - in a real app we'd load from JSON
            project = {"id": project_id, "name": "Sample Project", "start_date": "2023-03-01", "end_date": "2023-09-30"}
        
        if not project:
            messagebox.showerror("Error", f"Project with ID {project_id} not found")
            return
        
        # Create main container with header
        self.create_view_header(f"Timeline: {project.get('name', '')}", "Visualize project timeline and manage tasks")
        
        # Create a notebook for different timeline views
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        gantt_tab = ttk.Frame(notebook)
        calendar_tab = ttk.Frame(notebook)
        dependencies_tab = ttk.Frame(notebook)
        
        notebook.add(gantt_tab, text="Gantt Chart")
        notebook.add(calendar_tab, text="Calendar View")
        notebook.add(dependencies_tab, text="Task Dependencies")
        
        # Setup each tab
        self.setup_gantt_tab(gantt_tab, project)
        self.setup_calendar_tab(calendar_tab, project)
        self.setup_dependencies_tab(dependencies_tab, project)
        
        # Bottom navigation
        navigation_frame = ttk.Frame(self.parent_frame)
        navigation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            navigation_frame, 
            text="Back to Project",
            command=lambda: self.back_to_project(project_id)
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            navigation_frame, 
            text="Print Timeline",
            command=self.print_timeline
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            navigation_frame, 
            text="Export to PDF",
            command=self.export_timeline
        ).pack(side=tk.RIGHT, padx=10)
    
    def create_view_header(self, title, subtitle=None):
        """Create a header for a view"""
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=title, font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        if subtitle:
            ttk.Label(header_frame, text=subtitle, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.parent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
    
    def setup_gantt_tab(self, parent, project):
        """Setup the Gantt chart tab for project timeline visualization"""
        # Create control frame with buttons and filters
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Add Task",
            command=lambda: self.show_add_task_form(project)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="+ Add Milestone",
            command=lambda: self.show_add_milestone_form(project)
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_gantt(parent, project)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Zoom control
        ttk.Label(control_frame, text="Zoom:").pack(side=tk.LEFT, padx=10)
        zoom_slider = ttk.Scale(control_frame, from_=1, to=4, orient=tk.HORIZONTAL, length=100)
        zoom_slider.set(2)  # Default zoom level
        zoom_slider.pack(side=tk.LEFT, padx=5)
        
        # Time range filter
        ttk.Label(control_frame, text="Time Range:").pack(side=tk.LEFT, padx=10)
        time_range = ttk.Combobox(control_frame, values=["All", "This Month", "Next 3 Months", "Next 6 Months"], width=15)
        time_range.current(0)
        time_range.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Apply",
            command=lambda: self.apply_gantt_filters(zoom_slider.get(), time_range.get())
        ).pack(side=tk.LEFT, padx=5)