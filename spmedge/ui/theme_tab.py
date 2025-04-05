"""
Theme tab for SPM Edge UI - Customize the application appearance
"""
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import json
import os

class ThemeTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Theme")
        
        # Default theme settings
        self.theme_settings = {
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
        
        # Load saved theme if available
        self.theme_file = os.path.join(os.path.expanduser("~"), ".spm_edge_theme.json")
        self.load_theme()
        
        # Create UI components
        self.create_header()
        self.create_theme_options()
        self.create_preview()
        self.create_actions()
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="Theme Customization", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Customize the appearance of the application"
        ).pack(anchor=tk.W)
    
    def create_theme_options(self):
        """Create theme customization options"""
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Split into left and right panels
        left_panel = ttk.Frame(options_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_panel = ttk.Frame(options_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Theme Mode section (left panel)
        mode_frame = ttk.LabelFrame(left_panel, text="Theme Mode")
        mode_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        self.theme_mode_var = tk.StringVar(value=self.theme_settings["theme_mode"])
        ttk.Radiobutton(
            mode_frame,
            text="Light Mode",
            value="light",
            variable=self.theme_mode_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        ttk.Radiobutton(
            mode_frame,
            text="Dark Mode",
            value="dark",
            variable=self.theme_mode_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        ttk.Radiobutton(
            mode_frame,
            text="System Default",
            value="system",
            variable=self.theme_mode_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        # Colors section (left panel)
        colors_frame = ttk.LabelFrame(left_panel, text="Colors")
        colors_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        # Primary Color
        primary_frame = ttk.Frame(colors_frame)
        primary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(primary_frame, text="Primary Color:").pack(side=tk.LEFT)
        
        self.primary_color_var = tk.StringVar(value=self.theme_settings["primary_color"])
        primary_entry = ttk.Entry(primary_frame, textvariable=self.primary_color_var, width=10)
        primary_entry.pack(side=tk.LEFT, padx=5)
        
        self.primary_color_btn = tk.Button(
            primary_frame, 
            bg=self.primary_color_var.get(),
            width=3,
            command=lambda: self.choose_color("primary")
        )
        self.primary_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Secondary Color
        secondary_frame = ttk.Frame(colors_frame)
        secondary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(secondary_frame, text="Secondary Color:").pack(side=tk.LEFT)
        
        self.secondary_color_var = tk.StringVar(value=self.theme_settings["secondary_color"])
        secondary_entry = ttk.Entry(secondary_frame, textvariable=self.secondary_color_var, width=10)
        secondary_entry.pack(side=tk.LEFT, padx=5)
        
        self.secondary_color_btn = tk.Button(
            secondary_frame, 
            bg=self.secondary_color_var.get(),
            width=3,
            command=lambda: self.choose_color("secondary")
        )
        self.secondary_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Accent Color
        accent_frame = ttk.Frame(colors_frame)
        accent_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(accent_frame, text="Accent Color:").pack(side=tk.LEFT)
        
        self.accent_color_var = tk.StringVar(value=self.theme_settings["accent_color"])
        accent_entry = ttk.Entry(accent_frame, textvariable=self.accent_color_var, width=10)
        accent_entry.pack(side=tk.LEFT, padx=5)
        
        self.accent_color_btn = tk.Button(
            accent_frame, 
            bg=self.accent_color_var.get(),
            width=3,
            command=lambda: self.choose_color("accent")
        )
        self.accent_color_btn.pack(side=tk.LEFT, padx=5)
        
        # Font settings (right panel)
        font_frame = ttk.LabelFrame(right_panel, text="Font Settings")
        font_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        # Font Family
        font_family_frame = ttk.Frame(font_frame)
        font_family_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(font_family_frame, text="Font Family:").pack(side=tk.LEFT)
        
        self.font_family_var = tk.StringVar(value=self.theme_settings["font_family"])
        font_combo = ttk.Combobox(font_family_frame, textvariable=self.font_family_var, width=15)
        font_combo["values"] = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Tahoma"]
        font_combo.pack(side=tk.LEFT, padx=5)
        font_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        # Font Size
        font_size_frame = ttk.Frame(font_frame)
        font_size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(font_size_frame, text="Font Size:").pack(side=tk.LEFT)
        
        self.font_size_var = tk.IntVar(value=self.theme_settings["font_size"])
        font_size_spinbox = ttk.Spinbox(
            font_size_frame, 
            from_=8, 
            to=16, 
            textvariable=self.font_size_var, 
            width=5,
            command=self.update_preview
        )
        font_size_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Button Style section (right panel)
        button_frame = ttk.LabelFrame(right_panel, text="Button Style")
        button_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        self.button_style_var = tk.StringVar(value=self.theme_settings["button_style"])
        ttk.Radiobutton(
            button_frame,
            text="Default",
            value="default",
            variable=self.button_style_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        ttk.Radiobutton(
            button_frame,
            text="Rounded",
            value="rounded",
            variable=self.button_style_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        ttk.Radiobutton(
            button_frame,
            text="Flat",
            value="flat",
            variable=self.button_style_var,
            command=self.update_preview
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        # Custom Colors section (right panel)
        custom_frame = ttk.LabelFrame(right_panel, text="Custom Colors")
        custom_frame.pack(fill=tk.X, pady=10, ipady=5)
        
        self.use_custom_colors_var = tk.BooleanVar(value=self.theme_settings["use_custom_colors"])
        ttk.Checkbutton(
            custom_frame,
            text="Use Custom Colors",
            variable=self.use_custom_colors_var,
            command=self.toggle_custom_colors
        ).pack(anchor=tk.W, padx=10, pady=2)
        
        # Custom Background
        self.custom_bg_frame = ttk.Frame(custom_frame)
        self.custom_bg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.custom_bg_frame, text="Background:").pack(side=tk.LEFT)
        
        self.custom_bg_var = tk.StringVar(value=self.theme_settings["custom_background"])
        custom_bg_entry = ttk.Entry(self.custom_bg_frame, textvariable=self.custom_bg_var, width=10)
        custom_bg_entry.pack(side=tk.LEFT, padx=5)
        
        self.custom_bg_btn = tk.Button(
            self.custom_bg_frame, 
            bg=self.custom_bg_var.get(),
            width=3,
            command=lambda: self.choose_color("custom_bg")
        )
        self.custom_bg_btn.pack(side=tk.LEFT, padx=5)
        
        # Custom Foreground
        self.custom_fg_frame = ttk.Frame(custom_frame)
        self.custom_fg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.custom_fg_frame, text="Text Color:").pack(side=tk.LEFT)
        
        self.custom_fg_var = tk.StringVar(value=self.theme_settings["custom_foreground"])
        custom_fg_entry = ttk.Entry(self.custom_fg_frame, textvariable=self.custom_fg_var, width=10)
        custom_fg_entry.pack(side=tk.LEFT, padx=5)
        
        self.custom_fg_btn = tk.Button(
            self.custom_fg_frame, 
            bg=self.custom_fg_var.get(),
            width=3,
            command=lambda: self.choose_color("custom_fg")
        )
        self.custom_fg_btn.pack(side=tk.LEFT, padx=5)
        
        # Set initial state of custom color fields
        self.toggle_custom_colors()
    
    def create_preview(self):
        """Create theme preview area"""
        preview_frame = ttk.LabelFrame(self.frame, text="Theme Preview")
        preview_frame.pack(fill=tk.X, padx=20, pady=10, ipady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, height=150, highlightthickness=0)
        self.preview_canvas.pack(fill=tk.X)
        
        # Initial preview
        self.update_preview()
    
    def create_actions(self):
        """Create action buttons for theme management"""
        actions_frame = ttk.Frame(self.frame)
        actions_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(
            actions_frame,
            text="Restore Defaults",
            command=self.restore_defaults
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Apply Theme",
            command=self.apply_theme
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="Save Theme",
            command=self.save_theme
        ).pack(side=tk.RIGHT, padx=5)
    
    def choose_color(self, target):
        """Open color picker and update selected color"""
        if target == "primary":
            current_color = self.primary_color_var.get()
            title = "Choose Primary Color"
        elif target == "secondary":
            current_color = self.secondary_color_var.get()
            title = "Choose Secondary Color"
        elif target == "accent":
            current_color = self.accent_color_var.get()
            title = "Choose Accent Color"
        elif target == "custom_bg":
            current_color = self.custom_bg_var.get()
            title = "Choose Background Color"
        elif target == "custom_fg":
            current_color = self.custom_fg_var.get()
            title = "Choose Text Color"
        else:
            return
        
        color = colorchooser.askcolor(color=current_color, title=title)
        if color[1]:  # Color selected (not cancelled)
            if target == "primary":
                self.primary_color_var.set(color[1])
                self.primary_color_btn.config(bg=color[1])
            elif target == "secondary":
                self.secondary_color_var.set(color[1])
                self.secondary_color_btn.config(bg=color[1])
            elif target == "accent":
                self.accent_color_var.set(color[1])
                self.accent_color_btn.config(bg=color[1])
            elif target == "custom_bg":
                self.custom_bg_var.set(color[1])
                self.custom_bg_btn.config(bg=color[1])
            elif target == "custom_fg":
                self.custom_fg_var.set(color[1])
                self.custom_fg_btn.config(bg=color[1])
            
            # Update preview
            self.update_preview()
    
    def toggle_custom_colors(self):
        """Enable/disable custom color settings based on checkbox"""
        enabled = self.use_custom_colors_var.get()
        state = "normal" if enabled else "disabled"
        
        # Update widget states
        for widget in self.custom_bg_frame.winfo_children():
            if isinstance(widget, (ttk.Entry, tk.Button)):
                if isinstance(widget, ttk.Entry):
                    widget.config(state=state)
                elif isinstance(widget, tk.Button):
                    widget.config(state=state)
        
        for widget in self.custom_fg_frame.winfo_children():
            if isinstance(widget, (ttk.Entry, tk.Button)):
                if isinstance(widget, ttk.Entry):
                    widget.config(state=state)
                elif isinstance(widget, tk.Button):
                    widget.config(state=state)
    
    def update_preview(self):
        """Update the theme preview"""
        # Check if preview_canvas exists yet
        if not self.preview_canvas:
            return
        
        # Clear canvas
        self.preview_canvas.delete("all")
    
        # Get current theme settings
        theme_mode = self.theme_mode_var.get()
        primary_color = self.primary_color_var.get()
        secondary_color = self.secondary_color_var.get()
        accent_color = self.accent_color_var.get()
        button_style = self.button_style_var.get()
        use_custom = self.use_custom_colors_var.get()
        
        # Determine background and foreground colors based on theme mode
        if use_custom:
            bg_color = self.custom_bg_var.get()
            fg_color = self.custom_fg_var.get()
        else:
            if theme_mode == "dark":
                bg_color = "#343a40"
                fg_color = "#f8f9fa"
            else:  # light or system
                bg_color = "#f8f9fa"
                fg_color = "#343a40"
        
        # Draw background
        width = self.preview_canvas.winfo_width() or 400
        height = self.preview_canvas.winfo_height() or 150
        self.preview_canvas.config(bg=bg_color)
        
        # Draw header
        self.preview_canvas.create_rectangle(
            0, 0, width, 40,
            fill=primary_color,
            outline=""
        )
        
        self.preview_canvas.create_text(
            20, 20,
            text="Application Title",
            fill="#ffffff",
            anchor=tk.W,
            font=(self.font_family_var.get(), self.font_size_var.get() + 2, "bold")
        )
        
        # Draw sidebar
        self.preview_canvas.create_rectangle(
            0, 40, 100, height,
            fill=secondary_color,
            outline=""
        )
        
        # Draw content area text
        self.preview_canvas.create_text(
            110, 50,
            text="Content Area",
            fill=fg_color,
            anchor=tk.NW,
            font=(self.font_family_var.get(), self.font_size_var.get())
        )
        
        # Draw buttons based on style
        if button_style == "rounded":
            # Rounded primary button
            self.preview_canvas.create_oval(
                120, 80, 130, 105,
                fill=primary_color,
                outline=""
            )
            self.preview_canvas.create_rectangle(
                125, 80, 195, 105,
                fill=primary_color,
                outline=""
            )
            self.preview_canvas.create_oval(
                190, 80, 200, 105,
                fill=primary_color,
                outline=""
            )
            
            # Rounded accent button
            self.preview_canvas.create_oval(
                210, 80, 220, 105,
                fill=accent_color,
                outline=""
            )
            self.preview_canvas.create_rectangle(
                215, 80, 285, 105,
                fill=accent_color,
                outline=""
            )
            self.preview_canvas.create_oval(
                280, 80, 290, 105,
                fill=accent_color,
                outline=""
            )
        
        elif button_style == "flat":
            # Flat primary button
            self.preview_canvas.create_rectangle(
                120, 80, 200, 105,
                fill=primary_color,
                outline=""
            )
            
            # Flat accent button
            self.preview_canvas.create_rectangle(
                210, 80, 290, 105,
                fill=accent_color,
                outline=""
            )
        
        else:  # default
            # Default primary button
            self.preview_canvas.create_rectangle(
                120, 80, 200, 105,
                fill=primary_color,
                outline="#000000",
                width=1
            )
            
            # Default accent button
            self.preview_canvas.create_rectangle(
                210, 80, 290, 105,
                fill=accent_color,
                outline="#000000",
                width=1
            )
        
        # Button text
        self.preview_canvas.create_text(
            160, 92,
            text="Primary Button",
            fill="#ffffff",
            font=(self.font_family_var.get(), self.font_size_var.get() - 1)
        )
        
        self.preview_canvas.create_text(
            250, 92,
            text="Accent Button",
            fill="#212529",
            font=(self.font_family_var.get(), self.font_size_var.get() - 1)
        )
        
        # Draw menu items in sidebar
        menu_items = ["Dashboard", "Documents", "Analysis", "Reports"]
        for i, item in enumerate(menu_items):
            y_pos = 50 + i * 25
            self.preview_canvas.create_text(
                10, y_pos,
                text="•",
                fill="#ffffff",
                anchor=tk.W,
                font=(self.font_family_var.get(), self.font_size_var.get())
            )
            self.preview_canvas.create_text(
                25, y_pos,
                text=item,
                fill="#ffffff",
                anchor=tk.W,
                font=(self.font_family_var.get(), self.font_size_var.get())
            )
        
    def load_theme(self):
        """Load theme settings from file"""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r') as f:
                    loaded_theme = json.load(f)
                    # Update theme settings with loaded values
                    for key, value in loaded_theme.items():
                        if key in self.theme_settings:
                            self.theme_settings[key] = value
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load theme settings: {e}")
    
    def save_theme(self):
        """Save theme settings to file"""
        try:
            # Update theme settings from UI variables
            self.theme_settings["theme_mode"] = self.theme_mode_var.get()
            self.theme_settings["primary_color"] = self.primary_color_var.get()
            self.theme_settings["secondary_color"] = self.secondary_color_var.get()
            self.theme_settings["accent_color"] = self.accent_color_var.get()
            self.theme_settings["font_family"] = self.font_family_var.get()
            self.theme_settings["font_size"] = self.font_size_var.get()
            self.theme_settings["use_custom_colors"] = self.use_custom_colors_var.get()
            self.theme_settings["custom_background"] = self.custom_bg_var.get()
            self.theme_settings["custom_foreground"] = self.custom_fg_var.get()
            self.theme_settings["button_style"] = self.button_style_var.get()
            
            # Save to file
            with open(self.theme_file, 'w') as f:
                json.dump(self.theme_settings, f, indent=2)
            
            messagebox.showinfo("Success", "Theme settings saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme settings: {e}")
    
    def apply_theme(self):
        """Apply the theme to the application"""
        # Update theme settings from UI variables
        self.theme_settings["theme_mode"] = self.theme_mode_var.get()
        self.theme_settings["primary_color"] = self.primary_color_var.get()
        self.theme_settings["secondary_color"] = self.secondary_color_var.get()
        self.theme_settings["accent_color"] = self.accent_color_var.get()
        self.theme_settings["font_family"] = self.font_family_var.get()
        self.theme_settings["font_size"] = self.font_size_var.get()
        self.theme_settings["use_custom_colors"] = self.use_custom_colors_var.get()
        self.theme_settings["custom_background"] = self.custom_bg_var.get()
        self.theme_settings["custom_foreground"] = self.custom_fg_var.get()
        self.theme_settings["button_style"] = self.button_style_var.get()
        
        # Apply the theme to the application if applicable
        if hasattr(self.app, 'apply_theme'):
            self.app.apply_theme(self.theme_settings)
            messagebox.showinfo("Success", "Theme applied successfully")
        else:
            messagebox.showinfo("Info", "Theme will be applied on next application restart")
    
    def restore_defaults(self):
        """Restore default theme settings"""
        if messagebox.askyesno("Confirm", "Are you sure you want to restore default theme settings?"):
            # Reset to default values
            self.theme_mode_var.set("light")
            self.primary_color_var.set("#007bff")
            self.secondary_color_var.set("#6c757d")
            self.accent_color_var.set("#ffc107")
            self.font_family_var.set("Arial")
            self.font_size_var.set(10)
            self.use_custom_colors_var.set(False)
            self.custom_bg_var.set("#ffffff")
            self.custom_fg_var.set("#212529")
            self.button_style_var.set("default")
            
            # Update color buttons
            self.primary_color_btn.config(bg="#007bff")
            self.secondary_color_btn.config(bg="#6c757d")
            self.accent_color_btn.config(bg="#ffc107")
            self.custom_bg_btn.config(bg="#ffffff")
            self.custom_fg_btn.config(bg="#212529")
            
            # Update custom colors state
            self.toggle_custom_colors()
            
            # Update preview
            self.update_preview()
            
            messagebox.showinfo("Success", "Default theme settings restored.\nClick 'Apply Theme' to apply.")
            