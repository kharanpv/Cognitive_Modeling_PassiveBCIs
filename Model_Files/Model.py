from .Processing_Module.Webcam_Process import Webcam_Process

class Model:
    def __init__(self):
        self.data_folder = str()
        self.webcam_process = Webcam_Process()

    def generate_model(self):
        # First step is processing data
        self.process_data()

    def process_data(self):
        self.webcam_process.process_webcam_video(self.data_folder)
        # Process all the different modalities of data to be meaningful in model generation
