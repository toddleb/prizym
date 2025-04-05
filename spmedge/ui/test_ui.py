import tkinter as tk
from tkinter import ttk

# Import the tab classes
from deliverables_tab import DeliverablesTab
from settings_tab import SettingsTab
from theme_tab import ThemeTab

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPM Edge UI Test")
        self.root.geometry("900x600")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Initialize tabs
        self.deliverables_tab = DeliverablesTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        self.theme_tab = ThemeTab(self.notebook, self)
        
        # Basic theme application method
        self.current_theme = {}
    
    def apply_theme(self, theme_settings):
        """Apply theme to the application"""
        self.current_theme = theme_settings
        
        # Basic theme application (in a real app, you'd do more here)
        font_family = theme_settings.get("font_family", "Arial")
        font_size = theme_settings.get("font_size", 10)
        
        # Example of setting a font
        default_font = (font_family, font_size)
        
        # You would typically set styles for all widgets here
        style = ttk.Style()
        
        # Configure some basic styles based on theme
        if theme_settings.get("theme_mode") == "dark":
            # Basic dark mode styling
            bg_color = theme_settings.get("custom_background", "#343a40") if theme_settings.get("use_custom_colors") else "#343a40"
            fg_color = theme_settings.get("custom_foreground", "#f8f9fa") if theme_settings.get("use_custom_colors") else "#f8f9fa"
            
            self.root.configure(bg=bg_color)
            style.configure("TFrame", background=bg_color)
            style.configure("TLabel", background=bg_color, foreground=fg_color)
        else:
            # Basic light mode styling
            bg_color = theme_settings.get("custom_background", "#f8f9fa") if theme_settings.get("use_custom_colors") else "#f8f9fa"
            fg_color = theme_settings.get("custom_foreground", "#343a40") if theme_settings.get("use_custom_colors") else "#343a40"
            
            self.root.configure(bg=bg_color)
            style.configure("TFrame", background=bg_color)
            style.configure("TLabel", background=bg_color, foreground=fg_color)
    
    def update_settings(self, settings):
        """Update application settings"""
        # In a real app, you would apply these settings
        print("Settings updated:", settings)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()