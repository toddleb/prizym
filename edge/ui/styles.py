import tkinter as tk
from tkinter import ttk

class StyleManager:
    """Manages styles for the KPMG Edge application"""
    
    def __init__(self, root):
        self.root = root
        
        # Define KPMG color palette
        self.colors = {
            "primary": "#00338D",  # KPMG blue
            "secondary": "#005EB8",
            "accent": "#0091DA",
            "light": "#E0E6ED",
            "white": "#FFFFFF",
            "dark": "#333333",
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545"
        }
        
        # Apply theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam as base theme
        self.configure_styles()
    
    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Frame styles
        self.style.configure('Sidebar.TFrame', background=self.colors["primary"])
        self.style.configure('Content.TFrame', background=self.colors["white"])
        self.style.configure('TopBar.TFrame', background=self.colors["light"])
        
        # Button styles
        self.style.configure('Sidebar.TButton', 
                           background=self.colors["primary"],
                           foreground=self.colors["white"],
                           borderwidth=0,
                           focuscolor=self.colors["primary"],
                           lightcolor=self.colors["primary"],
                           darkcolor=self.colors["primary"])
                           
        self.style.map('Sidebar.TButton',
                     background=[('active', self.colors["secondary"])],
                     foreground=[('active', self.colors["white"])])
        
        # Accent button (for primary actions)
        self.style.configure('Accent.TButton', 
                           background=self.colors["accent"],
                           foreground=self.colors["white"])
        
        self.style.map('Accent.TButton',
                     background=[('active', self.colors["secondary"])],
                     foreground=[('active', self.colors["white"])])
        
        # Success button (for positive actions)
        self.style.configure('Success.TButton', 
                           background=self.colors["success"],
                           foreground=self.colors["white"])
        
        self.style.map('Success.TButton',
                     background=[('active', "#218838")],  # Darker green on hover
                     foreground=[('active', self.colors["white"])])
        
        # Danger button (for destructive actions)
        self.style.configure('Danger.TButton', 
                           background=self.colors["danger"],
                           foreground=self.colors["white"])
        
        self.style.map('Danger.TButton',
                     background=[('active', "#c82333")],  # Darker red on hover
                     foreground=[('active', self.colors["white"])])
        
        # Label styles
        self.style.configure('Title.TLabel', 
                           font=("Arial", 16, "bold"),
                           background=self.colors["light"])
        
        self.style.configure('Subtitle.TLabel', 
                           font=("Arial", 12, "bold"),
                           background=self.colors["light"])
        
        # Treeview styles (for tables)
        self.style.configure("Treeview", 
                           background=self.colors["white"],
                           foreground=self.colors["dark"],
                           rowheight=25,
                           fieldbackground=self.colors["white"])
        
        self.style.map('Treeview',
                     background=[('selected', self.colors["accent"])],
                     foreground=[('selected', self.colors["white"])])
        
        self.style.configure("Treeview.Heading",
                           background=self.colors["light"],
                           foreground=self.colors["dark"],
                           font=("Arial", 10, "bold"))
        
        # Notebook styles (for tabs)
        self.style.configure("TNotebook", 
                           background=self.colors["white"])
        
        self.style.configure("TNotebook.Tab", 
                           background=self.colors["light"],
                           foreground=self.colors["dark"],
                           padding=[10, 5])
        
        self.style.map("TNotebook.Tab",
                     background=[("selected", self.colors["white"])],
                     foreground=[("selected", self.colors["primary"])])