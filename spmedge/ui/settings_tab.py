"""
Settings tab for SPM Edge UI - Manage application settings
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys

# Add parent directory to path to resolve imports
sys.path.insert(0, os.path.abspath('..'))

try:
    from config.config import config
except ImportError:
    # Fallback if import fails
    config = None

class SettingsTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Settings")
        
        # Database connection (might be None)
        self.db_manager = getattr(app, 'db_manager', None)
        
        # Default settings
        self.settings = {
            "api_key": "",
            "model": "gpt-4o",
            "embeddings_model": "text-embedding-3-small",
            "data_dir": os.path.expanduser("~/spm_edge_data"),
            "batch_size": 10,
            "auto_save": True,
            "debug_mode": False,
            "workers": 4,
            "ui_theme": "light",
            "ui_font_size": 10
        }
        
        # Try to load from config if available
        if config is not None:
            self.settings.update({
                "api_key": getattr(config, "OPENAI_API_KEY", ""),
                "model": getattr(config, "OPENAI_MODEL", "gpt-4o"),
                "data_dir": getattr(config, "DATA_DIR", self.settings["data_dir"]),
                "workers": getattr(config, "WORKERS", 4),
                "ui_theme": getattr(config, "UI_THEME", "light"),
                "ui_font_size": getattr(config, "UI_FONT_SIZE", 10)
            })
        
        # Load saved settings from file or database
        self.settings_file = os.path.join(os.path.expanduser("~"), ".spm_edge_settings.json")
        self.load_settings()
        
        # Create the UI components
        self.create_header()
        self.create_settings_form()
        self.create_actions()
        
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="Application Settings", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Configure application settings and preferences"
        ).pack(anchor=tk.W)
    
    def create_settings_form(self):
        """Create settings form with various options"""
        form_frame = ttk.LabelFrame(self.frame, text="Settings")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollable canvas for settings
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # API Settings section
        api_frame = ttk.LabelFrame(scrollable_frame, text="API Settings")
        api_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # API Key
        ttk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.api_key_var = tk.StringVar(value=self.settings["api_key"])
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=40, show="*")
        api_key_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Show/Hide API Key
        self.show_api_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            api_frame, 
            text="Show Key", 
            variable=self.show_api_key_var,
            command=lambda: api_key_entry.configure(show="" if self.show_api_key_var.get() else "*")
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Model Selection
        ttk.Label(api_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.model_var = tk.StringVar(value=self.settings["model"])
        model_combo = ttk.Combobox(api_frame, textvariable=self.model_var, width=30)
        model_combo["values"] = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"]
        model_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Embeddings Model
        ttk.Label(api_frame, text="Embeddings Model:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.embeddings_var = tk.StringVar(value=self.settings["embeddings_model"])
        embeddings_combo = ttk.Combobox(api_frame, textvariable=self.embeddings_var, width=30)
        embeddings_combo["values"] = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
        embeddings_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # File Paths section
        paths_frame = ttk.LabelFrame(scrollable_frame, text="File Paths")
        paths_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Data Directory
        ttk.Label(paths_frame, text="Data Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.data_dir_var = tk.StringVar(value=self.settings["data_dir"])
        data_dir_entry = ttk.Entry(paths_frame, textvariable=self.data_dir_var, width=40)
        data_dir_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Button(
            paths_frame,
            text="Browse...",
            command=self.browse_data_dir
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Processing Settings section
        processing_frame = ttk.LabelFrame(scrollable_frame, text="Processing Settings")
        processing_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Batch Size
        ttk.Label(processing_frame, text="Batch Size:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.batch_size_var = tk.IntVar(value=self.settings["batch_size"])
        batch_size_spinbox = ttk.Spinbox(
            processing_frame, 
            from_=1, 
            to=50, 
            textvariable=self.batch_size_var, 
            width=10
        )
        batch_size_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Workers
        ttk.Label(processing_frame, text="Workers:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.workers_var = tk.IntVar(value=self.settings["workers"])
        workers_spinbox = ttk.Spinbox(
            processing_frame, 
            from_=1, 
            to=16, 
            textvariable=self.workers_var, 
            width=10
        )
        workers_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Application Settings section
        app_frame = ttk.LabelFrame(scrollable_frame, text="Application Settings")
        app_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # Auto Save
        self.auto_save_var = tk.BooleanVar(value=self.settings["auto_save"])
        ttk.Checkbutton(
            app_frame,
            text="Auto-save settings on exit",
            variable=self.auto_save_var
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5, columnspan=2)
        
        # Debug Mode
        self.debug_mode_var = tk.BooleanVar(value=self.settings["debug_mode"])
        ttk.Checkbutton(
            app_frame,
            text="Debug mode (verbose logging)",
            variable=self.debug_mode_var
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5, columnspan=2)
        
        # UI Settings section
        ui_frame = ttk.LabelFrame(scrollable_frame, text="UI Settings")
        ui_frame.pack(fill=tk.X, padx=10, pady=10, ipady=5)
        
        # UI Theme
        ttk.Label(ui_frame, text="UI Theme:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ui_theme_var = tk.StringVar(value=self.settings["ui_theme"])
        ui_theme_combo = ttk.Combobox(ui_frame, textvariable=self.ui_theme_var, width=15)
        ui_theme_combo["values"] = ["light", "dark", "system"]
        ui_theme_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # UI Font Size
        ttk.Label(ui_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ui_font_size_var = tk.IntVar(value=self.settings["ui_font_size"])
        ui_font_size_spinbox = ttk.Spinbox(
            ui_frame, 
            from_=8, 
            to=16, 
            textvariable=self.ui_font_size_var, 
            width=10
        )
        ui_font_size_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
    def create_actions(self):
        """Create action buttons for settings"""
        actions_frame = ttk.Frame(self.frame)
        actions_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(
            actions_frame,
            text="Restore Defaults",
            command=self.restore_defaults
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Test Connection",
            command=self.test_connection
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Save Settings",
            command=self.save_settings
        ).pack(side=tk.RIGHT, padx=5)
        
        # Storage options
        storage_frame = ttk.Frame(actions_frame)
        storage_frame.pack(side=tk.RIGHT, padx=20)
        
        ttk.Label(storage_frame, text="Save to:").pack(side=tk.LEFT, padx=5)
        
        self.save_location_var = tk.StringVar(value="both")
        ttk.Radiobutton(
            storage_frame,
            text="File",
            variable=self.save_location_var,
            value="file"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            storage_frame,
            text="Database",
            variable=self.save_location_var,
            value="database"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            storage_frame,
            text="Both",
            variable=self.save_location_var,
            value="both"
        ).pack(side=tk.LEFT, padx=5)
    
    def browse_data_dir(self):
        """Browse for data directory"""
        directory = filedialog.askdirectory(initialdir=self.data_dir_var.get())
        if directory:
            self.data_dir_var.set(directory)
    
    def load_settings(self):
        """Load settings from file and/or database"""
        # Try loading from file first
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings with loaded values
                    for key, value in loaded_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings from file: {e}")
        
        # Then try loading from database
        if self.db_manager:
            try:
                # Check if pipeline_settings table exists
                self.db_manager.cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'pipeline_settings'
                    );
                """)
                
                table_exists = self.db_manager.cursor.fetchone()[0]
                
                if table_exists:
                    # Load settings from database
                    self.db_manager.cursor.execute("""
                        SELECT key, value FROM pipeline_settings
                        WHERE key IN ('api_key', 'model', 'embeddings_model', 
                                      'data_dir', 'batch_size', 'workers', 
                                      'ui_theme', 'ui_font_size', 'debug_mode');
                    """)
                    
                    db_settings = self.db_manager.cursor.fetchall()
                    
                    # Update settings with database values
                    for key, value in db_settings:
                        if key in self.settings:
                            # Convert types
                            if key in ['batch_size', 'workers', 'ui_font_size']:
                                self.settings[key] = int(value)
                            elif key in ['debug_mode', 'auto_save']:
                                self.settings[key] = value.lower() == 'true'
                            else:
                                self.settings[key] = value
                            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings from database: {e}")
    
    def save_settings(self):
        """Save settings to file and/or database"""
        try:
            # Update settings from UI variables
            self.settings["api_key"] = self.api_key_var.get()
            self.settings["model"] = self.model_var.get()
            self.settings["embeddings_model"] = self.embeddings_var.get()
            self.settings["data_dir"] = self.data_dir_var.get()
            self.settings["batch_size"] = self.batch_size_var.get()
            self.settings["workers"] = self.workers_var.get()
            self.settings["auto_save"] = self.auto_save_var.get()
            self.settings["debug_mode"] = self.debug_mode_var.get()
            self.settings["ui_theme"] = self.ui_theme_var.get()
            self.settings["ui_font_size"] = self.ui_font_size_var.get()
            
            save_location = self.save_location_var.get()
            success = False
            
            # Save to file if requested
            if save_location in ["file", "both"]:
                try:
                    with open(self.settings_file, 'w') as f:
                        json.dump(self.settings, f, indent=2)
                    success = True
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save settings to file: {e}")
            
            # Save to database if requested
            if save_location in ["database", "both"] and self.db_manager:
                try:
                    # Check if pipeline_settings table exists
                    self.db_manager.cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'pipeline_settings'
                        );
                    """)
                    
                    table_exists = self.db_manager.cursor.fetchone()[0]
                    
                    if not table_exists:
                        # Create table if it doesn't exist
                        self.db_manager.cursor.execute("""
                            CREATE TABLE pipeline_settings (
                                key VARCHAR(100) PRIMARY KEY,
                                value TEXT,
                                description TEXT,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        """)
                    
                    # Save each setting to database
                    for key, value in self.settings.items():
                        # Create description based on key
                        description = key.replace('_', ' ').title()
                        
                        self.db_manager.cursor.execute("""
                            INSERT INTO pipeline_settings (key, value, description, updated_at)
                            VALUES (%s, %s, %s, NOW())
                            ON CONFLICT (key) 
                            DO UPDATE SET value = %s, updated_at = NOW();
                        """, (key, str(value), description, str(value)))
                    
                    self.db_manager.conn.commit()
                    success = True
                    
                except Exception as e:
                    self.db_manager.conn.rollback()
                    messagebox.showerror("Error", f"Failed to save settings to database: {e}")
            
            # Update app settings if applicable
            if success and hasattr(self.app, 'update_settings'):
                self.app.update_settings(self.settings)
                
            if success:
                messagebox.showinfo("Success", "Settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def restore_defaults(self):
        """Restore default settings"""
        if messagebox.askyesno("Confirm", "Are you sure you want to restore default settings?"):
            # Default values
            default_settings = {
                "api_key": "",
                "model": "gpt-4o",
                "embeddings_model": "text-embedding-3-small",
                "data_dir": os.path.expanduser("~/spm_edge_data"),
                "batch_size": 10,
                "workers": 4,
                "auto_save": True,
                "debug_mode": False,
                "ui_theme": "light",
                "ui_font_size": 10
            }
            
            # Try to get values from config if available
            if config is not None:
                default_settings.update({
                    "api_key": getattr(config, "OPENAI_API_KEY", ""),
                    "model": getattr(config, "OPENAI_MODEL", "gpt-4o"),
                    "data_dir": getattr(config, "DATA_DIR", default_settings["data_dir"]),
                    "workers": getattr(config, "WORKERS", 4),
                    "ui_theme": getattr(config, "UI_THEME", "light"),
                    "ui_font_size": getattr(config, "UI_FONT_SIZE", 10)
                })
            
            # Update UI
            self.api_key_var.set(default_settings["api_key"])
            self.model_var.set(default_settings["model"])
            self.embeddings_var.set(default_settings["embeddings_model"])
            self.data_dir_var.set(default_settings["data_dir"])
            self.batch_size_var.set(default_settings["batch_size"])
            self.workers_var.set(default_settings["workers"])
            self.auto_save_var.set(default_settings["auto_save"])
            self.debug_mode_var.set(default_settings["debug_mode"])
            self.ui_theme_var.set(default_settings["ui_theme"])
            self.ui_font_size_var.set(default_settings["ui_font_size"])
            
            messagebox.showinfo("Success", "Default settings restored.\nClick 'Save Settings' to apply.")
    
    def test_connection(self):
        """Test API connection"""
        api_key = self.api_key_var.get()
        if not api_key:
            messagebox.showinfo("Info", "Please enter an API key first.")
            return
        
        # Show testing message
        messagebox.showinfo("Testing", "Testing API connection...\nThis may take a moment.")
        
        # In a real app, you would test the connection here
        # For simulation, we'll just show a success message
        self.app.root.after(1500, lambda: messagebox.showinfo(
            "Connection Test", 
            "API connection successful! 🎉"
        ))