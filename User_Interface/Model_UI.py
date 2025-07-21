import tkinter as tk
from tkinter import filedialog
import os
import sys
import multiprocessing
from Model_Files.Model import Model

class ModelUI:
    """
    A graphical user interface class for managing cognitive model creation.
    
    This class provides UI components for selecting data sources and 
    creating cognitive models from recorded data sessions.
    """

    def __init__(self, parent_frame, app_instance):
        """
        Initialize the Model UI components.

        Args:
            parent_frame: The tkinter frame where this UI will be embedded
            app_instance: Reference to the main application instance
        """
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
        """
        Set up the main UI components including title, location selection,
        and model creation controls.
        """
        self._setup_title()
        self._setup_location_selection()
        self._setup_model_controls()

        
    def _setup_title(self):
        """
        Create and configure the title section.
        """
        title_frame = tk.Frame(self.top_frame)
        title_frame.pack(side='top', fill='x', pady=10)
        
        title_label = tk.Label(title_frame, text="Model", font=("Arial", 16, "bold"))
        title_label.pack()
    
    def _setup_location_selection(self):
        """
        Create UI elements for selecting the data source location.
        Includes entry field, browse button, and open location button.
        """
        location_frame = tk.Frame(self.top_frame, padx=20, pady=10)
        location_frame.pack(side='top', fill='x')
        
        location_label = tk.Label(location_frame, text="Data Source Location:")
        location_label.pack(anchor='w')
        
        path_frame = tk.Frame(location_frame)
        path_frame.pack(fill='x', pady=5)
        
        self.location_entry = tk.Entry(path_frame)
        self.location_entry.insert(0, self.app.default_data_dir)
        self.location_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        choose_button = tk.Button(path_frame, text="Choose Location", command=self._choose_location)
        choose_button.pack(side='right')
        
        open_button = tk.Button(location_frame, text="Open Location", command=self._open_location)
        open_button.pack(anchor='w', pady=5)
    
    def _setup_model_controls(self):
        """
        Set up the model creation controls.
        """
        controls_frame = tk.Frame(self.top_frame, padx=20, pady=20)
        controls_frame.pack(side='top', fill='x')
        
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
            directory = filedialog.askdirectory(initialdir=self.app.default_data_dir)
            if directory:
                self.location_entry.delete(0, tk.END)
                self.location_entry.insert(0, directory)
        except Exception as e:
            error_msg = f"Error selecting directory: {str(e)}"
            self.app.update_status(error_msg, "red")
    
    def _open_location(self):
        """
        Open the current data source location in the system's file explorer.
        Handles different operating systems (Windows, macOS, Linux).
        Updates status on errors.
        """
        try:
            location = self.location_entry.get()
            if not location:
                self.app.update_status("Error: No location specified", "red")
                return
                
            if os.path.exists(location):
                if os.name == 'nt':
                    os.startfile(location)
                elif os.name == 'posix':
                    import subprocess
                    import sys
                    subprocess.call(['open', location] if sys.platform == 'darwin' else ['xdg-open', location])
            else:
                self.app.update_status("Error: Location does not exist", "red")
        except Exception as e:
            error_msg = f"Error opening location: {str(e)}"
            self.app.update_status(error_msg, "red")
    
    def _create_model(self):
        """
        Creates a Model object and executes generate_model() in a separate process.
        Updates the program status and handles errors appropriately.
        """
        try:
            data_folder = self.location_entry.get()
            
            # Validate data folder exists
            if not data_folder or not os.path.exists(data_folder):
                self.app.update_status("Error: Invalid data folder path", "red")
                return
            
            # Update status to show model creation is starting
            self.app.update_status("Creating Model", "#8A2BE2")  # Violet color
            
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
            
            # Monitor process completion
            self._monitor_process_completion()
            
        except Exception as e:
            # Handle any errors in the main thread
            error_msg = f"Error starting model creation: {str(e)}"
            self.app.update_status(error_msg, "red")
            print(error_msg)
    
    def _monitor_process_completion(self):
        """
        Monitor the model creation process and update status when complete.
        """
        if hasattr(self, 'model_process') and self.model_process is not None:
            if self.model_process.is_alive():
                # Process is still running, check again in 1 second
                self.parent_frame.after(1000, self._monitor_process_completion)
            else:
                # Process has completed
                if self.model_process.exitcode == 0:
                    # Process completed successfully
                    self.app.update_status("Model Created", "#00BFFF")  # Light blue/cyan color
                else:
                    # Process completed with error
                    self.app.update_status("Model Creation Failed", "red")
                print("Model generation process completed.")
