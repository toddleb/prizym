"""
Main entry point for the KPMG Edge application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("main")

# Import UI components
from ui.styles import StyleManager
from ui.sidebar import Sidebar
from ui.topbar import Topbar
from ui.dashboard import Dashboard

# Import modules
from modules.project_module import ProjectModule
from modules.asset_analyzer import AssetAnalyzerModule
from modules.settings_module import SettingsModule

# Import project management modules
from modules.project_integration import ProjectManagementModule
from modules.resource_module import ResourceModule
from modules.timeline_module import TimelineModule
from modules.task_module import TaskModule
from modules.report_module import ReportModule
# Make sure to import the new modules


# Import utilities
from utils.config import config
from utils.database import DatabaseManager
from utils.database_schema import CREATE_TABLES  # Add this line




class KPMGEdgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KPMG Edge - The Consultant's Toolkit for SPM Delivery")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        logger.info("Initializing application...")
        
        # Check configuration
        valid_config = config.validate_config()
        if not valid_config:
            logger.warning("Configuration validation failed. Some features may be unavailable.")
        
        # Initialize database connection
        self.db_connected = False
        try:
            self.db_manager = DatabaseManager()
            
            # Check if successfully connected
            if self.db_manager.is_connected():
                # Initialize database tables if needed
                if self.db_manager.init_db():
                    self.db_connected = True
                    logger.info("Database connection established and initialized")
                else:
                    logger.error("Failed to initialize database tables")
            else:
                logger.warning("Application running without database connection")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            self.db_manager = None
            
            # Show dialog if this is a fresh start (not during development)
            if not os.path.exists('.env'):
                messagebox.showwarning(
                    "Database Connection Failed",
                    "Could not connect to the database. The application will run in limited mode.\n\n"
                    "Please configure your database settings in Settings."
                )
        
        # Initialize styles
        self.style_manager = StyleManager(root)
        self.colors = config.get_color_scheme()
        
        logger.info("Setting up main layout...")
        
        # Create main container
        self.setup_main_layout()
        
        # Initialize modules
        self.init_modules()
        
        # Start with dashboard
        self.show_dashboard()
        
        logger.info("Application initialized successfully!")
    
    def setup_main_layout(self):
        """Set up the main application layout"""
        # Main container
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize sidebar
        self.sidebar = Sidebar(self.main_container, self.colors, self.handle_navigation)
        
        # Content container (right side)
        self.content_container = ttk.Frame(self.main_container, style='Content.TFrame')
        
        # Add to main container
        self.main_container.add(self.sidebar.frame, weight=0)
        self.main_container.add(self.content_container, weight=3)
        
        # Top bar for functional modules
        self.topbar = Topbar(self.content_container, self.colors)
        
        # Main content area (below top bar)
        self.content_frame = ttk.Frame(self.content_container, style='Content.TFrame')
        self.content_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def init_modules(self):
        """Initialize the application modules"""
        logger.info("Initializing modules...")
        
        # Initialize original modules
        self.project_module = ProjectModule(self.content_frame, self.colors, self.db_manager)
        self.asset_analyzer = AssetAnalyzerModule(self.content_frame, self.colors)
        self.settings_module = SettingsModule(self.content_frame, self.colors)
        
        # Initialize new project management modules
        self.project_integration = ProjectManagementModule(self.content_frame, self.colors, self.db_manager)
        self.resource_module = ResourceModule(self.content_frame, self.colors, self.db_manager)
        self.timeline_module = TimelineModule(self.content_frame, self.colors, self.db_manager)
        self.task_module = TaskModule(self.content_frame, self.colors, self.db_manager)
        self.report_module = ReportModule(self.content_frame, self.colors, self.db_manager)
    
    def handle_navigation(self, section, item=None):
        """Handle navigation events from sidebar"""
        logger.info(f"Navigation: {section} - {item}")
        self.clear_content()
        
        if section == "Dashboard":
            self.show_dashboard()
        elif section == "Project Management":
            if item == "Current Projects":
                self.show_current_projects()
            elif item == "New Project":
                self.show_new_project()
            elif item == "Project Dashboard":
                self.project_integration.show_dashboard()
            elif item == "Resources":
                self.show_resource_management()
            elif item == "Tasks":
                self.task_module.show_task_dashboard()
            elif item == "Timeline":
                self.show_timeline_selection()
            elif item == "Reports":
                self.report_module.show_reports_dashboard()
        elif section == "Resource Management":
            if item == "Team Allocation":
                self.show_team_allocation()
            elif item == "Resource Planning":
                self.show_resource_planning()
        elif section == "Training":
            if item == "SPM 101":
                # This is a submenu, so we don't handle it directly
                pass
            elif item == "Sales Planning":
                self.show_sales_planning_training()
            elif item == "Incentive Compensation Management":
                self.show_icm_training()
            elif item == "Sales Intelligence":
                self.show_sales_intelligence_training()
            elif item == "KPMG SPM TOM":
                self.show_spm_tom()
            elif item == "KPMG Edge":
                self.show_edge_training()
        elif section == "Settings":
            self.show_settings()
    
    def clear_content(self):
        """Clear the current content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show the dashboard view"""
        self.topbar.set_title("Dashboard")
        dashboard = Dashboard(self.content_frame, self.colors)
        dashboard.display()
        
        # Show config warning if needed
        if not config.validate_config():
            ttk.Label(
                self.content_frame, 
                text="⚠️ Some configuration settings are missing. Go to Settings to complete setup.",
                foreground="orange",
                font=("Arial", 10, "bold")
            ).pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
    
    # Project Management functions
    def show_current_projects(self):
        """Show current projects view"""
        self.topbar.set_title("Current Projects")
        
        # Check if database is available for this feature
        if not self.db_connected:
            self.show_db_required_message("Current Projects")
            return
            
        self.project_module.show_current_projects()
    
    def show_new_project(self):
        """Show new project form"""
        self.topbar.set_title("New Project")
        
        # Check if database is available for this feature
        if not self.db_connected:
            self.show_db_required_message("New Project")
            return
            
        self.project_module.show_new_project()
    
    def show_resource_management(self):
        """Show the resource management interface"""
        self.topbar.set_title("Resource Management")
        
        # Check if database is available for this feature
        if not self.db_connected:
            self.show_db_required_message("Resource Management")
            return
            
        self.resource_module.show_resource_management()
    
    def show_timeline_selection(self):
        """Show a dialog to select which project timeline to view"""
        # This is a simple implementation - in a real app, we'd show a project selection dialog
        
        # For now, let's just pass a default project ID
        self.show_project_timeline(1)
    
    def show_project_timeline(self, project_id):
        """Show the timeline for a specific project"""
        self.topbar.set_title("Project Timeline")
        
        # Check if database is available for this feature
        if not self.db_connected:
            self.show_db_required_message("Project Timeline")
            return
            
        self.timeline_module.show_project_timeline(project_id)
    
    def show_asset_analyzer(self):
        """Show asset analyzer module"""
        self.topbar.set_title("Asset Analyzer")
        
        # Check if AI features are configured
        ai_available = False
        if config.OPENAI_API_KEY:
            ai_available = True
        elif config.ANTHROPIC_API_KEY:
            ai_available = True
        elif config.HUGGINGFACE_API_KEY:
            ai_available = True
            
        if not ai_available:
            ttk.Label(
                self.content_frame, 
                text="⚠️ No AI API keys are configured. AI-powered analysis features will be limited.",
                foreground="orange",
                font=("Arial", 10, "bold")
            ).pack(padx=20, pady=10)
            
        self.asset_analyzer.create_ui()

    # Settings
    def show_settings(self):
        """Show the settings interface"""
        self.topbar.set_title("Settings")
        self.settings_module.display()
    
    def show_db_required_message(self, feature_name):
        """Show a message that this feature requires database connection"""
        frame = ttk.Frame(self.content_frame, padding=50)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text=f"⚠️ {feature_name} requires database connection",
            font=("Arial", 16, "bold"),
            foreground="orange"
        ).pack(pady=20)
        
        ttk.Label(
            frame, 
            text="Database connection is not available. Please configure your database settings\n"
                 "in Settings and restart the application.",
            font=("Arial", 12)
        ).pack(pady=10)
        
        ttk.Button(
            frame, 
            text="Go to Settings",
            command=self.show_settings
        ).pack(pady=20)
        
    # Placeholder methods for other functions
    def show_team_allocation(self):
        self.topbar.set_title("Team Allocation")
        ttk.Label(self.content_frame, text="Team Allocation", font=("Arial", 24)).pack(pady=20)
    
    def show_resource_planning(self):
        self.topbar.set_title("Resource Planning")
        ttk.Label(self.content_frame, text="Resource Planning", font=("Arial", 24)).pack(pady=20)
    
    def show_sales_planning_training(self):
        self.topbar.set_title("Sales Planning Training")
        ttk.Label(self.content_frame, text="Sales Planning Training", font=("Arial", 24)).pack(pady=20)
    
    def show_icm_training(self):
        self.topbar.set_title("ICM Training")
        ttk.Label(self.content_frame, text="Incentive Compensation Management Training", font=("Arial", 24)).pack(pady=20)
    
    def show_sales_intelligence_training(self):
        self.topbar.set_title("Sales Intelligence Training")
        ttk.Label(self.content_frame, text="Sales Intelligence Training", font=("Arial", 24)).pack(pady=20)
    
    def show_spm_tom(self):
        self.topbar.set_title("KPMG SPM TOM Framework")
        ttk.Label(self.content_frame, text="KPMG SPM TOM Framework", font=("Arial", 24)).pack(pady=20)
    
    def show_edge_training(self):
        self.topbar.set_title("KPMG Edge Training")
        ttk.Label(self.content_frame, text="KPMG Edge Training", font=("Arial", 24)).pack(pady=20)
        
    def __del__(self):
        """Clean up resources on application exit"""
        try:
            if hasattr(self, 'db_manager') and self.db_manager:
                self.db_manager.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

# Main entry point
if __name__ == "__main__":
    try:
        logger.info("Application starting...")
        
        # Create .env file if it doesn't exist
        if not os.path.exists('.env'):
            try:
                with open('.env', 'w') as f:
                    f.write("# KPMG Edge Environment Configuration\n\n")
                logger.info("Created new .env file")
            except Exception as e:
                logger.error(f"Failed to create .env file: {e}")
        
        logger.info("Creating main window...")
        root = tk.Tk()
        logger.info("Initializing application...")
        app = KPMGEdgeApp(root)
        logger.info("Starting main event loop...")
        root.mainloop()
        logger.info("Application closed normally")
    except Exception as e:
        logger.critical(f"Application error: {e}", exc_info=True)
        # Show error to user if UI is available
        if 'root' in locals() and root:
            messagebox.showerror("Error", f"An error occurred: {e}\n\nSee log for details.")
        sys.exit(1)