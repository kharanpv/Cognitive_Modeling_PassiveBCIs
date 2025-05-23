from pynput import keyboard, mouse
import pandas as pd
import numpy as np
import time

class Keyboard_Handler:
    def __init__(self):
        self.key_log = pd.DataFrame(column=['time', 'key', 'event'])
        self.listner = keyboard.Listener()
    
    def on_press(self, key): 
        if isinstance(key, keyboard.KeyCode):     
            new_entry =   pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key.char], 'event': ['press']})
        elif isinstance(key, keyboard.Key):
            new_entry =   pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key], 'event': ['press']})

        self.key_log = pd.concat([self.key_log, new_entry], ignore_index=True)

    def on_release(self, key): 
        if isinstance(key, keyboard.KeyCode):     
            new_entry =   pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key.char], 'event': ['release']})
        elif isinstance(key, keyboard.Key):
            new_entry =   pd.DataFrame({'time': [pd.Timestamp.now()], 'key': [key], 'event': ['release']})

        self.key_log = pd.concat([self.key_log, new_entry], ignore_index=True)

class Mouse_Handler:
    def __init__(self):
        self.mouse_log = pd.DataFrame(column=['time', 'x', 'y', 'event', 'button', 'scroll'])
        self.listner = mouse.Listener()

    def on_move(self, x, y):
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 'event': ['move'], 
        'button': [None], 'scroll': [None]})
        self.key_log = pd.concat([self.key_log, new_entry], ignore_index=True)

    def on_click(self, x, y, button, pressed):
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 'event': ['press' if pressed else 'release'], 
        'button': [button], 'scroll': [None]})
        self.key_log = pd.concat([self.key_log, new_entry], ignore_index=True)
        

    def on_scroll(self, x, y, dx, dy):
        new_entry = pd.DataFrame({'time': [pd.Timestamp.now()], 'x': [x], 'y': [y], 'event': [None], 
        'button': [None], 'scroll': [dy]})
        self.key_log = pd.concat([self.key_log, new_entry], ignore_index=True)
        


