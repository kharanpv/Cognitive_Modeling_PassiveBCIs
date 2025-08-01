import tkinter as tk
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Recording_Module.Central_Data_Controller import Central_Data_Controller

class BaseUI:
    """
    Base class for UI components that provides common functionality
    like status management and data directory handling.
    """
    
    def __init__(self, root, title="Cognitive Modeler"):
        self.root = root
        self.root.title(title)
        self.root.geometry("600x800")  # Width x Height for individual UIs
        
        # Get default data directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_data_dir = os.path.join(os.path.dirname(self.script_dir), "Data")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.default_data_dir):
            os.makedirs(self.default_data_dir)
        
        # Data-handling objects
        self.central_data_controller = Central_Data_Controller()
        
        # Setup status box first
        self._setup_status_box()
    
    def _setup_status_box(self):
        """
        Create and configure the status display box that shows current
        program state.
        """
        status_frame = tk.Frame(self.root, padx=20, pady=10)
        status_frame.pack(side='top', fill='x')
        
        status_label = tk.Label(status_frame, text="Program Status:", anchor='w')
        status_label.pack(side='left')
        
        self.status_text = tk.Label(status_frame, text="Ready", anchor='w', fg="green")
        self.status_text.pack(side='left', padx=5)
    
    def update_status(self, message, color="black"):
        """
        Update the status message display.

        Args:
            message (str): Status message to display
            color (str): Color of the status text (default: "black")
        """
        self.status_text.config(text=message, fg=color)
