from pynput import keyboard, mouse
import pandas as pd
from multiprocessing import Process, Pipe, Event
import time
import os

"""
Keyboard and Mouse Event Handlers for Cognitive Modeling BCI System

Provides classes for capturing keyboard and mouse events using pynput in separate processes.
Each handler saves its log data directly to disk upon stopping.
"""

class Keyboard_Handler:
    """
    Asynchronous keyboard event handler.

    Captures keyboard events in a separate process and saves them directly to disk.
    """
    def __init__(self):
        self.stop_event = Event()
        self.process = None
        self.active = False
        self.parent_conn, self.child_conn  = Pipe() 

    def trigger_listener(self, command, save_dir=None):
        """
        Start or stop the keyboard listener process.

        Parameters:
            command (str): 'start' to begin listening, 'stop' to end and save events.
            save_dir (str, optional): Directory to save the log when stopping.
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

    def _run_listener(self, stop_event, pipe_conn):
        """
        Listen for keyboard events and store them locally. Save to disk upon stopping.

        Parameters:
            stop_event (multiprocessing.Event): Event to signal stopping.

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
        if save_dir:
            df = pd.DataFrame(log_data)
            os.makedirs(save_dir, exist_ok=True)
            df.to_csv(os.path.join(save_dir, 'keyboard_log.csv'), index=False)

class Mouse_Handler:
    """
    Asynchronous mouse event handler.

    Captures mouse events in a separate process and saves them directly to disk.
    """
    def __init__(self):
        self.stop_event = Event()
        self.process = None
        self.active = False
        self.parent_conn, self.child_conn  = Pipe()

    def trigger_listener(self, command, save_dir=None):
        """
        Start or stop the mouse listener process.

        Parameters:
            command (str): 'start' to begin listening, 'stop' to end and save events.
            save_dir (str, optional): Directory to save the log when stopping.
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

    def _run_listener(self, stop_event, pipe_conn):
        """
        Listen for mouse events and store them locally. Save to disk upon stopping.

        Parameters:
            stop_event (multiprocessing.Event): Event to signal stopping.

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
        if save_dir:
            df = pd.DataFrame(log_data)
            os.makedirs(save_dir, exist_ok=True)
            df.to_csv(os.path.join(save_dir, 'mouse_log.csv'), index=False)
