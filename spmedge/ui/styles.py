"""
UI styles and themes for SPM Edge application
"""
import tkinter as tk
from tkinter import ttk

def setup_styles(root):
    """Configure application styles and return style controller and colors"""
    style = ttk.Style()
    
    # Try to use a more modern theme if available
    available_themes = style.theme_names()
    preferred_themes = ['azure', 'clam', 'vista']
    
    theme_found = False
    for theme in preferred_themes:
        if theme in available_themes:
            style.theme_use(theme)
            theme_found = True
            break
    
    if not theme_found:
        style.theme_use('clam')  # Fallback theme
        
    # Custom colors
    colors = {
        'primary': '#2563eb',       # Blue
        'primary_light': '#93c5fd', # Light blue
        'secondary': '#475569',     # Slate gray
        'success': '#22c55e',       # Green
        'warning': '#f59e0b',       # Amber
        'danger': '#ef4444',        # Red
        'background': '#f8fafc',    # Light gray
        'text': '#1e293b',          # Dark gray
        'border': '#cbd5e1'         # Light border
    }
    
    # Configure styles for different elements
    style.configure('TFrame', background=colors['background'])
    style.configure('TLabel', background=colors['background'], foreground=colors['text'])
    style.configure('TNotebook', background=colors['background'])
    
    # Tab styling
    style.configure(
        'TNotebook.Tab',
        background=colors['background'],
        padding=[15, 5],
        foreground=colors['text']
    )
    style.map(
        'TNotebook.Tab',
        background=[('selected', colors['primary_light'])],
        foreground=[('selected', colors['text'])]
    )
    
    # Button styling
    style.configure(
        'TButton',
        background=colors['primary'],
        foreground='white',
        padding=[10, 5]
    )
    style.map(
        'TButton',
        background=[('active', colors['primary_light'])],
        foreground=[('active', colors['text'])]
    )
    
    # Define additional button styles
    style.configure(
        'Success.TButton',
        background=colors['success'],
        foreground='white'
    )
    style.map(
        'Success.TButton',
        background=[('active', '#16a34a')]  # Darker green on hover
    )
    
    style.configure(
        'Danger.TButton',
        background=colors['danger'],
        foreground='white'
    )
    style.map(
        'Danger.TButton',
        background=[('active', '#dc2626')]  # Darker red on hover
    )
    
    return style, colors