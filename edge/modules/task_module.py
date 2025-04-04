import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger("task_module")

class TaskModule:
    """Task management module for the KPMG Edge application"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        self.tasks = []
        self.projects = []
        self.resources = []
        
        # Load data if database not available
        if self.db_manager is None or not self.db_manager.is_connected():
            self.load_from_json()
    
    def load_from_json(self):
        """Load data from JSON files (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            # Load tasks
            if os.path.exists("data/tasks.json"):
                with open("data/tasks.json", "r") as f:
                    self.tasks = json.load(f)
                    logger.info(f"Loaded {len(self.tasks)} tasks from JSON file")
            
            # Load projects
            if os.path.exists("data/projects.json"):
                with open("data/projects.json", "r") as f:
                    self.projects = json.load(f)
                    logger.info(f"Loaded {len(self.projects)} projects from JSON file")
            
            # Load resources
            if os.path.exists("data/resources.json"):
                with open("data/resources.json", "r") as f:
                    self.resources = json.load(f)
                    logger.info(f"Loaded {len(self.resources)} resources from JSON file")
        except Exception as e:
            logger.error(f"Error loading data from JSON: {e}")
            self.tasks = []
            self.projects = []
            self.resources = []
    
    def save_tasks_to_json(self):
        """Save tasks to a JSON file (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            with open("data/tasks.json", "w") as f:
                json.dump(self.tasks, f, indent=2)
                logger.info(f"Saved {len(self.tasks)} tasks to JSON file")
        except Exception as e:
            logger.error(f"Error saving tasks to JSON: {e}")
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def show_task_dashboard(self):
        """Show the task dashboard view"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Load data from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.projects = self.db_manager.get_all_projects()
            self.resources = self.db_manager.get_all_resources()
            
            # Load tasks from all projects
            self.tasks = []
            for project in self.projects:
                project_tasks = self.db_manager.get_tasks_by_project(project.get("id", -1))
                if project_tasks:
                    # Add project name to each task for identification
                    for task in project_tasks:
                        task["project_name"] = project.get("name", "")
                    
                    self.tasks.extend(project_tasks)
        
        # Create main container with header
        self.create_view_header("Task Dashboard", "Manage tasks across all projects")
        
        # Create main notebook for task views
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        all_tasks_tab = ttk.Frame(notebook)
        my_tasks_tab = ttk.Frame(notebook)
        overdue_tab = ttk.Frame(notebook)
        by_project_tab = ttk.Frame(notebook)
        
        notebook.add(all_tasks_tab, text="All Tasks")
        notebook.add(my_tasks_tab, text="My Tasks")
        notebook.add(overdue_tab, text="Overdue")
        notebook.add(by_project_tab, text="By Project")
        
        # Setup each tab
        self.setup_all_tasks_tab(all_tasks_tab)
        self.setup_my_tasks_tab(my_tasks_tab)
        self.setup_overdue_tab(overdue_tab)
        self.setup_by_project_tab(by_project_tab)
        
        # Navigation button
        navigation_frame = ttk.Frame(self.parent_frame)
        navigation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            navigation_frame, 
            text="Back to Dashboard",
            command=self.back_to_dashboard
        ).pack(side=tk.LEFT)
    
    def create_view_header(self, title, subtitle=None):
        """Create a header for a view"""
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=title, font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        if subtitle:
            ttk.Label(header_frame, text=subtitle, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.parent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
    
    def setup_all_tasks_tab(self, parent):
        """Setup the all tasks tab"""
        # Create control frame with buttons and filters
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Add Task",
            command=self.show_add_task_form
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_tasks_tab(parent)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter controls
        ttk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=10)
        status_filter = ttk.Combobox(control_frame, values=["All", "Not Started", "In Progress", "On Hold", "Completed"], width=12)
        status_filter.current(0)
        status_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Project:").pack(side=tk.LEFT, padx=10)
        
        # Get project names for filter
        project_names = ["All"]
        for project in self.projects:
            project_names.append(project.get("name", ""))
        
        project_filter = ttk.Combobox(control_frame, values=project_names, width=15)
        project_filter.current(0)
        project_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Assigned To:").pack(side=tk.LEFT, padx=10)
        
        # Get resource names for filter
        resource_names = ["All", "Unassigned"]
        for resource in self.resources:
            resource_names.append(resource.get("name", ""))
        
        assigned_filter = ttk.Combobox(control_frame, values=resource_names, width=15)
        assigned_filter.current(0)
        assigned_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Filter",
            command=lambda: self.apply_task_filters(
                status_filter.get(), 
                project_filter.get(), 
                assigned_filter.get()
            )
        ).pack(side=tk.LEFT, padx=5)