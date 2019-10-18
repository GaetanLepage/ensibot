#!/usr/bin/env python3

import socket
import threading
import struct
import time

class SocketClient(threading.Thread):

    def __init__(self, server_ip, server_port):

        threading.Thread.__init__(self)

        self.server_ip = server_ip
        self.server_port = server_port

        self.socket = None


    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.setblocking(False)
        self.socket.connect((self.server_ip, self.server_port))
    
    def run(self):
        self.connect_to_server()
        print("Connected to server")
        while True:
            time.sleep(1)

    def send_string_message(self, string_message):
        """
        """
        if string_message[-1] != '\0':
            string_message += '\0'
        message_bytes = string_message.encode()
        self.socket.sendall(message_bytes)
        print("sent message \"{}\"".format(string_message))
    
    def receive_float(self):
        float_bytes = self.socket.recv(bufsize=4)

        return struct.unpack('f', float_bytes)