from pynput import keyboard, mouse
import pandas as pd
from multiprocessing import Process, Queue, Event
import time

"""
Keyboard and Mouse Event Handlers for Cognitive Modeling BCI System

Provides classes for capturing keyboard and mouse events using pynput in separate processes.
"""

class Keyboard_Handler:
    """
    Asynchronous keyboard event handler using multiprocessing.Queue.

    Listens for keyboard events in a separate process and stores them in a queue.
    """
    def __init__(self):
        self.log_data = []
        self.queue = Queue()
        self.stop_event = Event()
        self.process = Process(target=self._run_listener, args=(self.queue, self.stop_event), daemon=True)
        self.active = False

    def trigger_listener(self, command):
        """
        Start or stop the keyboard listener process.

        Parameters:
            command (str): 'start' to begin listening, 'stop' to end and collect events.

        Returns:
            None
        """
        if command == 'start' and not self.active:
            self.queue = Queue()
            self.stop_event = Event()
            self.process = Process(target=self._run_listener, args=(self.queue, self.stop_event), daemon=True)
            self.process.start()
            self.active = True
        elif command == 'stop' and self.active:
            self.stop_event.set()
            self.process.join(timeout=5)  # wait 5 seconds max
            if self.process.is_alive():
                self.process.terminate()
            while not self.queue.empty():
                self.log_data.append(self.queue.get())
            self.active = False

    def _run_listener(self, queue, stop_event):
        """
        Listen for keyboard events and put them in the queue.

        Parameters:
            queue (multiprocessing.Queue): Queue to store events.
            stop_event (multiprocessing.Event): Event to signal stopping.

        Returns:
            None
        """
        def on_press(key):
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            queue.put({
                'time': pd.Timestamp.now(),
                'key': k,
                'event': 'press'
            })

        def on_release(key):
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            queue.put({
                'time': pd.Timestamp.now(),
                'key': k,
                'event': 'release'
            })

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        while not stop_event.is_set():
            time.sleep(0.01)
        listener.stop()
    
    @property
    def log(self):
        """
        Get all recorded keyboard events as a DataFrame.

        Returns:
            pd.DataFrame: DataFrame with event time, key, and event type.
        """
        return pd.DataFrame(self.log_data)


class Mouse_Handler:
    """
    Asynchronous mouse event handler using multiprocessing.Queue.

    Listens for mouse events in a separate process and stores them in a queue.
    """
    def __init__(self):
        self.log_data = []
        self.queue = Queue()
        self.stop_event = Event()
        self.process = Process(target=self._run_listener, args=(self.queue, self.stop_event), daemon=True)
        self.active = False

    def trigger_listener(self, command):
        """
        Start or stop the mouse listener process.

        Parameters:
            command (str): 'start' to begin listening, 'stop' to end and collect events.

        Returns:
            None
        """
        if command == 'start' and not self.active:
            self.queue = Queue()
            self.stop_event = Event()
            self.process = Process(target=self._run_listener, args=(self.queue, self.stop_event), daemon=True)
            self.process.start()
            self.active = True
        elif command == 'stop' and self.active:
            self.stop_event.set()
            self.process.join(timeout=5)  # wait 5 seconds max
            if self.process.is_alive():
                self.process.terminate()
            while not self.queue.empty():
                self.log_data.append(self.queue.get())
            self.active = False

    def _run_listener(self, queue, stop_event):
        """
        Listen for mouse events and put them in the queue.

        Parameters:
            queue (multiprocessing.Queue): Queue to store events.
            stop_event (multiprocessing.Event): Event to signal stopping.

        Returns:
            None
        """
        def on_move(x, y):
            queue.put({
                'time': pd.Timestamp.now(),
                'x': x,
                'y': y,
                'event': 'move'
            })

        def on_click(x, y, button, pressed):
            queue.put({
                'time': pd.Timestamp.now(),
                'x': x,
                'y': y,
                'button': str(button),
                'event': 'press' if pressed else 'release'
            })

        def on_scroll(x, y, dx, dy):
            queue.put({
                'time': pd.Timestamp.now(),
                'x': x,
                'y': y,
                'scroll_dx': dx,
                'scroll_dy': dy,
                'event': 'scroll'
            })

        listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move)
        listener.start()
        while not stop_event.is_set():
            time.sleep(0.01)
        listener.stop()
    
    @property
    def log(self):
        """
        Get all recorded mouse events as a DataFrame.

        Returns:
            pd.DataFrame: DataFrame with event time, coordinates, event type, and details.
        """
        return pd.DataFrame(self.log_data)
