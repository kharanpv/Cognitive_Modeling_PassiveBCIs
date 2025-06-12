import pytest
from multiprocessing import Event, connection
import multiprocessing

from Recording_Module.Recorders.Handler import Handler

class DummyHandler(Handler):
    def _run_listener(self, stop_event, pipe_conn):
        return 'Dummy Method'

@pytest.fixture
def handler():
    return DummyHandler()

def test_init(handler):

    assert isinstance(handler.stop_event, multiprocessing.synchronize.Event)
    assert handler.process is None
    assert isinstance(handler.active, bool)
    assert isinstance(handler.parent_conn, connection.Connection)
    assert isinstance(handler.child_conn, connection.Connection)
