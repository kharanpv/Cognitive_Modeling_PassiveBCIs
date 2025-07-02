import cv2
from unittest.mock import patch, MagicMock
from Recording_Module.Recorders.Webcam_Handler import Webcam_Handler

def test_webcam_handler_init():
    mock_callback = MagicMock()
    handler = Webcam_Handler(update_status_callback=mock_callback)

    assert handler.fps == 28.8
    assert handler.codec == cv2.VideoWriter_fourcc(*"XVID")
    assert isinstance(handler.resolution, tuple)
    assert handler.update_status_callback == mock_callback


@patch('Recording_Module.Recorders.Webcam_Handler.os.makedirs')
@patch('Recording_Module.Recorders.Webcam_Handler.shutil.move')
@patch('Recording_Module.Recorders.Webcam_Handler.cv2.VideoCapture')
@patch('Recording_Module.Recorders.Webcam_Handler.cv2.VideoWriter')
@patch('Recording_Module.Recorders.Webcam_Handler.tempfile.TemporaryDirectory')
def test_webcam_handler_run_listener(
    mock_tempdir,
    mock_videowriter_class,
    mock_videocapture_class,
    mock_move,
    mock_makedirs
):
    handler = Webcam_Handler(update_status_callback=MagicMock())

    stop_event = MagicMock()
    stop_event.is_set.side_effect = [False, True]

    pipe_conn = MagicMock()
    pipe_conn.recv.return_value = '/dummy_location'

    mock_tempdir_instance = MagicMock()
    mock_tempdir_instance.__enter__.return_value = '/tmp/dir'
    mock_tempdir.return_value = mock_tempdir_instance

    mock_frame = MagicMock()
    mock_cam = MagicMock()
    mock_cam.read.return_value = True, mock_frame
    mock_videocapture_class.return_value = mock_cam

    mock_writer = MagicMock()
    mock_writer.isOpened.return_value = True
    mock_videowriter_class.return_value = mock_writer

    handler._run_listener(stop_event, pipe_conn)

    mock_tempdir.assert_called_once()
    mock_cam.read.assert_called_once()
    mock_cam.release.assert_called_once()
    mock_videowriter_class.assert_called_once()
    mock_writer.write.assert_called_once_with(mock_frame)
    mock_writer.release.assert_called_once()
    pipe_conn.recv.assert_called_once()
    mock_makedirs.assert_called_once_with('/dummy_location', exist_ok=True)
    mock_move.assert_called_once_with('/tmp/dir/webcam_capture.avi', '/dummy_location/webcam_capture.avi')
   

