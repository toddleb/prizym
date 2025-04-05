"""
SPM Edge UI - Main Application
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import sys

# Import tab modules
from deliverables_tab import DeliverablesTab
from settings_tab import SettingsTab
from theme_tab import ThemeTab
from projects_tab import ProjectsTab
from documents_tab import DocumentsTab
from processing_tab import ProcessingTab
from framework_tab import FrameworkTab
from rag_tab import RAGTab
from dashboard_tab import create_dashboard_tab
from styles import setup_styles

class SPMEdgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPM Edge")
        self.root.geometry("1024x768")
        
        # Set up styles and colors
        self.style, self.colors = setup_styles(root)
        
        # Load settings and theme
        self.settings = self.load_settings()
        self.theme = self.load_theme()
        
        # Initialize database connection (set to None for now)
        self.db_manager = None
        # Will add real connection later
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create side panel for navigation
        self.create_sidebar()
        
        # Create content area with notebook
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Apply initial theme
        self.apply_theme(self.theme)
    
    def create_sidebar(self):
        """Create sidebar for navigation"""
        self.sidebar = ttk.Frame(self.main_frame, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # App logo/title
        logo_frame = ttk.Frame(self.sidebar)
        logo_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Label(
            logo_frame, 
            text="SPM Edge",
            font=("Arial", 18, "bold")
        ).pack(anchor=tk.CENTER)
        
        # Navigation buttons
        self.create_nav_button("Dashboard", self.show_dashboard)
        self.create_nav_button("Projects", self.show_projects)
        self.create_nav_button("Documents", self.show_documents)
        self.create_nav_button("Processing", self.show_processing)
        self.create_nav_button("RAG", self.show_rag)
        self.create_nav_button("Framework", self.show_framework)
        self.create_nav_button("Analysis", self.show_analysis)
        self.create_nav_button("Deliverables", self.show_deliverables)
        self.create_nav_button("Settings", self.show_settings)
        self.create_nav_button("Theme", self.show_theme)
        
        # Add a spacer
        ttk.Frame(self.sidebar).pack(fill=tk.Y, expand=True)
        
        # Version info at bottom
        version_frame = ttk.Frame(self.sidebar)
        version_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            version_frame,
            text="Version 1.0.0",
            font=("Arial", 8)
        ).pack(anchor=tk.CENTER)
    
    def create_nav_button(self, text, command):
        """Create a navigation button in the sidebar"""
        btn_frame = ttk.Frame(self.sidebar)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn = ttk.Button(
            btn_frame,
            text=text,
            command=command,
            width=18
        )
        btn.pack(fill=tk.X)
    
    def create_content_area(self):
        """Create the main content area with notebook for tabs"""
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create dashboard tab
        self.dashboard_frame = create_dashboard_tab(self.notebook, self)
        
        # Initialize specialized tab modules
        self.projects_tab = ProjectsTab(self.notebook, self)
        self.documents_tab = DocumentsTab(self.notebook, self)
        self.processing_tab = ProcessingTab(self.notebook, self)
        self.rag_tab = RAGTab(self.notebook, self)
        self.framework_tab = FrameworkTab(self.notebook, self)
        
        # Create analysis tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Analysis")
        ttk.Label(self.analysis_frame, text="Analysis Content", font=("Arial", 14)).pack(pady=20)
        
        # Add specialized tabs
        self.deliverables_tab = DeliverablesTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        self.theme_tab = ThemeTab(self.notebook, self)
    
    def create_status_bar(self):
        """Create status bar at the bottom of the window"""
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.status_bar, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Additional status info
        self.status_info1 = tk.StringVar(value="Documents: 0")
        ttk.Label(self.status_bar, textvariable=self.status_info1).pack(side=tk.RIGHT, padx=10)
        
        self.status_info2 = tk.StringVar(value="API: Ready")
        ttk.Label(self.status_bar, textvariable=self.status_info2).pack(side=tk.RIGHT, padx=10)
    
    def show_dashboard(self):
        """Switch to dashboard tab"""
        self.notebook.select(0)
    
    def show_projects(self):
        """Switch to projects tab"""
        self.notebook.select(1)
    
    def show_documents(self):
        """Switch to documents tab"""
        self.notebook.select(2)
    
    def show_processing(self):
        """Switch to processing tab"""
        self.notebook.select(3)
    
    def show_rag(self):
        """Switch to RAG tab"""
        self.notebook.select(4)
    
    def show_framework(self):
        """Switch to framework tab"""
        self.notebook.select(5)
    
    def show_analysis(self):
        """Switch to analysis tab"""
        self.notebook.select(6)
    
    def show_deliverables(self):
        """Switch to deliverables tab"""
        self.notebook.select(7)
    
    def show_settings(self):
        """Switch to settings tab"""
        self.notebook.select(8)
    
    def show_theme(self):
        """Switch to theme tab"""
        self.notebook.select(9)
    
    def load_settings(self):
        """Load application settings from file"""
        settings_file = os.path.join(os.path.expanduser("~"), ".spm_edge_settings.json")
        default_settings = {
            "api_key": "",
            "model": "gpt-4o",
            "embeddings_model": "text-embedding-3-small",
            "data_dir": os.path.expanduser("~/spm_edge_data"),
            "batch_size": 10,
            "auto_save": True,
            "debug_mode": False
        }
        
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update default settings with loaded values
                    for key, value in loaded_settings.items():
                        if key in default_settings:
                            default_settings[key] = value
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")
        
        return default_settings
    
    def load_theme(self):
        """Load theme settings from file"""
        theme_file = os.path.join(os.path.expanduser("~"), ".spm_edge_theme.json")
        default_theme = {
            "theme_mode": "light",
            "primary_color": "#007bff",
            "secondary_color": "#6c757d",
            "accent_color": "#ffc107",
            "font_family": "Arial",
            "font_size": 10,
            "use_custom_colors": False,
            "custom_background": "#ffffff",
            "custom_foreground": "#212529",
            "button_style": "default"
        }
        
        try:
            if os.path.exists(theme_file):
                with open(theme_file, 'r') as f:
                    loaded_theme = json.load(f)
                    # Update default theme with loaded values
                    for key, value in loaded_theme.items():
                        if key in default_theme:
                            default_theme[key] = value
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load theme settings: {e}")
        
        return default_theme
    
    def apply_theme(self, theme):
        """Apply theme settings to the application"""
        # Store the theme
        self.theme = theme
        
        # Apply font changes
        font_family = theme.get("font_family", "Arial")
        font_size = theme.get("font_size", 10)
        
        # Set default font
        default_font = (font_family, font_size)
        
        # Apply custom colors if enabled
        if theme.get("use_custom_colors", False):
            bg_color = theme.get("custom_background", "#ffffff")
            fg_color = theme.get("custom_foreground", "#212529")
            
            # Apply to all widgets
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TLabel", background=bg_color, foreground=fg_color)
            self.style.configure("TButton", background=bg_color, foreground=fg_color)
            self.style.configure("TNotebook", background=bg_color)
            self.style.configure("TNotebook.Tab", background=bg_color, foreground=fg_color)
        
        # Apply button style
        button_style = theme.get("button_style", "default")
        if button_style == "rounded":
            # Rounded buttons would need custom drawing
            pass
        elif button_style == "flat":
            self.style.configure("TButton", relief=tk.FLAT)
        else:
            self.style.configure("TButton", relief=tk.RAISED)
    
    def update_settings(self, settings):
        """Update application settings"""
        self.settings = settings
        
        # Apply settings if applicable
        # (e.g., update API connections, batch sizes, etc.)
        
        # Show confirmation
        self.update_status("Settings updated", "Settings applied", "API: Ready")
    
    def update_status(self, message, info1=None, info2=None):
        """Update status bar information"""
        self.status_var.set(message)
        
        if info1:
            self.status_info1.set(info1)
        
        if info2:
            self.status_info2.set(info2)
    
    def new_project(self):
        """Create a new project"""
        self.show_projects()
        if hasattr(self.projects_tab, 'new_project'):
            self.projects_tab.new_project()
    
    def import_documents(self):
        """Import documents"""
        self.show_documents()
        if hasattr(self.documents_tab, 'upload_documents'):
            self.documents_tab.upload_documents()
    
    def run_pipeline(self):
        """Run processing pipeline"""
        self.show_processing()
        if hasattr(self.processing_tab, 'run_full_pipeline'):
            self.processing_tab.run_full_pipeline()
    
    def chat_with_documents(self):
        """Open RAG tab to chat with documents"""
        self.show_rag()
        # Select some documents by default if none are selected
        if hasattr(self.rag_tab, 'toggle_all_documents'):
            if not self.rag_tab.selected_documents:
                self.rag_tab.toggle_all_documents(True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SPMEdgeApp(root)
    root.mainloop()