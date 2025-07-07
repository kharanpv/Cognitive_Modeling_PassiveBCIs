import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler
from .Recorders.Screen_Handler import Screen_Handler
from .Recorders.Webcam_Handler import Webcam_Handler

import datetime

class Central_Data_Controller:
    """
    Central controller for managing multiple data recording handlers.
    
    This class coordinates the recording of various data streams including:
    - Keyboard input
    - Mouse movements and clicks
    - Screen recordings
    - Webcam footage
    
    Each data stream is handled by a specialized handler class and can be
    activated/deactivated independently. The controller manages the recording lifecycle,
    including starting, stopping, and post-processing of recordings.
    """

    def __init__(self):
        """
        Initialize the controller with all available handlers.
        
        Creates instances of all recording handlers and initializes tracking variables
        for recording sessions. The handlers include:
        - Screen recording handler
        - Webcam recording handler
        - Keyboard input handler
        - Mouse movement handler
        """
        self.screen_handler = Screen_Handler()
        self.webcam_handler = Webcam_Handler()
        self.keyboard_handler = Keyboard_Handler()
        self.mouse_handler = Mouse_Handler()

        self.active_handlers = []
        self.latest_start_time = str()
        self.latest_stop_time = str()
        self.recording_folder = str()

    def start_recording(self):
        """
        Start recording for all active handlers.
        
        Creates a timestamp for the recording start time and triggers
        all active handlers to begin their recording processes.
        
        Active handlers are identified by single-letter codes:
        - 'k': Keyboard recording
        - 'm': Mouse movement recording
        - 's': Screen recording
        - 'w': Webcam recording
        
        The start time is stored in YYYY-MM-DD_HH-MM-SS format.
        """
        self.latest_start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  

        if 'k' in self.active_handlers:
            self.keyboard_handler.trigger_listener('start')

        if 'm' in self.active_handlers:
            self.mouse_handler.trigger_listener('start')

        if 's' in self.active_handlers:
            self.screen_handler.trigger_listener('start')
        
        if 'w' in self.active_handlers:
            self.webcam_handler.trigger_listener('start')

    def stop_recording(self, recording_location):
        """
        Stop all active recordings and save data to specified location.
        
        Args:
            recording_location (str): Base directory where recording data will be saved.
                                    A new subfolder will be created using the start
                                    and stop timestamps.
        
        Creates a new folder named with the format:
        'start_timestamp_--_stop_timestamp' under the specified location.
        Each active handler's data is saved to this folder and the handler
        is deactivated after saving.
        """
        self.latest_stop_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.recording_folder = os.path.join(recording_location, self.latest_start_time + '_--_' + self.latest_stop_time)
        
        # Create the recording folder
        os.makedirs(self.recording_folder, exist_ok=True)
        
        if 'k' in self.active_handlers:
            self.keyboard_handler.trigger_listener('stop', self.recording_folder)
            self.active_handlers.remove('k')

        if 'm' in self.active_handlers:
            self.mouse_handler.trigger_listener('stop', self.recording_folder)
            self.active_handlers.remove('m')
        
        if 's' in self.active_handlers:
            self.screen_handler.trigger_listener('stop', self.recording_folder)
            self.active_handlers.remove('s')
        
        if 'w' in self.active_handlers:
            self.webcam_handler.trigger_listener('stop', self.recording_folder)
            self.active_handlers.remove('w')


    def process_recordings(self):
        """
        Post-process recorded data to ensure synchronization and quality.
        
        Currently handles screen recording synchronization:
        1. Determines actual duration of the screen recording using ffprobe
        2. Calculates the nominal duration from start/stop timestamps
        3. Adjusts video playback speed to match the nominal duration
        4. Reencodes the video using Xvid codec at 3200k bitrate
        
        This ensures that the screen recording matches the actual timeline
        of other recorded data streams.
        
        Note:
            Requires ffmpeg and ffprobe to be installed on the system.
            Currently only processes screen recordings, other data streams
            may be added in future versions.
        """
        # Post-process recordings
        
        # Screen capture
        screen_recording_filepath = os.path.join(self.recording_folder, 'screen_capture.avi')
        actual_duration = float(
            subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of",
                            "default=noprint_wrappers=1:nokey=1", screen_recording_filepath],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout
        )
    
        latest_start_time = datetime.datetime.strptime(self.latest_start_time, '%Y-%m-%d_%H-%M-%S')
        latest_stop_time = datetime.datetime.strptime(self.latest_stop_time, '%Y-%m-%d_%H-%M-%S')
        nominal_duration = (latest_stop_time - latest_start_time).seconds

        stretch_factor = nominal_duration / actual_duration
        
        if stretch_factor > 1.01 or stretch_factor < 0.99:
            adjusted_capture_path = os.path.join(self.recording_folder, '_screen_capture.avi')
            
            cmd = [
                "ffmpeg",
                "-i", screen_recording_filepath,
                "-filter:v", f"setpts={stretch_factor:.6f}*PTS",
                "-c:v", "libxvid",               # assuming Xvid
                "-b:v", "3200k",                 # match original bitrate
                "-y",                            # overwrite
                adjusted_capture_path
            ]
            subprocess.run(cmd, check=True)
            os.replace(adjusted_capture_path, screen_recording_filepath)

        # Webcam Capture
        screen_recording_filepath = os.path.join(self.recording_folder, 'webcam_capture.avi')
        actual_duration = float(
            subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of",
                            "default=noprint_wrappers=1:nokey=1", screen_recording_filepath],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout
        )
    
        nominal_duration = (latest_stop_time - latest_start_time).seconds

        stretch_factor = nominal_duration / actual_duration
        
        if stretch_factor > 1.01 or stretch_factor < 0.99:
            adjusted_capture_path = os.path.join(self.recording_folder, '_webcam_capture.avi')
            
            cmd = [
                "ffmpeg",
                "-i", screen_recording_filepath,
                "-filter:v", f"setpts={stretch_factor:.6f}*PTS",
                "-c:v", "libxvid",               # assuming Xvid
                "-b:v", "3200k",                 # match original bitrate
                "-y",                            # overwrite
                adjusted_capture_path
            ]
            subprocess.run(cmd, check=True)
            os.replace(adjusted_capture_path, screen_recording_filepath)