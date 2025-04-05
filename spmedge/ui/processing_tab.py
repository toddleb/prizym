"""
Processing tab for SPM Edge UI
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from datetime import datetime

class ProcessingTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Processing")
        
        # Initialize state
        self.processing = False
        self.stage_indicators = {}  # Initialize this first before using it
        
        # Create components
        self.create_header()
        self.create_pipeline_visualization()
        self.create_controls()
        self.create_progress_section()
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="Document Processing Pipeline", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Process documents through the SPM Edge AI pipeline"
        ).pack(anchor=tk.W)
    
    def create_pipeline_visualization(self):
        """Create the pipeline stages visualization"""
        pipeline_frame = ttk.Frame(self.frame)
        pipeline_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create pipeline stages with indicators
        stages = ["Input", "Load", "Clean", "Process", "RAG", "Report"]
        
        # Pipeline grid
        pipeline_grid = ttk.Frame(pipeline_frame)
        pipeline_grid.pack(fill=tk.X)
        
        for i, stage in enumerate(stages):
            stage_frame = ttk.LabelFrame(pipeline_grid, text=stage)
            stage_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            pipeline_grid.columnconfigure(i, weight=1)
            
            # Create indicator canvas
            canvas = tk.Canvas(stage_frame, width=30, height=30, highlightthickness=0)
            canvas.pack(padx=10, pady=5)
            
            # Draw circle indicator
            indicator = canvas.create_oval(5, 5, 25, 25, fill="gray", outline="")
            
            # Status and count labels
            status_var = tk.StringVar(value="Not Started")
            status_label = ttk.Label(stage_frame, textvariable=status_var)
            status_label.pack(pady=2)
            
            count_var = tk.StringVar(value="0 docs")
            count_label = ttk.Label(stage_frame, textvariable=count_var)
            count_label.pack(pady=2)
            
            # Store references to widgets
            self.stage_indicators[stage] = {
                "canvas": canvas,
                "indicator": indicator,
                "status": status_var,
                "count": count_var
            }
            
            # Action button
            ttk.Button(
                stage_frame,
                text=f"Run {stage}",
                command=lambda s=stage: self.run_pipeline_stage(s)
            ).pack(pady=(5, 10), padx=10, fill=tk.X)
    
    def create_controls(self):
        """Create pipeline controls section"""
        controls_frame = ttk.LabelFrame(self.frame, text="Pipeline Controls")
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        controls_content = ttk.Frame(controls_frame)
        controls_content.pack(padx=10, pady=10, fill=tk.X)
        
        # Project selection
        ttk.Label(controls_content, text="Project:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.project_combo = ttk.Combobox(controls_content, width=30)
        self.project_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Add some sample projects
        self.project_combo["values"] = ["SPM Implementation", "Sales Comp Migration", "ICM Configuration"]
        
        # Batch size
        ttk.Label(controls_content, text="Batch Size:").grid(row=0, column=2, padx=(20, 5), pady=5, sticky=tk.W)
        self.batch_size = ttk.Spinbox(controls_content, from_=10, to=1000, increment=10, width=5)
        self.batch_size.set(50)
        self.batch_size.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # AI model selection
        ttk.Label(controls_content, text="AI Model:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.model_combo = ttk.Combobox(controls_content, width=30, values=["gpt-4o", "gpt-3.5-turbo", "llama-3"])
        self.model_combo.set("gpt-4o")
        self.model_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Main action buttons
        button_frame = ttk.Frame(controls_content)
        button_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.E)
        
        ttk.Button(
            button_frame,
            text="Run Complete Pipeline",
            command=self.run_full_pipeline
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Stop Processing",
            command=self.stop_processing
        ).pack(side=tk.LEFT, padx=5)
    
    def create_progress_section(self):
        """Create progress section with bar and log"""
        progress_frame = ttk.LabelFrame(self.frame, text="Progress")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Progress section split into progress bar and log
        progress_content = ttk.Frame(progress_frame)
        progress_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress bar
        progress_labels = ttk.Frame(progress_content)
        progress_labels.pack(fill=tk.X)
        
        ttk.Label(progress_labels, text="Overall Progress:").pack(side=tk.LEFT)
        self.progress_percent = ttk.Label(progress_labels, text="0%")
        self.progress_percent.pack(side=tk.RIGHT)
        
        self.progress_bar = ttk.Progressbar(progress_content, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Log section
        ttk.Label(progress_content, text="Processing Logs:").pack(anchor=tk.W)
        
        # Create a frame with border for the log
        log_frame = ttk.Frame(progress_content, borderwidth=1, relief=tk.SUNKEN)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log display with scrollbar
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Set log text to read-only
        self.log_text.config(state=tk.DISABLED)
        
        # Add initial log message
        self.log_message("Pipeline initialized and ready")
    
    def run_pipeline_stage(self, stage):
        """Run a specific pipeline stage"""
        # Get the selected project
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project first")
            return
            
        # Update stage indicator
        self.update_stage_indicator(stage, "running", "2 docs")
        
        # Log the action
        self.log_message(f"Running {stage} stage for project: {project}")
        
        # In a real implementation, you would call the actual pipeline stage process
        # For simulation, we'll use a thread to update the UI
        threading.Thread(target=self.simulate_stage_processing, args=(stage,), daemon=True).start()
    
    def run_full_pipeline(self):
        """Run the complete pipeline"""
        # Get the selected project
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project first")
            return
            
        # Check if already processing
        if self.processing:
            messagebox.showinfo("Info", "Pipeline is already running")
            return
            
        # Get batch size
        try:
            batch_size = int(self.batch_size.get())
        except ValueError:
            batch_size = 50
            
        # Get model
        model = self.model_combo.get()
        
        # Log the action
        self.log_message(f"Running full pipeline for project: {project}")
        self.log_message(f"Batch size: {batch_size}, Model: {model}")
        
        # Update progress bar
        self.progress_bar["value"] = 0
        self.progress_percent["text"] = "0%"
        
        # Update status
        if hasattr(self.app, 'update_status'):
            self.app.update_status("Processing pipeline...", f"Project: {project}", f"Model: {model}")
        
        # Set processing flag
        self.processing = True
        
        # In a real implementation, you would call the actual pipeline process
        # For simulation, we'll use a thread to update the UI
        threading.Thread(target=self.simulate_pipeline_processing, daemon=True).start()
    
    def simulate_pipeline_processing(self):
        """Simulate the pipeline processing for UI demonstration"""
        stages = ["Input", "Load", "Clean", "Process", "RAG", "Report"]
        total_stages = len(stages)
        
        try:
            # Reset all indicators
            for stage in stages:
                self.update_stage_indicator(stage, "pending", "0 docs")
            
            # Process each stage
            for i, stage in enumerate(stages):
                # Update progress
                progress = int((i / total_stages) * 100)
                self.update_progress(progress)
                
                # Update stage indicator
                self.update_stage_indicator(stage, "running", "2 docs")
                
                # Log stage start
                self.log_message(f"Starting {stage} stage")
                
                # Simulate processing time
                for j in range(5):
                    if not self.processing:
                        # Processing was stopped
                        self.log_message(f"Processing stopped during {stage} stage")
                        self.update_stage_indicator(stage, "failed", "0 docs")
                        return
                        
                    time.sleep(0.5)
                    self.log_message(f"  {stage} processing step {j+1}/5")
                
                # Mark stage as completed
                self.update_stage_indicator(stage, "completed", "2 docs")
                
                # Log stage completion
                self.log_message(f"Completed {stage} stage")
            
            # Final progress update
            self.update_progress(100)
            
            # Update status
            if hasattr(self.app, 'update_status'):
                self.app.update_status("Processing completed", "Documents: 2", "API: Connected")
            
            # Show completion message
            self.app.root.after(0, lambda: messagebox.showinfo("Success", "Pipeline processing completed successfully"))
        
        finally:
            # Reset processing flag
            self.processing = False
    
    def simulate_stage_processing(self, stage):
        """Simulate processing a single stage"""
        try:
            # Update progress
            self.update_progress(0)
            
            # Simulate processing time
            for i in range(5):
                time.sleep(0.5)
                
                # Update progress
                progress = int(((i + 1) / 5) * 100)
                self.update_progress(progress)
                
                # Log progress
                self.log_message(f"  {stage} processing step {i+1}/5")
            
            # Mark stage as completed
            self.update_stage_indicator(stage, "completed", "2 docs")
            
            # Update status
            if hasattr(self.app, 'update_status'):
                self.app.update_status(f"{stage} processing completed", "Documents: 2", "API: Connected")
            
            # Log completion
            self.log_message(f"Completed {stage} stage")
        except Exception as e:
            self.log_message(f"Error during {stage} stage: {str(e)}")
            self.update_stage_indicator(stage, "failed", "0 docs")
    
    def update_progress(self, value):
        """Update the progress bar"""
        def _update():
            self.progress_bar["value"] = value
            self.progress_percent["text"] = f"{value}%"
        self.app.root.after(0, _update)
    
    def update_stage_indicator(self, stage, status, count):
        """Update the pipeline stage indicator"""
        if stage not in self.stage_indicators:
            return
        
        def _update():
            indicator = self.stage_indicators[stage]
            canvas = indicator["canvas"]
            circle = indicator["indicator"]
            
            # Update color based on status
            if status == "pending":
                canvas.itemconfig(circle, fill="gray")
                indicator["status"].set("Pending")
            elif status == "running":
                canvas.itemconfig(circle, fill="#f59e0b")  # Warning color
                indicator["status"].set("Running")
            elif status == "completed":
                canvas.itemconfig(circle, fill="#22c55e")  # Success color
                indicator["status"].set("Completed")
            elif status == "failed":
                canvas.itemconfig(circle, fill="#ef4444")  # Danger color
                indicator["status"].set("Failed")
            
            # Update count
            indicator["count"].set(count)
        
        self.app.root.after(0, _update)
    
    def log_message(self, message):
        """Add a message to the log"""
        def _log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Enable text widget for editing
            self.log_text.config(state=tk.NORMAL)
            
            # Insert message with timestamp
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            
            # Auto-scroll to bottom
            self.log_text.see(tk.END)
            
            # Return to read-only state
            self.log_text.config(state=tk.DISABLED)
        
        self.app.root.after(0, _log)
    
    def stop_processing(self):
        """Stop the current processing job"""
        if not self.processing:
            messagebox.showinfo("Info", "No processing job is currently running")
            return
            
        # Reset processing flag
        self.processing = False
        
        messagebox.showinfo("Stop Processing", "Processing will be stopped after current task completes")
        
        # Update status
        if hasattr(self.app, 'update_status'):
            self.app.update_status("Processing stopped", "Documents: 0", "API: Connected")
        
        # Log the action
        self.log_message("Pipeline processing stopped by user")
    
    def import_documents(self):
        """Import documents into the system"""
        # Get selected project
        project = self.project_combo.get()
        if not project:
            messagebox.showinfo("Info", "Please select a project first")
            return
            
        files = filedialog.askopenfilenames(
            title="Select Documents to Upload",
            filetypes=(
                ("All Documents", "*.pdf;*.docx;*.xlsx;*.pptx;*.txt;*.json"), 
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx"),
                ("Excel Spreadsheets", "*.xlsx"),
                ("PowerPoint Presentations", "*.pptx"),
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            )
        )
        
        if not files:
            return
            
        # Show upload progress
        self.log_message(f"Uploading {len(files)} files to project '{project}'")
        
        # Simulate upload progress
        self.update_progress(0)
        
        for i, file in enumerate(files):
            progress = int(((i + 1) / len(files)) * 100)
            self.update_progress(progress)
            self.log_message(f"Uploading {file.split('/')[-1]}")
            time.sleep(0.2)  # Simulate upload time
        
        # Update status
        if hasattr(self.app, 'update_status'):
            self.app.update_status(f"Uploaded {len(files)} files", f"Documents: {len(files)}", "API: Connected")
        
        # Log completion
        self.log_message(f"Upload completed: {len(files)} files")
        
        # Show success message
        messagebox.showinfo("Upload Complete", f"Successfully uploaded {len(files)} files to project '{project}'")