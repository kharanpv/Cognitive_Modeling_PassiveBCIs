from pynput import keyboard, mouse
import pandas as pd
import numpy as np
from multiprocessing import Process, Pipe

"""
Keyboard and Mouse Event Handlers for Cognitive Modeling BCI System

This module provides classes for capturing and logging keyboard and mouse events
using the pynput library in separate processes. Events are collected with high-precision 
timestamps and stored in pandas DataFrames for analysis.

Classes:
    Keyboard_Handler: Captures keyboard press and release events with timestamps
    Mouse_Handler: Captures mouse movements, clicks, and scroll events with position data

Dependencies:
    - pynput
    - pandas
    - numpy
    - multiprocessing
"""

class Keyboard_Handler:
    """
    Asynchronous keyboard input event handler for BCI data collection.

    Captures keyboard events (press and release) in a separate process. Events are
    timestamped and collected for later analysis. Both character keys and special keys
    are supported.

    Attributes:
        log_data (list): Raw event data collected from the child process
        parent_conn (Connection): Parent end of the multiprocessing pipe
        child_conn (Connection): Child end of the multiprocessing pipe  
        process (Process): Separate process running the keyboard listener
        active (bool): Flag indicating if the listener is currently running

    Example:
        >>> handler = Keyboard_Handler()
        >>> handler.trigger_listener('start')
        >>> # ... perform other tasks ...
        >>> handler.trigger_listener('stop')
        >>> df = handler.log
    """
    def __init__(self):
        self.log_data = []
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=self._run_listener, args=(self.child_conn,))
        self.active = False

    def trigger_listener(self, command):
        """
        Start or stop the keyboard listener process.

        Args:
            command (str): 'start' to begin capturing events, 'stop' to halt and retrieve data.
        """
        if command == 'start' and not self.active:
            self.process.start()
            self.active = True
        elif command == 'stop' and self.active:
            self.parent_conn.send('stop')
            self.process.join()
            if self.parent_conn.poll():
                self.log_data = self.parent_conn.recv()
            self.active = False

    def _run_listener(self, conn):
        """
        Internal method that runs the keyboard listener in a separate process.

        Args:
            conn (Connection): Child end of the pipe for communication with parent.
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

        while True:
            if conn.poll():
                message = conn.recv()
                if message == 'stop':
                    listener.stop()
                    break

        conn.send(log_data)
    
    @property
    def log(self):
        """
        Returns:
            DataFrame: Captured keyboard events with columns ['time', 'key', 'event'].
        """
        return pd.DataFrame(self.log_data)


class Mouse_Handler:
    """
    Asynchronous mouse input event handler for BCI data collection.

    Captures mouse interactions (movement, clicks, scrolling) in a separate process.
    Mouse events include position, button, and scroll data, all timestamped.

    Attributes:
        log_data (list): Raw event data collected from the child process
        parent_conn (Connection): Parent end of the multiprocessing pipe
        child_conn (Connection): Child end of the multiprocessing pipe
        process (Process): Separate process running the mouse listener
        active (bool): Flag indicating if the listener is currently running

    Example:
        >>> handler = Mouse_Handler()
        >>> handler.trigger_listener('start')
        >>> # ... user interacts with mouse ...
        >>> handler.trigger_listener('stop')
        >>> df = handler.log
    """
    def __init__(self):
        self.log_data = []
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=self._run_listener, args=(self.child_conn,))
        self.active = False

    def trigger_listener(self, command):
        """
        Start or stop the mouse listener process.

        Args:
            command (str): 'start' to begin capturing events, 'stop' to halt and retrieve data.
        """
        if command == 'start' and not self.active:
            self.process.start()
            self.active = True
        elif command == 'stop' and self.active:
            self.parent_conn.send('stop')
            self.process.join()
            if self.parent_conn.poll():
                self.log_data = self.parent_conn.recv()
            self.active = False

    def _run_listener(self, conn):
        """
        Internal method that runs the mouse listener in a separate process.

        Args:
            conn (Connection): Child end of the pipe for parent communication.
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

        while True:
            if conn.poll():
                message = conn.recv()
                if message == 'stop':
                    listener.stop()
                    break

        conn.send(log_data)
    
    @property
    def log(self):
        """
        Returns:
            DataFrame: Captured mouse events with columns such as ['time', 'x', 'y', 'button', 'event', 'scroll_dx', 'scroll_dy'].
        """
        return pd.DataFrame(self.log_data)
