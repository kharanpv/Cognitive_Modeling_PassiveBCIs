import pytest
from unittest.mock import patch

from Recording_Module.Central_Data_Controller import Central_Data_Controller
from Recording_Module.Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler
from Recording_Module.Recorders.Screen_Handler import Screen_Handler
from Recording_Module.Recorders.Webcam_Handler import Webcam_Handler

@pytest.fixture
def controller():
    return Central_Data_Controller()

def test_init(controller):
    controller.central_data_controller = Central_Data_Controller()
    
    assert isinstance(controller.central_data_controller.screen_handler, Screen_Handler)
    assert isinstance(controller.central_data_controller.webcam_handler, Webcam_Handler)
    assert isinstance(controller.central_data_controller.keyboard_handler, Keyboard_Handler)
    assert isinstance(controller.central_data_controller.mouse_handler, Mouse_Handler)

    assert len(controller.central_data_controller.active_handlers) == 0
    assert isinstance(controller.central_data_controller.latest_start_time, str)
    assert isinstance(controller.central_data_controller.latest_stop_time, str)

def test_start_recording(controller):
    controller.active_handlers = ['k', 'm', 's', 'w']
    
    with patch('Keyboard_Handler.trigger_listener') as mock_keyboard_trigger,\
    patch('Mouse_Handler.trigger_listener') as mock_mouse_trigger,\
    patch('Screen_Handler.trigger_listener') as mock_screen_trigger,\
    patch('Webcam_Handler.trigger_listener') as mock_webcam_trigger:

        mock_keyboard_trigger.assert_called_once_with('start') 
        mock_mouse_trigger.assert_called_once_with('start') 
        mock_screen_trigger.assert_called_once_with('start') 
        mock_webcam_trigger.assert_called_once_with('start') 
