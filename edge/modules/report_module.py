import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any, Optional
import csv

# Configure logger
logger = logging.getLogger("report_module")

class ReportModule:
    """Reporting module for the KPMG Edge application"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        self.projects = []
        self.resources = []
        self.tasks = []
        
        # Load data if database not available
        if self.db_manager is None or not self.db_manager.is_connected():
            self.load_from_json()
    
    def load_from_json(self):
        """Load data from JSON files (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
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
            
            # Load tasks
            if os.path.exists("data/tasks.json"):
                with open("data/tasks.json", "r") as f:
                    self.tasks = json.load(f)
                    logger.info(f"Loaded {len(self.tasks)} tasks from JSON file")
        except Exception as e:
            logger.error(f"Error loading data from JSON: {e}")
            self.projects = []
            self.resources = []
            self.tasks = []
    
    def show_reports_dashboard(self):
        """Show the reports dashboard view"""
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
        self.create_view_header("Reports & Analytics", "Generate reports and visualize project data")
        
        # Create main notebook for report views
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        project_status_tab = ttk.Frame(notebook)
        resource_allocation_tab = ttk.Frame(notebook)
        task_completion_tab = ttk.Frame(notebook)
        custom_reports_tab = ttk.Frame(notebook)
        
        notebook.add(project_status_tab, text="Project Status")
        notebook.add(resource_allocation_tab, text="Resource Allocation")
        notebook.add(task_completion_tab, text="Task Completion")
        notebook.add(custom_reports_tab, text="Custom Reports")
        
        # Setup each tab
        self.setup_project_status_tab(project_status_tab)
        self.setup_resource_allocation_tab(resource_allocation_tab)
        self.setup_task_completion_tab(task_completion_tab)
        self.setup_custom_reports_tab(custom_reports_tab)
        
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
    
    def setup_project_status_tab(self, parent):
        """Setup the project status report tab"""
        # Create control frame with export options
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_project_status(parent)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to CSV",
            command=self.export_project_status_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to PDF",
            command=self.export_project_status_pdf
        ).pack(side=tk.LEFT, padx=5)
        
        # Create summary cards
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Calculate summary statistics
        total_projects = len(self.projects)
        completed_projects = sum(1 for p in self.projects if p.get("status") == "Completed")
        on_track_projects = sum(1 for p in self.projects if p.get("status") == "On Track")
        at_risk_projects = sum(1 for p in self.projects if p.get("status") == "At Risk")
        delayed_projects = sum(1 for p in self.projects if p.get("status") == "Delayed")
        
        # Create summary cards
        self.create_summary_card(summary_frame, "Total Projects", total_projects, self.colors["primary"])
        self.create_summary_card(summary_frame, "Completed", completed_projects, self.colors["secondary"])
        self.create_summary_card(summary_frame, "On Track", on_track_projects, self.colors["success"])
        self.create_summary_card(summary_frame, "At Risk", at_risk_projects, self.colors["warning"])
        self.create_summary_card(summary_frame, "Delayed", delayed_projects, self.colors["danger"])
        
        # Progress overview visualization
        progress_frame = ttk.LabelFrame(parent, text="Project Progress Overview")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas for progress visualization
        canvas = tk.Canvas(progress_frame, background="white", height=300)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a simple bar chart
        canvas.create_text(300, 30, text="Project Progress Overview", font=("Arial", 14, "bold"))
        
        # Calculate positions
        bar_width = 20
        spacing = 40
        x_start = 100
        y_bottom = 250
        
        # Sort projects by progress
        sorted_projects = sorted(self.projects, key=lambda p: p.get("progress", 0))
        
        # Draw progress bars
        for i, project in enumerate(sorted_projects):
            x = x_start + i * spacing
            progress = project.get("progress", 0)
            
            # Determine color based on status
            status = project.get("status", "")
            if status == "Completed":
                color = self.colors["secondary"]
            elif status == "On Track":
                color = self.colors["success"]
            elif status == "At Risk":
                color = self.colors["warning"]
            elif status == "Delayed":
                color = self.colors["danger"]
            else:
                color = self.colors["primary"]
            
            # Draw progress bar
            bar_height = progress * 2  # Scale for better visibility
            canvas.create_rectangle(
                x, y_bottom - bar_height,
                x + bar_width, y_bottom,
                fill=color, outline=""
            )
            
            # Add project name (rotated)
            canvas.create_text(
                x + bar_width/2, y_bottom + 10,
                text=project.get("name", ""),
                angle=90,
                anchor=tk.W,
                font=("Arial", 8)
            )
            
            # Add progress label
            canvas.create_text(
                x + bar_width/2, y_bottom - bar_height - 10,
                text=f"{progress}%",
                anchor=tk.S,
                font=("Arial", 8, "bold")
            )
        
        # Draw axes
        canvas.create_line(50, 50, 50, y_bottom, width=2)  # Y-axis
        canvas.create_line(50, y_bottom, 750, y_bottom, width=2)  # X-axis
        
        # Y-axis labels
        for i in range(0, 101, 20):
            y = y_bottom - i * 2
            canvas.create_line(45, y, 50, y, width=1)
            canvas.create_text(40, y, text=f"{i}%", anchor=tk.E)
        
        # Project status table
        table_frame = ttk.LabelFrame(parent, text="Project Status Details")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create project status table
        columns = ("Project", "Client", "Start Date", "End Date", "Status", "Progress", "Days Remaining")
        self.status_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.status_table.heading(col, text=col)
            width = 100
            if col in ["Project", "Client"]:
                width = 150
            self.status_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.status_table.yview)
        self.status_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load project status data
        self.load_project_status_data()
    
    def create_summary_card(self, parent, title, value, color):
        """Create a summary card widget"""
        card = ttk.Frame(parent, padding=10)
        card.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        ttk.Label(card, text=title, font=("Arial", 10)).pack(anchor=tk.CENTER)
        ttk.Label(card, text=str(value), font=("Arial", 24, "bold"), foreground=color).pack(anchor=tk.CENTER, pady=5)
    
    def load_project_status_data(self):
        """Load project status data into the table"""
        # Clear existing items
        for item in self.status_table.get_children():
            self.status_table.delete(item)
        
        # Current date for comparison
        today = datetime.now().date()
        
        # Add projects to table
        for project in self.projects:
            # Calculate days remaining
            days_remaining = "N/A"
            try:
                end_date = datetime.strptime(project.get("end_date", ""), "%Y-%m-%d").date()
                if end_date >= today:
                    days_remaining = (end_date - today).days
            except ValueError:
                pass
            
            values = (
                project.get("name", ""),
                project.get("client", ""),
                project.get("start_date", ""),
                project.get("end_date", ""),
                project.get("status", ""),
                f"{project.get('progress', 0)}%",
                str(days_remaining)
            )
            
            # Set tag based on status for color coding
            tag = project.get("status", "").lower().replace(" ", "_")
            self.status_table.insert("", tk.END, values=values, tags=(tag,))
        
        # Configure tags for color coding
        self.status_table.tag_configure("on_track", background="#d4edda")
        self.status_table.tag_configure("at_risk", background="#fff3cd")
        self.status_table.tag_configure("delayed", background="#f8d7da")
        self.status_table.tag_configure("completed", background="#d1ecf1")
    
    def refresh_project_status(self, parent):
        """Refresh the project status report"""
        # Reload data from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.projects = self.db_manager.get_all_projects()
        
        # Reload project status data
        self.load_project_status_data()
        
        # Recreate the charts (in a real application, we'd update them dynamically)
        messagebox.showinfo("Refresh", "Charts and visualizations would be refreshed")
    
    def export_project_status_csv(self):
        """Export project status data to CSV"""
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Project Status Report"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Project", "Client", "Start Date", "End Date", "Status", "Progress", "Days Remaining"])
                
                # Current date for comparison
                today = datetime.now().date()
                
                # Write data
                for project in self.projects:
                    # Calculate days remaining
                    days_remaining = "N/A"
                    try:
                        end_date = datetime.strptime(project.get("end_date", ""), "%Y-%m-%d").date()
                        if end_date >= today:
                            days_remaining = (end_date - today).days
                    except ValueError:
                        pass
                    
                    writer.writerow([
                        project.get("name", ""),
                        project.get("client", ""),
                        project.get("start_date", ""),
                        project.get("end_date", ""),
                        project.get("status", ""),
                        f"{project.get('progress', 0)}%",
                        str(days_remaining)
                    ])
            
            messagebox.showinfo("Export Successful", f"Project status report exported to:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting to CSV: {e}")
    
    def export_project_status_pdf(self):
        """Export project status data to PDF"""
        # In a real application, we'd use a PDF library like ReportLab
        messagebox.showinfo(
            "PDF Export", 
            "This would export the project status report to PDF including charts and tables.\n\n"
            "In a real application, this would be implemented using a PDF library like ReportLab."
        )
    
    def setup_resource_allocation_tab(self, parent):
        """Setup the resource allocation report tab"""
        # Create control frame with export options
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_resource_allocation(parent)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to CSV",
            command=self.export_resource_allocation_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to PDF",
            command=self.export_resource_allocation_pdf
        ).pack(side=tk.LEFT, padx=5)
        
        # Filter controls
        ttk.Label(control_frame, text="Filter by:").pack(side=tk.LEFT, padx=10)
        
        ttk.Label(control_frame, text="Role:").pack(side=tk.LEFT, padx=5)
        role_filter = ttk.Combobox(control_frame, values=["All", "Project Manager", "Developer", "Business Analyst", "Tester", "Consultant"], width=15)
        role_filter.current(0)
        role_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Apply",
            command=lambda: self.apply_resource_filters(role_filter.get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Create container for charts and tables
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column - allocation chart
        left_col = ttk.Frame(content_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Resource allocation chart
        chart_frame = ttk.LabelFrame(left_col, text="Resource Allocation")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a canvas for the chart
        canvas = tk.Canvas(chart_frame, background="white", height=300)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a simple stacked bar chart
        canvas.create_text(200, 30, text="Resource Allocation by Project", font=("Arial", 14, "bold"))
        
        # In a real application, we'd calculate actual allocations
        # For now, let's create sample data
        resources = ["John Doe", "Jane Smith", "Michael Johnson", "Sarah Williams", "Robert Brown"]
        projects = ["Project A", "Project B", "Project C", "Available"]
        colors = ["#4e73df", "#1cc88a", "#f6c23e", "#e0e0e0"]  # Colors for projects
        
        # Calculate positions
        bar_height = 30
        spacing = 20
        y_start = 70
        x_left = 150
        x_right = 450
        
        # Draw resource bars
        for i, resource in enumerate(resources):
            y = y_start + i * (bar_height + spacing)
            
            # Draw resource name
            canvas.create_text(x_left - 10, y + bar_height/2, text=resource, anchor=tk.E)
            
            # Draw allocation segments
            x_pos = x_left
            for j, project in enumerate(projects):
                # In a real app, we'd calculate actual width based on allocation percentage
                # For this demo, we'll use random widths
                if project == "Available":
                    # Make "Available" segment last and variable
                    continue
                
                # Width based on position in list (just for demo)
                width = (j + 1) * 40 if j < len(projects) - 2 else 30
                
                # Draw segment
                canvas.create_rectangle(
                    x_pos, y,
                    x_pos + width, y + bar_height,
                    fill=colors[j],
                    outline="white"
                )
                
                # If segment is wide enough, add label
                if width > 40:
                    canvas.create_text(
                        x_pos + width/2, y + bar_height/2,
                        text=project,
                        fill="white",
                        font=("Arial", 8)
                    )
                
                x_pos += width
            
            # Add "Available" segment to fill the rest
            if x_pos < x_right:
                canvas.create_rectangle(
                    x_pos, y,
                    x_right, y + bar_height,
                    fill=colors[3],
                    outline="white"
                )
                
                # Add "Available" label if space permits
                if x_right - x_pos > 50:
                    canvas.create_text(
                        x_pos + (x_right - x_pos)/2, y + bar_height/2,
                        text="Available",
                        font=("Arial", 8)
                    )
        
        # Draw legend
        legend_y = 250
        for i, project in enumerate(projects):
            # Calculate position
            x = 200 + i * 100
            
            # Draw color box
            canvas.create_rectangle(
                x, legend_y,
                x + 15, legend_y + 15,
                fill=colors[i],
                outline=""
            )
            
            # Draw project name
            canvas.create_text(
                x + 20, legend_y + 7,
                text=project,
                anchor=tk.W
            )
        
        # Right column - allocation details table
        right_col = ttk.Frame(content_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Resource allocation table
        table_frame = ttk.LabelFrame(right_col, text="Resource Allocation Details")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create allocation table
        columns = ("Resource", "Role", "Project", "Allocation", "Start Date", "End Date")
        self.allocation_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.allocation_table.heading(col, text=col)
            width = 100
            if col in ["Resource", "Project"]:
                width = 150
            self.allocation_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.allocation_table.yview)
        self.allocation_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.allocation_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add sample allocation data
        # In a real application, we'd load this from the database
        for i in range(10):
            self.allocation_table.insert("", tk.END, values=(
                resources[i % len(resources)],
                "Developer" if i % 3 == 0 else "Business Analyst" if i % 3 == 1 else "Tester",
                f"Project {chr(65 + i % 3)}",  # A, B, C
                f"{50 + (i * 10) % 50}%",
                "2023-03-01",
                "2023-06-30"
            ))
        
        # Resource utilization summary
        util_frame = ttk.LabelFrame(right_col, text="Team Utilization Summary")
        util_frame.pack(fill=tk.X, pady=10)
        
        # Calculate utilization stats
        # In a real app, we'd calculate these from actual assignments
        total_capacity = len(resources) * 100  # 100% per resource
        allocated_capacity = sum((70 + i * 5) % 100 for i in range(len(resources)))
        utilization_rate = allocated_capacity / total_capacity * 100
        
        # Display stats
        stats_grid = ttk.Frame(util_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(stats_grid, text="Total Team Capacity:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=f"{total_capacity} person-hours").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Allocated Capacity:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_grid, text=f"{allocated_capacity} person-hours").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_grid, text="Team Utilization Rate:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        util_label = ttk.Label(stats_grid, text=f"{utilization_rate:.1f}%", font=("Arial", 12, "bold"))
        util_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Color-code utilization rate
        if utilization_rate > 90:
            util_label.configure(foreground="red")  # Overallocated
        elif utilization_rate > 75:
            util_label.configure(foreground="green")  # Good utilization
        else:
            util_label.configure(foreground="orange")  # Underutilized
    
    def refresh_resource_allocation(self, parent):
        """Refresh the resource allocation report"""
        # Reload data from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.resources = self.db_manager.get_all_resources()
        
        # Reload allocation data (in a real application)
        messagebox.showinfo("Refresh", "Resource allocation data would be refreshed")
    
    def apply_resource_filters(self, role_filter):
        """Apply filters to the resource allocation report"""
        # In a real application, we'd filter the data and update the displays
        messagebox.showinfo("Apply Filters", f"Filtering resources by role: {role_filter}")
    
    def export_resource_allocation_csv(self):
        """Export resource allocation data to CSV"""
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Resource Allocation Report"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Resource", "Role", "Project", "Allocation", "Start Date", "End Date"])
                
                # Get all children from the table
                for item_id in self.allocation_table.get_children():
                    item = self.allocation_table.item(item_id)
                    writer.writerow(item['values'])
            
            messagebox.showinfo("Export Successful", f"Resource allocation report exported to:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting to CSV: {e}")
    
    def export_resource_allocation_pdf(self):
        """Export resource allocation data to PDF"""
        messagebox.showinfo(
            "PDF Export", 
            "This would export the resource allocation report to PDF including charts and tables."
        )
    
    def setup_task_completion_tab(self, parent):
        """Setup the task completion report tab"""
        # Create control frame with export options
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_task_completion(parent)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to CSV",
            command=self.export_task_completion_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Export to PDF",
            command=self.export_task_completion_pdf
        ).pack(side=tk.LEFT, padx=5)
        
        # Filter controls
        ttk.Label(control_frame, text="Filter by:").pack(side=tk.LEFT, padx=10)
        
        ttk.Label(control_frame, text="Project:").pack(side=tk.LEFT, padx=5)
        
        # Get project names for filter
        project_names = ["All"]
        for project in self.projects:
            project_names.append(project.get("name", ""))
        
        project_filter = ttk.Combobox(control_frame, values=project_names, width=15)
        project_filter.current(0)
        project_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Date Range:").pack(side=tk.LEFT, padx=10)
        date_range = ttk.Combobox(control_frame, values=["All Time", "Last 7 Days", "Last 30 Days", "This Quarter"], width=15)
        date_range.current(0)
        date_range.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Apply",
            command=lambda: self.apply_task_completion_filters(project_filter.get(), date_range.get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Create two-column layout
        columns_frame = ttk.Frame(parent)
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column - completion charts
        left_col = ttk.Frame(columns_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Task completion summary
        summary_frame = ttk.LabelFrame(left_col, text="Task Completion Summary")
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Calculate task statistics
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t.get("status") == "Completed")
        in_progress_tasks = sum(1 for t in self.tasks if t.get("status") == "In Progress")
        not_started_tasks = sum(1 for t in self.tasks if t.get("status") == "Not Started")
        on_hold_tasks = sum(1 for t in self.tasks if t.get("status") == "On Hold")
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Create summary grid
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(summary_grid, text="Total Tasks:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=str(total_tasks), font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(summary_grid, text="Completed:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=str(completed_tasks), foreground=self.colors["success"]).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(summary_grid, text="In Progress:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=str(in_progress_tasks), foreground=self.colors["primary"]).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(summary_grid, text="Not Started:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=str(not_started_tasks), foreground=self.colors["secondary"]).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(summary_grid, text="On Hold:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=str(on_hold_tasks), foreground=self.colors["warning"]).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(summary_grid, text="Completion Rate:", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(summary_grid, text=f"{completion_rate:.1f}%", font=("Arial", 12, "bold"), foreground=self.colors["primary"]).grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Task completion by project chart
        completion_frame = ttk.LabelFrame(left_col, text="Task Completion by Project")
        completion_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create canvas for chart
        canvas = tk.Canvas(completion_frame, background="white", height=300)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a stacked bar chart
        canvas.create_text(200, 30, text="Task Completion by Project", font=("Arial", 14, "bold"))
        
        # Group tasks by project
        project_tasks = {}
        for task in self.tasks:
            project_name = task.get("project_name", "Unknown")
            if project_name not in project_tasks:
                project_tasks[project_name] = {
                    "Completed": 0,
                    "In Progress": 0,
                    "Not Started": 0,
                    "On Hold": 0
                }
            
            status = task.get("status", "Not Started")
            project_tasks[project_name][status] += 1
        
        # Calculate positions
        bar_width = 40
        spacing = 60
        x_start = 100
        y_bottom = 250
        
        # Status colors
        status_colors = {
            "Completed": self.colors["success"],
            "In Progress": self.colors["primary"],
            "Not Started": self.colors["secondary"],
            "On Hold": self.colors["warning"]
        }
        
        # Draw project bars
        for i, (project_name, statuses) in enumerate(project_tasks.items()):
            x = x_start + i * spacing
            
            # Calculate total tasks for this project
            total_project_tasks = sum(statuses.values())
            
            # Start from bottom
            y_pos = y_bottom
            
            # Draw segments for each status
            for status, count in statuses.items():
                if count == 0:
                    continue
                
                # Calculate segment height
                segment_height = (count / total_project_tasks) * 200  # Scale to 200px max height
                
                # Draw segment
                canvas.create_rectangle(
                    x, y_pos - segment_height,
                    x + bar_width, y_pos,
                    fill=status_colors.get(status, "gray"),
                    outline="white"
                )
                
                # Add count label if segment is tall enough
                if segment_height > 20:
                    canvas.create_text(
                        x + bar_width/2, y_pos - segment_height/2,
                        text=str(count),
                        fill="white",
                        font=("Arial", 9, "bold")
                    )
                
                # Move position up for next segment
                y_pos -= segment_height
            
            # Add project name
            canvas.create_text(
                x + bar_width/2, y_bottom + 20,
                text=project_name,
                width=bar_width * 2,  # Allow wrapping
                anchor=tk.N,
                font=("Arial", 8)
            )
        
        # Draw axes
        canvas.create_line(50, 50, 50, y_bottom, width=2)  # Y-axis
        canvas.create_line(50, y_bottom, 550, y_bottom, width=2)  # X-axis
        
        # Draw legend
        legend_y = 70
        for i, (status, color) in enumerate(status_colors.items()):
            # Calculate position
            x = 400
            y = legend_y + i * 20
            
            # Draw color box
            canvas.create_rectangle(
                x, y,
                x + 15, y + 15,
                fill=color,
                outline=""
            )
            
            # Draw status name
            canvas.create_text(
                x + 20, y + 7,
                text=status,
                anchor=tk.W
            )
        
        # Right column - task completion details
        right_col = ttk.Frame(columns_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Recently completed tasks
        completed_frame = ttk.LabelFrame(right_col, text="Recently Completed Tasks")
        completed_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create table
        columns = ("Task", "Project", "Completion Date", "Assigned To")
        self.completed_table = ttk.Treeview(completed_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.completed_table.heading(col, text=col)
            width = 100
            if col in ["Task", "Project"]:
                width = 150
            self.completed_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(completed_frame, orient=tk.VERTICAL, command=self.completed_table.yview)
        self.completed_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.completed_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add completed tasks
        for task in self.tasks:
            if task.get("status") == "Completed":
                # Get assigned resources
                assigned_to = "Unassigned"
                if "assigned_resources" in task and task["assigned_resources"]:
                    resource_names = []
                    for resource_id in task["assigned_resources"]:
                        for resource in self.resources:
                            if resource.get("id") == resource_id:
                                resource_names.append(resource.get("name", ""))
                                break
                    
                    if resource_names:
                        assigned_to = ", ".join(resource_names)
                
                # Get completion date (using placeholder data)
                completion_date = "2023-03-15"  # In a real app, we'd use actual date
                
                self.completed_table.insert("", tk.END, values=(
                    task.get("title", ""),
                    task.get("project_name", ""),
                    completion_date,
                    assigned_to
                ))
        
        # Upcoming tasks
        upcoming_frame = ttk.LabelFrame(right_col, text="Upcoming Task Deadlines")
        upcoming_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create table
        columns = ("Task", "Project", "Due Date", "Days Remaining", "Status")
        self.upcoming_table = ttk.Treeview(upcoming_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.upcoming_table.heading(col, text=col)
            width = 100
            if col in ["Task", "Project"]:
                width = 150
            self.upcoming_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar2 = ttk.Scrollbar(upcoming_frame, orient=tk.VERTICAL, command=self.upcoming_table.yview)
        self.upcoming_table.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.upcoming_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Current date for comparison
        today = datetime.now().date()
        
        # Add upcoming tasks (not completed and with due dates)
        upcoming_tasks = []
        for task in self.tasks:
            if task.get("status") != "Completed" and task.get("due_date"):
                try:
                    due_date = datetime.strptime(task.get("due_date"), "%Y-%m-%d").date()
                    days_remaining = (due_date - today).days
                    
                    # Only include future and recent tasks
                    if days_remaining > -7:  # Include tasks up to 7 days overdue
                        upcoming_tasks.append({
                            "task": task,
                            "days_remaining": days_remaining
                        })
                except ValueError:
                    # Skip tasks with invalid dates
                    continue
        
        # Sort by days remaining
        upcoming_tasks.sort(key=lambda x: x["days_remaining"])
        
        # Add to table
        for item in upcoming_tasks:
            task = item["task"]
            days = item["days_remaining"]
            
            # Format days remaining text
            if days < 0:
                days_text = f"Overdue by {abs(days)} days"
            elif days == 0:
                days_text = "Due today"
            else:
                days_text = f"{days} days"
            
            # Add to table
            values = (
                task.get("title", ""),
                task.get("project_name", ""),
                task.get("due_date", ""),
                days_text,
                task.get("status", "")
            )
            
            # Set tag based on days remaining for color coding
            if days < 0:
                tag = "overdue"
            elif days == 0:
                tag = "due_today"
            elif days <= 2:
                tag = "due_soon"
            else:
                tag = "upcoming"
            
            self.upcoming_table.insert("", tk.END, values=values, tags=(tag,))
        
        # Configure tags for color coding
        self.upcoming_table.tag_configure("overdue", background="#f8d7da")
        self.upcoming_table.tag_configure("due_today", background="#fff3cd")
        self.upcoming_table.tag_configure("due_soon", background="#d1ecf1")
        self.upcoming_table.tag_configure("upcoming", background="#d4edda")
    
    def refresh_task_completion(self, parent):
        """Refresh the task completion report"""
        # Reload data from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.tasks = []
            for project in self.projects:
                project_tasks = self.db_manager.get_tasks_by_project(project.get("id", -1))
                if project_tasks:
                    # Add project name to each task for identification
                    for task in project_tasks:
                        task["project_name"] = project.get("name", "")
                    
                    self.tasks.extend(project_tasks)
        
        # In a real application, we'd reload all the charts and tables
        messagebox.showinfo("Refresh", "Task completion data would be refreshed")
    
    def apply_task_completion_filters(self, project_filter, date_range):
        """Apply filters to the task completion report"""
        # In a real application, we'd filter the data and update the displays
        messagebox.showinfo("Apply Filters", f"Filtering tasks by project: {project_filter}, date range: {date_range}")
    
    def export_task_completion_csv(self):
        """Export task completion data to CSV"""
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Task Completion Report"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Task", "Project", "Status", "Due Date", "Completion Date", "Assigned To"])
                
                # Write data
                for task in self.tasks:
                    # Get assigned resources
                    assigned_to = "Unassigned"
                    if "assigned_resources" in task and task["assigned_resources"]:
                        resource_names = []
                        for resource_id in task["assigned_resources"]:
                            for resource in self.resources:
                                if resource.get("id") == resource_id:
                                    resource_names.append(resource.get("name", ""))
                                    break
                        
                        if resource_names:
                            assigned_to = ", ".join(resource_names)
                    
                    # Use placeholder completion date for completed tasks
                    completion_date = "2023-03-15" if task.get("status") == "Completed" else ""
                    
                    writer.writerow([
                        task.get("title", ""),
                        task.get("project_name", ""),
                        task.get("status", ""),
                        task.get("due_date", ""),
                        completion_date,
                        assigned_to
                    ])
            
            messagebox.showinfo("Export Successful", f"Task completion report exported to:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting to CSV: {e}")
    
    def export_task_completion_pdf(self):
        """Export task completion data to PDF"""
        messagebox.showinfo(
            "PDF Export", 
            "This would export the task completion report to PDF including charts and tables."
        )
    
    def setup_custom_reports_tab(self, parent):
        """Setup the custom reports tab"""
        # Create a frame for custom report options
        options_frame = ttk.LabelFrame(parent, text="Report Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a two-column grid for options
        options_grid = ttk.Frame(options_frame)
        options_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Report type selection
        ttk.Label(options_grid, text="Report Type:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        report_type = ttk.Combobox(options_grid, values=[
            "Project Status Summary", 
            "Resource Utilization", 
            "Task Completion by Project",
            "Project Timeline",
            "Budget vs. Actual",
            "Team Performance"
        ], width=30)
        report_type.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        report_type.current(0)
        
        # Project selection
        ttk.Label(options_grid, text="Projects:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        projects_frame = ttk.Frame(options_grid)
        projects_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        select_all_var = tk.BooleanVar(value=True)
        select_all_cb = ttk.Checkbutton(projects_frame, text="All Projects", variable=select_all_var)
        select_all_cb.pack(anchor=tk.W)
        
        # In a real app, we'd create checkboxes for each project
        # For simplicity, we'll just show a placeholder message
        ttk.Label(projects_frame, text="Individual project selection would appear here").pack(anchor=tk.W, pady=5)
        
        # Date range selection
        ttk.Label(options_grid, text="Date Range:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        date_range = ttk.Combobox(options_grid, values=[
            "All Time",
            "This Month",
            "Last Month",
            "This Quarter",
            "Last Quarter",
            "This Year",
            "Custom Range"
        ], width=15)
        date_range.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        date_range.current(0)
        
        # Group by selection
        ttk.Label(options_grid, text="Group By:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        group_by = ttk.Combobox(options_grid, values=[
            "Project",
            "Status",
            "Client",
            "Resource",
            "Month",
            "Quarter"
        ], width=15)
        group_by.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        group_by.current(0)
        
        # Format selection
        ttk.Label(options_grid, text="Output Format:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        format_frame = ttk.Frame(options_grid)
        format_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        include_charts_var = tk.BooleanVar(value=True)
        include_charts_cb = ttk.Checkbutton(format_frame, text="Include Charts", variable=include_charts_var)
        include_charts_cb.pack(side=tk.LEFT, padx=5)
        
        include_tables_var = tk.BooleanVar(value=True)
        include_tables_cb = ttk.Checkbutton(format_frame, text="Include Tables", variable=include_tables_var)
        include_tables_cb.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        generate_frame = ttk.Frame(options_frame)
        generate_frame.pack(pady=10)
        
        generate_btn = ttk.Button(
            generate_frame,
            text="Generate Report",
            style='Accent.TButton',
            width=20,
            command=lambda: self.generate_custom_report(
                report_type.get(),
                select_all_var.get(),
                date_range.get(),
                group_by.get(),
                include_charts_var.get(),
                include_tables_var.get()
            )
        )
        generate_btn.pack()
        
        # Preview area
        preview_frame = ttk.LabelFrame(parent, text="Report Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas for the preview
        preview_canvas = tk.Canvas(preview_frame, background="white")
        preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw a placeholder preview
        preview_canvas.create_text(
            300, 150,
            text="Select report options and click 'Generate Report'\nto preview custom reports here.",
            font=("Arial", 14),
            justify=tk.CENTER
        )
        
        # Export options at the bottom
        export_frame = ttk.Frame(parent)
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            export_frame,
            text="Export to PDF",
            command=self.export_custom_report_pdf
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            export_frame,
            text="Export to Excel",
            command=self.export_custom_report_excel
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            export_frame,
            text="Print Report",
            command=self.print_custom_report
        ).pack(side=tk.RIGHT, padx=5)
    
    def generate_custom_report(self, report_type, all_projects, date_range, group_by, include_charts, include_tables):
        """Generate a custom report based on selected options"""
        # In a real application, we'd generate the report based on the options
        messagebox.showinfo(
            "Generate Report",
            f"Would generate a {report_type} report\n"
            f"Projects: {'All' if all_projects else 'Selected'}\n"
            f"Date Range: {date_range}\n"
            f"Group By: {group_by}\n"
            f"Include Charts: {include_charts}\n"
            f"Include Tables: {include_tables}"
        )
    
    def export_custom_report_pdf(self):
        """Export custom report to PDF"""
        messagebox.showinfo(
            "PDF Export", 
            "This would export the custom report to PDF."
        )
    
    def export_custom_report_excel(self):
        """Export custom report to Excel"""
        messagebox.showinfo(
            "Excel Export", 
            "This would export the custom report to Excel with multiple sheets for different sections."
        )
    
    def print_custom_report(self):
        """Print the custom report"""
        messagebox.showinfo(
            "Print Report", 
            "This would send the custom report to the printer."
        )
    
    def back_to_dashboard(self):
        """Navigate back to the dashboard"""
        # This is a placeholder - in a real app, we'd navigate back to the dashboard
        messagebox.showinfo("Back to Dashboard", "Would navigate back to the dashboard")