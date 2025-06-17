import pytest
from unittest.mock import patch, MagicMock
import os

from Recording_Module.Recorders.Keyboard_Mouse_Handler import Keyboard_Handler, Mouse_Handler


@pytest.fixture
def keyboard_handler():
    return Keyboard_Handler()


@pytest.fixture
def mouse_handler():
    return Mouse_Handler()


class Test_Keyboard_Handler:

    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.keyboard.Listener')
    def test_run_listener(self, mock_listener, keyboard_handler):
        keyboard_handler._save_log = MagicMock()

        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, True]

        pipe_conn = MagicMock()
        pipe_conn.recv.return_value = '/dummy_location'

        keyboard_handler._run_listener(stop_event, pipe_conn)

        mock_listener.assert_called_once()
        _, called_kwargs = mock_listener.call_args
        on_press = called_kwargs.get('on_press')
        on_release = called_kwargs.get('on_release')
        assert callable(on_press)
        assert callable(on_release)

        pipe_conn.recv.assert_called_once()
        keyboard_handler._save_log.assert_called_once()
        called_args, _ = keyboard_handler._save_log.call_args
        log_data, save_dir, filename = called_args
        assert isinstance(log_data, list)
        assert save_dir == '/dummy_location'
        assert filename == 'keyboard_log.csv'

    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.os.makedirs')
    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.pd.DataFrame')
    def test_save_log(self, mock_dataframe_class, mock_makedirs, keyboard_handler):
        save_dir = '/dummy_location'
        log_data = [{
            'time': 'time',
            'key': 'key',
            'event': 'event'
        }]
        filename = 'test.csv'

        mock_dataframe = mock_dataframe_class.return_value

        keyboard_handler._save_log(log_data, save_dir, filename)

        mock_dataframe_class.assert_called_once_with(log_data)
        mock_makedirs.assert_called_once_with(save_dir, exist_ok=True)
        mock_dataframe.to_csv.assert_called_once_with(os.path.join(save_dir, filename), index=False)


class Test_Mouse_Handler:

    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.mouse.Listener')
    def test_run_listener(self, mock_listener, mouse_handler):
        mouse_handler._save_log = MagicMock()

        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, True]

        pipe_conn = MagicMock()
        pipe_conn.recv.return_value = '/dummy_location'

        mouse_handler._run_listener(stop_event, pipe_conn)

        mock_listener.assert_called_once()
        _, called_kwargs = mock_listener.call_args
        on_click = called_kwargs.get('on_click')
        on_scroll = called_kwargs.get('on_scroll')
        on_move = called_kwargs.get('on_move')

        assert callable(on_click)
        assert callable(on_scroll)
        assert callable(on_move)

        pipe_conn.recv.assert_called_once()
        mouse_handler._save_log.assert_called_once()
        called_args, _ = mouse_handler._save_log.call_args
        log_data, save_dir, filename = called_args
        assert isinstance(log_data, list)
        assert save_dir == '/dummy_location'
        assert filename == 'mouse_log.csv'

    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.os.makedirs')
    @patch('Recording_Module.Recorders.Keyboard_Mouse_Handler.pd.DataFrame')
    def test_save_log(self, mock_dataframe_class, mock_makedirs, mouse_handler):
        save_dir = '/dummy_location'
        log_data = [{
            'time': 'time',
            'key': 'key',
            'event': 'event'
        }]
        filename = 'test.csv'

        mock_dataframe = mock_dataframe_class.return_value

        mouse_handler._save_log(log_data, save_dir, filename)

        mock_dataframe_class.assert_called_once_with(log_data)
        mock_makedirs.assert_called_once_with(save_dir, exist_ok=True)
        mock_dataframe.to_csv.assert_called_once_with(os.path.join(save_dir, filename), index=False)
