import threading
import socket
import time
import re

from Game import Game
from Player import Player

class Client():

    def __init__(self, server, port, game: Game):
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("# connecting #")
        self.socket.connect((server, port))
        print("# connected #")
        self.listening= True
        self.game = game

    def listener(self):
        while self.listening:
            data= ""
            try:
                data= self.socket.recv(4096).decode('utf-8')
                # print("j'ai recu")
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
       
    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            # username_result = re.search('^USERNAME (.*)$', message)
            # if not username_result:
                # message= "{0}: {1}".format(self.id, message)
            self.socket.sendall(message.encode("utf-8"))
        except socket.error:
            print("unable to send message")
   
    def tidy_up(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data=="QUIT":
            self.tidy_up()
        elif data=="":
            self.tidy_up()
        else:
            self.game.on_msg(data)

if __name__ == "__main__":
    username= input("username: ")
    # server= input("server: ")
    #port = int(input("port: "))
    server = 'localhost'
    port = 59001
    client= Client(username, server, port)
    client.listen()
    message= ""
    while message!="QUIT":
        message= input()
        client.send(message)
