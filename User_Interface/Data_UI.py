import tkinter as tk
from tkinter import Checkbutton, BooleanVar, filedialog
import os
import sys
import time

class DataUI:
    def __init__(self, parent_frame, app_instance):
        self.parent_frame = parent_frame
        self.app = app_instance
        
        # Initialize checkbox variables
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
        self._setup_status_box()
        
        title_frame = tk.Frame(self.parent_frame)
        title_frame.pack(side='top', fill='x', pady=10)
        
        title_label = tk.Label(title_frame, text="Data", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Timer label placeholder (starts hidden)
        self.recording_timer_label = tk.Label(self.parent_frame, font=("Arial", 12), fg="gray")
        
        self._setup_checkboxes()
        self._setup_location_selection()
        self._setup_recording_controls()
    
    def _setup_status_box(self):
        status_frame = tk.Frame(self.parent_frame, padx=20, pady=10)
        status_frame.pack(side='top', fill='x')
        
        status_label = tk.Label(status_frame, text="Program Status:", anchor='w')
        status_label.pack(side='left')
        
        self.status_text = tk.Label(status_frame, text="Ready", anchor='w', fg="green")
        self.status_text.pack(side='left', padx=5)
    
    def _update_status(self, message, color="black"):
        self.status_text.config(text=message, fg=color)
    
    def _setup_checkboxes(self):
        checkbox_frame = tk.Frame(self.parent_frame, padx=20, pady=10)
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
        location_frame = tk.Frame(self.parent_frame, padx=20, pady=10)
        location_frame.pack(side='top', fill='x')
        
        location_label = tk.Label(location_frame, text="Data Storage Location:")
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
    
    def _setup_recording_controls(self):
        controls_frame = tk.Frame(self.parent_frame, padx=20, pady=20)
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
        directory = filedialog.askdirectory(initialdir=self.app.default_data_dir)
        if directory:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, directory)
    
    def _open_location(self):
        location = self.location_entry.get()
        if os.path.exists(location):
            if os.name == 'nt':
                os.startfile(location)
            elif os.name == 'posix':
                import subprocess
                import sys
                subprocess.call(['open', location] if sys.platform == 'darwin' else ['xdg-open', location])
    
    def _start_recording(self):
        recording_modes_selected = False
        
        # Clear any previous handlers to avoid duplicates
        self.app.central_data_controller.active_handlers = []
        
        if self.record_keyboard_var.get():
            self.app.central_data_controller.active_handlers.append('k')
            recording_modes_selected = True
        
        if self.record_mouse_var.get():
            self.app.central_data_controller.active_handlers.append('m')
            recording_modes_selected = True

        if self.record_screen_var.get():
            self.app.central_data_controller.active_handlers.append('s')
            recording_modes_selected = True

        if self.record_webcam_var.get():
            self.app.central_data_controller.active_handlers.append('w')
            recording_modes_selected = True

        if not recording_modes_selected:
            self._update_status("No recording modes selected", "red")
            return

        try:
            self._update_status("Starting recording...", "orange")
            self.parent_frame.update()  # Force UI update
            
            self.app.central_data_controller.start_recording()
            self._update_status("Recording Started", "blue")
            
            # Start the timer
            self._start_timer()
            
        except Exception as e:
            self._update_status(f"Error: {str(e)}", "red")
            print(f"Error in start_recording: {e}")
    
    def _end_recording(self):
        if len(self.app.central_data_controller.active_handlers) > 0:
            self.app.central_data_controller.stop_recording(self.location_entry.get())
            self._update_status("Recording Ended", "green")
            
            # Stop the timer
            self._stop_timer()
        else:
            self._update_status("No recording was in progress", "orange")
    
    # Timer methods
    def _start_timer(self):
        self.recording_start_time = time.time()
        self.recording_timer_label.config(text="Recording for: 00:00:00", fg="gray")
        self.recording_timer_label.pack(after=self.status_text.master)
        self._update_timer()

    def _update_timer(self):
        if self.recording_start_time is None:
            return
        elapsed = int(time.time() - self.recording_start_time)
        hrs, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.recording_timer_label.config(text=f"Recording for: {time_str}")
        self.recording_timer_job = self.parent_frame.after(1000, self._update_timer)

    def _stop_timer(self):
        if self.recording_timer_job:
            self.parent_frame.after_cancel(self.recording_timer_job)
            self.recording_timer_job = None
        if self.recording_start_time is not None:
            elapsed = int(time.time() - self.recording_start_time)
            hrs, rem = divmod(elapsed, 3600)
            mins, secs = divmod(rem, 60)
            time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
            self.recording_timer_label.config(text=f"Last Recording: {time_str}", fg="gray")
            self.recording_start_time = None
