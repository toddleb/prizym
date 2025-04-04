"""
Project Management Integration Module for KPMG Edge.
This module integrates the project management functionality into the main application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any, Optional

# Import project management modules
from modules.project_module import ProjectModule
from modules.resource_module import ResourceModule
from modules.timeline_module import TimelineModule

# Configure logger
logger = logging.getLogger("project_integration")

class ProjectManagementModule:
    """Integration module for project management functionality"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        
        # Initialize sub-modules
        self.project_module = ProjectModule(parent_frame, colors, db_manager)
        self.resource_module = ResourceModule(parent_frame, colors, db_manager)
        self.timeline_module = TimelineModule(parent_frame, colors, db_manager)
        
        # Current selection
        self.current_project = None
        self.current_view = None
    
    def show_dashboard(self):
        """Show the project management dashboard"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create main container with header
        self.create_view_header("Project Management Dashboard", "Overview of projects, resources, and timelines")
        
        # Create dashboard layout
        dashboard_frame = ttk.Frame(self.parent_frame)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Three-column layout
        left_col = ttk.Frame(dashboard_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        middle_col = ttk.Frame(dashboard_frame)
        middle_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_col = ttk.Frame(dashboard_frame)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Left column - Project overview
        self.create_projects_overview(left_col)
        
        # Middle column - Resource overview
        self.create_resources_overview(middle_col)
        
        # Right column - Timeline overview
        self.create_timeline_overview(right_col)
        
        # Bottom navigation options
        self.create_navigation_options()
    
    def create_view_header(self, title, subtitle=None):
        """Create a header for a view"""
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=title, font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        if subtitle:
            ttk.Label(header_frame, text=subtitle, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.parent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
    
    def create_projects_overview(self, parent):
        """Create the projects overview section"""
        # Project stats
        stats_frame = ttk.LabelFrame(parent, text="Project Statistics")
        stats_frame.pack(fill=tk.X, pady=10)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Load project stats
        total_projects = 0
        projects_by_status = {"On Track": 0, "At Risk": 0, "Delayed": 0, "Completed": 0}
        
        if self.db_manager and self.db_manager.is_connected():
            # Get projects from database
            projects = self.db_manager.get_all_projects()
            total_projects = len(projects)
            
            # Count projects by status
            for project in projects:
                status = project.get("status", "")
                if status in projects_by_status:
                    projects_by_status[status] += 1
        
        # Display stats
        ttk.Label(stats_grid, text="Total Projects:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(total_projects), font=("Arial", 16, "bold"), foreground=self.colors["primary"]).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="On Track:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(projects_by_status["On Track"]), font=("Arial", 12), foreground=self.colors["success"]).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="At Risk:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(projects_by_status["At Risk"]), font=("Arial", 12), foreground=self.colors["warning"]).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Delayed:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(projects_by_status["Delayed"]), font=("Arial", 12), foreground=self.colors["danger"]).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Completed:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(projects_by_status["Completed"]), font=("Arial", 12), foreground=self.colors["secondary"]).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Recent projects
        recent_frame = ttk.LabelFrame(parent, text="Recent Projects")
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Project list
        projects_list = tk.Listbox(recent_frame, height=8)
        projects_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(projects_list, orient=tk.VERTICAL, command=projects_list.yview)
        projects_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add sample projects
        projects_list.insert(tk.END, "SPM Implementation - ABC Corp")
        projects_list.insert(tk.END, "Sales Planning Assessment - XYZ Inc")
        projects_list.insert(tk.END, "ICM Migration - Global Retail")
        projects_list.insert(tk.END, "Optimization Project - 123 Industries")
        projects_list.insert(tk.END, "SPM Support - Financial Services")
        
        # Bind double-click to view project
        projects_list.bind("<Double-1>", lambda e: self.view_selected_project(projects_list))
        
        # Quick actions
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            actions_frame, 
            text="Create New Project",
            command=self.show_new_project_form
        ).pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            actions_frame, 
            text="View All Projects",
            command=self.show_all_projects
        ).pack(fill=tk.X, padx=10, pady=5)
    
    def create_resources_overview(self, parent):
        """Create the resources overview section"""
        # Resource stats
        stats_frame = ttk.LabelFrame(parent, text="Resource Statistics")
        stats_frame.pack(fill=tk.X, pady=10)
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Load resource stats
        total_resources = 0
        available_resources = 0
        fully_allocated_resources = 0
        
        if self.db_manager and self.db_manager.is_connected():
            # Get resources from database
            resources = self.db_manager.get_all_resources()
            total_resources = len(resources)
            
            # Count resources by availability
            for resource in resources:
                availability = resource.get("availability", {})
                if isinstance(availability, dict):
                    if availability.get("status") == "Available":
                        available_resources += 1
                    elif availability.get("status") == "Unavailable":
                        fully_allocated_resources += 1
        
        # Display stats
        ttk.Label(stats_grid, text="Total Resources:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(total_resources), font=("Arial", 16, "bold"), foreground=self.colors["primary"]).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Available Resources:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(available_resources), font=("Arial", 12), foreground=self.colors["success"]).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Fully Allocated:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(fully_allocated_resources), font=("Arial", 12), foreground=self.colors["warning"]).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Resource allocation chart (simplified representation)
        chart_frame = ttk.LabelFrame(parent, text="Resource Allocation")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Simple canvas chart
        canvas = tk.Canvas(chart_frame, background="white", height=200)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a simple bar chart
        canvas.create_text(150, 20, text="Resource Allocation Overview", font=("Arial", 12, "bold"))
        
        # Draw bars for each role
        roles = ["Project Manager", "Business Analyst", "Developer", "Tester", "Consultant"]
        values = [80, 60, 90, 70, 50]  # Sample percentages
        
        bar_width = 30
        x_start = 50
        y_bottom = 150
        
        for i, (role, value) in enumerate(zip(roles, values)):
            x = x_start + i * 60
            
            # Draw bar
            bar_height = value * 1.2  # Scale for visual appeal
            canvas.create_rectangle(
                x, y_bottom - bar_height,
                x + bar_width, y_bottom,
                fill=self.colors["primary"],
                outline=""
            )
            
            # Draw role label
            canvas.create_text(
                x + bar_width/2, y_bottom + 20,
                text=role,
                width=60,
                anchor=tk.N,
                font=("Arial", 8)
            )
            
            # Draw value label
            canvas.create_text(
                x + bar_width/2, y_bottom - bar_height - 10,
                text=f"{value}%",
                anchor=tk.S,
                font=("Arial", 8, "bold")
            )
        
        # Quick actions
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            actions_frame, 
            text="Manage Resources",
            command=self.show_resource_management
        ).pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            actions_frame, 
            text="View Resource Allocation",
            command=self.show_resource_allocation
        ).pack(fill=tk.X, padx=10, pady=5)
    
    def create_timeline_overview(self, parent):
        """Create the timeline overview section"""
        # Upcoming milestones
        milestones_frame = ttk.LabelFrame(parent, text="Upcoming Milestones")
        milestones_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Milestones list
        for i in range(5):
            item_frame = ttk.Frame(milestones_frame)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Status indicator
            status_color = "green" if i % 3 == 0 else "orange" if i % 3 == 1 else "red"
            status_indicator = tk.Label(item_frame, text="•", foreground=status_color, font=("Arial", 16))
            status_indicator.pack(side=tk.LEFT)
            
            # Milestone info
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            milestone_name = "Project Kickoff" if i == 0 else "Requirements Sign-off" if i == 1 else "Design Approval" if i == 2 else "Development Complete" if i == 3 else "UAT Sign-off"
            project_name = f"Project {i+1}"
            
            ttk.Label(info_frame, text=milestone_name, font=("Arial", 10, "bold")).pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Due: 2023-{3+i}-{10+i}", font=("Arial", 8)).pack(anchor=tk.W)
            ttk.Label(info_frame, text=project_name, font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
            
            # Status text
            status_text = "On Track" if i % 3 == 0 else "At Risk" if i % 3 == 1 else "Delayed"
            ttk.Label(item_frame, text=status_text, foreground=status_color).pack(side=tk.RIGHT)
        
        # This week's tasks
        tasks_frame = ttk.LabelFrame(parent, text="This Week's Tasks")
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tasks list
        for i in range(5):
            item_frame = ttk.Frame(tasks_frame)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Status indicator
            status_color = "blue" if i % 2 == 0 else "green"
            status_indicator = tk.Label(item_frame, text="•", foreground=status_color, font=("Arial", 16))
            status_indicator.pack(side=tk.LEFT)
            
            # Task info
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            task_name = f"Task {i+1} - Some description here"
            project_name = f"Project {i % 3 + 1}"
            
            ttk.Label(info_frame, text=task_name, font=("Arial", 10)).pack(anchor=tk.W)
            ttk.Label(info_frame, text=project_name, font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
            
            # Status text
            status_text = "In Progress" if i % 2 == 0 else "Completed"
            ttk.Label(item_frame, text=status_text, foreground=status_color).pack(side=tk.RIGHT)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions")
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            actions_frame, 
            text="View Project Timelines",
            command=self.show_project_timelines
        ).pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            actions_frame, 
            text="Task Dashboard",
            command=self.show_task_dashboard
        ).pack(fill=tk.X, padx=10, pady=5)
    
    def create_navigation_options(self):
        """Create navigation options at the bottom of the dashboard"""
        nav_frame = ttk.Frame(self.parent_frame)
        nav_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            nav_frame, 
            text="Refresh Dashboard",
            command=self.show_dashboard
        ).pack(side=tk.RIGHT)
    
    def view_selected_project(self, listbox):
        """View the selected project from a listbox"""
        selection = listbox.curselection()
        if selection:
            project_name = listbox.get(selection[0])
            messagebox.showinfo("View Project", f"Would open project details for: {project_name}")
    
    def show_new_project_form(self):
        """Show the new project form"""
        self.project_module.show_new_project()
    
    def show_all_projects(self):
        """Show all projects"""
        self.project_module.show_current_projects()
    
    def show_resource_management(self):
        """Show the resource management view"""
        self.resource_module.show_resource_management()
    
    def show_resource_allocation(self):
        """Show the resource allocation view"""
        # This is a placeholder - in a real app, we'd navigate to the allocation tab
        self.resource_module.show_resource_management()
        messagebox.showinfo("Resource Allocation", "Would navigate to the Resource Allocation tab")
    
    def show_project_timelines(self):
        """Show project timelines view"""
        # This is a placeholder - in a real app, we'd ask which project to view
        messagebox.showinfo("Project Timelines", "Would show a list of projects to select for timeline view")
    
    def show_task_dashboard(self):
        """Show the task dashboard view"""
        # This is a placeholder
        messagebox.showinfo("Task Dashboard", "Would show the task dashboard with all tasks across projects")
    
    def navigate_to_view(self, view_name, **kwargs):
        """Navigate to a specific view"""
        self.current_view = view_name
        
        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "projects":
            self.show_all_projects()
        elif view_name == "new_project":
            self.show_new_project_form()
        elif view_name == "project_detail" and "project_id" in kwargs:
            # Navigate to project detail
            # This would be implemented in a real app
            messagebox.showinfo("Project Detail", f"Would show details for project ID: {kwargs['project_id']}")
        elif view_name == "resources":
            self.show_resource_management()
        elif view_name == "timeline" and "project_id" in kwargs:
            self.timeline_module.show_project_timeline(kwargs["project_id"])
        else:
            logger.warning(f"Unknown view: {view_name}")
            self.show_dashboard()