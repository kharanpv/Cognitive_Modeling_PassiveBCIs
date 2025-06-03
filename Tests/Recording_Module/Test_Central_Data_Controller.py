import pytest

from Recording_Module.Central_Data_Controller import Central_Data_Controller
from Recording_Module.Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler
from Recording_Module.Recorders.Screen_Handler import Screen_Handler
from Recording_Module.Recorders.Webcam_Handler import Webcam_Handler

class Test_Central_data_Controller:
    def test_init(self):
        self.central_data_controller = Central_Data_Controller()
        
        assert isinstance(self.central_data_controller.screen_handler, Screen_Handler)
        assert isinstance(self.central_data_controller.webcam_handler, Webcam_Handler)
        assert isinstance(self.central_data_controller.keyboard_handler, Keyboard_Handler)
        assert isinstance(self.central_data_controller.mouse_handler, Mouse_Handler)

        assert len(self.central_data_controller.active_handlers) == 0
        assert isinstance(self.central_data_controller.latest_start_time, str)
        assert isinstance(self.central_data_controller.latest_stop_time, str)
    
