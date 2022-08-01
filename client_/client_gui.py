import os
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

from client_.client import client_connect, client_send_file
import client_.environment as env

if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

t = Thread()

Builder.load_file(os.path.join('client_', 'client.kv'))

main_layout = GridLayout()
file_chooser_layout = GridLayout()
is_chooser_opened_before = False


class FileChooserWidget(GridLayout):
    pass


file_chooser_widget = FileChooserWidget()


class ClientWidget(GridLayout):

    def start_callback(self, instance):
        global t
        t = Thread(target=client_connect)
        t.daemon = True
        print(t.getName())
        print(t.ident)
        t.start()


    def choose_callback(self, instance):

        global is_chooser_opened_before
        global file_chooser_widget

        if not is_chooser_opened_before:
            is_chooser_opened_before = True
            send = Button(text='Send')
            back = Button(text='Back')

            send.bind(on_press=self.send_callback)
            back.bind(on_press=self.back_callback)

            button_layout = GridLayout()
            button_layout.cols = 2
            button_layout.size_hint = (0.05, 0.1)

            button_layout.add_widget(send)
            button_layout.add_widget(back)

            file_chooser_layout.add_widget(file_chooser_widget)
            file_chooser_layout.cols = 1
            file_chooser_layout.add_widget(button_layout)

        self.remove_widget(main_layout)
        self.add_widget(file_chooser_layout)

    def send_callback(self, instance):

        path = file_chooser_widget.ids.label.text

        if os.path.isdir(path):
            print("\nIt is a directory")
        elif os.path.isfile(path):
            env.path = path
            client_send_file(path)

        else:
            print("It is a special file (socket, FIFO, device file)")

    def back_callback(self, instance):
        print(file_chooser_widget.ids.label.text)
        # if file_chooser_widget.ids.label.text == '/storage/emulated/0/' or
        self.remove_widget(file_chooser_layout)
        self.add_widget(main_layout)

    def __init__(self, **kwargs):
        super(ClientWidget, self).__init__(**kwargs)
        global main_layout
        main_layout.cols = 1

        # self.window = GridLayout()
        self.cols = 1

        self.size_hint = (0.9, 0.9)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        start_button = Button(text='Start')
        file_chooser = Button(text='Choose a file')

        start_button.bind(on_press=self.start_callback)
        file_chooser.bind(on_press=self.choose_callback)

        button_widget = BoxLayout(orientation='horizontal')
        button_widget.size_hint = (0.3, 0.3)
        file_chooser.size_hint = (0.3, 0.3)

        button_widget.add_widget(start_button)

        main_layout.add_widget(env.text_input)
        main_layout.add_widget(button_widget)
        main_layout.add_widget(file_chooser)

        self.add_widget(main_layout)
