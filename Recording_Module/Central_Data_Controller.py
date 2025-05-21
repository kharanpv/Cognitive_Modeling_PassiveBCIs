from Recorders.DOM_Handler import DOM_Handler
from Recorders.Keyboard_Mouse_Handler import Keyboard_Mouse_Handler
from Recorders.Screen_Media_Handler import Screen_Media_Handler
from Recorders.Webcam_Handler import Webcam_Handler

class Central_Data_Controller:
    def __init__(self):
        self.DOM_Handler = DOM_Handler()
        self.Keyboard_Mouse_Handler = Keyboard_Mouse_Handler()
        self.Screen_Media_Handler = Screen_Media_Handler()
        self.Webcam_Handler = Webcam_Handler()
    
    