import subprocess
import glob
from pathlib import Path
import os
import json

class Webcam_Process:
    def __init__(self):
        self.openface_exe_path = 'external/OpenFace/build/bin/FeatureExtraction'

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

    def process_webcam_video(self, folder):
        # Run Openface CLI to run and store feature extraction of all webcam videos
        # in given folder

        # Get list of all videos named "webcam_capture.avi" in folder
        file_list = glob.glob(f'{folder}/**/webcam_capture.avi', recursive=True)

        for file in file_list:
            # Create output folder for given file
            file_path = Path(file)
            output_foldername = file_path.parent.name
            data_folder = file_path.parent.parent

            output_dir = data_folder / 'Openface' / output_foldername
            output_dir.mkdir(parents=True, exist_ok=True)

            subprocess.run([
                self.openface_exe_path,
                '-f', file,
                '-out_dir', str(output_dir),
                '-2Dfp', '-3Dfp', '-pose', '-gaze', '-aus', '-pdmparams',
                '-hogalign', '-simalign', '-nomask', '-nobadaligned', 
                '-tracked' if self.config["create_tracked_video"] else ''
            ])
