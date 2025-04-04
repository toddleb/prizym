"""
Settings module for the KPMG Edge application.
Provides a UI for managing application settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from utils.config import config
from dotenv import set_key, load_dotenv
import logging

logger = logging.getLogger("settings")

class SettingsModule:
    """Settings module for managing application configuration."""
    
    def __init__(self, parent_frame, colors):
        self.parent_frame = parent_frame
        self.colors = colors
        self.env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        
        # Ensure .env file exists
        if not os.path.exists(self.env_file_path):
            try:
                with open(self.env_file_path, 'w') as f:
                    f.write("# KPMG Edge Environment Configuration\n\n")
                logger.info("Created new .env file")
            except Exception as e:
                logger.error(f"Failed to create .env file: {e}")
        
        # Reload environment variables to make sure we have the latest
        load_dotenv(self.env_file_path, override=True)
        
        # Store original values to detect changes
        self.original_values = {
            "openai_key": config.OPENAI_API_KEY or "",
            "openai_model": config.OPENAI_MODEL or "gpt-4o",
            "anthropic_key": config.ANTHROPIC_API_KEY or "",
            "anthropic_model": config.ANTHROPIC_MODEL or "claude-3-opus-20240229",
            "huggingface_key": config.HUGGINGFACE_API_KEY or "",
            "workers": str(config.WORKERS) or "4",
            "db_name": config.DB_NAME or "edge_db",
            "db_user": config.DB_USER or "todd",
            "db_password": config.DB_PASSWORD or "Fubijar",
            "db_host": config.DB_HOST or "localhost",
            "db_port": str(config.DB_PORT) or "5432",
            "input_dir": config.PLAN_INPUT_DIR or "",
            "output_dir": config.PLAN_OUTPUT_DIR or "",
            "plan_dir": config.PLAN_DIR or "",
            "ui_theme": config.UI_THEME or "light",
            "ui_font_size": str(config.UI_FONT_SIZE) or "10"
        }
        
        # Current values (will be updated when user changes settings)
        self.current_values = self.original_values.copy()
    
    def display(self, active_tab=None):
        """Display the settings UI"""
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create a notebook for different settings categories
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs for different setting categories
        general_tab = ttk.Frame(notebook)
        api_tab = ttk.Frame(notebook)
        db_tab = ttk.Frame(notebook)
        paths_tab = ttk.Frame(notebook)
        
        notebook.add(general_tab, text="General")
        notebook.add(api_tab, text="API Settings")
        notebook.add(db_tab, text="Database")
        notebook.add(paths_tab, text="Data Paths")
        
        # Setup each tab
        self.setup_general_tab(general_tab)
        self.setup_api_tab(api_tab)
        self.setup_db_tab(db_tab)
        self.setup_paths_tab(paths_tab)
        
        # Add buttons at the bottom
        button_frame = ttk.Frame(self.parent_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="Save Changes", command=self.save_settings, style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_changes).pack(side=tk.RIGHT, padx=5)
    
    def setup_general_tab(self, parent):
        """Setup the general settings tab"""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Application theme
        ttk.Label(frame, text="Application Theme:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)
        
        self.theme_var = tk.StringVar(value=self.current_values["ui_theme"])
        theme_frame = ttk.Frame(frame)
        theme_frame.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, value="light").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, value="dark").pack(side=tk.LEFT, padx=10)
        
        # Font size
        ttk.Label(frame, text="UI Font Size:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        font_frame = ttk.Frame(frame)
        font_frame.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        self.font_size_var = tk.StringVar(value=self.current_values["ui_font_size"])
        ttk.Spinbox(font_frame, from_=8, to=16, width=5, textvariable=self.font_size_var).pack(side=tk.LEFT, padx=5)
        
        # Number of worker processes
        ttk.Label(frame, text="Worker Processes:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=10)
        
        workers_frame = ttk.Frame(frame)
        workers_frame.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        self.workers_var = tk.StringVar(value=self.current_values["workers"])
        ttk.Spinbox(workers_frame, from_=1, to=16, width=5, textvariable=self.workers_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(workers_frame, text="(Restart required to apply)").pack(side=tk.LEFT, padx=5)
    
    def setup_api_tab(self, parent):
        """Setup the API settings tab"""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # OpenAI API settings
        openai_frame = ttk.LabelFrame(frame, text="OpenAI API Settings")
        openai_frame.pack(fill=tk.X, pady=10)
        
        # OpenAI API Key
        ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.openai_key_var = tk.StringVar(value=self.current_values["openai_key"])
        openai_key_entry = ttk.Entry(openai_frame, textvariable=self.openai_key_var, width=50, show="*")
        openai_key_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.show_openai_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(openai_frame, text="Show API Key", variable=self.show_openai_key_var, 
                      command=lambda: openai_key_entry.config(show="" if self.show_openai_key_var.get() else "*")).grid(
                          row=0, column=2, sticky=tk.W, padx=10, pady=5)
        
        # OpenAI Model
        ttk.Label(openai_frame, text="Default Model:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.openai_model_var = tk.StringVar(value=self.current_values["openai_model"])
        ttk.Combobox(openai_frame, textvariable=self.openai_model_var, values=[
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ], width=20).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Anthropic API settings
        anthropic_frame = ttk.LabelFrame(frame, text="Anthropic API Settings")
        anthropic_frame.pack(fill=tk.X, pady=10)
        
        # Anthropic API Key
        ttk.Label(anthropic_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.anthropic_key_var = tk.StringVar(value=self.current_values["anthropic_key"])
        anthropic_key_entry = ttk.Entry(anthropic_frame, textvariable=self.anthropic_key_var, width=50, show="*")
        anthropic_key_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.show_anthropic_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(anthropic_frame, text="Show API Key", variable=self.show_anthropic_key_var, 
                      command=lambda: anthropic_key_entry.config(show="" if self.show_anthropic_key_var.get() else "*")).grid(
                          row=0, column=2, sticky=tk.W, padx=10, pady=5)
        
        # Anthropic Model
        ttk.Label(anthropic_frame, text="Default Model:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.anthropic_model_var = tk.StringVar(value=self.current_values["anthropic_model"])
        ttk.Combobox(anthropic_frame, textvariable=self.anthropic_model_var, values=[
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307",
            "claude-2.1"
        ], width=25).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Hugging Face API settings
        hf_frame = ttk.LabelFrame(frame, text="Hugging Face API Settings")
        hf_frame.pack(fill=tk.X, pady=10)
        
        # Hugging Face API Key
        ttk.Label(hf_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.huggingface_key_var = tk.StringVar(value=self.current_values["huggingface_key"])
        hf_key_entry = ttk.Entry(hf_frame, textvariable=self.huggingface_key_var, width=50, show="*")
        hf_key_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.show_hf_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(hf_frame, text="Show API Key", variable=self.show_hf_key_var, 
                      command=lambda: hf_key_entry.config(show="" if self.show_hf_key_var.get() else "*")).grid(
                          row=0, column=2, sticky=tk.W, padx=10, pady=5)
    
    def setup_db_tab(self, parent):
        """Setup the database settings tab"""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Database connection settings
        settings_frame = ttk.LabelFrame(frame, text="Database Connection Settings")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Database name
        ttk.Label(settings_frame, text="Database Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.db_name_var = tk.StringVar(value=self.current_values["db_name"])
        ttk.Entry(settings_frame, textvariable=self.db_name_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Database user
        ttk.Label(settings_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.db_user_var = tk.StringVar(value=self.current_values["db_user"])
        ttk.Entry(settings_frame, textvariable=self.db_user_var, width=30).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Database password
        ttk.Label(settings_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.db_password_var = tk.StringVar(value=self.current_values["db_password"])
        password_entry = ttk.Entry(settings_frame, textvariable=self.db_password_var, width=30, show="*")
        password_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Show Password", variable=self.show_password_var, 
                      command=lambda: password_entry.config(show="" if self.show_password_var.get() else "*")).grid(
                          row=2, column=2, sticky=tk.W, padx=10, pady=5)
        
        # Database host
        ttk.Label(settings_frame, text="Host:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.db_host_var = tk.StringVar(value=self.current_values["db_host"])
        ttk.Entry(settings_frame, textvariable=self.db_host_var, width=30).grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Database port
        ttk.Label(settings_frame, text="Port:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.db_port_var = tk.StringVar(value=self.current_values["db_port"])
        ttk.Entry(settings_frame, textvariable=self.db_port_var, width=10).grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Connection test button
        ttk.Button(settings_frame, text="Test Connection", command=self.test_db_connection).grid(
            row=5, column=1, sticky=tk.E, padx=10, pady=10)
        
        # Warning message
        warning_frame = ttk.LabelFrame(frame, text="Important Note")
        warning_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(warning_frame, text="""
Changes to database settings require an application restart to take effect.
The application will update the .env file but will continue to use the current 
connection until restarted.
        """, foreground="red").pack(padx=10, pady=10, fill=tk.X)
    
    def setup_paths_tab(self, parent):
        """Setup the paths settings tab"""
        frame = ttk.Frame(parent, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Data directories settings
        paths_frame = ttk.LabelFrame(frame, text="Data Directories")
        paths_frame.pack(fill=tk.X, pady=10)
        
        # Input directory
        ttk.Label(paths_frame, text="Plan Input Directory:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        input_frame = ttk.Frame(paths_frame)
        input_frame.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.input_dir_var = tk.StringVar(value=self.current_values["input_dir"])
        ttk.Entry(input_frame, textvariable=self.input_dir_var, width=40).pack(side=tk.LEFT)
        ttk.Button(input_frame, text="Browse...", command=lambda: self.browse_directory("input_dir")).pack(side=tk.LEFT, padx=5)
        
        # Output directory
        ttk.Label(paths_frame, text="Plan Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        output_frame = ttk.Frame(paths_frame)
        output_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.output_dir_var = tk.StringVar(value=self.current_values["output_dir"])
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=40).pack(side=tk.LEFT)
        ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_directory("output_dir")).pack(side=tk.LEFT, padx=5)
        
        # Plan directory
        ttk.Label(paths_frame, text="General Plan Directory:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        plan_frame = ttk.Frame(paths_frame)
        plan_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.plan_dir_var = tk.StringVar(value=self.current_values["plan_dir"])
        ttk.Entry(plan_frame, textvariable=self.plan_dir_var, width=40).pack(side=tk.LEFT)
        ttk.Button(plan_frame, text="Browse...", command=lambda: self.browse_directory("plan_dir")).pack(side=tk.LEFT, padx=5)
        
        # Directory structure information
        info_frame = ttk.LabelFrame(frame, text="Directory Structure Information")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text="""
• Plan Input Directory: Where new compensation plans are uploaded for processing
• Plan Output Directory: Where processed plans and analysis results are saved
• General Plan Directory: Parent directory for all plan-related data (optional)

These directories are used by the Asset Analyzer for AI-powered compensation plan analysis.
        """, justify=tk.LEFT).pack(padx=10, pady=10, fill=tk.X)
    
    def browse_directory(self, var_name):
        """Open a directory browser and update the corresponding variable"""
        directory = filedialog.askdirectory(title=f"Select {var_name.replace('_', ' ').title()}")
        if directory:
            if var_name == "input_dir":
                self.input_dir_var.set(directory)
            elif var_name == "output_dir":
                self.output_dir_var.set(directory)
            elif var_name == "plan_dir":
                self.plan_dir_var.set(directory)
    
    def test_db_connection(self):
        """Test the database connection with the current settings"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                dbname=self.db_name_var.get(),
                user=self.db_user_var.get(),
                password=self.db_password_var.get(),
                host=self.db_host_var.get(),
                port=self.db_port_var.get()
            )
            conn.close()
            messagebox.showinfo("Connection Test", "Database connection successful!")
        except Exception as e:
            messagebox.showerror("Connection Test", f"Failed to connect to database: {e}")
    
    def save_settings(self):
        """Save the settings to the .env file"""
        # Update current values from UI
        self.current_values.update({
            "openai_key": self.openai_key_var.get(),
            "openai_model": self.openai_model_var.get(),
            "anthropic_key": self.anthropic_key_var.get(),
            "anthropic_model": self.anthropic_model_var.get(),
            "huggingface_key": self.huggingface_key_var.get(),
            "workers": self.workers_var.get(),
            "db_name": self.db_name_var.get(),
            "db_user": self.db_user_var.get(),
            "db_password": self.db_password_var.get(),
            "db_host": self.db_host_var.get(),
            "db_port": self.db_port_var.get(),
            "input_dir": self.input_dir_var.get(),
            "output_dir": self.output_dir_var.get(),
            "plan_dir": self.plan_dir_var.get(),
            "ui_theme": self.theme_var.get(),
            "ui_font_size": self.font_size_var.get()
        })
        
        # Check if any values have changed
        if self.current_values == self.original_values:
            messagebox.showinfo("Settings", "No changes were made.")
            return
        
        try:
            # Create .env file if it doesn't exist
            if not os.path.exists(self.env_file_path):
                with open(self.env_file_path, 'w') as f:
                    f.write("# KPMG Edge Environment Configuration\n\n")
            
            # Update the .env file
            set_key(self.env_file_path, "OPENAI_API_KEY", self.current_values["openai_key"])
            set_key(self.env_file_path, "OPENAI_MODEL", self.current_values["openai_model"])
            set_key(self.env_file_path, "ANTHROPIC_API_KEY", self.current_values["anthropic_key"])
            set_key(self.env_file_path, "ANTHROPIC_MODEL", self.current_values["anthropic_model"])
            set_key(self.env_file_path, "HUGGINGFACE_API_KEY", self.current_values["huggingface_key"])
            set_key(self.env_file_path, "WORKERS", self.current_values["workers"])
            set_key(self.env_file_path, "DB_NAME", self.current_values["db_name"])
            set_key(self.env_file_path, "DB_USER", self.current_values["db_user"])
            set_key(self.env_file_path, "DB_PASSWORD", self.current_values["db_password"])
            set_key(self.env_file_path, "DB_HOST", self.current_values["db_host"])
            set_key(self.env_file_path, "DB_PORT", self.current_values["db_port"])
            set_key(self.env_file_path, "PLAN_INPUT_DIR", self.current_values["input_dir"])
            set_key(self.env_file_path, "PLAN_OUTPUT_DIR", self.current_values["output_dir"])
            set_key(self.env_file_path, "PLAN_DIR", self.current_values["plan_dir"])
            set_key(self.env_file_path, "UI_THEME", self.current_values["ui_theme"])
            set_key(self.env_file_path, "UI_FONT_SIZE", self.current_values["ui_font_size"])
            
            # Update the original values to match current
            self.original_values = self.current_values.copy()
            
            messagebox.showinfo("Settings", "Settings saved successfully.\n\nSome changes may require an application restart to take effect.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def reset_defaults(self):
        """Reset all settings to default values"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            # Set default values
            default_values = {
                "openai_key": "",
                "openai_model": "gpt-4o",
                "anthropic_key": "",
                "anthropic_model": "claude-3-opus-20240229",
                "huggingface_key": "",
                "workers": "4",
                "db_name": "edge_db",
                "db_user": "postgres",
                "db_password": "",
                "db_host": "localhost",
                "db_port": "5432",
                "input_dir": "",
                "output_dir": "",
                "plan_dir": "",
                "ui_theme": "light",
                "ui_font_size": "10"
            }
            
            # Update UI
            self.openai_key_var.set(default_values["openai_key"])
            self.openai_model_var.set(default_values["openai_model"])
            self.anthropic_key_var.set(default_values["anthropic_key"])
            self.anthropic_model_var.set(default_values["anthropic_model"])
            self.huggingface_key_var.set(default_values["huggingface_key"])
            self.workers_var.set(default_values["workers"])
            self.db_name_var.set(default_values["db_name"])
            self.db_user_var.set(default_values["db_user"])
            self.db_password_var.set(default_values["db_password"])
            self.db_host_var.set(default_values["db_host"])
            self.db_port_var.set(default_values["db_port"])
            self.input_dir_var.set(default_values["input_dir"])
            self.output_dir_var.set(default_values["output_dir"])
            self.plan_dir_var.set(default_values["plan_dir"])
            self.theme_var.set(default_values["ui_theme"])
            self.font_size_var.set(default_values["ui_font_size"])
    
    def cancel_changes(self):
        """Cancel changes and reset to original values"""
        # If changes have been made, ask for confirmation
        current = {
            "openai_key": self.openai_key_var.get(),
            "openai_model": self.openai_model_var.get(),
            "anthropic_key": self.anthropic_key_var.get(),
            "anthropic_model": self.anthropic_model_var.get(),
            "huggingface_key": self.huggingface_key_var.get(),
            "workers": self.workers_var.get(),
            "db_name": self.db_name_var.get(),
            "db_user": self.db_user_var.get(),
            "db_password": self.db_password_var.get(),
            "db_host": self.db_host_var.get(),
            "db_port": self.db_port_var.get(),
            "input_dir": self.input_dir_var.get(),
            "output_dir": self.output_dir_var.get(),
            "plan_dir": self.plan_dir_var.get(),
            "ui_theme": self.theme_var.get(),
            "ui_font_size": self.font_size_var.get()
        }
        
        if current != self.original_values:
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Are you sure you want to discard them?"):
                return
        
        # Refresh to original view
        self.display()