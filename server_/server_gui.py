import multiprocessing
import os
import subprocess
import sys
import threading
from threading import Thread

from kivy import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from server_.server import run_server
import server_.environment as env

Builder.load_file(os.path.join('server_', 'file_chooser.kv'))

if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

t = Thread()

main_layout = GridLayout()
file_chooser_layout = GridLayout()
is_chooser_opened_before = False


class FileChooserWidget(GridLayout):
    pass


file_chooser_widget = FileChooserWidget()


class ServerWidget(GridLayout):

    def start_callback(self, instance):
        global t
        t = Thread(target=run_server)
        print(t.getName())
        print(t.ident)
        t.start()

    def send_callback(self, instance):
        print(file_chooser_widget.ids.label.text)
        path = file_chooser_widget.ids.label.text

        if os.path.isdir(path):
            print("\nIt is a directory")
        elif os.path.isfile(path):
            env.path = path
        else:
            print("It is a special file (socket, FIFO, device file)")

    def back_callback(self, instance):
        self.remove_widget(file_chooser_layout)
        self.add_widget(main_layout)

    def __init__(self, **kwargs):
        super(ServerWidget, self).__init__(**kwargs)
        global main_layout
        main_layout.cols = 1

        self.cols = 1

        self.size_hint = (0.9, 0.9)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        start_button = Button(text='Start')

        start_button.bind(on_press=self.start_callback)

        button_widget = BoxLayout(orientation='horizontal')
        button_widget.size_hint = (0.3, 0.3)

        button_widget.add_widget(start_button)

        main_layout.add_widget(env.text_input)
        main_layout.add_widget(button_widget)

        self.add_widget(main_layout)
