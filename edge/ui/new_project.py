from tkinter import ttk

class NewProject:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="New Project View", font=("Arial", 16)).pack(pady=20)