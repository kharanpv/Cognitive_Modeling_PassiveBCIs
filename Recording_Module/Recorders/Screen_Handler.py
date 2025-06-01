from mss import mss
import cv2
import numpy as np
import os
import tempfile
import shutil
import pyautogui
from .Handler import Handler


class Screen_Handler(Handler):
    def __init__(self):
        super().__init__()
        self.resolution = (1280, 720)
        self.fps = 24
        self.codec = cv2.VideoWriter_fourcc(*"XVID")

    def _run_listener(self, stop_event, pipe_conn):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = os.path.join(temp_dir, 'screen_capture.avi')

                with mss() as sct:
                    monitor = sct.monitors[0]  # Full screen

                    output = cv2.VideoWriter(temp_path, self.codec, self.fps, self.resolution)
                    if not output.isOpened():
                        return

                    frame_count = 0
                    while not stop_event.is_set():
                        try:
                            sct_img = sct.grab(monitor)
                            frame = np.array(sct_img)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                            resized_frame = cv2.resize(frame, self.resolution, interpolation=cv2.INTER_AREA)

                            # Draw the mouse cursor onto the frame
                            x, y = pyautogui.position()
                            cursor_color = (0, 0, 255)  # Red dot
                            cursor_radius = 5
                            cv2.circle(resized_frame, (x, y), cursor_radius, cursor_color, -1)

                            # Save individual frames for debugging
                            debug_frame_path = os.path.join(temp_dir, f"debug_frame_{frame_count}.jpg")
                            cv2.imwrite(debug_frame_path, resized_frame)

                            output.write(resized_frame)
                            if not output.isOpened():
                                break
                            frame_count += 1
                        except Exception as e:
                            pass

                    output.release()
                
                save_dir = pipe_conn.recv()
                os.makedirs(save_dir, exist_ok=True)
                save_location = os.path.join(save_dir, 'screen_capture.avi')

                try:
                    shutil.move(temp_path, save_location)
                except Exception as e:
                    pass
        except Exception as e:
            pass


