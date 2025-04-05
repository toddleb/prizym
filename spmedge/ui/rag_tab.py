"""
RAG tab for SPM Edge UI - Interact with documents using conversational AI
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import random

class RAGTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="RAG")
        
        # Initialize state
        self.conversation_history = []
        self.selected_documents = []
        self.processing = False
        
        # Create layout
        self.create_header()
        self.create_main_layout()
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            header_frame, 
            text="Document Chat", 
            font=("Arial", 16, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            header_frame, 
            text="Ask questions about your documents using AI"
        ).pack(anchor=tk.W)
    
    def create_main_layout(self):
        """Create the main layout with sidebar and chat area"""
        main_container = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left sidebar - Document selection and model settings
        sidebar = ttk.Frame(main_container)
        main_container.add(sidebar, weight=1)
        
        # Document selection section
        doc_frame = ttk.LabelFrame(sidebar, text="Documents")
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Document list with checkboxes
        docs_container = ttk.Frame(doc_frame)
        docs_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create scrollable frame for documents
        docs_canvas = tk.Canvas(docs_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(docs_container, orient=tk.VERTICAL, command=docs_canvas.yview)
        
        docs_scrollframe = ttk.Frame(docs_canvas)
        docs_scrollframe.bind(
            "<Configure>",
            lambda e: docs_canvas.configure(scrollregion=docs_canvas.bbox("all"))
        )
        
        docs_canvas.create_window((0, 0), window=docs_scrollframe, anchor=tk.NW)
        docs_canvas.configure(yscrollcommand=scrollbar.set)
        
        docs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load and display available documents
        self.load_document_list(docs_scrollframe)
        
        # Document action buttons
        doc_buttons = ttk.Frame(doc_frame)
        doc_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            doc_buttons,
            text="Refresh Documents",
            command=lambda: self.load_document_list(docs_scrollframe)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            doc_buttons,
            text="Select All",
            command=lambda: self.toggle_all_documents(True)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            doc_buttons,
            text="Clear Selection",
            command=lambda: self.toggle_all_documents(False)
        ).pack(side=tk.LEFT, padx=2)
        
        # Model settings section
        settings_frame = ttk.LabelFrame(sidebar, text="Chat Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # AI model selection
        ttk.Label(settings_frame, text="AI Model:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.model_var = tk.StringVar(value="gpt-4o")
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, width=15)
        model_combo["values"] = ["gpt-4o", "gpt-3.5-turbo", "claude-3", "llama-3"]
        model_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Temperature setting
        ttk.Label(settings_frame, text="Temperature:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.temp_var = tk.DoubleVar(value=0.7)
        temp_scale = ttk.Scale(settings_frame, from_=0.0, to=1.0, variable=self.temp_var)
        temp_scale.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(settings_frame, textvariable=self.temp_var).grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Context window setting
        ttk.Label(settings_frame, text="Context Window:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.context_var = tk.IntVar(value=5)
        context_spin = ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.context_var, width=5)
        context_spin.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Right area - Chat interface
        chat_frame = ttk.Frame(main_container)
        main_container.add(chat_frame, weight=3)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            height=20,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chat_input = scrolledtext.ScrolledText(
            input_frame, 
            wrap=tk.WORD, 
            height=3,
            font=("Arial", 10)
        )
        self.chat_input.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # Bind enter key to send message
        self.chat_input.bind("<Return>", self.on_enter_pressed)
        self.chat_input.bind("<Shift-Return>", lambda e: None)  # Allow Shift+Enter for newlines
        
        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            width=10
        )
        send_button.pack(side=tk.RIGHT, padx=5)
        
        # Add welcome message
        self.add_system_message("Welcome to Document Chat! Select documents from the sidebar and ask questions about them.")
    
    def load_document_list(self, container):
        """Load document list into the container"""
        # Clear existing content
        for widget in container.winfo_children():
            widget.destroy()
        
        self.doc_vars = {}  # Store document checkbox variables
        
        # Add some demo documents
        demo_docs = [
            {"id": "doc1", "name": "SPM Implementation Guide.pdf", "type": "PDF", "size": "1.2 MB"},
            {"id": "doc2", "name": "Compensation Plan Rules.docx", "type": "Word", "size": "458 KB"},
            {"id": "doc3", "name": "Sales Territories 2024.xlsx", "type": "Excel", "size": "620 KB"},
            {"id": "doc4", "name": "Commission Calculations.txt", "type": "Text", "size": "45 KB"},
            {"id": "doc5", "name": "Incentive Structure.pdf", "type": "PDF", "size": "3.1 MB"},
            {"id": "doc6", "name": "Quota Model Documentation.pdf", "type": "PDF", "size": "2.6 MB"},
            {"id": "doc7", "name": "Performance Metrics.xlsx", "type": "Excel", "size": "512 KB"},
            {"id": "doc8", "name": "Contract Terms.docx", "type": "Word", "size": "310 KB"}
        ]
        
        # Create a checkbox for each document
        for i, doc in enumerate(demo_docs):
            var = tk.BooleanVar(value=False)
            self.doc_vars[doc["id"]] = var
            
            doc_frame = ttk.Frame(container)
            doc_frame.pack(fill=tk.X, padx=2, pady=2)
            
            cb = ttk.Checkbutton(
                doc_frame, 
                text=doc["name"],
                variable=var,
                command=self.update_document_selection
            )
            cb.pack(side=tk.LEFT)
            
            # Document info
            ttk.Label(
                doc_frame,
                text=f"({doc['type']}, {doc['size']})",
                foreground="gray"
            ).pack(side=tk.RIGHT)
            
            # Store reference to document
            var.doc_info = doc
    
    def toggle_all_documents(self, state):
        """Select or deselect all documents"""
        for var in self.doc_vars.values():
            var.set(state)
        
        self.update_document_selection()
    
    def update_document_selection(self):
        """Update the selected documents list based on checkboxes"""
        self.selected_documents = []
        
        for doc_id, var in self.doc_vars.items():
            if var.get():
                self.selected_documents.append(var.doc_info)
        
        # Update status bar
        if hasattr(self.app, "update_status"):
            if self.selected_documents:
                self.app.update_status(
                    f"Selected {len(self.selected_documents)} documents", 
                    f"Documents: {len(self.selected_documents)}", 
                    f"Model: {self.model_var.get()}"
                )
            else:
                self.app.update_status("No documents selected", "Documents: 0", "Ready")
    
    def on_enter_pressed(self, event):
        """Handle Enter key to send message"""
        if not event.state & 0x1:  # No Shift key
            self.send_message()
            return "break"  # Prevent default behavior (newline)
    
    def send_message(self):
        """Send user message and get AI response"""
        # Get user input
        user_input = self.chat_input.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # Check if documents are selected
        if not self.selected_documents:
            messagebox.showinfo("No Documents", "Please select at least one document from the sidebar before asking questions.")
            return
        
        # Clear input area
        self.chat_input.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_user_message(user_input)
        
        # Simulate AI thinking
        self.add_system_message("Thinking...", temp=True)
        
        # Start processing in background
        if not self.processing:
            self.processing = True
            threading.Thread(target=self.process_query, args=(user_input,), daemon=True).start()
    
    def process_query(self, query):
        """Process the user query and generate a response"""
        try:
            # In a real implementation, this would call the RAG API
            # For demo, we'll simulate processing time
            time.sleep(1.5)
            
            # Get selected model and settings
            model = self.model_var.get()
            temp = self.temp_var.get()
            
            # Generate demo response based on query and selected documents
            response = self.generate_demo_response(query)
            
            # Remove temporary message
            self.remove_temp_message()
            
            # Add AI response to chat
            self.add_ai_message(response)
            
            # Update status
            if hasattr(self.app, "update_status"):
                self.app.update_status(
                    "Response generated", 
                    f"Documents: {len(self.selected_documents)}", 
                    f"Model: {model}"
                )
        except Exception as e:
            # Remove temporary message
            self.remove_temp_message()
            
            # Show error
            self.add_system_message(f"Error: {str(e)}")
        finally:
            self.processing = False
    
    def generate_demo_response(self, query):
        """Generate a demo response based on the query and selected documents"""
        # Simple demo responses based on selected documents and query keywords
        query_lower = query.lower()
        
        # Get document names for reference
        doc_names = [doc["name"] for doc in self.selected_documents]
        
        # Default response if no specific match
        response = f"Based on the {len(self.selected_documents)} documents you've selected, I can provide information about SPM (Sales Performance Management) systems and processes."
        
        # Check for specific document types and keywords
        if any("pdf" in doc["name"].lower() for doc in self.selected_documents):
            if "implementation" in query_lower:
                response = "According to the SPM Implementation Guide, the typical implementation process has 5 phases: Planning, Design, Build, Test, and Deploy. Each phase has specific milestones and deliverables that should be tracked for project success."
            elif "compensation" in query_lower or "plan" in query_lower:
                response = "The Compensation Plan Rules document outlines several key components of an effective sales compensation plan:\n\n1. Base salary structure\n2. Commission rates and tiers\n3. Bonus structures\n4. Accelerators for overachievement\n5. Special incentives for strategic products"
            elif "quota" in query_lower:
                response = "The Quota Model Documentation describes best practices for quota setting, including:\n\n• Using 3-year historical data for baseline\n• Adjusting for territory potential\n• Setting achievable yet stretching targets (typically 10-15% growth)\n• Including seasonality factors\n• Establishing clear adjustment policies"
        
        if any("xlsx" in doc["name"].lower() for doc in self.selected_documents):
            if "territory" in query_lower:
                response = "The Sales Territories 2024 spreadsheet shows geographical divisions with the following information:\n\n• 5 regions (North, South, East, West, Central)\n• 27 territories in total\n• Average territory size: $3.2M in potential revenue\n• Territory alignment based on customer concentration and travel efficiency"
            elif "performance" in query_lower or "metric" in query_lower:
                response = "According to the Performance Metrics document, the key performance indicators for sales representatives include:\n\n• Quota attainment (target: >90%)\n• Deal size (avg target: $45,000)\n• Sales cycle length (target: <90 days)\n• Win rate (target: >25%)\n• Customer retention rate (target: >85%)"
        
        if any("commission" in doc["name"].lower() for doc in self.selected_documents):
            if "calculation" in query_lower:
                response = "The Commission Calculations document explains that commissions are calculated using the following formula:\n\nCommission = Sale Amount × Commission Rate × Attainment Multiplier\n\nWhere:\n• Commission Rate varies by product line (5-12%)\n• Attainment Multiplier ranges from 0.8 to 2.0 based on quota attainment"
        
        # Add citation
        response += f"\n\nThis information was retrieved from {', '.join(doc_names[:2])}"
        if len(doc_names) > 2:
            response += f" and {len(doc_names) - 2} other documents"
        response += "."
        
        return response
    
    def add_user_message(self, message):
        """Add user message to chat display"""
        self.enable_chat_display()
        self.chat_display.insert(tk.END, "You: ", "user_tag")
        self.chat_display.insert(tk.END, f"{message}\n\n", "user_message")
        self.chat_display.see(tk.END)
        self.disable_chat_display()
        
        # Configure tags
        self.chat_display.tag_configure("user_tag", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("user_message", font=("Arial", 10))
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
    
    def add_ai_message(self, message):
        """Add AI message to chat display"""
        self.enable_chat_display()
        self.chat_display.insert(tk.END, "AI: ", "ai_tag")
        self.chat_display.insert(tk.END, f"{message}\n\n", "ai_message")
        self.chat_display.see(tk.END)
        self.disable_chat_display()
        
        # Configure tags
        self.chat_display.tag_configure("ai_tag", font=("Arial", 10, "bold"), foreground="#0066cc")
        self.chat_display.tag_configure("ai_message", font=("Arial", 10))
        
        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": message})
    
    def add_system_message(self, message, temp=False):
        """Add system message to chat display"""
        self.enable_chat_display()
        
        if temp:
            self.chat_display.insert(tk.END, message + "\n", "temp_message")
            self.chat_display.tag_configure("temp_message", font=("Arial", 10, "italic"), foreground="gray")
        else:
            self.chat_display.insert(tk.END, f"System: {message}\n\n", "system_message")
            self.chat_display.tag_configure("system_message", font=("Arial", 10, "italic"), foreground="gray")
        
        self.chat_display.see(tk.END)
        self.disable_chat_display()
    
    def remove_temp_message(self):
        """Remove temporary thinking message"""
        self.enable_chat_display()
        
        # Find and delete the "Thinking..." line
        line_count = int(self.chat_display.index('end-1c').split('.')[0])
        for i in range(1, line_count + 1):
            line = self.chat_display.get(f"{i}.0", f"{i}.end")
            if line == "Thinking...":
                self.chat_display.delete(f"{i}.0", f"{i+1}.0")
                break
        
        self.disable_chat_display()
    
    def enable_chat_display(self):
        """Enable chat display for editing"""
        self.chat_display.config(state=tk.NORMAL)
    
    def disable_chat_display(self):
        """Disable chat display (read-only)"""
        self.chat_display.config(state=tk.DISABLED)