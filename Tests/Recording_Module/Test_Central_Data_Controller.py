import pytest
from datetime import datetime as real_datetime
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


@patch('Recording_Module.Central_Data_Controller.Webcam_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Screen_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Mouse_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Keyboard_Handler.trigger_listener')
def test_start_recording(mock_keyboard_trigger, mock_mouse_trigger, mock_screen_trigger, mock_webcam_trigger, controller):
    
    controller.active_handlers = ['k', 'm', 's', 'w']
    controller.start_recording()

    mock_keyboard_trigger.assert_called_once_with('start') 
    mock_mouse_trigger.assert_called_once_with('start') 
    mock_screen_trigger.assert_called_once_with('start') 
    mock_webcam_trigger.assert_called_once_with('start') 

@patch('Recording_Module.Central_Data_Controller.Webcam_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Screen_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Mouse_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.Keyboard_Handler.trigger_listener')
@patch('Recording_Module.Central_Data_Controller.os.makedirs')
@patch('Recording_Module.Central_Data_Controller.datetime.datetime')
def test_stop_recording(mock_datetime, mock_os_makedirs, mock_keyboard_trigger, mock_mouse_trigger, mock_screen_trigger, mock_webcam_trigger, controller):
    
    mock_datetime.now.return_value = real_datetime(2025, 6, 12, 16, 32, 5, 0)
    mock_datetime.side_effect = lambda *args, **kwargs: real_datetime(*args, **kwargs)

    controller.active_handlers = ['k', 'm', 's', 'w']
    controller.latest_start_time = real_datetime(2025, 6, 12, 16, 30, 5, 0).strftime('%Y-%m-%d_%H-%M-%S')
    controller.stop_recording('/dummy_location')

    mock_os_makedirs.assert_called_once_with('/dummy_location/2025-06-12_16-30-05_--_2025-06-12_16-32-05', exist_ok=True)
    mock_keyboard_trigger.assert_called_once_with('stop', '/dummy_location/2025-06-12_16-30-05_--_2025-06-12_16-32-05') 
    mock_mouse_trigger.assert_called_once_with('stop', '/dummy_location/2025-06-12_16-30-05_--_2025-06-12_16-32-05') 
    mock_screen_trigger.assert_called_once_with('stop', '/dummy_location/2025-06-12_16-30-05_--_2025-06-12_16-32-05') 
    mock_webcam_trigger.assert_called_once_with('stop', '/dummy_location/2025-06-12_16-30-05_--_2025-06-12_16-32-05') 

    assert controller.active_handlers == []