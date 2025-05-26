from pynput import keyboard, mouse
import pandas as pd
import numpy as np

"""
Keyboard and Mouse Event Handlers

This module provides classes for tracking and logging keyboard and mouse events
using the pynput library. Events are stored in pandas DataFrames with timestamps.

Classes:
    Keyboard_Handler: Records keyboard press and release events
    Mouse_Handler: Records mouse movements, clicks, and scroll events
"""

class Keyboard_Handler:
    """
    Handles keyboard input events (key press and release).
    
    Records keyboard events with timestamps in a pandas DataFrame.
    
    Attributes:
        log (DataFrame): Stores keyboard events with time, key, and event type
        listener (keyboard.Listener): pynput listener for keyboard events
    """
    def __init__(self):
        self.log = pd.DataFrame(columns=['time', 'key', 'event'])
        self.listner = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
    
    def trigger_listener(self, command):
        """
        Start or stop the keyboard listener.
        
        Args:
            command (str): 'start' to begin listening or 'stop' to end
        """
        if command == 'start':
            self.listner.start()
        elif command == 'stop':
            self.listner.stop()

    def on_press(self, key):
        """
        Callback for key press events.
        
        Args:
            key (keyboard.Key or keyboard.KeyCode): The key that was pressed
        """
        if isinstance(key, keyboard.KeyCode):     
            new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key.char], 'event': ['press']})
        elif isinstance(key, keyboard.Key):
            new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key], 'event': ['press']})

        self.log = pd.concat([self.log, new_entry], ignore_index=True)

    def on_release(self, key):
        """
        Callback for key release events.
        
        Args:
            key (keyboard.Key or keyboard.KeyCode): The key that was released
        """
        if isinstance(key, keyboard.KeyCode):     
            new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key.char], 'event': ['release']})
        elif isinstance(key, keyboard.Key):
            new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key], 'event': ['release']})

        self.log = pd.concat([self.log, new_entry], ignore_index=True)


class Mouse_Handler:
    """
    Handles mouse input events (movement, clicks, and scrolling).
    
    Records mouse events with timestamps and position data in a pandas DataFrame.
    
    Attributes:
        log (DataFrame): Stores mouse events with time, position, event type, button, and scroll data
        listener (mouse.Listener): pynput listener for mouse events
    """
    def __init__(self):
        self.log = pd.DataFrame(columns=['time', 'x', 'y', 'event', 'button', 'scroll'])  # Fixed typo in 'columns'
        self.listner = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
    
    def trigger_listener(self, command):
        """
        Start or stop the mouse listener.
        
        Args:
            command (str): 'start' to begin listening or 'stop' to end
        """
        if command == 'start':
            self.listner.start()
        elif command == 'stop':
            self.listner.stop()

    def on_move(self, x, y):
        """
        Callback for mouse movement events.
        
        Args:
            x (int): X-coordinate of the pointer
            y (int): Y-coordinate of the pointer
        """
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 'event': ['move'], 
                                 'button': [None], 'scroll': [None]})
        self.log = pd.concat([self.log, new_entry], ignore_index=True)

    def on_click(self, x, y, button, pressed):
        """
        Callback for mouse click events.
        
        Args:
            x (int): X-coordinate of the pointer
            y (int): Y-coordinate of the pointer
            button (mouse.Button): The button that was clicked
            pressed (bool): True if pressed, False if released
        """
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 
                                 'event': ['press' if pressed else 'release'], 
                                 'button': [button], 'scroll': [None]})
        self.log = pd.concat([self.log, new_entry], ignore_index=True)

    def on_scroll(self, x, y, dx, dy):
        """
        Callback for mouse scroll events.
        
        Args:
            x (int): X-coordinate of the pointer
            y (int): Y-coordinate of the pointer
            dx (int): Horizontal scroll (not used)
            dy (int): Vertical scroll amount
        """
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 'event': ['scroll'], 
                                 'button': [None], 'scroll': [dy]})
        self.log = pd.concat([self.log, new_entry], ignore_index=True)
        


