from pynput import keyboard
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
    def __init__():
        pass

