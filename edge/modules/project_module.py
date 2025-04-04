import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger("project_module")

class ProjectModule:
    """Enhanced project management module for the KPMG Edge application"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        self.projects = []
        self.current_project = None
        self.resources = []
        
        # Load projects if database not available
        if self.db_manager is None or not self.db_manager.is_connected():
            self.load_projects_from_json()
    
    def load_projects_from_json(self):
        """Load projects from a JSON file (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            if os.path.exists("data/projects.json"):
                with open("data/projects.json", "r") as f:
                    self.projects = json.load(f)
                    logger.info(f"Loaded {len(self.projects)} projects from JSON file")
        except Exception as e:
            logger.error(f"Error loading projects from JSON: {e}")
            self.projects = []
    
    def save_projects_to_json(self):
        """Save projects to a JSON file (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            with open("data/projects.json", "w") as f:
                json.dump(self.projects, f, indent=2)
                logger.info(f"Saved {len(self.projects)} projects to JSON file")
        except Exception as e:
            logger.error(f"Error saving projects to JSON: {e}")
            messagebox.showerror("Error", f"Failed to save projects: {e}")
    
    def show_current_projects(self):
        """Display the current projects view"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Load projects from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.projects = self.db_manager.get_all_projects()
        
        # Create main container with header
        self.create_view_header("Current Projects", "Manage and view all your project portfolio")
        
        # Create a frame for filters
        filter_frame = ttk.Frame(self.parent_frame)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(filter_frame, text="Filter by:").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "Not Started", "On Track", "At Risk", "Delayed", "Completed"], width=10)
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.current(0)
        self.status_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        ttk.Label(filter_frame, text="Client:").pack(side=tk.LEFT, padx=5)
        
        # Get unique clients
        clients = ["All"]
        if self.projects:
            unique_clients = set()
            for p in self.projects:
                if p.get("client"):
                    unique_clients.add(p.get("client"))
            clients.extend(sorted(list(unique_clients)))
        
        self.client_filter = ttk.Combobox(filter_frame, values=clients, width=15)
        self.client_filter.pack(side=tk.LEFT, padx=5)
        self.client_filter.current(0)
        self.client_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        ttk.Label(filter_frame, text="Type:").pack(side=tk.LEFT, padx=5)
        self.type_filter = ttk.Combobox(filter_frame, values=["All", "Implementation", "Assessment", "Migration", "Optimization"], width=15)
        self.type_filter.pack(side=tk.LEFT, padx=5)
        self.type_filter.current(0)
        self.type_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        ttk.Button(filter_frame, text="Reset Filters", command=self.reset_filters).pack(side=tk.LEFT, padx=10)
        
        new_project_btn = ttk.Button(
            filter_frame, 
            text="+ New Project", 
            style='Accent.TButton',
            command=self.show_new_project
        )
        new_project_btn.pack(side=tk.RIGHT)
        
        # Create projects table
        table_frame = ttk.Frame(self.parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Columns
        columns = ("Project Name", "Client", "Type", "Start Date", "End Date", "Status", "Progress", "Team Lead")
        self.projects_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.projects_table.heading(col, text=col)
            width = 100
            if col == "Project Name" or col == "Client":
                width = 150
            self.projects_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.projects_table.yview)
        self.projects_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.projects_table.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event to view project details
        self.projects_table.bind("<Double-1>", self.view_project_details)
        
        # Context menu for projects
        self.create_project_context_menu()
        
        # Populate with projects
        self.populate_projects_table()
        
        # Create summary section
        summary_frame = ttk.Frame(self.parent_frame)
        summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Stats in a row
        stats = [
            {"label": "Total Projects", "value": str(len(self.projects)), "color": self.colors["primary"]},
            {"label": "Not Started", "value": str(sum(1 for p in self.projects if p.get("status") == "Not Started")), "color": self.colors["accent"]},
            {"label": "On Track", "value": str(sum(1 for p in self.projects if p.get("status") == "On Track")), "color": self.colors["success"]},
            {"label": "At Risk", "value": str(sum(1 for p in self.projects if p.get("status") == "At Risk")), "color": self.colors["warning"]},
            {"label": "Delayed", "value": str(sum(1 for p in self.projects if p.get("status") == "Delayed")), "color": self.colors["danger"]},
            {"label": "Completed", "value": str(sum(1 for p in self.projects if p.get("status") == "Completed")), "color": self.colors["secondary"]}
        ]
        
        for stat in stats:
            stat_frame = ttk.Frame(summary_frame, padding=10)
            stat_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            ttk.Label(stat_frame, text=stat["label"], font=("Arial", 10)).pack(anchor=tk.CENTER)
            ttk.Label(stat_frame, text=stat["value"], font=("Arial", 16, "bold"), foreground=stat["color"]).pack(anchor=tk.CENTER)
    
    def create_view_header(self, title, subtitle=None):
        """Create a header for a view"""
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=title, font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        if subtitle:
            ttk.Label(header_frame, text=subtitle, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.parent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
    
    def create_project_context_menu(self):
        """Create context menu for projects table"""
        self.project_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.project_menu.add_command(label="View Project Details", command=self.view_selected_project)
        self.project_menu.add_command(label="Edit Project", command=self.edit_selected_project)
        self.project_menu.add_separator()
        self.project_menu.add_command(label="View Tasks", command=lambda: self.view_project_tasks())
        self.project_menu.add_command(label="View Resources", command=lambda: self.view_project_resources())
        self.project_menu.add_command(label="View Timeline", command=lambda: self.view_project_timeline())
        self.project_menu.add_separator()
        self.project_menu.add_command(label="Delete Project", command=self.delete_selected_project)
        
        # Bind right-click event
        self.projects_table.bind("<Button-3>", self.show_project_menu)
    
    def show_project_menu(self, event):
        """Show context menu on right-click"""
        # Select row under mouse
        iid = self.projects_table.identify_row(event.y)
        if iid:
            # Select the item
            self.projects_table.selection_set(iid)
            
            # Show menu
            try:
                self.project_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.project_menu.grab_release()
    
    def populate_projects_table(self, filtered_projects=None):
        """Populate the projects table with data"""
        # Clear existing items
        for item in self.projects_table.get_children():
            self.projects_table.delete(item)
        
        # Use filtered list if provided, otherwise use all projects
        projects_to_show = filtered_projects if filtered_projects is not None else self.projects
        
        # Add projects
        for project in projects_to_show:
            # Get team lead if available
            team_lead = ""
            if self.db_manager and self.db_manager.is_connected():
                resources = self.db_manager.get_resources_by_project(project.get("id"))
                for resource in resources:
                    if resource.get("project_role", "").lower() == "project lead" or resource.get("project_role", "").lower() == "team lead":
                        team_lead = resource.get("name", "")
                        break
            
            values = (
                project.get("name", ""),
                project.get("client", ""),
                project.get("type", ""),
                project.get("start_date", ""),
                project.get("end_date", ""),
                project.get("status", ""),
                f"{project.get('progress', 0)}%",
                team_lead
            )
            
            # Set tag based on status for color coding
            tag = project.get("status", "").lower().replace(" ", "_")
            self.projects_table.insert("", tk.END, values=values, tags=(tag,))
        
        # Configure tags for color coding
        self.projects_table.tag_configure("not_started", background="#f8f9fa")
        self.projects_table.tag_configure("on_track", background="#d4edda")
        self.projects_table.tag_configure("at_risk", background="#fff3cd")
        self.projects_table.tag_configure("delayed", background="#f8d7da")
        self.projects_table.tag_configure("completed", background="#d1ecf1")
    
    def apply_filters(self):
        """Apply filters to the projects table"""
        status_filter = self.status_filter.get()
        client_filter = self.client_filter.get()
        type_filter = self.type_filter.get()
        
        filtered_projects = []
        
        for project in self.projects:
            # Apply status filter
            if status_filter != "All" and project.get("status", "") != status_filter:
                continue
                
            # Apply client filter
            if client_filter != "All" and project.get("client", "") != client_filter:
                continue
                
            # Apply type filter
            if type_filter != "All" and project.get("type", "") != type_filter:
                continue
                
            # All filters passed
            filtered_projects.append(project)
        
        # Update table with filtered projects
        self.populate_projects_table(filtered_projects)
    
    def reset_filters(self):
        """Reset all filters to default"""
        self.status_filter.current(0)
        self.client_filter.current(0)
        self.type_filter.current(0)
        self.populate_projects_table()
    
    def view_project_details(self, event):
        """Handle double-click on project to view details"""
        selected_items = self.projects_table.selection()
        if selected_items:
            self.view_project_details_by_selection(selected_items[0])
    
    def view_selected_project(self):
        """View details of selected project"""
        selected_items = self.projects_table.selection()
        if selected_items:
            self.view_project_details_by_selection(selected_items[0])
        else:
            messagebox.showinfo("No Selection", "Please select a project to view")
    
    def view_project_details_by_selection(self, selected_item):
        """View details of selected project"""
        # Get values from selected item
        values = self.projects_table.item(selected_item, 'values')
        project_name = values[0]
        
        # Find project in list
        project = None
        for p in self.projects:
            if p.get("name") == project_name:
                project = p
                break
        
        if project:
            self.current_project = project
            self.show_project_dashboard(project)
        else:
            messagebox.showerror("Error", f"Project '{project_name}' not found")
    
    def edit_selected_project(self):
        """Edit selected project"""
        selected_items = self.projects_table.selection()
        if selected_items:
            # Get values from selected item
            values = self.projects_table.item(selected_items[0], 'values')
            project_name = values[0]
            
            # Find project in list
            project = None
            for p in self.projects:
                if p.get("name") == project_name:
                    project = p
                    break
            
            if project:
                self.current_project = project
                self.show_edit_project(project)
            else:
                messagebox.showerror("Error", f"Project '{project_name}' not found")
        else:
            messagebox.showinfo("No Selection", "Please select a project to edit")
    
    def delete_selected_project(self):
        """Delete selected project"""
        selected_items = self.projects_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a project to delete")
            return
            
        # Get values from selected item
        values = self.projects_table.item(selected_items[0], 'values')
        project_name = values[0]
        
        # Find project in list
        project = None
        for p in self.projects:
            if p.get("name") == project_name:
                project = p
                break
        
        if not project:
            messagebox.showerror("Error", f"Project '{project_name}' not found")
            return
            
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the project '{project_name}'?\nThis action cannot be undone."):
            return
            
        # Delete from database if available
        if self.db_manager and self.db_manager.is_connected():
            success = self.db_manager.delete_project(project.get("id"))
            if not success:
                messagebox.showerror("Error", f"Failed to delete project '{project_name}'")
                return
        else:
            # Remove from local list
            self.projects.remove(project)
            self.save_projects_to_json()
        
        # Refresh the view
        messagebox.showinfo("Success", f"Project '{project_name}' has been deleted")
        self.show_current_projects()
    
    def show_project_dashboard(self, project):
        """Show the project dashboard view"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create header
        self.create_view_header(project.get("name"), f"Client: {project.get('client')}")
        
        # Main content area with tabs
        tab_control = ttk.Notebook(self.parent_frame)
        tab_control.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        overview_tab = ttk.Frame(tab_control)
        tasks_tab = ttk.Frame(tab_control)
        resources_tab = ttk.Frame(tab_control)
        timeline_tab = ttk.Frame(tab_control)
        documents_tab = ttk.Frame(tab_control)
        
        tab_control.add(overview_tab, text="Overview")
        tab_control.add(tasks_tab, text="Tasks")
        tab_control.add(resources_tab, text="Resources")
        tab_control.add(timeline_tab, text="Timeline")
        tab_control.add(documents_tab, text="Documents")
        
        # Populate tabs
        self.populate_overview_tab(overview_tab, project)
        self.populate_tasks_tab(tasks_tab, project)
        self.populate_resources_tab(resources_tab, project)
        self.populate_timeline_tab(timeline_tab, project)
        self.populate_documents_tab(documents_tab, project)
        
        # Bottom navigation
        navigation_frame = ttk.Frame(self.parent_frame)
        navigation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            navigation_frame, 
            text="Back to Projects",
            command=self.show_current_projects
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            navigation_frame, 
            text="Edit Project",
            command=lambda: self.show_edit_project(project)
        ).pack(side=tk.RIGHT)
    
    def populate_overview_tab(self, parent, project):
        """Populate the overview tab of the project dashboard"""
        # Project info container with two columns
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column - Project details
        left_col = ttk.Frame(container)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Project details card
        details_frame = ttk.LabelFrame(left_col, text="Project Details")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Create a grid for details
        details_grid = ttk.Frame(details_frame)
        details_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Row 1
        ttk.Label(details_grid, text="Project Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=project.get("name", "")).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_grid, text="Client:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=project.get("client", "")).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Row 2
        ttk.Label(details_grid, text="Type:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=project.get("type", "")).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_grid, text="Status:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        status_label = ttk.Label(details_grid, text=project.get("status", ""))
        status_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Style status label by status
        status = project.get("status", "").lower()
        if status == "on track":
            status_label.configure(foreground=self.colors["success"])
        elif status == "at risk":
            status_label.configure(foreground=self.colors["warning"])
        elif status == "delayed":
            status_label.configure(foreground=self.colors["danger"])
        elif status == "completed":
            status_label.configure(foreground=self.colors["secondary"])
        
        # Row 3
        ttk.Label(details_grid, text="Start Date:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=project.get("start_date", "")).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_grid, text="End Date:", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=project.get("end_date", "")).grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Row 4
        ttk.Label(details_grid, text="Progress:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Progress frame with progress bar
        progress_frame = ttk.Frame(details_grid)
        progress_frame.grid(row=3, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        progress_value = project.get("progress", 0)
        progress_bar = ttk.Progressbar(progress_frame, length=200, value=progress_value)
        progress_bar.pack(side=tk.LEFT)
        
        ttk.Label(progress_frame, text=f"{progress_value}%").pack(side=tk.LEFT, padx=5)
        
        # Description
        ttk.Label(details_grid, text="Description:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.NW, padx=5, pady=5)
        description_text = tk.Text(details_grid, height=4, width=40, wrap=tk.WORD)
        description_text.grid(row=4, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
        description_text.insert(tk.END, project.get("description", ""))
        description_text.config(state=tk.DISABLED)
        
        # Project Components
        components_frame = ttk.LabelFrame(left_col, text="Project Components")
        components_frame.pack(fill=tk.X, pady=10)
        
        # Get components if available
        components = project.get("components", [])
        if components:
            for comp in components:
                comp_frame = ttk.Frame(components_frame)
                comp_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Status indicator
                status_color = "green" if comp.get("status") == "On Track" else "orange" if comp.get("status") == "At Risk" else "red" if comp.get("status") == "Delayed" else "blue" if comp.get("status") == "Completed" else "gray"
                status_indicator = tk.Label(comp_frame, text="•", foreground=status_color, font=("Arial", 16))
                status_indicator.pack(side=tk.LEFT)
                
                # Component name and type
                ttk.Label(comp_frame, text=comp.get("name", ""), font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
                ttk.Label(comp_frame, text=f"({comp.get('type', 'Standard')})", font=("Arial", 8)).pack(side=tk.LEFT)
                
                # Status
                ttk.Label(comp_frame, text=comp.get("status", "Not Started")).pack(side=tk.RIGHT)
        else:
            ttk.Label(components_frame, text="No components defined for this project").pack(padx=10, pady=10)
        
        # Right column - Statistics, milestones and team
        right_col = ttk.Frame(container)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Project Statistics card
        stats_frame = ttk.LabelFrame(right_col, text="Project Statistics")
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Load tasks and resources if database available
        tasks = []
        team_members = []
        milestones = []
        
        if self.db_manager and self.db_manager.is_connected():
            tasks = self.db_manager.get_tasks_by_project(project.get("id", -1))
            team_members = self.db_manager.get_resources_by_project(project.get("id", -1))
            milestones = self.db_manager.get_milestones_by_project(project.get("id", -1))
        
        # Calculate stats
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.get("status") == "Completed")
        total_team = len(team_members)
        
        # Upcoming milestones
        upcoming_milestones = []
        for m in milestones:
            if m.get("status") != "Completed":
                upcoming_milestones.append(m)
        
        # Row 1
        ttk.Label(stats_grid, text="Total Tasks:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(total_tasks)).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Completed Tasks:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=f"{completed_tasks} ({int(completed_tasks/total_tasks*100) if total_tasks else 0}%)").grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Row 2
        ttk.Label(stats_grid, text="Team Size:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(total_team)).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Upcoming Milestones:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=str(len(upcoming_milestones))).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Upcoming Milestones
        milestones_frame = ttk.LabelFrame(right_col, text="Upcoming Milestones")
        milestones_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        if upcoming_milestones:
            for milestone in upcoming_milestones[:3]:  # Show top 3
                item_frame = ttk.Frame(milestones_frame)
                item_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Status indicator
                status_color = "green" if milestone.get("status") == "On Track" else "orange" if milestone.get("status") == "At Risk" else "red"
                status_indicator = tk.Label(item_frame, text="•", foreground=status_color, font=("Arial", 16))
                status_indicator.pack(side=tk.LEFT)
                
                # Milestone info
                info_frame = ttk.Frame(item_frame)
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                
                ttk.Label(info_frame, text=milestone.get("title", ""), font=("Arial", 10, "bold")).pack(anchor=tk.W)
                ttk.Label(info_frame, text=f"Due: {milestone.get('due_date', '')}", font=("Arial", 8)).pack(anchor=tk.W)
                
                # Status text
                ttk.Label(item_frame, text=milestone.get("status", "")).pack(side=tk.RIGHT)
            
            if len(upcoming_milestones) > 3:
                ttk.Label(milestones_frame, text=f"+ {len(upcoming_milestones) - 3} more milestones", foreground="blue").pack(anchor=tk.E, padx=10, pady=5)
        else:
            ttk.Label(milestones_frame, text="No upcoming milestones").pack(padx=10, pady=10)
        
        # Team Members
        team_frame = ttk.LabelFrame(right_col, text="Core Team Members")
        team_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        if team_members:
            for member in team_members[:5]:  # Show top 5
                member_frame = ttk.Frame(team_frame)
                member_frame.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Label(member_frame, text=member.get("name", ""), font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                ttk.Label(member_frame, text=f"({member.get('project_role', '')})", font=("Arial", 8)).pack(side=tk.LEFT, padx=5)
                ttk.Label(member_frame, text=f"{member.get('allocation', 100)}%", foreground="blue").pack(side=tk.RIGHT)
            
            if len(team_members) > 5:
                ttk.Label(team_frame, text=f"+ {len(team_members) - 5} more team members", foreground="blue").pack(anchor=tk.E, padx=10, pady=5)
        else:
            ttk.Label(team_frame, text="No team members assigned").pack(padx=10, pady=10)
    
    def populate_tasks_tab(self, parent, project):
        """Populate the tasks tab of the project dashboard"""
        # Create control frame with buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Add Task",
            command=lambda: self.show_add_task_form(project)
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_tasks_tab(parent, project)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter controls
        ttk.Label(control_frame, text="Status:").pack(side=tk.LEFT, padx=10)
        status_filter = ttk.Combobox(control_frame, values=["All", "Not Started", "In Progress", "On Hold", "Completed"], width=12)
        status_filter.current(0)
        status_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Assigned To:").pack(side=tk.LEFT, padx=10)
        assigned_filter = ttk.Combobox(control_frame, values=["All", "Unassigned"], width=15)
        assigned_filter.current(0)
        assigned_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Filter",
            command=lambda: self.apply_task_filters(status_filter.get(), assigned_filter.get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Task table
        columns = ("Task", "Status", "Priority", "Start Date", "Due Date", "Assigned To", "Progress")
        self.tasks_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.tasks_table.heading(col, text=col)
            width = 100
            if col == "Task":
                width = 200
            self.tasks_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tasks_table.yview)
        self.tasks_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_table.pack(fill=tk.BOTH, expand=True)
        
        # Context menu for tasks
        self.create_task_context_menu(project)
        
        # Bind double-click event
        self.tasks_table.bind("<Double-1>", lambda e: self.view_task_details())
        
        # Load tasks
        self.load_project_tasks(project)
    
    def load_project_tasks(self, project):
        """Load tasks for a project into the tasks table"""
        # Clear existing items
        for item in self.tasks_table.get_children():
            self.tasks_table.delete(item)
        
        # Get tasks from database if available
        tasks = []
        if self.db_manager and self.db_manager.is_connected():
            tasks = self.db_manager.get_tasks_by_project(project.get("id", -1))
        
        # Process tasks and add to table
        for task in tasks:
            # Get assigned resources
            assigned_to = "Unassigned"
            if self.db_manager and self.db_manager.is_connected() and task.get("assigned_resources"):
                # Fetch resource names
                resources = []
                for resource_id in task.get("assigned_resources", []):
                    # This is inefficient but works for now. In a real app, we'd batch this.
                    project_resources = self.db_manager.get_resources_by_project(project.get("id", -1))
                    for resource in project_resources:
                        if resource.get("id") == resource_id:
                            resources.append(resource.get("name"))
                            break
                
                if resources:
                    assigned_to = ", ".join(resources)
            
            # Calculate progress
            progress = "0%"
            if task.get("status") == "Completed":
                progress = "100%"
            elif task.get("status") == "In Progress":
                progress = "50%"  # Simplified for demo
            
            values = (
                task.get("title", ""),
                task.get("status", "Not Started"),
                task.get("priority", "Medium"),
                task.get("start_date", ""),
                task.get("due_date", ""),
                assigned_to,
                progress
            )
            
            # Set tag based on status for color coding
            tag = task.get("status", "").lower().replace(" ", "_")
            self.tasks_table.insert("", tk.END, values=values, tags=(tag,))
        
        # Configure tags for color coding
        self.tasks_table.tag_configure("not_started", background="#f8f9fa")
        self.tasks_table.tag_configure("in_progress", background="#e6f2ff")
        self.tasks_table.tag_configure("on_hold", background="#fff3cd")
        self.tasks_table.tag_configure("completed", background="#d4edda")
    
    def create_task_context_menu(self, project):
        """Create context menu for tasks table"""
        self.task_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.task_menu.add_command(label="View Task Details", command=self.view_task_details)
        self.task_menu.add_command(label="Edit Task", command=self.edit_task)
        self.task_menu.add_separator()
        
        # Status submenu
        status_menu = tk.Menu(self.task_menu, tearoff=0)
        status_menu.add_command(label="Not Started", command=lambda: self.update_task_status("Not Started"))
        status_menu.add_command(label="In Progress", command=lambda: self.update_task_status("In Progress"))
        status_menu.add_command(label="On Hold", command=lambda: self.update_task_status("On Hold"))
        status_menu.add_command(label="Completed", command=lambda: self.update_task_status("Completed"))
        self.task_menu.add_cascade(label="Update Status", menu=status_menu)
        
        self.task_menu.add_separator()
        self.task_menu.add_command(label="Delete Task", command=self.delete_task)
        
        # Bind right-click event
        self.tasks_table.bind("<Button-3>", self.show_task_menu)
    
    def show_task_menu(self, event):
        """Show context menu on right-click"""
        # Select row under mouse
        iid = self.tasks_table.identify_row(event.y)
        if iid:
            # Select the item
            self.tasks_table.selection_set(iid)
            
            # Show menu
            try:
                self.task_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.task_menu.grab_release()
    
    def view_task_details(self):
        """View details of selected task"""
        selected_items = self.tasks_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a task to view")
            return
        
        # Get task title from selected item
        values = self.tasks_table.item(selected_items[0], 'values')
        task_title = values[0]
        
        # This is a simplified implementation - in a real app, we'd use the task ID
        messagebox.showinfo("Task Details", f"Details for task: {task_title}\n\nThis would show the full task details.")
    
    def edit_task(self):
        """Edit selected task"""
        selected_items = self.tasks_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a task to edit")
            return
        
        # Get task title from selected item
        values = self.tasks_table.item(selected_items[0], 'values')
        task_title = values[0]
        
        # This is a simplified implementation - in a real app, we'd open a form to edit the task
        messagebox.showinfo("Edit Task", f"Editing task: {task_title}\n\nThis would open a form to edit the task.")
    
    def update_task_status(self, status):
        """Update status of selected task"""
        selected_items = self.tasks_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a task to update")
            return
        
        # Get task title from selected item
        values = self.tasks_table.item(selected_items[0], 'values')
        task_title = values[0]
        
        # This is a simplified implementation - in a real app, we'd update the database
        messagebox.showinfo("Update Task Status", f"Status of task '{task_title}' updated to: {status}")
    
    def delete_task(self):
        """Delete selected task"""
        selected_items = self.tasks_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a task to delete")
            return
        
        # Get task title from selected item
        values = self.tasks_table.item(selected_items[0], 'values')
        task_title = values[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the task '{task_title}'?\nThis action cannot be undone."):
            return
        
        # This is a simplified implementation - in a real app, we'd delete from the database
        messagebox.showinfo("Task Deleted", f"Task '{task_title}' has been deleted")
    
    def refresh_tasks_tab(self, parent, project):
        """Refresh the tasks tab"""
        self.load_project_tasks(project)
    
    def apply_task_filters(self, status_filter, assigned_filter):
        """Apply filters to tasks table"""
        # This is a simplified implementation - in a real app, we'd filter the tasks
        messagebox.showinfo("Apply Filters", f"Filtering tasks by Status: {status_filter}, Assigned To: {assigned_filter}")
    
    def show_add_task_form(self, project):
        """Show form to add a new task"""
        # This is a placeholder - in a real app, we'd show a form
        messagebox.showinfo("Add Task", "This would open a form to add a new task to the project")
    
    def populate_resources_tab(self, parent, project):
        """Populate the resources tab of the project dashboard"""
        # Create control frame with buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Assign Resource",
            command=lambda: self.show_assign_resource_form(project)
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_resources_tab(parent, project)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resources table
        columns = ("Name", "Role", "Email", "Allocation", "Start Date", "End Date")
        self.resources_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.resources_table.heading(col, text=col)
            width = 100
            if col in ["Name", "Email"]:
                width = 150
            self.resources_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.resources_table.yview)
        self.resources_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resources_table.pack(fill=tk.BOTH, expand=True)
        
        # Context menu for resources
        self.create_resource_context_menu(project)
        
        # Load resources
        self.load_project_resources(project)
    
    def load_project_resources(self, project):
        """Load resources for a project into the resources table"""
        # Clear existing items
        for item in self.resources_table.get_children():
            self.resources_table.delete(item)
        
        # Get resources from database if available
        resources = []
        if self.db_manager and self.db_manager.is_connected():
            resources = self.db_manager.get_resources_by_project(project.get("id", -1))
        
        # Add resources to table
        for resource in resources:
            values = (
                resource.get("name", ""),
                resource.get("project_role", ""),
                resource.get("email", ""),
                f"{resource.get('allocation', 100)}%",
                resource.get("start_date", ""),
                resource.get("end_date", "")
            )
            
            self.resources_table.insert("", tk.END, values=values)
    
    def create_resource_context_menu(self, project):
        """Create context menu for resources table"""
        self.resource_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.resource_menu.add_command(label="View Resource Details", command=self.view_resource_details)
        self.resource_menu.add_command(label="Edit Assignment", command=self.edit_resource_assignment)
        self.resource_menu.add_separator()
        self.resource_menu.add_command(label="Remove Assignment", command=self.remove_resource_assignment)
        
        # Bind right-click event
        self.resources_table.bind("<Button-3>", self.show_resource_menu)
    
    def show_resource_menu(self, event):
        """Show context menu on right-click"""
        # Select row under mouse
        iid = self.resources_table.identify_row(event.y)
        if iid:
            # Select the item
            self.resources_table.selection_set(iid)
            
            # Show menu
            try:
                self.resource_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.resource_menu.grab_release()
    
    def view_resource_details(self):
        """View details of selected resource"""
        selected_items = self.resources_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a resource to view")
            return
        
        # Get resource name from selected item
        values = self.resources_table.item(selected_items[0], 'values')
        resource_name = values[0]
        
        # This is a simplified implementation - in a real app, we'd show resource details
        messagebox.showinfo("Resource Details", f"Details for resource: {resource_name}\n\nThis would show the full resource details.")
    
    def edit_resource_assignment(self):
        """Edit assignment of selected resource"""
        selected_items = self.resources_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a resource to edit")
            return
        
        # Get resource name from selected item
        values = self.resources_table.item(selected_items[0], 'values')
        resource_name = values[0]
        
        # This is a simplified implementation - in a real app, we'd open a form to edit the assignment
        messagebox.showinfo("Edit Assignment", f"Editing assignment for: {resource_name}\n\nThis would open a form to edit the assignment.")
    
    def remove_resource_assignment(self):
        """Remove assignment of selected resource"""
        selected_items = self.resources_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a resource to remove")
            return
        
        # Get resource name from selected item
        values = self.resources_table.item(selected_items[0], 'values')
        resource_name = values[0]
        
        # Confirm removal
        if not messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove {resource_name} from this project?"):
            return
        
        # This is a simplified implementation - in a real app, we'd remove from the database
        messagebox.showinfo("Resource Removed", f"{resource_name} has been removed from the project")
    
    def refresh_resources_tab(self, parent, project):
        """Refresh the resources tab"""
        self.load_project_resources(project)
    
    def show_assign_resource_form(self, project):
        """Show form to assign a resource to the project"""
        # This is a placeholder - in a real app, we'd show a form
        messagebox.showinfo("Assign Resource", "This would open a form to assign a resource to the project")
    
    def populate_timeline_tab(self, parent, project):
        """Populate the timeline tab of the project dashboard with a Gantt chart"""
        # Create control frame with buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Add Milestone",
            command=lambda: self.show_add_milestone_form(project)
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_timeline_tab(parent, project)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # View controls
        ttk.Label(control_frame, text="View:").pack(side=tk.LEFT, padx=10)
        view_options = ttk.Combobox(control_frame, values=["Gantt Chart", "Calendar View", "Task Dependencies"], width=15)
        view_options.current(0)
        view_options.pack(side=tk.LEFT, padx=5)
        
        # This is a simplified timeline view - just basic description and placeholders
        timeline_frame = ttk.Frame(parent)
        timeline_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(timeline_frame, text="Project Timeline", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(timeline_frame, text="A Gantt chart visualization would be shown here.").pack(pady=10)
        ttk.Label(timeline_frame, text="This would show tasks, milestones, and timelines in a Gantt chart view.").pack()
        
        # Create placeholder for Gantt chart
        canvas = tk.Canvas(timeline_frame, background="white", height=300)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a simple placeholder timeline
        # In a real app, we'd draw a proper Gantt chart
        canvas.create_text(200, 30, text="Timeline Visualization (Placeholder)", font=("Arial", 12, "bold"))
        
        # Draw timeline
        canvas.create_line(50, 70, 550, 70, width=2)
        
        # Draw time markers
        for i in range(6):
            x = 50 + i * 100
            canvas.create_line(x, 65, x, 75, width=1)
            canvas.create_text(x, 85, text=f"Week {i+1}")
        
        # Draw some sample tasks
        y_pos = 120
        colors = ["#4e73df", "#1cc88a", "#f6c23e", "#e74a3b"]
        
        for i in range(4):
            # Randomize task position and length
            start_week = i % 3
            duration = 2 + i % 3
            
            task_name = f"Task {i+1}"
            if i == 0:
                task_name = "Project Setup"
            elif i == 1:
                task_name = "Development"
            elif i == 2:
                task_name = "Testing"
            elif i == 3:
                task_name = "Deployment"
            
            # Draw task bar
            start_x = 50 + start_week * 100
            end_x = start_x + duration * 100
            canvas.create_rectangle(start_x, y_pos-10, end_x, y_pos+10, fill=colors[i], outline="")
            canvas.create_text(start_x - 10, y_pos, text=task_name, anchor="e")
            
            y_pos += 40
        
        # Draw milestone markers
        canvas.create_polygon(250, 200, 260, 190, 270, 200, 260, 210, fill="red")
        canvas.create_text(270, 200, text="Milestone 1", anchor="w")
        
        canvas.create_polygon(450, 200, 460, 190, 470, 200, 460, 210, fill="red")
        canvas.create_text(470, 200, text="Milestone 2", anchor="w")
    
    def show_add_milestone_form(self, project):
        """Show form to add a milestone to the project"""
        # This is a placeholder - in a real app, we'd show a form
        messagebox.showinfo("Add Milestone", "This would open a form to add a milestone to the project")
    
    def refresh_timeline_tab(self, parent, project):
        """Refresh the timeline tab"""
        # This is a placeholder - in a real app, we'd refresh the timeline
        messagebox.showinfo("Refresh Timeline", "Timeline would be refreshed with latest data")
    
    def populate_documents_tab(self, parent, project):
        """Populate the documents tab of the project dashboard"""
        # Create control frame with buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Upload Document",
            command=self.upload_document
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_documents_tab(parent, project)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Documents table
        columns = ("Document Name", "Type", "Size", "Uploaded By", "Upload Date", "Description")
        self.documents_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.documents_table.heading(col, text=col)
            width = 100
            if col == "Document Name" or col == "Description":
                width = 200
            self.documents_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.documents_table.yview)
        self.documents_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.documents_table.pack(fill=tk.BOTH, expand=True)
        
        # Add placeholder documents
        # In a real app, we'd load documents from the database
        self.documents_table.insert("", tk.END, values=("Project Charter.docx", "Word Document", "25 KB", "John Doe", "2023-01-15", "Project charter document"))
        self.documents_table.insert("", tk.END, values=("Requirements Spec.pdf", "PDF Document", "150 KB", "Jane Smith", "2023-01-20", "Detailed requirements specification"))
        self.documents_table.insert("", tk.END, values=("Project Plan.xlsx", "Excel Spreadsheet", "75 KB", "Michael Johnson", "2023-01-25", "Project plan with timeline"))
    
    def upload_document(self):
        """Upload a document to the project"""
        # This is a placeholder - in a real app, we'd show a file dialog and upload
        messagebox.showinfo("Upload Document", "This would open a dialog to select and upload a document")
    
    def refresh_documents_tab(self, parent, project):
        """Refresh the documents tab"""
        # This is a placeholder - in a real app, we'd refresh the documents list
        messagebox.showinfo("Refresh Documents", "Documents list would be refreshed with latest data")
    
    def show_new_project(self):
        """Display the new project form"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create header
        self.create_view_header("Create New Project", "Set up a new project with all required details")
        
        # Create a notebook for project setup steps
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        details_tab = ttk.Frame(notebook)
        components_tab = ttk.Frame(notebook)
        team_tab = ttk.Frame(notebook)
        timeline_tab = ttk.Frame(notebook)
        
        notebook.add(details_tab, text="Project Details")
        notebook.add(components_tab, text="Project Components")
        notebook.add(team_tab, text="Team Assignment")
        notebook.add(timeline_tab, text="Timeline & Milestones")
        
        # Setup each tab
        self.setup_details_tab(details_tab)
        self.setup_components_tab(components_tab)
        self.setup_team_tab(team_tab)
        self.setup_timeline_tab(timeline_tab)
        
        # Bottom buttons
        button_frame = ttk.Frame(self.parent_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=self.show_current_projects
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Save as Draft"
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Create Project", 
            style='Accent.TButton', 
            command=self.create_project
        ).pack(side=tk.RIGHT, padx=5)
    
    def setup_details_tab(self, parent):
        """Setup the project details tab"""
        # Create a form for project details
        form_frame = ttk.Frame(parent, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Project name
        ttk.Label(form_frame, text="Project Name *", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.project_name_entry = ttk.Entry(form_frame, width=40)
        self.project_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Client name
        ttk.Label(form_frame, text="Client *", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_entry = ttk.Entry(form_frame, width=40)
        self.client_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Project type
        ttk.Label(form_frame, text="Project Type *", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.project_type = ttk.Combobox(form_frame, values=["Implementation", "Assessment", "Migration", "Optimization", "Support"], width=20)
        self.project_type.current(0)
        self.project_type.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Start date
        ttk.Label(form_frame, text="Start Date *", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        start_date_frame = ttk.Frame(form_frame)
        start_date_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.start_year = ttk.Combobox(start_date_frame, values=[str(i) for i in range(2024, 2030)], width=5)
        self.start_year.current(0)
        self.start_year.pack(side=tk.LEFT, padx=2)
        
        self.start_month = ttk.Combobox(start_date_frame, values=[f"{i:02d}" for i in range(1, 13)], width=3)
        self.start_month.current(0)
        self.start_month.pack(side=tk.LEFT, padx=2)
        
        self.start_day = ttk.Combobox(start_date_frame, values=[f"{i:02d}" for i in range(1, 32)], width=3)
        self.start_day.current(0)
        self.start_day.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(start_date_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT, padx=5)
        
        # End date
        ttk.Label(form_frame, text="End Date *", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        end_date_frame = ttk.Frame(form_frame)
        end_date_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.end_year = ttk.Combobox(end_date_frame, values=[str(i) for i in range(2024, 2030)], width=5)
        self.end_year.current(0)
        self.end_year.pack(side=tk.LEFT, padx=2)
        
        self.end_month = ttk.Combobox(end_date_frame, values=[f"{i:02d}" for i in range(1, 13)], width=3)
        self.end_month.current(2)  # Default to 3 months
        self.end_month.pack(side=tk.LEFT, padx=2)
        
        self.end_day = ttk.Combobox(end_date_frame, values=[f"{i:02d}" for i in range(1, 32)], width=3)
        self.end_day.current(0)
        self.end_day.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(end_date_frame, text="(YYYY-MM-DD)").pack(side=tk.LEFT, padx=5)
        
        # Status
        ttk.Label(form_frame, text="Initial Status", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.status = ttk.Combobox(form_frame, values=["Not Started", "On Track", "At Risk", "Delayed"], width=20)
        self.status.current(0)
        self.status.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.NW, padx=5, pady=5)
        self.description_text = tk.Text(form_frame, height=5, width=40)
        self.description_text.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Required fields note
        ttk.Label(form_frame, text="* Required fields", font=("Arial", 8, "italic")).grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(20, 5))
    
    def setup_components_tab(self, parent):
        """Setup the project components tab"""
        # Create a frame for components selection
        components_frame = ttk.Frame(parent, padding=20)
        components_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(components_frame, text="Select components for this project:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Create checkboxes for common components
        components = [
            "Requirements Gathering",
            "Analysis & Design",
            "Development",
            "Testing",
            "Deployment",
            "Training",
            "Post-Implementation Support"
        ]
        
        self.component_vars = {}
        
        for component in components:
            var = tk.BooleanVar(value=True)  # Default to selected
            self.component_vars[component] = var
            
            cb = ttk.Checkbutton(components_frame, text=component, variable=var)
            cb.pack(anchor=tk.W, pady=3)
        
        # Custom component section
        ttk.Separator(components_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        ttk.Label(components_frame, text="Add custom components:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        # Custom component entry
        custom_frame = ttk.Frame(components_frame)
        custom_frame.pack(fill=tk.X, pady=5)
        
        self.custom_component_entry = ttk.Entry(custom_frame, width=30)
        self.custom_component_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(custom_frame, text="Add Component").pack(side=tk.LEFT, padx=5)
        
        # Custom components list (placeholder)
        ttk.Label(components_frame, text="Custom components will appear here").pack(anchor=tk.W, pady=10)
    
    def setup_team_tab(self, parent):
        """Setup the team assignment tab"""
        # Create a frame for team assignment
        team_frame = ttk.Frame(parent, padding=20)
        team_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(team_frame, text="Assign team members to this project:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Two-column layout
        columns_frame = ttk.Frame(team_frame)
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Available resources
        left_col = ttk.LabelFrame(columns_frame, text="Available Resources")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(left_col)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search").pack(side=tk.LEFT, padx=5)
        
        # Resources list
        resources_frame = ttk.Frame(left_col)
        resources_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Resources listbox with scrollbar
        scrollbar = ttk.Scrollbar(resources_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.resources_listbox = tk.Listbox(resources_frame, height=10, width=30, yscrollcommand=scrollbar.set)
        self.resources_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.resources_listbox.yview)
        
        # Placeholder resources
        resources = ["John Doe", "Jane Smith", "Michael Johnson", "Sarah Williams", "Robert Brown"]
        for resource in resources:
            self.resources_listbox.insert(tk.END, resource)
        
        # Assignment controls
        controls_frame = ttk.Frame(columns_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(controls_frame, text="→").pack(pady=5)
        ttk.Button(controls_frame, text="←").pack(pady=5)
        
        # Right column - Assigned team
        right_col = ttk.LabelFrame(columns_frame, text="Assigned Team")
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Team table
        team_table_frame = ttk.Frame(right_col)
        team_table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("Name", "Role", "Allocation")
        self.team_table = ttk.Treeview(team_table_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            self.team_table.heading(col, text=col)
            self.team_table.column(col, width=80)
        
        # Add scrollbar
        scrollbar2 = ttk.Scrollbar(team_table_frame, orient=tk.VERTICAL, command=self.team_table.yview)
        self.team_table.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.team_table.pack(fill=tk.BOTH, expand=True)
        
        # Assignment details frame
        details_frame = ttk.LabelFrame(team_frame, text="Assignment Details")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Form grid for assignment details
        form_grid = ttk.Frame(details_frame)
        form_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Resource role
        ttk.Label(form_grid, text="Project Role:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        role_combobox = ttk.Combobox(form_grid, values=["Project Lead", "Business Analyst", "Developer", "Tester", "Consultant"], width=20)
        role_combobox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Allocation percentage
        ttk.Label(form_grid, text="Allocation (%):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        allocation_spinbox = ttk.Spinbox(form_grid, from_=10, to=100, increment=10, width=5)
        allocation_spinbox.set(100)
        allocation_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Assignment dates
        ttk.Label(form_grid, text="Start Date:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        start_entry = ttk.Entry(form_grid, width=12)
        start_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_grid, text="End Date:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        end_entry = ttk.Entry(form_grid, width=12)
        end_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Assignment button
        ttk.Button(details_frame, text="Update Assignment").pack(anchor=tk.E, padx=10, pady=10)
    
    def setup_timeline_tab(self, parent):
        """Setup the timeline tab"""
        # Create a frame for timeline setup
        timeline_frame = ttk.Frame(parent, padding=20)
        timeline_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(timeline_frame, text="Set up project timeline and milestones:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Timeline visualization (placeholder)
        timeline_viz = ttk.LabelFrame(timeline_frame, text="Project Timeline")
        timeline_viz.pack(fill=tk.X, pady=10)
        
        ttk.Label(timeline_viz, text="Timeline visualization will be shown here once the project is created").pack(pady=20)
        
        # Milestones section
        milestones_frame = ttk.LabelFrame(timeline_frame, text="Project Milestones")
        milestones_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add milestone controls
        add_frame = ttk.Frame(milestones_frame)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="Milestone Title:").pack(side=tk.LEFT, padx=5)
        milestone_entry = ttk.Entry(add_frame, width=30)
        milestone_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(add_frame, text="Due Date:").pack(side=tk.LEFT, padx=5)
        due_date_entry = ttk.Entry(add_frame, width=12)
        due_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(add_frame, text="Add Milestone").pack(side=tk.LEFT, padx=5)
        
        # Milestones list
        milestones_list_frame = ttk.Frame(milestones_frame)
        milestones_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Title", "Due Date", "Status")
        self.milestones_table = ttk.Treeview(milestones_list_frame, columns=columns, show="headings", height=5)
        
        # Configure columns
        for col in columns:
            self.milestones_table.heading(col, text=col)
            width = 150 if col == "Title" else 100
            self.milestones_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(milestones_list_frame, orient=tk.VERTICAL, command=self.milestones_table.yview)
        self.milestones_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.milestones_table.pack(fill=tk.BOTH, expand=True)
        
        # Add placeholder milestones
        self.milestones_table.insert("", tk.END, values=("Project Kickoff", "2023-03-01", "Not Started"))
        self.milestones_table.insert("", tk.END, values=("Requirements Sign-off", "2023-03-15", "Not Started"))
        self.milestones_table.insert("", tk.END, values=("Development Complete", "2023-04-15", "Not Started"))
        self.milestones_table.insert("", tk.END, values=("User Acceptance Testing", "2023-04-30", "Not Started"))
        self.milestones_table.insert("", tk.END, values=("Go-Live", "2023-05-15", "Not Started"))
    
    def create_project(self):
        """Create a new project based on form inputs"""
        # Validate required fields
        if not self.project_name_entry.get():
            messagebox.showerror("Validation Error", "Project Name is required")
            return
            
        if not self.client_entry.get():
            messagebox.showerror("Validation Error", "Client is required")
            return
        
        # Get start date and end date
        try:
            start_date = f"{self.start_year.get()}-{self.start_month.get()}-{self.start_day.get()}"
            end_date = f"{self.end_year.get()}-{self.end_month.get()}-{self.end_day.get()}"
        except Exception as e:
            messagebox.showerror("Validation Error", f"Invalid date format: {e}")
            return
        
        # Create project object
        project_data = {
            "name": self.project_name_entry.get(),
            "client": self.client_entry.get(),
            "type": self.project_type.get(),
            "start_date": start_date,
            "end_date": end_date,
            "status": self.status.get(),
            "progress": 0,
            "description": self.description_text.get("1.0", tk.END).strip()
        }
        
        # Get selected components
        components = []
        for component, var in self.component_vars.items():
            if var.get():
                components.append(component)
        
        project_data["components"] = components
        
        # Save to database if available
        if self.db_manager and self.db_manager.is_connected():
            project_id = self.db_manager.save_project(project_data)
            
            if project_id > 0:
                messagebox.showinfo("Success", f"Project '{project_data['name']}' has been created successfully")
                
                # Get the full project with ID
                project = self.db_manager.get_project_by_id(project_id)
                
                # Update UI and show project details
                self.current_project = project
                self.show_project_dashboard(project)
            else:
                messagebox.showerror("Error", "Failed to create project in database")
        else:
            # Add to local projects list
            project_data["id"] = len(self.projects) + 1
            self.projects.append(project_data)
            self.save_projects_to_json()
            
            messagebox.showinfo("Success", f"Project '{project_data['name']}' has been created successfully")
            
            # Update UI and show project details
            self.current_project = project_data
            self.show_project_dashboard(project_data)
    
    def show_view_project_tasks(self, project_id):
        """Show the tasks view for a project"""
        # Get project
        project = None
        if self.db_manager and self.db_manager.is_connected():
            project = self.db_manager.get_project_by_id(project_id)
        else:
            # Find in local list
            for p in self.projects:
                if p.get("id") == project_id:
                    project = p
                    break
        
        if not project:
            messagebox.showerror("Error", f"Project with ID {project_id} not found")
            return
        
        self.current_project = project
        self.show_project_dashboard(project)
        
        # Switch to tasks tab
        # In a real implementation, we'd need to keep a reference to the notebook widget
    
    def show_edit_project(self, project):
        """Show the edit project form"""
        # This is a simplified implementation - similar to new project but with prepopulated fields
        messagebox.showinfo("Edit Project", f"Editing project: {project.get('name')}\n\nThis would open a form to edit the project.")
    
    def view_project_tasks(self):
        """View tasks for selected project"""
        selected_items = self.projects_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a project to view tasks")
            return
        
        # Get project name from selected item
        values = self.projects_table.item(selected_items[0], 'values')
        project_name = values[0]
        
        # Find project in list
        project = None
        for p in self.projects:
            if p.get("name") == project_name:
                project = p
                break
        
        if project:
            self.current_project = project
            self.show_project_dashboard(project)
            
            # In a real implementation, we'd switch to the tasks tab
            messagebox.showinfo("View Tasks", f"Viewing tasks for project: {project_name}")
        else:
            messagebox.showerror("Error", f"Project '{project_name}' not found")
    
    def view_project_resources(self):
        """View resources for selected project"""
        selected_items = self.projects_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a project to view resources")
            return
        
        # Get project name from selected item
        values = self.projects_table.item(selected_items[0], 'values')
        project_name = values[0]
        
        # Find project in list
        project = None
        for p in self.projects:
            if p.get("name") == project_name:
                project = p
                break
        
        if project:
            self.current_project = project
            self.show_project_dashboard(project)
            
            # In a real implementation, we'd switch to the resources tab
            messagebox.showinfo("View Resources", f"Viewing resources for project: {project_name}")
        else:
            messagebox.showerror("Error", f"Project '{project_name}' not found")
    
    def view_project_timeline(self):
        """View timeline for selected project"""
        selected_items = self.projects_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a project to view timeline")
            return
        
        # Get project name from selected item
        values = self.projects_table.item(selected_items[0], 'values')
        project_name = values[0]
        
        # Find project in list
        project = None
        for p in self.projects:
            if p.get("name") == project_name:
                project = p
                break
        
        if project:
            self.current_project = project
            self.show_project_dashboard(project)
            
            # In a real implementation, we'd switch to the timeline tab
            messagebox.showinfo("View Timeline", f"Viewing timeline for project: {project_name}")
        else:
            messagebox.showerror("Error", f"Project '{project_name}' not found")