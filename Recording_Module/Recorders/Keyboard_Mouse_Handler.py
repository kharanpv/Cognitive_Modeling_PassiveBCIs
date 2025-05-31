from pynput import keyboard, mouse
from .Handler import Handler
import pandas as pd
import time
import os

class Keyboard_Handler(Handler):
    """
    Asynchronous keyboard event handler.

    Captures keyboard events in a separate process and saves them directly to disk.
    """
    def _run_listener(self, stop_event, pipe_conn):
        """
        Listen for keyboard events and store them locally. Save to disk upon stopping.

        Parameters:
            stop_event (multiprocessing.Event): Event to signal stopping.
            pipe_conn (multiprocessing.Pipe): Pipe connection for communication.

        Returns:
            None
        """
        log_data = []

        def on_press(key):
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            log_data.append({
                'time': pd.Timestamp.now(),
                'key': k,
                'event': 'press'
            })

        def on_release(key):
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            log_data.append({
                'time': pd.Timestamp.now(),
                'key': k,
                'event': 'release'
            })

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        while not stop_event.is_set():
            time.sleep(0.01)
        listener.stop()
        listener.join()

        # Save to CSV if directory provided
        save_dir = pipe_conn.recv()
        self._save_log(log_data, save_dir, 'keyboard_log.csv')

    def _save_log(self, log_data, save_dir, filename):
        """
        Save log data to a CSV file.

        Parameters:
            log_data (list): List of event data dictionaries.
            save_dir (str): Directory to save the log file.
            filename (str): Name of the log file.

        Returns:
            None
        """
        if save_dir:
            df = pd.DataFrame(log_data)
            os.makedirs(save_dir, exist_ok=True)
            df.to_csv(os.path.join(save_dir, filename), index=False)

class Mouse_Handler(Handler):
    """
    Asynchronous mouse event handler.

    Captures mouse events in a separate process and saves them directly to disk.
    """
    def _run_listener(self, stop_event, pipe_conn):
        """
        Listen for mouse events and store them locally. Save to disk upon stopping.

        Parameters:
            stop_event (multiprocessing.Event): Event to signal stopping.
            pipe_conn (multiprocessing.Pipe): Pipe connection for communication.

        Returns:
            None
        """
        log_data = []

        def on_move(x, y):
            log_data.append({
                'time': pd.Timestamp.now(),
                'x': x,
                'y': y,
                'event': 'move'
            })

        def on_click(x, y, button, pressed):
            log_data.append({
                'time': pd.Timestamp.now(),
                'x': x,
                'y': y,
                'button': str(button),
                'event': 'press' if pressed else 'release'
            })

        def on_scroll(x, y, dx, dy):
            log_data.append({
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
        listener.join()

        # Save to CSV if directory provided
        save_dir = pipe_conn.recv()
        self._save_log(log_data, save_dir, 'mouse_log.csv')

    def _save_log(self, log_data, save_dir, filename):
        """
        Save log data to a CSV file.

        Parameters:
            log_data (list): List of event data dictionaries.
            save_dir (str): Directory to save the log file.
            filename (str): Name of the log file.

        Returns:
            None
        """
        if save_dir:
            df = pd.DataFrame(log_data)
            os.makedirs(save_dir, exist_ok=True)
            df.to_csv(os.path.join(save_dir, filename), index=False)
