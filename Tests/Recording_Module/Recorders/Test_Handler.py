import pytest
from multiprocessing import connection
import multiprocessing
from unittest.mock import patch, MagicMock

from Recording_Module.Recorders.Handler import Handler

class Dummy_Handler(Handler):
    def _run_listener(self, stop_event, pipe_conn):
        return 'Dummy Method'


@pytest.fixture
def handler():
    return Dummy_Handler()


def test_init(handler):

    assert isinstance(handler.stop_event, multiprocessing.synchronize.Event)
    assert handler.process is None
    assert isinstance(handler.active, bool)
    assert isinstance(handler.parent_conn, connection.Connection)
    assert isinstance(handler.child_conn, connection.Connection)


@patch('Recording_Module.Recorders.Handler.Process')
def test_start_trigger(mock_process, handler):

    handler.stop_event = MagicMock()
    handler.child_conn = MagicMock()
    handler.trigger_listener('start')

    mock_process.assert_called_once_with(
        target=handler._run_listener,
        args=(handler.stop_event, handler.child_conn),
        daemon=True
    )

    mock_process.return_value.start.assert_called_once()


@patch('Recording_Module.Recorders.Handler.Process')
@patch('Recording_Module.Recorders.Handler.Event')
def test_stop_trigger(mock_event, mock_process, handler):

    mock_event = MagicMock()
    mock_process = MagicMock()

    handler.stop_event = mock_event
    handler.process = mock_process
    handler.parent_conn = MagicMock()
    handler.active = True

    handler.trigger_listener('stop', '/dummy_location')

    mock_event.set.assert_called_once()
    handler.parent_conn.send.assert_called_once_with('/dummy_location')
    mock_process.join.assert_called_once()
    assert handler.active is False