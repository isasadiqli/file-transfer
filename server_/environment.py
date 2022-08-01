import socket
import threading

from kivy.uix.textinput import TextInput

server = socket.socket()
is_server_set_to_run_event = threading.Event()
text_input = TextInput(is_focusable=False)
text = ''
path = ''
is_widget_opened_before = False


def init():
    global server
    global is_server_set_to_run_event
    global text_input
    global text
    global path
    global is_widget_opened_before
