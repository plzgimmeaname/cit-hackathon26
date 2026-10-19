import socket
from threading import Thread
class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.socket.connect((host, port)) 
        self.takein = Thread(target=self.reciever)
        self.takein.start()
        self.sendout = Thread(target= self.sender)
        self.sendout.start()

    def reciever(self):
        while self.running:
            data = self.socket.recv(1024)
            data = data.decode()
            print('Server: ' + str(data))

    def sender(self):
        while self.running:
            x = input("Send: ")
            x = x.encode()
            self.socket.sendall(x)

if __name__ == "__main__":
    client = Client("10.180.49.86" , 12345)