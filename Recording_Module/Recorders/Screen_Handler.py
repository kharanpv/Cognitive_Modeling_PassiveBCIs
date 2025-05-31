from mss import mss
import cv2
import numpy as np
import os
import tempfile
import shutil
from .Handler import Handler


class Screen_Handler(Handler):
    def __init__(self):
        super().__init__()
        self.resolution = (1280, 720)
        self.fps = 24
        self.codec = cv2.VideoWriter_fourcc(*"XVID")

    def _run_listener(self, stop_event, pipe_conn):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, 'screen_capture.avi')

            with mss() as sct:
                monitor = sct.monitors[0]  # Full screen
                self.resolution = (monitor['width'], monitor['height'])
                output = cv2.VideoWriter(temp_path, self.codec, self.fps, self.resolution)

                if not output.isOpened():
                    print(f"Failed to open VideoWriter at: {temp_path}")
                    return

                while not stop_event.is_set():
                    sct_img = sct.grab(monitor)
                    frame = np.array(sct_img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    output.write(frame)

                output.release()

            save_dir = pipe_conn.recv()
            os.makedirs(save_dir, exist_ok=True)
            save_location = os.path.join(save_dir, 'screen_capture.avi')
            
            try:
                shutil.move(temp_path, save_location)
            except Exception as e:
                print(f"Error while moving video file: {e}")


