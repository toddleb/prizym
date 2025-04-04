import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger("resource_module")

class ResourceModule:
    """Resource management module for the KPMG Edge application"""
    
    def __init__(self, parent_frame, colors, db_manager=None):
        self.parent_frame = parent_frame
        self.colors = colors
        self.db_manager = db_manager
        self.resources = []
        
        # Load resources if database not available
        if self.db_manager is None or not self.db_manager.is_connected():
            self.load_resources_from_json()
    
    def load_resources_from_json(self):
        """Load resources from a JSON file (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            if os.path.exists("data/resources.json"):
                with open("data/resources.json", "r") as f:
                    self.resources = json.load(f)
                    logger.info(f"Loaded {len(self.resources)} resources from JSON file")
        except Exception as e:
            logger.error(f"Error loading resources from JSON: {e}")
            self.resources = []
    
    def save_resources_to_json(self):
        """Save resources to a JSON file (fallback when database is not available)"""
        try:
            # Check if data directory exists, create if not
            if not os.path.exists('data'):
                os.makedirs('data')
                
            with open("data/resources.json", "w") as f:
                json.dump(self.resources, f, indent=2)
                logger.info(f"Saved {len(self.resources)} resources to JSON file")
        except Exception as e:
            logger.error(f"Error saving resources to JSON: {e}")
            messagebox.showerror("Error", f"Failed to save resources: {e}")
    
    def show_resource_management(self):
        """Show the resource management main view"""
        # Clear the frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Load resources from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.resources = self.db_manager.get_all_resources()
        
        # Create main container with header
        self.create_view_header("Resource Management", "Manage team members and resource allocation")
        
        # Create main notebook for resource views
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        team_tab = ttk.Frame(notebook)
        allocation_tab = ttk.Frame(notebook)
        skills_tab = ttk.Frame(notebook)
        
        notebook.add(team_tab, text="Team Members")
        notebook.add(allocation_tab, text="Resource Allocation")
        notebook.add(skills_tab, text="Skills Matrix")
        
        # Setup each tab
        self.setup_team_tab(team_tab)
        self.setup_allocation_tab(allocation_tab)
        self.setup_skills_tab(skills_tab)
    
    def create_view_header(self, title, subtitle=None):
        """Create a header for a view"""
        header_frame = ttk.Frame(self.parent_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text=title, font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        if subtitle:
            ttk.Label(header_frame, text=subtitle, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(self.parent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=5)
    
    def setup_team_tab(self, parent):
        """Set up the team members tab"""
        # Create control frame with buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="+ Add Resource",
            command=self.show_add_resource_form
        ).pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_team_tab(parent)
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter controls
        ttk.Label(control_frame, text="Role:").pack(side=tk.LEFT, padx=10)
        role_filter = ttk.Combobox(control_frame, values=["All", "Project Manager", "Developer", "Business Analyst", "Tester", "Consultant"], width=15)
        role_filter.current(0)
        role_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=10)
        search_entry = ttk.Entry(control_frame, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Filter",
            command=lambda: self.apply_resource_filters(role_filter.get(), search_entry.get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Create table frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resources table
        columns = ("Name", "Role", "Email", "Phone", "Skills", "Availability")
        self.resources_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.resources_table.heading(col, text=col)
            width = 100
            if col in ["Name", "Email"]:
                width = 150
            elif col == "Skills":
                width = 200
            self.resources_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.resources_table.yview)
        self.resources_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resources_table.pack(fill=tk.BOTH, expand=True)
        
        # Context menu for resources
        self.create_resource_context_menu()
        
        # Bind double-click event
        self.resources_table.bind("<Double-1>", lambda e: self.view_resource_details())
        
        # Load resources
        self.load_resources_table()
        
        # Create summary section
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Calculate some stats
        total_resources = len(self.resources)
        
        # Get roles summary
        roles = {}
        for resource in self.resources:
            role = resource.get("role", "Unknown")
            roles[role] = roles.get(role, 0) + 1
        
        # Stats in a row
        ttk.Label(summary_frame, text=f"Total Resources: {total_resources}", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        
        for role, count in roles.items():
            if role and role != "Unknown":
                ttk.Label(summary_frame, text=f"{role}: {count}").pack(side=tk.LEFT, padx=20)
    
    def load_resources_table(self, filtered_resources=None):
        """Load resources into the resources table"""
        # Clear existing items
        for item in self.resources_table.get_children():
            self.resources_table.delete(item)
        
        # Use filtered list if provided, otherwise use all resources
        resources_to_show = filtered_resources if filtered_resources is not None else self.resources
        
        # Add resources to table
        for resource in resources_to_show:
            # Format skills list
            skills = resource.get("skills", [])
            if isinstance(skills, list):
                skills_str = ", ".join(skills)
            else:
                skills_str = str(skills)
            
            # Format availability
            availability = resource.get("availability", {})
            if isinstance(availability, dict):
                if availability.get("status") == "Available":
                    avail_str = "Available"
                elif availability.get("status") == "Partial":
                    avail_str = f"Partial ({availability.get('percentage', 0)}%)"
                else:
                    avail_str = "Unavailable"
            else:
                avail_str = "Unknown"
            
            values = (
                resource.get("name", ""),
                resource.get("role", ""),
                resource.get("email", ""),
                resource.get("phone", ""),
                skills_str,
                avail_str
            )
            
            self.resources_table.insert("", tk.END, values=values)
    
    def create_resource_context_menu(self):
        """Create context menu for resources table"""
        self.resource_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.resource_menu.add_command(label="View Details", command=self.view_resource_details)
        self.resource_menu.add_command(label="Edit Resource", command=self.edit_resource)
        self.resource_menu.add_separator()
        self.resource_menu.add_command(label="View Assignments", command=self.view_resource_assignments)
        self.resource_menu.add_separator()
        self.resource_menu.add_command(label="Delete Resource", command=self.delete_resource)
        
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
        resource_email = values[2]  # Email is unique, good for identifying resource
        
        # Find resource in list
        resource = None
        for r in self.resources:
            if r.get("name") == resource_name and r.get("email") == resource_email:
                resource = r
                break
        
        if not resource:
            messagebox.showerror("Error", f"Resource '{resource_name}' not found")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the resource '{resource_name}'?\nThis action cannot be undone."):
            return
            
        # Delete from database if available
        if self.db_manager and self.db_manager.is_connected():
            # In a real implementation, we'd have a delete_resource method
            success = True  # Placeholder
            
            if success:
                messagebox.showinfo("Success", f"Resource '{resource_name}' has been deleted")
                self.refresh_team_tab(None)  # Refresh the view
            else:
                messagebox.showerror("Error", f"Failed to delete resource '{resource_name}'")
        else:
            # Remove from local list
            self.resources.remove(resource)
            self.save_resources_to_json()
            messagebox.showinfo("Success", f"Resource '{resource_name}' has been deleted")
            self.refresh_team_tab(None)  # Refresh the view
    
    def refresh_team_tab(self, parent):
        """Refresh the team members tab"""
        # Load resources from database if available
        if self.db_manager and self.db_manager.is_connected():
            self.resources = self.db_manager.get_all_resources()
        
        # Reload resources table
        self.load_resources_table()
    
    def apply_resource_filters(self, role_filter, search_text):
        """Apply filters to resources table"""
        filtered_resources = []
        
        for resource in self.resources:
            # Apply role filter
            if role_filter != "All" and resource.get("role", "") != role_filter:
                continue
                
            # Apply search text
            if search_text:
                search_text = search_text.lower()
                name = resource.get("name", "").lower()
                email = resource.get("email", "").lower()
                
                if search_text not in name and search_text not in email:
                    continue
                
            # All filters passed
            filtered_resources.append(resource)
        
        # Update table with filtered resources
        self.load_resources_table(filtered_resources)
    
    def show_add_resource_form(self):
        """Show form to add a new resource"""
        # Create dialog window
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Add New Resource")
        dialog.geometry("600x600")
        dialog.transient(self.parent_frame)
        dialog.grab_set()  # Make dialog modal
        
        # Create content frame
        content_frame = ttk.Frame(dialog, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        ttk.Label(content_frame, text="Name *", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(content_frame, text="Role *", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        role_combobox = ttk.Combobox(content_frame, values=["Project Manager", "Developer", "Business Analyst", "Tester", "Consultant"], width=20)
        role_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        role_combobox.current(0)
        
        ttk.Label(content_frame, text="Email *", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        email_entry = ttk.Entry(content_frame, width=30)
        email_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(content_frame, text="Phone", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        phone_entry = ttk.Entry(content_frame, width=20)
        phone_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Availability section
        ttk.Label(content_frame, text="Availability", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        
        avail_status = tk.StringVar(value="Available")
        
        avail_frame = ttk.Frame(content_frame)
        avail_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(avail_frame, text="Available", variable=avail_status, value="Available").pack(anchor=tk.W)
        ttk.Radiobutton(avail_frame, text="Partially Available", variable=avail_status, value="Partial").pack(anchor=tk.W)
        ttk.Radiobutton(avail_frame, text="Unavailable", variable=avail_status, value="Unavailable").pack(anchor=tk.W)
        
        # Percentage frame for partial availability
        percent_frame = ttk.Frame(avail_frame)
        percent_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(percent_frame, text="Available Percentage:").pack(side=tk.LEFT)
        
        percent_spinbox = ttk.Spinbox(percent_frame, from_=10, to=90, increment=10, width=5)
        percent_spinbox.pack(side=tk.LEFT, padx=5)
        percent_spinbox.set(50)
        
        # Skills section
        ttk.Label(content_frame, text="Skills", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.NW, padx=5, pady=5)
        
        skills_frame = ttk.Frame(content_frame)
        skills_frame.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Skills entry
        skills_text = ttk.Entry(skills_frame, width=40)
        skills_text.pack(fill=tk.X)
        
        ttk.Label(skills_frame, text="Enter skills separated by commas", font=("Arial", 8, "italic")).pack(anchor=tk.W)
        
        # Common skills quick-add
        common_skills_frame = ttk.LabelFrame(skills_frame, text="Common Skills")
        common_skills_frame.pack(fill=tk.X, pady=10)
        
        common_skills = ["Python", "Java", "JavaScript", "SQL", "Agile", "Scrum", "Business Analysis", "Project Management", "Testing"]
        
        row, col = 0, 0
        for skill in common_skills:
            skill_btn = ttk.Button(
                common_skills_frame, 
                text=skill,
                command=lambda s=skill: self.add_skill_to_entry(skills_text, s)
            )
            skill_btn.grid(row=row, column=col, padx=3, pady=3)
            
            # Move to next column or row
            col += 1
            if col > 2:  # 3 columns max
                col = 0
                row += 1
        
        # Notes field
        ttk.Label(content_frame, text="Notes", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.NW, padx=5, pady=5)
        
        notes_text = tk.Text(content_frame, height=5, width=40, wrap=tk.WORD)
        notes_text.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Required fields note
        ttk.Label(content_frame, text="* Required fields", font=("Arial", 8, "italic")).grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(20, 5))
        
        # Bottom buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=8, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        save_btn = ttk.Button(
            button_frame, 
            text="Add Resource",
            style='Accent.TButton',
            command=lambda: self.save_new_resource(
                dialog,
                name_entry.get(),
                role_combobox.get(),
                email_entry.get(),
                phone_entry.get(),
                avail_status.get(),
                percent_spinbox.get(),
                skills_text.get(),
                notes_text.get("1.0", tk.END)
            )
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def save_new_resource(self, dialog, name, role, email, phone, avail_status, percent, skills_text, notes):
        """Save a new resource"""
        # Validate required fields
        if not name:
            messagebox.showerror("Validation Error", "Name is required")
            return
            
        if not role:
            messagebox.showerror("Validation Error", "Role is required")
            return
            
        if not email:
            messagebox.showerror("Validation Error", "Email is required")
            return
        
        # Parse skills
        skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        
        # Create availability dict
        availability = {
            "status": avail_status,
            "percentage": int(percent) if avail_status == "Partial" else 100 if avail_status == "Available" else 0
        }
        
        # Create resource object
        resource = {
            "name": name,
            "role": role,
            "email": email,
            "phone": phone,
            "skills": skills,
            "availability": availability,
            "notes": notes.strip()
        }
        
        # Save to database if available
        if self.db_manager and self.db_manager.is_connected():
            resource_id = self.db_manager.save_resource(resource)
            
            if resource_id > 0:
                messagebox.showinfo("Success", f"Resource '{name}' has been added successfully")
                dialog.destroy()
                self.refresh_team_tab(None)  # Refresh the view
            else:
                messagebox.showerror("Error", f"Failed to add resource '{name}'")
        else:
            # Add to local list
            resource["id"] = len(self.resources) + 1
            self.resources.append(resource)
            self.save_resources_to_json()
            
            messagebox.showinfo("Success", f"Resource '{name}' has been added successfully")
            dialog.destroy()
            self.refresh_team_tab(None)  # Refresh the view
    
    def setup_allocation_tab(self, parent):
        """Set up the resource allocation tab"""
        # Create control frame with filters
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Filter by:").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Date Range:").pack(side=tk.LEFT, padx=10)
        
        # Date range selector (simplified)
        date_range = ttk.Combobox(control_frame, values=["Current Month", "Next Month", "Next Quarter", "Custom"], width=15)
        date_range.current(0)
        date_range.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Project:").pack(side=tk.LEFT, padx=10)
        
        # Project selector
        projects = ["All Projects"]
        if self.db_manager and self.db_manager.is_connected():
            db_projects = self.db_manager.get_all_projects()
            for p in db_projects:
                projects.append(p.get("name", ""))
        
        project_selector = ttk.Combobox(control_frame, values=projects, width=20)
        project_selector.current(0)
        project_selector.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Apply Filters",
            command=lambda: self.apply_allocation_filters(date_range.get(), project_selector.get())
        ).pack(side=tk.LEFT, padx=10)
        
        # Allocation chart
        chart_frame = ttk.LabelFrame(parent, text="Resource Allocation Chart")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # In a real app, we'd use a proper charting library
        # For now, we'll create a simple canvas-based chart
        
        canvas = tk.Canvas(chart_frame, background="white")
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw chart title
        canvas.create_text(300, 30, text="Resource Allocation by Project", font=("Arial", 14, "bold"))
        
        # Draw axes
        canvas.create_line(50, 50, 50, 350, width=2)  # Y-axis
        canvas.create_line(50, 350, 550, 350, width=2)  # X-axis
        
        # Draw Y-axis labels (resources)
        resources = self.resources[:8]  # Limit to 8 resources for this simple chart
        
        y_step = 35
        y_pos = 80
        
        for resource in resources:
            canvas.create_text(40, y_pos, text=resource.get("name", ""), anchor=tk.E)
            y_pos += y_step
        
        # Draw sample allocation bars
        y_pos = 70
        
        # Colors for projects
        colors = ["#4e73df", "#1cc88a", "#f6c23e", "#e74a3b", "#5a5c69"]
        
        for i, resource in enumerate(resources):
            # For this demo, let's create random allocations
            x_pos = 50
            
            # Create 2-3 allocation blocks per resource
            for j in range(2 + i % 2):
                width = 50 + (j * 40) + (i * 20 % 100)
                
                # Draw allocation block
                canvas.create_rectangle(
                    x_pos, y_pos - 10, 
                    x_pos + width, y_pos + 10, 
                    fill=colors[j % len(colors)], 
                    outline=""
                )
                
                # Add project name inside block if space allows
                if width > 50:
                    canvas.create_text(
                        x_pos + width/2, y_pos, 
                        text=f"Project {j+1}", 
                        fill="white", 
                        font=("Arial", 8)
                    )
                
                x_pos += width + 10
            
            y_pos += y_step
        
        # Draw legend
        legend_y = 380
        legend_x = 50
        
        canvas.create_text(legend_x, legend_y, text="Legend:", anchor=tk.W, font=("Arial", 10, "bold"))
        
        for i in range(5):
            canvas.create_rectangle(
                legend_x + 60 + (i * 100), legend_y - 10,
                legend_x + 80 + (i * 100), legend_y + 10,
                fill=colors[i],
                outline=""
            )
            canvas.create_text(
                legend_x + 90 + (i * 100), legend_y,
                text=f"Project {i+1}",
                anchor=tk.W
            )
        
        # Resource allocation details
        details_frame = ttk.LabelFrame(parent, text="Allocation Details")
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Table for allocation details
        allocation_frame = ttk.Frame(details_frame)
        allocation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Resource", "Project", "Role", "Allocation", "Start Date", "End Date")
        allocation_table = ttk.Treeview(allocation_frame, columns=columns, show="headings", height=7)
        
        # Configure columns
        for col in columns:
            allocation_table.heading(col, text=col)
            width = 100
            if col in ["Resource", "Project"]:
                width = 150
            allocation_table.column(col, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(allocation_frame, orient=tk.VERTICAL, command=allocation_table.yview)
        allocation_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        allocation_table.pack(fill=tk.BOTH, expand=True)
        
        # Add sample allocation data
        for i in range(10):
            allocation_table.insert("", tk.END, values=(
                f"Resource {i+1}",
                f"Project {(i % 3) + 1}",
                "Developer" if i % 3 == 0 else "Analyst" if i % 3 == 1 else "Tester",
                f"{50 + (i * 5) % 50}%",
                "2023-03-01",
                "2023-06-30"
            ))
    
    def apply_allocation_filters(self, date_range, project):
        """Apply filters to the allocation view"""
        # This is a placeholder implementation
        messagebox.showinfo("Apply Filters", f"Filtering allocations by Date Range: {date_range}, Project: {project}")
    
    def setup_skills_tab(self, parent):
        """Set up the skills matrix tab"""
        # Create control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            control_frame, 
            text="Export Skills Matrix",
            command=self.export_skills_matrix
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="↻ Refresh",
            command=lambda: self.refresh_skills_tab(parent)
        ).pack(side=tk.LEFT, padx=5)
        
        # Filters
        ttk.Label(control_frame, text="Filter by:").pack(side=tk.LEFT, padx=10)
        
        ttk.Label(control_frame, text="Skill Category:").pack(side=tk.LEFT, padx=5)
        category_filter = ttk.Combobox(control_frame, values=["All", "Technical", "Soft Skills", "Domain Knowledge", "Tools"], width=15)
        category_filter.current(0)
        category_filter.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Apply Filter",
            command=lambda: self.apply_skills_filter(category_filter.get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Skills matrix
        matrix_frame = ttk.LabelFrame(parent, text="Skills Matrix")
        matrix_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas with scrollbars for the matrix
        canvas_frame = ttk.Frame(matrix_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = ttk.Scrollbar(canvas_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(canvas_frame, background="white")
        canvas.pack(fill=tk.BOTH, expand=True)
        
        canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        h_scrollbar.configure(command=canvas.xview)
        v_scrollbar.configure(command=canvas.yview)
        
        # Create a frame inside the canvas for the matrix
        matrix_content = ttk.Frame(canvas)
        
        # Create the matrix
        self.create_skills_matrix(matrix_content)
        
        # Create window for the matrix content
        canvas_window = canvas.create_window(0, 0, window=matrix_content, anchor=tk.NW)
        
        # Update scroll region when matrix content changes size
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        matrix_content.bind("<Configure>", update_scroll_region)
        
        # Ensure the canvas window resizes with the canvas
        def resize_canvas_window(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", resize_canvas_window)
    
    def create_skills_matrix(self, parent):
        """Create the skills matrix with resources and skills"""
        # Get the skills used across all resources
        all_skills = set()
        for resource in self.resources:
            skills = resource.get("skills", [])
            if isinstance(skills, list):
                all_skills.update(skills)
        
        all_skills = sorted(list(all_skills))
        
        # Create header row with skills
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="Resource", width=20, font=("Arial", 10, "bold"), relief=tk.RIDGE, padding=5).grid(row=0, column=0, sticky=tk.NSEW)
        
        for i, skill in enumerate(all_skills):
            ttk.Label(header_frame, text=skill, width=15, font=("Arial", 10, "bold"), relief=tk.RIDGE, padding=5).grid(row=0, column=i+1, sticky=tk.NSEW)
        
        # Create rows for each resource
        for r, resource in enumerate(self.resources):
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill=tk.X)
            
            ttk.Label(row_frame, text=resource.get("name", ""), width=20, relief=tk.RIDGE, padding=5).grid(row=0, column=0, sticky=tk.NSEW)
            
            resource_skills = resource.get("skills", [])
            if not isinstance(resource_skills, list):
                resource_skills = []
            
            for i, skill in enumerate(all_skills):
                has_skill = skill in resource_skills
                
                if has_skill:
                    label = ttk.Label(row_frame, text="✓", width=15, relief=tk.RIDGE, padding=5, background="#d4edda")
                else:
                    label = ttk.Label(row_frame, text="", width=15, relief=tk.RIDGE, padding=5)
                
                label.grid(row=0, column=i+1, sticky=tk.NSEW)
    
    def apply_skills_filter(self, category):
        """Apply filter to skills matrix"""
        # This is a placeholder implementation
        messagebox.showinfo("Apply Filter", f"Filtering skills by category: {category}")
    
    def refresh_skills_tab(self, parent):
        """Refresh the skills tab"""
        # In a real implementation, we'd reload the data and redraw the matrix
        messagebox.showinfo("Refresh", "Skills matrix would be refreshed with latest data")
    
    def export_skills_matrix(self):
        """Export the skills matrix to a file"""
        # This is a placeholder implementation
        messagebox.showinfo("Export", "Skills matrix would be exported to Excel or CSV")
    
    # The next method would start here
    def show_resource_details_dialog(self, resource):
        """Show a dialog with resource details"""
        # Method implementation...
        
        self.show_resource_details_dialog(resource)
    
    def show_resource_details_dialog(self, resource):
        """Show a dialog with resource details"""
        # Create dialog window
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(f"Resource Details: {resource.get('name', '')}")
        dialog.geometry("600x500")
        dialog.transient(self.parent_frame)
        dialog.grab_set()  # Make dialog modal
        
        # Create content frame
        content_frame = ttk.Frame(dialog, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Resource details
        details_frame = ttk.LabelFrame(content_frame, text="Personal Information")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Create a grid for details
        details_grid = ttk.Frame(details_frame)
        details_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Row 1
        ttk.Label(details_grid, text="Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=resource.get("name", "")).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_grid, text="Role:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=resource.get("role", "")).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Row 2
        ttk.Label(details_grid, text="Email:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=resource.get("email", "")).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(details_grid, text="Phone:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Label(details_grid, text=resource.get("phone", "")).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Skills section
        skills_frame = ttk.LabelFrame(content_frame, text="Skills")
        skills_frame.pack(fill=tk.X, pady=10)
        
        # Get skills
        skills = resource.get("skills", [])
        if skills:
            skills_container = ttk.Frame(skills_frame)
            skills_container.pack(fill=tk.X, padx=10, pady=10)
            
            # Display skills as tags
            row, col = 0, 0
            for skill in skills:
                skill_label = ttk.Label(
                    skills_container, 
                    text=skill,
                    background=self.colors["light"],
                    padding=(5, 2)
                )
                skill_label.grid(row=row, column=col, padx=5, pady=5)
                
                # Move to next column or row
                col += 1
                if col > 3:  # 4 columns max
                    col = 0
                    row += 1
        else:
            ttk.Label(skills_frame, text="No skills defined for this resource").pack(padx=10, pady=10)
        
        # Current assignments section
        assignments_frame = ttk.LabelFrame(content_frame, text="Current Project Assignments")
        assignments_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Get assignments if db available
        assignments = []
        if self.db_manager and self.db_manager.is_connected():
            # In a real implementation, we'd have a method to get assignments by resource
            pass
        
        if assignments:
            # Create assignments table
            columns = ("Project", "Role", "Allocation", "Start Date", "End Date")
            assignments_table = ttk.Treeview(assignments_frame, columns=columns, show="headings", height=5)
            
            # Configure columns
            for col in columns:
                assignments_table.heading(col, text=col)
                width = 100
                if col == "Project":
                    width = 150
                assignments_table.column(col, width=width)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(assignments_frame, orient=tk.VERTICAL, command=assignments_table.yview)
            assignments_table.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            assignments_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add assignments to table
            for assignment in assignments:
                values = (
                    assignment.get("project_name", ""),
                    assignment.get("role", ""),
                    f"{assignment.get('allocation', 100)}%",
                    assignment.get("start_date", ""),
                    assignment.get("end_date", "")
                )
                
                assignments_table.insert("", tk.END, values=values)
        else:
            ttk.Label(assignments_frame, text="No current project assignments").pack(padx=10, pady=10)
        
        # Bottom buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Edit Resource",
            command=lambda: self.edit_resource_from_dialog(dialog, resource)
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            button_frame, 
            text="Close",
            command=dialog.destroy
        ).pack(side=tk.RIGHT)
    
    def edit_resource_from_dialog(self, dialog, resource):
        """Edit a resource from the details dialog"""
        dialog.destroy()  # Close the current dialog
        self.show_edit_resource_form(resource)
    
    def edit_resource(self):
        """Edit selected resource"""
        selected_items = self.resources_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a resource to edit")
            return
        
        # Get resource name from selected item
        values = self.resources_table.item(selected_items[0], 'values')
        resource_name = values[0]
        resource_email = values[2]  # Email is unique, good for identifying resource
        
        # Find resource in list
        resource = None
        for r in self.resources:
            if r.get("name") == resource_name and r.get("email") == resource_email:
                resource = r
                break
        
        if not resource:
            messagebox.showerror("Error", f"Resource '{resource_name}' not found")
            return
        
        self.show_edit_resource_form(resource)
    
    def show_edit_resource_form(self, resource):
        """Show form to edit a resource"""
        # Create dialog window
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(f"Edit Resource: {resource.get('name', '')}")
        dialog.geometry("600x600")
        dialog.transient(self.parent_frame)
        dialog.grab_set()  # Make dialog modal
        
        # Create content frame
        content_frame = ttk.Frame(dialog, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        ttk.Label(content_frame, text="Name *", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        name_entry.insert(0, resource.get("name", ""))
        
        ttk.Label(content_frame, text="Role *", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        role_combobox = ttk.Combobox(content_frame, values=["Project Manager", "Developer", "Business Analyst", "Tester", "Consultant"], width=20)
        role_combobox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Set current role if valid
        role = resource.get("role", "")
        if role in role_combobox["values"]:
            role_combobox.set(role)
        
        ttk.Label(content_frame, text="Email *", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        email_entry = ttk.Entry(content_frame, width=30)
        email_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        email_entry.insert(0, resource.get("email", ""))
        
        ttk.Label(content_frame, text="Phone", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        phone_entry = ttk.Entry(content_frame, width=20)
        phone_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        phone_entry.insert(0, resource.get("phone", ""))
        
        # Availability section
        ttk.Label(content_frame, text="Availability", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        
        availability = resource.get("availability", {})
        avail_status = tk.StringVar(value=availability.get("status", "Available"))
        
        avail_frame = ttk.Frame(content_frame)
        avail_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(avail_frame, text="Available", variable=avail_status, value="Available").pack(anchor=tk.W)
        ttk.Radiobutton(avail_frame, text="Partially Available", variable=avail_status, value="Partial").pack(anchor=tk.W)
        ttk.Radiobutton(avail_frame, text="Unavailable", variable=avail_status, value="Unavailable").pack(anchor=tk.W)
        
        # Percentage frame for partial availability
        percent_frame = ttk.Frame(avail_frame)
        percent_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(percent_frame, text="Available Percentage:").pack(side=tk.LEFT)
        
        percent_spinbox = ttk.Spinbox(percent_frame, from_=10, to=90, increment=10, width=5)
        percent_spinbox.pack(side=tk.LEFT, padx=5)
        percent_spinbox.set(availability.get("percentage", 50))
        
        # Skills section
        ttk.Label(content_frame, text="Skills", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.NW, padx=5, pady=5)
        
        skills_frame = ttk.Frame(content_frame)
        skills_frame.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Current skills
        current_skills = resource.get("skills", [])
        skills_text = ttk.Entry(skills_frame, width=40)
        skills_text.pack(fill=tk.X)
        skills_text.insert(0, ", ".join(current_skills) if isinstance(current_skills, list) else "")
        
        ttk.Label(skills_frame, text="Enter skills separated by commas", font=("Arial", 8, "italic")).pack(anchor=tk.W)
        
        # Common skills quick-add
        common_skills_frame = ttk.LabelFrame(skills_frame, text="Common Skills")
        common_skills_frame.pack(fill=tk.X, pady=10)
        
        common_skills = ["Python", "Java", "JavaScript", "SQL", "Agile", "Scrum", "Business Analysis", "Project Management", "Testing"]
        
        row, col = 0, 0
        for skill in common_skills:
            skill_btn = ttk.Button(
                common_skills_frame, 
                text=skill,
                command=lambda s=skill: self.add_skill_to_entry(skills_text, s)
            )
            skill_btn.grid(row=row, column=col, padx=3, pady=3)
            
            # Move to next column or row
            col += 1
            if col > 2:  # 3 columns max
                col = 0
                row += 1
        
        # Notes field
        ttk.Label(content_frame, text="Notes", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.NW, padx=5, pady=5)
        
        notes_text = tk.Text(content_frame, height=5, width=40, wrap=tk.WORD)
        notes_text.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        notes_text.insert(tk.END, resource.get("notes", ""))
        
        # Required fields note
        ttk.Label(content_frame, text="* Required fields", font=("Arial", 8, "italic")).grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(20, 5))
        
        # Bottom buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=8, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        save_btn = ttk.Button(
            button_frame, 
            text="Save Changes",
            style='Accent.TButton',
            command=lambda: self.save_resource_changes(
                dialog,
                resource,
                name_entry.get(),
                role_combobox.get(),
                email_entry.get(),
                phone_entry.get(),
                avail_status.get(),
                percent_spinbox.get(),
                skills_text.get(),
                notes_text.get("1.0", tk.END)
            )
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def add_skill_to_entry(self, entry_widget, skill):
        """Add a skill to the skills entry"""
        current_text = entry_widget.get()
        
        if not current_text:
            entry_widget.insert(0, skill)
        else:
            # Check if skill already exists
            skills = [s.strip() for s in current_text.split(",")]
            if skill not in skills:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, current_text + ", " + skill)
    
    def save_resource_changes(self, dialog, original_resource, name, role, email, phone, avail_status, percent, skills_text, notes):
        """Save changes to a resource"""
        # Validate required fields
        if not name:
            messagebox.showerror("Validation Error", "Name is required")
            return
            
        if not role:
            messagebox.showerror("Validation Error", "Role is required")
            return
            
        if not email:
            messagebox.showerror("Validation Error", "Email is required")
            return
        
        # Parse skills
        skills = [s.strip() for s in skills_text.split(",") if s.strip()]
        
        # Create availability dict
        availability = {
            "status": avail_status,
            "percentage": int(percent) if avail_status == "Partial" else 100 if avail_status == "Available" else 0
        }
        
        # Create updated resource object
        updated_resource = {
            "id": original_resource.get("id"),
            "name": name,
            "role": role,
            "email": email,
            "phone": phone,
            "skills": skills,
            "availability": availability,
            "notes": notes.strip()
        }
        
        # Save to database if available
        if self.db_manager and self.db_manager.is_connected():
            # In a real implementation, we'd have an update_resource method
            success = True  # Placeholder
            
            if success:
                messagebox.showinfo("Success", f"Resource '{name}' has been updated successfully")
                dialog.destroy()
                self.refresh_team_tab(None)  # Refresh the view
            else:
                messagebox.showerror("Error", f"Failed to update resource '{name}'")
        else:
            # Update in local list
            for i, resource in enumerate(self.resources):
                if resource.get("id") == original_resource.get("id"):
                    self.resources[i] = updated_resource
                    break
            
            self.save_resources_to_json()
            messagebox.showinfo("Success", f"Resource '{name}' has been updated successfully")
            dialog.destroy()
            self.refresh_team_tab(None)  # Refresh the view
    
    def view_resource_assignments(self):
        """View assignments for selected resource"""
        selected_items = self.resources_table.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a resource to view assignments")
            return
        
        # Get resource name from selected item
        values = self.resources_table.item(selected_items[0], 'values')
        resource_name = values[0]
        
        # This is a simplified implementation - in a real app, we'd show assignments
        messagebox.showinfo("View Assignments", f"Viewing assignments for resource: {resource_name}\n\nThis would show all project assignments for this resource.")
    
def delete_resource(self):
    """Delete selected resource"""
    selected_items = self.resources_table.selection()
    if not selected_items:
        messagebox.showinfo("No Selection", "Please select a resource to delete")
        return
    
    # Get resource name from selected item
    values = self.resources_table.item(selected_items[0], 'values')
    resource_name = values[0]
    resource_email = values[2]  # Email is unique, good for identifying resource
    
    # Find resource in list
    resource = None
    for r in self.resources:
        if r.get("name") == resource_name and r.get("email") == resource_email:
            resource = r
            break
    
    if not resource:
        messagebox.showerror("Error", f"Resource '{resource_name}' not found")
        return
        
    # Confirm deletion
    if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the resource '{resource_name}'?\nThis action cannot be undone."):
        return
        
    # Delete from database if available
    if self.db_manager and self.db_manager.is_connected():
        success = self.db_manager.delete_resource(resource.get("id"))
        
        if success:
            messagebox.showinfo("Success", f"Resource '{resource_name}' has been deleted")
            self.refresh_team_tab(None)  # Refresh the view
        else:
            messagebox.showerror("Error", f"Failed to delete resource '{resource_name}'")
    else:
        # Remove from local list
        self.resources.remove(resource)
        self.save_resources_to_json()
        messagebox.showinfo("Success", f"Resource '{resource_name}' has been deleted")
        self.refresh_team_tab(None)  # Refresh the view
        