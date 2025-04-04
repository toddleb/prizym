import tkinter as tk
from tkinter import ttk

class Dashboard:
    """Dashboard view for the KPMG Edge application"""
    
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
    
    def display(self):
        """Display the dashboard content"""
        frame = ttk.Frame(self.parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = ttk.Frame(frame)
        welcome_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(welcome_frame, text="Welcome to KPMG Edge", 
                font=("Arial", 24, "bold")).pack(anchor=tk.W)
        
        ttk.Label(welcome_frame, text="The Consultant's Toolkit for SPM Delivery", 
                font=("Arial", 14)).pack(anchor=tk.W, pady=5)
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Quick actions and stats in two columns
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Quick actions
        self.create_left_column(content_frame)
        
        # Right column - Stats and charts
        self.create_right_column(content_frame)
    
    def create_left_column(self, parent):
        """Create the left column of the dashboard"""
        left_col = ttk.Frame(parent)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Quick actions
        self.create_quick_actions(left_col)
        
        # Recent activity feed
        self.create_activity_feed(left_col)
    
    def create_right_column(self, parent):
        """Create the right column of the dashboard"""
        right_col = ttk.Frame(parent)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Project stats
        self.create_project_stats(right_col)
        
        # Upcoming milestones
        self.create_upcoming_milestones(right_col)
    
    def create_quick_actions(self, parent):
        """Create the quick actions section"""
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions")
        actions_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        actions = [
            ("Create New Project", "new_project"),
            ("Upload Compensation Plan", "asset_analyzer"),
            ("View Current Projects", "current_projects"),
            ("Access Training Materials", "training")
        ]
        
        for text, action in actions:
            btn = ttk.Button(actions_frame, text=text)
            btn.pack(fill=tk.X, padx=20, pady=10)
    
    def create_activity_feed(self, parent):
        """Create the recent activity feed"""
        activity_frame = ttk.LabelFrame(parent, text="Recent Activity")
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        activities = [
            ("Project created: SPM Implementation for ABC Corp", "Today, 10:30 AM"),
            ("Asset analysis completed: XYZ Inc Compensation Plans", "Yesterday, 3:45 PM"),
            ("New team member added: Sarah Williams", "Mar 11, 2025, 11:15 AM"),
            ("Project phase completed: Requirements for 123 Industries", "Mar 10, 2025, 2:20 PM")
        ]
        
        for activity, timestamp in activities:
            item_frame = ttk.Frame(activity_frame)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(item_frame, text=activity, wraplength=300).pack(anchor=tk.W)
            ttk.Label(item_frame, text=timestamp, 
                    font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
            
            ttk.Separator(activity_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
    
    def create_project_stats(self, parent):
        """Create the project statistics section"""
        stats_frame = ttk.LabelFrame(parent, text="Project Statistics")
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Simple stats display
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        stats = [
            ("Total Projects", "12"),
            ("On Track", "8"),
            ("At Risk", "3"),
            ("Delayed", "1")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = ttk.Frame(stats_grid)
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky=tk.W)
            
            ttk.Label(stat_frame, text=label).pack(anchor=tk.W)
            ttk.Label(stat_frame, text=value, 
                    font=("Arial", 18, "bold"),
                    foreground=self.colors["primary"]).pack(anchor=tk.W)
        
        # Current quarter progress
        ttk.Label(stats_frame, text="Current Quarter Progress", 
                font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=5)
        
        progress_frame = ttk.Frame(stats_frame)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Progress bar
        ttk.Label(progress_frame, text="Q1 2025").pack(side=tk.LEFT)
        
        progress = ttk.Progressbar(progress_frame, length=200, mode='determinate')
        progress.pack(side=tk.LEFT, padx=10)
        progress['value'] = 65  # 65% complete
        
        ttk.Label(progress_frame, text="65%").pack(side=tk.LEFT)
    
    def create_upcoming_milestones(self, parent):
        """Create the upcoming milestones section"""
        milestones_frame = ttk.LabelFrame(parent, text="Upcoming Milestones")
        milestones_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        milestones = [
            ("Project Kickoff: SPM Implementation", "Mar 15, 2025", "On Track"),
            ("Requirements Sign-off: ICM Migration", "Mar 22, 2025", "At Risk"),
            ("Vendor Selection: Global Retail", "Mar 30, 2025", "On Track")
        ]
        
        for milestone, date, status in milestones:
            item_frame = ttk.Frame(milestones_frame)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Status indicator
            status_color = "green" if status == "On Track" else "orange"
            status_indicator = tk.Label(item_frame, text="•", 
                                    foreground=status_color, 
                                    background=self.colors["white"],
                                    font=("Arial", 16))
            status_indicator.pack(side=tk.LEFT)
            
            # Milestone info
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            ttk.Label(info_frame, text=milestone).pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Due: {date}", 
                    font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
            
            # Status text
            ttk.Label(item_frame, text=status, 
                    foreground=status_color).pack(side=tk.RIGHT)
            
            ttk.Separator(milestones_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)