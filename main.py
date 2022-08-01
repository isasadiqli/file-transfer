from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

import client_.client_gui
import server_.server_gui
import server_.environment as env


class MainScreen(Screen):
    pass


class ServerScreen(Screen):
    def __init__(self, **kwargs):
        super(ServerScreen, self).__init__(**kwargs)
        back = Button(text='Back', size_hint=(1, 0.1), on_press=self.back_callback)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(back)

        layout.add_widget(server_.server_gui.ServerWidget())

        self.add_widget(layout)

    def back_callback(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_screen'


class ClientScreen(Screen):
    def __init__(self, **kwargs):
        super(ClientScreen, self).__init__(**kwargs)
        back = Button(text='Back', size_hint=(1, 0.1), on_press=self.back_callback)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(back)

        layout.add_widget(client_.client_gui.ClientWidget())

        self.add_widget(layout)

    def back_callback(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_screen'


class MainScreenManager(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        pass


if __name__ == '__main__':
    MainApp().run()
