import cv2
import tempfile
import os
import shutil
from .Handler import Handler

class Webcam_Handler(Handler):
    def __init__(self, update_status_callback=None):
        super().__init__()
        self.fps = 24
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.resolution = tuple()
        self.update_status_callback = update_status_callback  # Callback to update the status box

    def _run_listener(self, stop_event, pipe_conn):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = os.path.join(temp_dir, 'webcam_capture.avi')
                cam = cv2.VideoCapture(0)
                self.resolution = (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                output = cv2.VideoWriter(temp_path, self.codec, self.fps, self.resolution)

                if not output.isOpened():
                    if self.update_status_callback:
                        self.update_status_callback("Failed to open VideoWriter for webcam.", "red")
                    return

                while not stop_event.is_set():
                    try:
                        ret, frame = cam.read()
                        if not ret:
                            if self.update_status_callback:
                                self.update_status_callback("Failed to read frame from webcam.", "red")
                            continue

                        output.write(frame)
                    except Exception as e:
                        if self.update_status_callback:
                            self.update_status_callback(f"Error during webcam frame processing: {e}", "red")

                output.release()
                cam.release()

                save_dir = pipe_conn.recv()
                os.makedirs(save_dir, exist_ok=True)
                save_location = os.path.join(save_dir, 'webcam_capture.avi')

                try:
                    shutil.move(temp_path, save_location)
                except Exception as e:
                    if self.update_status_callback:
                        self.update_status_callback(f"Error while moving webcam video file: {e}", "red")
        except Exception as e:
            if self.update_status_callback:
                self.update_status_callback(f"Critical error in webcam listener: {e}", "red")

