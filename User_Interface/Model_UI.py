import tkinter as tk

class ModelUI:
    def __init__(self, parent_frame, app_instance):
        self.parent_frame = parent_frame
        self.app = app_instance
        
        # Create top_right and bottom_right frames
        self.top_frame = tk.Frame(self.parent_frame, height=400)
        self.bottom_frame = tk.Frame(self.parent_frame, height=400)
        
        self.top_frame.pack(side='top', fill='both', expand=True)
        self.bottom_frame.pack(side='bottom', fill='both', expand=True)
        
        # Setup the UI
        self._setup_ui()
        
    def _setup_ui(self):
        # This is currently empty but will be populated in the future
        # Placeholder for future model-related UI components
        pass
