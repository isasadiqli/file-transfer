import socket
import threading

from kivy.uix.textinput import TextInput

client = socket.socket()
is_server_set_to_run_event = threading.Event()
text_input = TextInput(is_focusable=False)
text = ''
path = ''

def init():
    global client
    global is_server_set_to_run_event
    global text_input
    global text
    global path