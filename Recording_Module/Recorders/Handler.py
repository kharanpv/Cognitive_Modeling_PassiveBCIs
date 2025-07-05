from abc import ABC, abstractmethod
from multiprocessing import Process, Pipe, Event

class Handler(ABC):
    """
    Abstract base class for event handlers.
    
    Provides common functionality for asynchronous event handling in a separate process.
    All recording handlers (keyboard, mouse, screen, webcam) inherit from this class.
    
    Attributes:
        stop_event (Event): Multiprocessing event for signaling process termination
        process (Process): The process where the handler runs
        active (bool): Current state of the handler
        parent_conn (Connection): Parent end of the pipe for communication
        child_conn (Connection): Child end of the pipe for communication
    """
    def __init__(self):
        self.stop_event = Event()
        self.process = None
        self.active = False
        self.parent_conn, self.child_conn = Pipe()

    def trigger_listener(self, command, save_dir=None):
        """
        Start or stop the listener process.

        Parameters:
            command (str): 'start' to begin listening, 'stop' to end the process.
            save_dir (str, optional): Directory to save the log when stopping.

        Returns:
            None
        """
        if command == 'start' and not self.active:
            self.stop_event = Event()
            self.process = Process(target=self._run_listener, args=(self.stop_event, self.child_conn), daemon=True)
            self.process.start()
            self.active = True

        elif command == 'stop' and self.active:
            self.stop_event.set()
            self.parent_conn.send(save_dir)
            self.process.join()
            self.active = False

    @abstractmethod
    def _run_listener(self, stop_event, pipe_conn):
        """
        Abstract method to implement task-specific event listening.

        Parameters:
            stop_event (multiprocessing.Event): Event to signal stopping.
            pipe_conn (multiprocessing.Pipe): Pipe connection for communication.

        Returns:
            None
        """
        pass
