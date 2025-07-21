import subprocess
import glob
from pathlib import Path

class Webcam_Process:
    def __init__(self):
        self.openface_exe_path = 'external/OpenFace/build/bin/FeatureExtraction'
    
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
            
            print(file)
            print(output_dir)

            subprocess.run([
                self.openface_exe_path,
                '-f', file,
                '-out_dir', str(output_dir),
                '-2Dfp', '-3Dfp', '-pose', '-gaze', '-aus', '-pdmparams',
                '-hogalign', '-simalign', '-nomask', '-nobadaligned', '-tracked'
            ])
