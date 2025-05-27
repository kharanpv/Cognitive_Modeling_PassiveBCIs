import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Recorders.DOM_Handler import DOM_Handler
from .Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler
from .Recorders.Screen_Handler import Screen_Handler
from .Recorders.Webcam_Handler import Webcam_Handler

import datetime
import pandas as pd

class Central_Data_Controller:
    def __init__(self):
        # self.DOM_handler = DOM_Handler()
        # self.screen_handler = Screen_Handler()
        # self.webcam_handler = Webcam_Handler()
        self.keyboard_handler = Keyboard_Handler()
        self.mouse_handler = Mouse_Handler()

        self.active_handlers = []
        self.latest_start_time = str()
        self.latest_stop_time = str()

    def start_recording(self):
        self.latest_start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  

        if 'k' in self.active_handlers:
            self.keyboard_handler.trigger_listener('start')

        if 'm' in self.active_handlers:
            self.mouse_handler.trigger_listener('start')

    def stop_recording(self, recording_location):
        self.latest_stop_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        recording_folder = os.path.join(recording_location, self.latest_start_time + '_--_' + self.latest_stop_time)
        
        # Create the recording folder
        os.makedirs(recording_folder, exist_ok=True)
        
        if 'k' in self.active_handlers:
            self.keyboard_handler.trigger_listener('stop')
            key_log = self.keyboard_handler.log 
            key_log.to_csv(os.path.join(recording_folder, 'key_log.csv'), index=False)
            self.active_handlers.remove('k')

        if 'm' in self.active_handlers:
            self.mouse_handler.trigger_listener('stop') 
            mouse_log = self.mouse_handler.log 
            mouse_log.to_csv(os.path.join(recording_folder, 'mouse_log.csv'), index=False)
            self.active_handlers.remove('m')