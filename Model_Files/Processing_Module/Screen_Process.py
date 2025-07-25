import easyocr
import os
import json
import glob
import cv2
from pathlib import Path
from numpyencoder import NumpyEncoder


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
        
        print(f"Found {len(file_list)} screen capture files to process")

        for file in file_list:
            print(f"Processing file: {file}")
            file_path = Path(file)
            output_foldername = file_path.parent.name
            data_folder = file_path.parent.parent

            output_dir = data_folder / 'EasyOCR' / output_foldername
            output_dir.mkdir(parents=True, exist_ok=True)

            output_filepath = output_dir / 'ocr_output.json'
            if not output_filepath.exists():
                output_filepath.touch()
        
            reader = easyocr.Reader(['en']) # Currently only english
            
            # Get number of frames
            probe_capture = cv2.VideoCapture(file)
            if not probe_capture.isOpened():
                print(f"❌ Failed to open video capture for: {file}")
                exit(1)

            frame_count = int(probe_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"✅ Successfully opened video capture for: {file}")
            print(f"Reported frame count: {frame_count}")
            probe_capture.release()

            ocr_result_buffer = []
            frame_interval = 10
            batch_size = 100

            
            for frame_idx in range(0, frame_count, frame_interval):
                capture = cv2.VideoCapture(file)
                if not capture.isOpened():
                    print(f"❌ Failed to re-open video at frame {frame_idx}")
                    continue

                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                return_val, frame = capture.read()
                capture.release()
                
                if not return_val:
                    print(f"🛑 Failed to read frame at index {frame_idx}")
                    break

                if frame_idx % frame_interval == 0:
                    ocr_out = reader.readtext(frame)

                    timestamp = frame_idx / 28.8
                    print(f"🔍 Processing OCR at timestamp: {timestamp:.2f}s (frame {frame_idx})")
            
                    for bbox, text, conf in ocr_out:
                        ocr_result_buffer.append({
                            'timestamp': timestamp,
                            'text': text,
                            'confidence': conf,
                            'bbox': bbox  # (x0, y0), (x1, y1), (x2, y2), (x3, y3)
                        })
                    
                    if len(ocr_result_buffer) >= batch_size:
                        with output_filepath.open('a', encoding='utf-8') as f:
                            for record in ocr_result_buffer:
                                f.write(json.dumps(record, cls=NumpyEncoder)+'\n')
                        ocr_result_buffer.clear()
                    
                
                frame_idx += 1

            capture.release()
            
            if ocr_result_buffer:
                with output_filepath.open('a', encoding='utf-8') as f:
                    for record in ocr_result_buffer:
                        f.write(json.dumps(record, cls=NumpyEncoder)+'\n')

            print(f"📝 Processed OCR results for {file}")

            # Restructure json file in a list format
            temp_filepath = output_dir / 'temp.json'
            with output_filepath.open('r', encoding='utf-8') as fin, \
                 temp_filepath.open('w', encoding='utf-8') as fout:
                fout.write('[\n')
                is_first = True

                for line in fin:
                    record = line.strip()
                    if not record:
                        continue

                    if not is_first:
                        fout.write(',\n')

                    fout.write(record)
                    is_first = False

                fout.write('\n]')

            print(f"💾 Saved OCR results to: {output_filepath}")

