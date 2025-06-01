import tkinter as tk
from tkinter import Checkbutton, BooleanVar, filedialog, PhotoImage
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Recording_Module.Central_Data_Controller import Central_Data_Controller

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cognitive Modeler")
        self.root.geometry("1200x800")  # Width x Height

        # Initialize checkbox variables
        self.record_keyboard_var = BooleanVar()
        self.record_mouse_var = BooleanVar()
        self.record_screen_var = BooleanVar()
        self.record_webcam_var = BooleanVar()

        # Data-handling objects
        self.central_data_controller = Central_Data_Controller()

        # Get default data directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_data_dir = os.path.join(os.path.dirname(self.script_dir), "Data")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.default_data_dir):
            os.makedirs(self.default_data_dir)
        
        self._setup_frames()

    def _setup_frames(self):
        # Main containers
        left_frame = tk.Frame(self.root, width=600, height=800)
        right_frame = tk.Frame(self.root, width=600, height=800)

        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)

        # Subdivide right frame
        top_right_frame = tk.Frame(right_frame, height=400)
        bottom_right_frame = tk.Frame(right_frame, height=400)

        top_right_frame.pack(side='top', fill='both', expand=True)
        bottom_right_frame.pack(side='bottom', fill='both', expand=True)

        # Setup the left frame components
        self._setup_left_frame(left_frame)

        # Save references if needed later
        self.left_frame = left_frame
        self.top_right_frame = top_right_frame
        self.bottom_right_frame = bottom_right_frame

    def _setup_left_frame(self, parent_frame):
        # Add status box at the very top
        self._setup_status_box(parent_frame)
        
        # Add a title below status box
        title_frame = tk.Frame(parent_frame)
        title_frame.pack(side='top', fill='x', pady=10)
        
        title_label = tk.Label(title_frame, text="Data", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Add checkboxes
        self._setup_checkboxes(parent_frame)
        
        # Add location selection
        self._setup_location_selection(parent_frame)
        
        # Add recording controls
        self._setup_recording_controls(parent_frame)
    
    def _setup_status_box(self, parent_frame):
        status_frame = tk.Frame(parent_frame, padx=20, pady=10)
        status_frame.pack(side='top', fill='x')
        
        status_label = tk.Label(status_frame, text="Program Status:", anchor='w')
        status_label.pack(side='left')
        
        self.status_text = tk.Label(status_frame, text="Ready", anchor='w', fg="green")
        self.status_text.pack(side='left', padx=5)
    
    def _update_status(self, message, color="black"):
        self.status_text.config(text=message, fg=color)

    def _setup_checkboxes(self, parent_frame):
        # Create a frame for checkboxes with padding
        checkbox_frame = tk.Frame(parent_frame, padx=20, pady=10)
        checkbox_frame.pack(side='top', fill='x')
        
        # Add checkboxes
        Checkbutton(checkbox_frame, text="Record Keyboard", 
                   variable=self.record_keyboard_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Mouse", 
                   variable=self.record_mouse_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Screen", 
                   variable=self.record_screen_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Webcam", 
                   variable=self.record_webcam_var).pack(anchor='w', pady=5)

    def _setup_location_selection(self, parent_frame):
        location_frame = tk.Frame(parent_frame, padx=20, pady=10)
        location_frame.pack(side='top', fill='x')
        
        location_label = tk.Label(location_frame, text="Data Storage Location:")
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
    
    def _setup_recording_controls(self, parent_frame):
        # Create a frame at the bottom of the left panel
        controls_frame = tk.Frame(parent_frame, padx=20, pady=20)
        controls_frame.pack(side='bottom', fill='x', pady=20)
        
        # Create simple text-based "icons" (can be replaced with actual icons)
        icons_frame = tk.Frame(controls_frame)
        icons_frame.pack(fill='x')
        
        play_icon = tk.Label(icons_frame, text="▶", font=("Arial", 16))
        stop_icon = tk.Label(icons_frame, text="⏹", font=("Arial", 16))
        
        play_icon.grid(row=0, column=0, padx=20)
        stop_icon.grid(row=0, column=1, padx=20)
        
        # Recording control buttons
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        # Configure the grid for both icons and buttons
        icons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        start_button = tk.Button(buttons_frame, text="Start Recording", command=self._start_recording)
        end_button = tk.Button(buttons_frame, text="End Recording", command=self._end_recording)
        
        start_button.grid(row=0, column=0, padx=10)
        end_button.grid(row=0, column=1, padx=10)
        
        # Adjust the icons to align with buttons
        play_icon.grid(row=0, column=0, padx=20, sticky='n')
        stop_icon.grid(row=0, column=1, padx=20, sticky='n')

    def _choose_location(self):
        directory = filedialog.askdirectory(initialdir=self.default_data_dir)
        if directory:  # If a directory was selected (not cancelled)
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, directory)
    
    def _open_location(self):
        location = self.location_entry.get()
        if os.path.exists(location):
            # Open file explorer to the location
            if os.name == 'nt':  # For Windows
                os.startfile(location)
            elif os.name == 'posix':  # For macOS and Linux
                import subprocess
                import sys
                subprocess.call(['open', location] if sys.platform == 'darwin' else ['xdg-open', location])
    
    def _start_recording(self):
        recording_modes_selected = False
        
        # Clear any previous handlers to avoid duplicates
        self.central_data_controller.active_handlers = []
        
        if self.record_keyboard_var.get():
            self.central_data_controller.active_handlers.append('k')
            recording_modes_selected = True
        
        if self.record_mouse_var.get():
            self.central_data_controller.active_handlers.append('m')
            recording_modes_selected = True

        if self.record_screen_var.get():
            self.central_data_controller.active_handlers.append('s')
            recording_modes_selected = True

        if self.record_webcam_var.get():
            self.central_data_controller.active_handlers.append('w')
            recording_modes_selected = True

        if not recording_modes_selected:
            self._update_status("No recording modes selected", "red")
            return

        try:
            self._update_status("Starting recording...", "orange")
            self.root.update()  # Force UI update
            
            self.central_data_controller.start_recording()
            self._update_status("Recording Started", "blue")
            
        except Exception as e:
            self._update_status(f"Error: {str(e)}", "red")
            print(f"Error in start_recording: {e}")

    def _end_recording(self):
        if len(self.central_data_controller.active_handlers) > 0:
            self.central_data_controller.stop_recording(self.location_entry.get())
            self._update_status("Recording Ended", "green")
        else:
            self._update_status("No recording was in progress", "orange")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()
