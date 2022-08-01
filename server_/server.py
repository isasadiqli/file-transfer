from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from kivy.clock import mainthread

import server_.environment as env

import socket

server = socket.socket()


def set_server(s):
    global server
    server = s


def run_server():
    @mainthread
    def change_text_input(str):
        env.text_input.insert_text(str + '\n')

    server = socket.socket()

    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = "utf-8"

    def start():
        global server
        change_text_input("[STARTING] Server is starting.")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        set_server(server)
        change_text_input("[LISTENING] Server is listening on " + str(IP) + ".")
        while True:
            conn, addr = server.accept()
            change_text_input(f"[NEW CONNECTION] {addr} connected.")
            conn.send('Connected'.encode(FORMAT))

            filename = conn.recv(SIZE).decode(FORMAT)
            size = conn.recv(SIZE).decode(FORMAT)
            change_text_input(f"[RECV] Receiving the filename.")
            file = open(filename, "wb")
            conn.send("Filename received.".encode(FORMAT))
            data = conn.recv(int(size) - 1)
            change_text_input(f"[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))
            """ Closing the file. """
            file.close()
            """ Closing the connection from the ws. """
            conn.close()
            change_text_input(f"[DISCONNECTED] {addr} disconnected.")

    start()
