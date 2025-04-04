import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Topbar:
    """Top navigation bar for the KPMG Edge application"""
    
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        
        # Create frame
        self.frame = ttk.Frame(parent, style='TopBar.TFrame', height=50)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create topbar elements
        self.create_topbar_elements()
    
    def create_topbar_elements(self):
        """Create elements in the top bar"""
        # Left side - Title and breadcrumbs
        self.left_frame = ttk.Frame(self.frame, style='TopBar.TFrame')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Title label (will be updated when navigating)
        self.title_label = ttk.Label(self.left_frame, text="Dashboard", 
                                   style='Title.TLabel')
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Right side - User info, notifications, etc.
        self.right_frame = ttk.Frame(self.frame, style='TopBar.TFrame')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Search box
        search_frame = ttk.Frame(self.right_frame, style='TopBar.TFrame')
        search_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT)
        
        search_button = ttk.Button(search_frame, text="Search")
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Current date
        date_label = ttk.Label(self.right_frame, 
                             text=datetime.now().strftime("%B %d, %Y"),
                             background=self.colors["light"])
        date_label.pack(side=tk.LEFT, padx=10)
        
        # Notifications button
        notification_button = ttk.Button(self.right_frame, text="🔔")
        notification_button.pack(side=tk.LEFT, padx=5)
        
        # User profile
        user_button = ttk.Button(self.right_frame, text="👤 User")
        user_button.pack(side=tk.LEFT, padx=10)
        
        # Tab container (will be populated when navigating to different sections)
        self.tabs_frame = ttk.Frame(self.frame, style='TopBar.TFrame')
        self.tabs_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20)
    
    def set_title(self, title):
        """Update the title in the top bar"""
        self.title_label.config(text=title)
    
    def set_tabs(self, tabs=None, active_tab=None):
        """Set the tabs in the top bar
        
        Args:
            tabs (list): List of tab names
            active_tab (str): Name of the active tab
        """
        # Clear existing tabs
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()
        
        # If no tabs, return
        if not tabs:
            return
        
        # Add new tabs
        for tab in tabs:
            tab_style = 'Accent.TButton' if tab == active_tab else 'TButton'
            tab_button = ttk.Button(self.tabs_frame, text=tab, style=tab_style)
            tab_button.pack(side=tk.LEFT, padx=5, pady=5)