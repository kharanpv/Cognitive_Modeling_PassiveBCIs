import tkinter as tk
from tkinter import filedialog, BooleanVar, Checkbutton
import os
import multiprocessing
import json
from Base_UI import BaseUI
from Model_Files.Model import Model

class ModelUI(BaseUI):
    """
    A graphical user interface class for managing cognitive model creation.
    
    This class provides UI components for selecting data sources and 
    creating cognitive models from recorded data sessions.
    """

    def __init__(self, root):
        """
        Initialize the Model UI components.

        Args:
            root: The tkinter root window
        """
        # Initialize the base UI with title
        super().__init__(root, "Model Creation - Cognitive Modeler")
        
        # Initialize checkbox variable
        self.create_tracked_video_var = BooleanVar()
        
        # Initialize process reference
        self.model_process = None
        
        # Setup the UI
        self._setup_ui()
        
    def _setup_ui(self):
        """
        Set up the main UI components including location selection,
        tracked video option, and model creation controls.
        """
        self._setup_location_selection()
        self._setup_tracked_video_option()
        self._setup_model_controls()

    def _setup_location_selection(self):
        """
        Create UI elements for selecting the data source location.
        Includes entry field, browse button, and open location button.
        """
        location_frame = tk.Frame(self.root, padx=20, pady=10)
        location_frame.pack(fill="x")
        
        location_label = tk.Label(location_frame, text="Data Source Location:")
        location_label.pack(anchor='w')
        
        path_frame = tk.Frame(location_frame)
        path_frame.pack(fill='x', pady=5)
        
        self.location_entry = tk.Entry(path_frame)
        self.location_entry.insert(0, self.default_data_dir)
        self.location_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        choose_button = tk.Button(path_frame, text="Choose Location", command=self._choose_location)
        choose_button.pack(side='right')
        
        open_button = tk.Button(location_frame, text="Open Location", command=self._open_location)
        open_button.pack(anchor='w', pady=5)

    def _setup_tracked_video_option(self):
        """
        Create checkbox for enabling tracked video processing.
        """
        option_frame = tk.Frame(self.root, padx=20, pady=10)
        option_frame.pack(fill="x")
        
        tracked_video_checkbox = Checkbutton(option_frame, text="Create tracked video", 
                                           variable=self.create_tracked_video_var)
        tracked_video_checkbox.pack(anchor='w')

    def _setup_model_controls(self):
        """
        Set up the model creation controls.
        """
        controls_frame = tk.Frame(self.root, padx=20, pady=20)
        controls_frame.pack(fill="x")
        
        # Icon frame
        icon_frame = tk.Frame(controls_frame)
        icon_frame.pack(fill='x', pady=(0, 5))
        
        # Tool/gear icon
        tool_icon = tk.Label(icon_frame, text="⚙", font=("Arial", 16))
        tool_icon.pack()
        
        # Button frame
        button_frame = tk.Frame(controls_frame)
        button_frame.pack(fill='x')
        
        create_button = tk.Button(button_frame, text="Create Model", command=self._create_model)
        create_button.pack()

    def _choose_location(self):
        """
        Open a directory selection dialog and update the location entry
        with the selected path. Updates status on errors.
        """
        try:
            directory = filedialog.askdirectory(initialdir=self.default_data_dir)
            if directory:
                self.location_entry.delete(0, tk.END)
                self.location_entry.insert(0, directory)
        except Exception as e:
            error_msg = f"Error selecting directory: {str(e)}"
            self.update_status(error_msg, "red")
    
    def _open_location(self):
        """
        Open the current data source location in the system's file explorer.
        Handles different operating systems (Windows, macOS, Linux).
        Updates status on errors.
        """
        try:
            location = self.location_entry.get()
            if not location:
                self.update_status("Error: No location specified", "red")
                return
                
            if os.path.exists(location):
                if os.name == 'nt':
                    os.startfile(location)
                elif os.name == 'posix':
                    import subprocess
                    import sys
                    subprocess.call(['open', location] if sys.platform == 'darwin' else ['xdg-open', location])
            else:
                self.update_status("Error: Location does not exist", "red")
        except Exception as e:
            error_msg = f"Error opening location: {str(e)}"
            self.update_status(error_msg, "red")

    def _create_model(self):
        """
        Creates a Model object and executes generate_model() in a separate process.
        Updates the program status and handles errors appropriately.
        """
        try:
            data_folder = self.location_entry.get()
            
            # Validate data folder exists
            if not data_folder or not os.path.exists(data_folder):
                self.update_status("Error: Invalid data folder path", "red")
                return
            
            # Create/update config.json with tracked video setting
            self._update_config_file()
            
            # Update status to show model creation is starting
            self.update_status("Creating Model", "#8A2BE2")  # Violet color
            
            # Create model instance
            model = Model()
            model.data_folder = data_folder
            
            # Create and start the process directly with generate_model
            process = multiprocessing.Process(target=model.generate_model)
            process.start()
            
            print(f"Creating model from data at: {data_folder}")
            print("Model generation started in separate process...")
            
            # Store the process reference for later management
            self.model_process = process
            
        except Exception as e:
            # Handle any errors in the main thread
            error_msg = f"Error starting model creation: {str(e)}"
            self.update_status(error_msg, "red")
            print(error_msg)
    
    def _update_config_file(self):
        """
        Create or update the config.json file in Processing_Module with the tracked video setting.
        """
        try:
            # Get the path to the Processing_Module directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            processing_module_dir = os.path.join(os.path.dirname(script_dir), "Model_Files", "Processing_Module")
            config_path = os.path.join(processing_module_dir, "config.json")
            
            # Load existing config if it exists, otherwise start with empty dict
            config = {}
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                except (json.JSONDecodeError, Exception):
                    # If file is corrupted or empty, start fresh
                    config = {}
            
            # Update the tracked video setting
            config["create_tracked_video"] = self.create_tracked_video_var.get()
            
            # Write the updated config back to the file
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            print(f"Updated config.json with tracked video setting: {self.create_tracked_video_var.get()}")
            
        except Exception as e:
            error_msg = f"Error updating config file: {str(e)}"
            self.update_status(error_msg, "red")
            print(error_msg)


if __name__ == "__main__":
    """
    Run the Model UI as a standalone application.
    """
    root = tk.Tk()
    app = ModelUI(root)
    root.mainloop()
