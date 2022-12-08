from socket import socket
import threading
import time

class ClientListener(threading.Thread):

    def __init__(self, on_msg, on_client_quit, socket, address, id):
        super(ClientListener, self).__init__()
        self.on_msg= on_msg
        self.on_client_quit= on_client_quit
        self.socket= socket
        self.address= address
        self.listening= True
        self.id= id

    def run(self):
        while self.listening:
            data= ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.on_client_quit(self.socket)
        self.on_msg("{0} has quit\n".format(self.address))

    def handle_msg(self, data):
        if data == "QUIT":
            self.quit()
        else:
            self.on_msg(data)

