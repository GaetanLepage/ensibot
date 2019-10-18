#!/usr/bin/env python3

import time
import struct
from socket_client import SocketClient

# HOST = '127.0.0.1'
HOST = '192.168.1.24'
PORT = 5555
CLIENT_NAME = "EnsiBot"

class Api():
    
    def __init__(self):

        self.socket_client = SocketClient(HOST, PORT)
        self.socket_client.run()

    def get_reward(self):
        """

        """
        self.socket_client.send_string_message("get_reward")

        return self.socket_client.receive_float()

def main():
    api = Api()

    print("init over")

    while True:
        reward = api.get_reward()
        print(reward)
        time.sleep(0.1)


if __name__=="__main__":
    main()
