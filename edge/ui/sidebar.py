import tkinter as tk
from tkinter import ttk

class Sidebar:
    """Sidebar navigation component for the KPMG Edge application"""
    
    def __init__(self, parent, colors, callback):
        self.parent = parent
        self.colors = colors
        self.callback = callback  # Callback function for navigation events
        
        # Create sidebar frame
        self.frame = ttk.Frame(parent, style='Sidebar.TFrame', width=250)
        
        # Create logo and navigation elements
        self.create_logo()
        self.create_navigation()
    
    def create_logo(self):
        """Create the app logo/title in the sidebar"""
        logo_frame = ttk.Frame(self.frame, style='Sidebar.TFrame')
        logo_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # App title
        title_label = ttk.Label(logo_frame, text="KPMG Edge", 
                              foreground=self.colors["white"],
                              background=self.colors["primary"],
                              font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
    
    def create_navigation(self):
        """Create the navigation menu"""
        # Define navigation structure
        self.nav_sections = {
            "Dashboard": self.create_callback("Dashboard"),
            "Project Management": {
                "Current Projects": self.create_callback("Project Management", "Current Projects"),
                "New Project": self.create_callback("Project Management", "New Project"),
                "Project Dashboard": self.create_callback("Project Management", "Project Dashboard"),
                "Resources": self.create_callback("Project Management", "Resources"),
                "Tasks": self.create_callback("Project Management", "Tasks"),
                "Timeline": self.create_callback("Project Management", "Timeline"),
                "Reports": self.create_callback("Project Management", "Reports")
            },
            "Resource Management": {
                "Team Allocation": self.create_callback("Resource Management", "Team Allocation"),
                "Resource Planning": self.create_callback("Resource Management", "Resource Planning")
            },
            "Training": {
                "SPM 101": {
                    "Sales Planning": self.create_callback("Training", "Sales Planning"),
                    "Incentive Compensation Management": self.create_callback("Training", "Incentive Compensation Management"),
                    "Sales Intelligence": self.create_callback("Training", "Sales Intelligence")
                },
                "KPMG SPM TOM": self.create_callback("Training", "KPMG SPM TOM"),
                "KPMG Edge": self.create_callback("Training", "KPMG Edge")
            },
            "Settings": self.create_callback("Settings", "Settings")
        }
        
        # Create navigation menu
        self.create_nav_menu(self.frame, self.nav_sections)
    
    def create_nav_menu(self, parent, items, level=0):
        """Recursively create navigation menu items"""
        for label, content in items.items():
            frame = ttk.Frame(parent, style='Sidebar.TFrame')
            frame.pack(fill=tk.X, padx=10*level)
            
            if isinstance(content, dict):
                # Create expandable section
                button = ttk.Button(frame, text=f"▸ {label}", style='Sidebar.TButton',
                                   command=lambda l=label, c=content, f=frame: self.toggle_submenu(l, c, f))
                button.pack(fill=tk.X, pady=2)
            else:
                # Create action button
                button = ttk.Button(frame, text=f"  {label}", style='Sidebar.TButton',
                                   command=content)
                button.pack(fill=tk.X, pady=2)
    
    def toggle_submenu(self, label, content, parent_frame):
        """Toggle submenu visibility"""
        # Check if submenu exists
        if hasattr(parent_frame, 'submenu_frame'):
            # Destroy submenu if it exists
            parent_frame.submenu_frame.destroy()
            delattr(parent_frame, 'submenu_frame')
            
            # Update button text
            for widget in parent_frame.winfo_children():
                if isinstance(widget, ttk.Button) and label in widget['text']:
                    widget.configure(text=f"▸ {label}")
            
        else:
            # Create submenu
            submenu_frame = ttk.Frame(parent_frame, style='Sidebar.TFrame')
            submenu_frame.pack(fill=tk.X)
            parent_frame.submenu_frame = submenu_frame
            
            # Update button text
            for widget in parent_frame.winfo_children():
                if isinstance(widget, ttk.Button) and label in widget['text']:
                    widget.configure(text=f"▾ {label}")
            
            # Add submenu items
            self.create_nav_menu(submenu_frame, content, level=1)
    
    def create_callback(self, section, item=None):
        """Create a callback function for navigation items"""
        return lambda: self.callback(section, item)
        