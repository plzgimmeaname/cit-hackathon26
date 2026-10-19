import socket 
from threading import Thread 

class Server: 
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.client, addr = self.socket.accept()
        self.running = True 
        self.take_in = Thread(target=self.reciever)
        self.take_in.start()
        self.send_out = Thread(target=self.sender)
        self.send_out.start()

    def reciever(self):
        while self.running: 
            data = self.client.recv(1024)
            data = data.decode() 
            print("Client: " + data)

    def sender(self):
        while self.running:
            x = input("Send: ")
            x = x.encode() 
            self.client.sendall(x)

if __name__ == "__main__":
    server = Server(socket.gethostbyname(socket.gethostname()), 12345)
