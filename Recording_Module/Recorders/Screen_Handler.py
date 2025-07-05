from mss import mss
import ctypes
import cv2
import numpy as np
import os
import tempfile
import shutil
import pyautogui
import time
import subprocess
from .Handler import Handler


class Screen_Handler(Handler):
    def __init__(self, update_status_callback=None):
        super().__init__()
        self.resolution = (1280, 720)
        self.fps = 28.8
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.update_status_callback = update_status_callback  # Callback to update the status box

    def _run_listener(self, stop_event, pipe_conn):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = os.path.join(temp_dir, 'screen_capture.avi')

                with mss() as sct:
                    if os.name == 'nt':
                        user32 = ctypes.windll.user32 
                        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                        monitor = {
                            "left": 0,
                            "top": 0,
                            "width": screensize[0],
                            "height": screensize[1],
                        }
                        
                    else:
                        monitor = sct.monitors[0]  # Full screen

                    output = cv2.VideoWriter(temp_path, self.codec, self.fps, self.resolution)
                    if not output.isOpened():
                        return

                    start_time = time.time()
                    frame_count = 0
                    
                    while not stop_event.is_set():
                        try:
                            frame = np.array(sct.grab(monitor))
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                            resized_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)
                            frame_count += 1
                            
                            # Draw the mouse cursor onto the frame
                            x, y = pyautogui.position()
                            cursor_color = (0, 0, 255)  # Red dot
                            cursor_radius = 5
                            cv2.circle(resized_frame, (x, y), cursor_radius, cursor_color, -1)

                            output.write(resized_frame)
                            
                            if not output.isOpened():
                                break
                            
                        except Exception as e:
                            if self.update_status_callback:
                                self.update_status_callback(f"Error during frame processing: {e}", "red")

                    output.release()
                    
                    # Matching length of recorded video with desired 28.8 fps
                    end_time = time.time()
                    duration = end_time - start_time
                    nominal_duration = frame_count / self.fps
                    stretch_factor = duration / nominal_duration
                    adjusted_capture_path = os.path.join(temp_dir, '_screen_capture.avi')
                    
                    cmd = [
                        "ffmpeg",
                        "-i", temp_path,
                        "-filter:v", f"setpts={stretch_factor:.6f}*PTS",
                        "-c:v", "libxvid",               # assuming Xvid
                        "-b:v", "3200k",                 # match original bitrate
                        "-y",                            # overwrite
                        adjusted_capture_path
                    ]
                    subprocess.run(cmd, check=True)
                
                save_dir = pipe_conn.recv()
                os.makedirs(save_dir, exist_ok=True)
                save_location = os.path.join(save_dir, 'screen_capture.avi')

                try:
                    shutil.move(adjusted_capture_path, save_location)
                except Exception as e:
                    if self.update_status_callback:
                        self.update_status_callback(f"Error while moving video file: {e}", "red")
        except Exception as e:
            if self.update_status_callback:
                self.update_status_callback(f"Critical error in _run_listener: {e}", "red")


