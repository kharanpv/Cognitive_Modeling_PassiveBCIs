from mss import mss
import ctypes
import cv2
import numpy as np
import os
import tempfile
import shutil
import pyautogui
import time
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

                    while not stop_event.is_set():
                        try:
                            start = time.time()
                            
                            frame = np.array(sct.grab(monitor))
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                            resized_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)

                            # Draw the mouse cursor onto the frame
                            x, y = pyautogui.position()
                            cursor_color = (0, 0, 255)  # Red dot
                            cursor_radius = 5
                            cv2.circle(resized_frame, (x, y), cursor_radius, cursor_color, -1)

                            output.write(resized_frame)
                            
                            # Frame synchronization
                            elapsed = time.time() - start
                            time_to_sleep = max(0, 1/self.fps - elapsed)
                            time.sleep(time_to_sleep)
                            
                            if not output.isOpened():
                                break
                            
                        except Exception as e:
                            if self.update_status_callback:
                                self.update_status_callback(f"Error during frame processing: {e}", "red")

                    output.release()
                
                save_dir = pipe_conn.recv()
                os.makedirs(save_dir, exist_ok=True)
                save_location = os.path.join(save_dir, 'screen_capture.avi')

                try:
                    shutil.move(temp_path, save_location)
                except Exception as e:
                    if self.update_status_callback:
                        self.update_status_callback(f"Error while moving video file: {e}", "red")
        except Exception as e:
            if self.update_status_callback:
                self.update_status_callback(f"Critical error in _run_listener: {e}", "red")


