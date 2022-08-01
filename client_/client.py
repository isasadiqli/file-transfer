import os
import socket

from kivy.clock import mainthread

import client_.environment as env

IP = '192.168.1.67'
PORT = 5050
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
client = socket.socket()


@mainthread
def change_text_input(str):
    env.text_input.insert_text(str + '\n')


def client_connect():
    global client
    change_text_input(" Staring a TCP socket.")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    change_text_input("Connecting to the server.")
    client.connect(ADDR)
    msg = client.recv(SIZE).decode(FORMAT)
    change_text_input(msg)


def client_send_file(path):
    global client

    file = open(os.path.abspath(path), "rb")
    data = file.read()

    filename = os.path.basename(path)

    size = str(len(data))

    client.send(filename.encode(FORMAT))
    client.send(size.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    change_text_input(f"[SERVER]: {msg}")
    client.send(data)
    msg = client.recv(SIZE).decode(FORMAT)
    change_text_input(f"[SERVER]: {msg}")
    file.close()
    client.close()
