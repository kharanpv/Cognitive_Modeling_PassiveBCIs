from .Processing_Module.Webcam_Process import Webcam_Process
from .Processing_Module.Screen_Process import Screen_Process
from multiprocessing import Process

class Model:
    def __init__(self):
        self.data_folder = str()
        self.webcam_processor = Webcam_Process()
        self.screen_processor = Screen_Process()

    def generate_model(self):
        # First step is processing data
        self.process_data()

    def process_data(self):
        webcam_process = Process(target=self.webcam_processor.process_webcam_video, args=(self.data_folder,))
        screen_Process = Process(target=self.screen_processor.process_screen_capture, args=(self.data_folder,))
        
        # Process all the different modalities of data to be meaningful in model generation
        webcam_process.start()
        screen_Process.start()

