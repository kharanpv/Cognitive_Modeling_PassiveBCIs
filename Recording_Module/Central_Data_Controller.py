import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler
from .Recorders.Screen_Handler import Screen_Handler
from .Recorders.Webcam_Handler import Webcam_Handler

import datetime

class Central_Data_Controller:
    def __init__(self, update_status_callback=None):
        self.screen_handler = Screen_Handler(update_status_callback)
        self.webcam_handler = Webcam_Handler()
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

        if 's' in self.active_handlers:
            self.screen_handler.trigger_listener('start')
        
        if 'w' in self.active_handlers:
            self.webcam_handler.trigger_listener('start')

    def stop_recording(self, recording_location):
        self.latest_stop_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        recording_folder = os.path.join(recording_location, self.latest_start_time + '_--_' + self.latest_stop_time)
        
        # Create the recording folder
        os.makedirs(recording_folder, exist_ok=True)
        
        if 'k' in self.active_handlers:
            self.keyboard_handler.trigger_listener('stop', recording_folder)
            self.active_handlers.remove('k')

        if 'm' in self.active_handlers:
            self.mouse_handler.trigger_listener('stop', recording_folder)
            self.active_handlers.remove('m')
        
        if 's' in self.active_handlers:
            self.screen_handler.trigger_listener('stop', recording_folder)
            self.active_handlers.remove('s')
        
        if 'w' in self.active_handlers:
            self.webcam_handler.trigger_listener('stop', recording_folder)
            self.active_handlers.remove('w')