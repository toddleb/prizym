#!/usr/bin/env python3
"""
SPM Edge UI - Entry point
"""
import tkinter as tk
from app import SPMEdgeApp

def main():
    root = tk.Tk()
    app = SPMEdgeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()