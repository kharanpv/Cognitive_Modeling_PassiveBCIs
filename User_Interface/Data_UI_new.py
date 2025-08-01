import tkinter as tk
from tkinter import Checkbutton, BooleanVar, filedialog
import os
import time
import threading
from Base_UI import BaseUI

class DataUI(BaseUI):
    """
    A graphical user interface class for managing data recording operations.
    
    This class provides a complete UI for controlling various recording options including:
    - Keyboard input recording
    - Mouse movement recording
    - Screen recording
    - Webcam recording
    
    It also handles recording timer display, storage location management,
    and status updates for the recording process.
    """

    def __init__(self, root):
        """
        Initialize the Data UI components.

        Args:
            root: The tkinter root window
        """
        # Initialize the base UI with title
        super().__init__(root, "Data Recording - Cognitive Modeler")
        
        # Initialize checkbox variables (matching original names)
        self.record_keyboard_var = BooleanVar()
        self.record_mouse_var = BooleanVar()
        self.record_screen_var = BooleanVar()
        self.record_webcam_var = BooleanVar()
        
        # Timer-related
        self.recording_start_time = None
        self.recording_timer_job = None
        self.recording_timer_label = None
        
        self._setup_ui()

    def _setup_ui(self):
        """
        Set up the main UI components including title,
        checkboxes, location selection, and recording controls.
        """
        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack(side='top', fill='x', pady=10)
        
        title_label = tk.Label(self.title_frame, text="Data", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Timer label placeholder (starts hidden)
        self.recording_timer_label = tk.Label(self.root, font=("Arial", 12), fg="gray")
        
        self._setup_checkboxes()
        self._setup_location_selection()
        self._setup_recording_controls()
    
    def _setup_checkboxes(self):
        """
        Create checkboxes for selecting different recording modes:
        keyboard, mouse, screen, and webcam.
        """
        checkbox_frame = tk.Frame(self.root, padx=20, pady=10)
        checkbox_frame.pack(side='top', fill='x')
        
        Checkbutton(checkbox_frame, text="Record Keyboard", 
                   variable=self.record_keyboard_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Mouse", 
                   variable=self.record_mouse_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Screen", 
                   variable=self.record_screen_var).pack(anchor='w', pady=5)
        Checkbutton(checkbox_frame, text="Record Webcam", 
                   variable=self.record_webcam_var).pack(anchor='w', pady=5)

    def _setup_location_selection(self):
        """
        Create UI elements for selecting and managing the data storage location.
        Includes entry field, browse button, and open location button.
        """
        location_frame = tk.Frame(self.root, padx=20, pady=10)
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

    def _setup_recording_controls(self):
        """
        Set up the recording control buttons and icons.
        Includes start and stop recording buttons with corresponding icons.
        """
        controls_frame = tk.Frame(self.root, padx=20, pady=20)
        controls_frame.pack(side='bottom', fill='x', pady=20)
        
        icons_frame = tk.Frame(controls_frame)
        icons_frame.pack(fill='x')
        
        play_icon = tk.Label(icons_frame, text="▶", font=("Arial", 16))
        stop_icon = tk.Label(icons_frame, text="⏹", font=("Arial", 16))
        
        play_icon.grid(row=0, column=0, padx=20)
        stop_icon.grid(row=0, column=1, padx=20)
        
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        icons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        start_button = tk.Button(buttons_frame, text="Start Recording", command=self._start_recording)
        end_button = tk.Button(buttons_frame, text="End Recording", command=self._end_recording)
        
        start_button.grid(row=0, column=0, padx=10)
        end_button.grid(row=0, column=1, padx=10)
        
        play_icon.grid(row=0, column=0, padx=20, sticky='n')
        stop_icon.grid(row=0, column=1, padx=20, sticky='n')

    def _choose_location(self):
        """
        Open a directory selection dialog and update the location entry
        with the selected path.
        """
        directory = filedialog.askdirectory(initialdir=self.default_data_dir)
        if directory:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, directory)

    def _open_location(self):
        """
        Open the current storage location in the system's file explorer.
        Handles different operating systems (Windows, macOS, Linux).
        """
        location = self.location_entry.get()
        if os.path.exists(location):
            if os.name == 'nt':
                os.startfile(location)
            elif os.name == 'posix':
                import subprocess
                import sys
                subprocess.call(['open', location] if sys.platform == 'darwin' else ['xdg-open', location])

    def _start_recording(self):
        """
        Start the recording process based on selected modes.
        
        - Validates that at least one recording mode is selected
        - Initializes the central data controller with selected modes
        - Updates UI status and starts the recording timer
        - Handles any errors during the recording start process
        """
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
            self.update_status("No recording modes selected", "red")
            return

        try:
            self.update_status("Starting recording...", "orange")
            self.root.update()  # Force UI update
            
            self.central_data_controller.start_recording()
            self.update_status("Recording Started", "blue")
            
            # Start the timer
            self._start_timer()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            print(f"Error in start_recording: {e}")
    
    def _end_recording(self):
        """
        Stop all active recordings and save the recorded data.
        Updates the UI status and stops the recording timer.
        """
        if len(self.central_data_controller.active_handlers) > 0:
            self.update_status("Processing recordings", "yellow")
            self.central_data_controller.stop_recording(self.location_entry.get())
            
            # Stop the timer
            self._stop_timer()

            # Start processing in a background thread
            threading.Thread(
                target=self._run_post_processing_thread,
                daemon=True
            ).start()

        else:
            self.update_status("No recording was in progress", "orange")
    
    def _run_post_processing_thread(self):
        self.central_data_controller._process_recordings()
        self.root.after(0, lambda: self.update_status("Recording Ended", "green"))

    def _start_timer(self):
        """
        Initialize and start the recording duration timer.
        Displays time in HH:MM:SS format.
        """
        self.recording_start_time = time.time()
        self.recording_timer_label.config(text="Recording for: 00:00:00", fg="gray")
        self.recording_timer_label.pack(after=self.title_frame)
        self._update_timer()

    def _update_timer(self):
        """
        Update the timer display every second while recording.
        Formats time as HH:MM:SS and schedules the next update.
        """
        if self.recording_start_time is None:
            return
        elapsed = int(time.time() - self.recording_start_time)
        hrs, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.recording_timer_label.config(text=f"Recording for: {time_str}")
        self.recording_timer_job = self.root.after(1000, self._update_timer)

    def _stop_timer(self):
        """
        Stop the recording timer and display the final duration.
        Cancels the timer update job and updates the timer label.
        """
        if self.recording_timer_job:
            self.root.after_cancel(self.recording_timer_job)
            self.recording_timer_job = None
        if self.recording_start_time is not None:
            elapsed = int(time.time() - self.recording_start_time)
            hrs, rem = divmod(elapsed, 3600)
            mins, secs = divmod(rem, 60)
            time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
            self.recording_timer_label.config(text=f"Last Recording: {time_str}", fg="gray")
            self.recording_start_time = None


if __name__ == "__main__":
    """
    Run the Data UI as a standalone application.
    """
    root = tk.Tk()
    app = DataUI(root)
    root.mainloop()
