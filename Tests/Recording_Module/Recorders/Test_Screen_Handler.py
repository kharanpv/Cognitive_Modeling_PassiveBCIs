from unittest.mock import patch, MagicMock
from Recording_Module.Recorders.Screen_Handler import Screen_Handler


def test_screen_handler_init():
    mock_callback = MagicMock()
    handler = Screen_Handler(update_status_callback=mock_callback)

    assert handler.resolution == (1280, 720)
    assert handler.fps == 24
    assert isinstance(handler.codec, int)
    assert handler.update_status_callback == mock_callback


@patch('Recording_Module.Recorders.Screen_Handler.shutil.move')
@patch('Recording_Module.Recorders.Screen_Handler.os.makedirs')
@patch('Recording_Module.Recorders.Screen_Handler.pyautogui.position')
@patch('Recording_Module.Recorders.Screen_Handler.cv2.circle')
@patch('Recording_Module.Recorders.Screen_Handler.cv2.resize')
@patch('Recording_Module.Recorders.Screen_Handler.cv2.cvtColor')
@patch('Recording_Module.Recorders.Screen_Handler.cv2.VideoWriter')
@patch('Recording_Module.Recorders.Screen_Handler.mss')
@patch('Recording_Module.Recorders.Screen_Handler.tempfile.TemporaryDirectory')
def test_screen_handler_run_listener(
    mock_tempdir,
    mock_mss,
    mock_videowriter_class,
    mock_cvtcolor,
    mock_resize,
    mock_circle,
    mock_position,
    mock_makedirs,
    mock_move
):
    handler = Screen_Handler(update_status_callback=MagicMock())

    stop_event = MagicMock()
    stop_event.is_set.side_effect = [False, True]

    pipe_conn = MagicMock()
    pipe_conn.recv.return_value = '/dummy_location'

    mock_tempdir_instance = MagicMock()
    mock_tempdir_instance.__enter__.return_value = '/tmp/dir'
    mock_tempdir.return_value = mock_tempdir_instance

    mock_sct = MagicMock()
    mock_sct.monitors = [{'width': 1920, 'height': 1080}]
    mock_sct.grab.return_value = MagicMock()
    mock_mss_instance = MagicMock()
    mock_mss_instance.__enter__.return_value = mock_sct
    mock_mss.return_value = mock_mss_instance

    mock_frame = MagicMock()
    mock_cvtcolor.return_value = mock_frame
    mock_resize.return_value = mock_frame
    mock_position.return_value = (100, 100)
    mock_circle.return_value = None 

    mock_writer = MagicMock()
    mock_writer.isOpened.return_value = True
    mock_videowriter_class.return_value = mock_writer

    handler._run_listener(stop_event, pipe_conn)

    mock_tempdir.assert_called_once()
    mock_mss.assert_called_once()
    mock_videowriter_class.assert_called_once()
    mock_writer.write.assert_called_once_with(mock_frame)
    mock_writer.release.assert_called_once()
    pipe_conn.recv.assert_called_once()
    mock_makedirs.assert_called_once_with('/dummy_location', exist_ok=True)
    mock_move.assert_called_once_with('/tmp/dir/screen_capture.avi', '/dummy_location/screen_capture.avi')

