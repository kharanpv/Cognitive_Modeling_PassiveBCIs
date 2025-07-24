import easyocr
import os
import json
import glob
import cv2
from pathlib import Path

class Screen_Process:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "config.json")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, Exception):
                # If file is corrupted or empty, start fresh
                raise ValueError("Config.json either corrupted or empty. Model generation failed")
        else:
            raise FileNotFoundError('config.json file not found. Model generation failed.')

        self.config = config

    def process_screen_capture(self, folder):
        # Run easyocr

        # Get list of all videos named "screen_capture.avi" in folder
        file_list = glob.glob(f'{folder}/**/screen_capture.avi', recursive=True)

        for file in file_list:
            file_path = Path(file)
            output_foldername = file_path.parent.name
            data_folder = file_path.parent.parent

            output_dir = data_folder / 'EasyOCR' / output_foldername
            output_dir.mkdir(parents=True, exist_ok=True)
        
            # Open video
            capture = cv2.VideoCapture()
            reader = easyocr.Reader(['en']) # Currently only english

            frame_idx = 0
            ocr_results = []
            frame_interval = 10

            while capture.isOpened():
                return_val, frame = capture.read()
                if not return_val:
                    break

                if frame_idx % frame_interval:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGR)
                    ocr_out = reader.readtext(rgb_frame)

                    timestamp = frame_idx / 28.8
                    for bbox, text, conf in ocr_out:
                        ocr_results.append({
                            'timestamp': timestamp,
                            'text': text,
                            'confidence': conf,
                            'bbox': bbox  # (x0, y0), (x1, y1), (x2, y2), (x3, y3)
                        })
                
                frame_idx += 1

            capture.release()

            output_filepath = output_dir / 'ocr_output.json'

            with output_filepath.open('w', encoding='utf-8') as f:
                json.dump(ocr_results, f, indent=2)

