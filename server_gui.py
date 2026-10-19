import socket 
from threading import Thread 
import pygame 
import pynput
import time 
from queue import Queue

class Server: 
    def __init__(self, host, port):
        pygame.init()
        self.win = pygame.display.set_mode((900, 500))
        pygame.display.set_caption("CatNet Server")
        self.font = pygame.font.Font(size=32)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.client, addr = self.socket.accept()
        self.running = True 
        self.submitted = Queue()
        self.terminal = ""
        self.line = 0 
        self.debug = False 
        self.gui = ["Server Started! Welcome to CatNet."]
        self.take_in = Thread(target=self.reciever)
        self.take_in.start()
        self.kyl = Thread(target=self.kl)
        self.kyl.start()
        self.main_loop() 
        
        

    def reciever(self):
        while self.running: 
            data = self.client.recv(1024)
            data = data.decode() 
            data = str(data)
            data = "Client: " + data
            self.gui.append(data)

    def on_press(self, key):
        key = str(key)
        key = key.replace("'","")
        if key == "Key.enter":
            if self.terminal == "debug":
                self.debug = not self.debug 
            else:
                self.gui.append("You: " + self.terminal)
                self.terminal = self.terminal.encode()
                self.client.sendall(self.terminal)
            self.terminal = ""
        elif key == "Key.backspace":
            self.terminal = self.terminal[:-1]
        elif key == "Key.space":
            self.terminal = self.terminal + " "
        else:
            self.terminal = self.terminal + key 



    def on_release(self, key):
        pass

    def kl(self):
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as kl:
            kl.join()

   

    def main_loop(self):
        while self.running: 
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: 
                    self.running = False
                    pygame.quit()
                

            self.win.fill((0,0,0))

            self.gui.reverse()

            for index, line in enumerate(self.gui):
                if self.debug:
                    self.font = pygame.font.Font(size=12)
                    sur = self.font.render(''.join(format(ord(char), '08b') for char in line), False, (255, 255, 255))
                else:
                    self.font = pygame.font.Font(size=32)
                    sur = self.font.render(line, False, (255, 255, 255))
                self.win.blit(sur, (50, 350 - (index * 35)))

            surface = self.font.render(self.terminal, False, (255, 0, 0))
            self.win.blit(surface, (50, 450))

            self.gui.reverse()

            pygame.display.flip()
            # ''.join(format(ord(char), '08b') for char in data))

if __name__ == "__main__":
    server = Server(socket.gethostbyname(socket.gethostname()), 12345)
