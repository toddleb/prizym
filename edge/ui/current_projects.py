from tkinter import ttk

class CurrentProjects:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Current Projects View", font=("Arial", 16)).pack(pady=20)