import socket
import threading
import re
import os
from Header import HttpRequestFormat as HREQ
from Header import HttpResponseFormat as HRES
import Urls
from Views import views

class Server:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    def accept_connection(self, conn, addr):
        with conn:
            print("-"*5)
            print(f"Connected by {addr}")
            data = conn.recv(1024)

            try:
                data_header = HREQ(data)
            except:
                error_response = HRES(400)
                conn.sendall(error_response())
                return None

            response_header = HRES(200)

            directory = data_header.directory

            print(f"Method: {data_header.method}")
            print("-" * 5)

            direct_path = False
            for path in Urls.endpoints:
                if path.url == directory:
                    response_header = path.response(data_header)
                    direct_path = True
            if not direct_path:
                response_header = views.document_fetch(data_header)

            conn.sendall(response_header())

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print(f"Listening... on port {PORT}")

            while views.connections <= 50:
                conn, addr = s.accept()
                self.accept_connection(conn, addr)

HOST = "0.0.0.0"
PORT = 65432

server = Server(HOST, PORT)
server.start()
