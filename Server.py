import socket
import signal #identifie les signaux pour kill le programme
import sys #utilisé pour sortir du programme
import time
from ClientThread import ClientListener

import threading
import json


from Ball import Ball




class Server():

    def __init__(self, port):
        self.listener= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets= []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    def run(self):
        self.p1_socket = None
        self.p2_socket = None

        while self.p1_socket == None or self.p2_socket == None:
            print("### Waitting ###")
            if self.p1_socket == None:
                print("listening for player 1")
                try:
                    (client_socket, client_adress) = self.listener.accept()
                except socket.error:
                    sys.exit("Cannot connect clients")
                self.clients_sockets.append(client_socket)
                self.p1_socket = client_socket
                print("Start the thread for client:", client_adress)
                client_thread= ClientListener(self.on_move, self.remove_socket, client_socket, client_adress, 1)
                client_thread.start()
            
            if self.p2_socket == None:
                print("listening for player 2")
                try:
                    (client_socket, client_adress) = self.listener.accept()
                except socket.error:
                    sys.exit("Cannot connect clients")
                self.clients_sockets.append(client_socket)
                self.p2_socket = client_socket
                print("Start the thread for client:", client_adress)
                client_thread= ClientListener(self.on_move, self.remove_socket, client_socket, client_adress, 2)
                client_thread.start()
            
            time.sleep(0.1)

    def remove_socket(self, socket):
        self.clients_sockets.remove(socket)

    def on_move(self, data):
        try:
            
            if '}{' in data:
                msg = json.loads('{' + data.split('}{')[-1])
            else:
                msg = json.loads(data)

            if "1" in msg:
                change = msg['1']['change']
                self.ball.leftPaddle.move(change)

            if "2" in msg:
                change = msg['2']['change']
                self.ball.rightPaddle.move(change)
            
        except:
            print(f"Server can't treat : {data}")

    def echo(self, data: str):
        # print(f'echoing: {data}')
            
        for sock in self.clients_sockets:
            try:
                # print('echoed !')
                sock.sendall(data.encode("utf-8"))
            except socket.error:
                print("Cannot send the message")

    def start_emittion(self, ball: Ball):
        self.ball = ball
        round = 0
        while True:
            round += 1
            scoreLeft, scoreRight = ball.move()
            ball.checkForPaddle()
            data = json.dumps(
                {
                'round': round,
                'ballX': ball.x, 'ballY': ball.y,
                'scoreLeft': scoreLeft, 'scoreRight': scoreRight,
                '1': {'x': self.ball.leftPaddle.x, 'y': self.ball.leftPaddle.y},
                '2': {'x': self.ball.rightPaddle.x, 'y': self.ball.rightPaddle.y}
                }
            )
            self.echo(data)
            # time.sleep(0.001)
            i = 50000
            while i > 0:
                i -= 1