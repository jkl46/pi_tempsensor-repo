from sense_hat import SenseHat
import time
import threading
import socket

HOST = '192.168.0.189'
PORT = 5353

se = SenseHat()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

get_temp = lambda: se.get_temperature()

clients = []
temp = lambda: str(se.get_temperature())[:4]

def handle(client):
    while 1:
        try:
            data = client.recv(255)
            client.send(temp().encode('utf-8'))
        except:
            clients.remove(client)
            client.close()
            
if __name__ == "__main__":
    while 1:
        client, address = s.accept()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()