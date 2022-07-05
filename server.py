import socket,msggen,msgfilter,json
from threading import Thread
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',5555))
server.listen()
print("Listening")
all_clients={}

def client_thread(client):
    while True:
        try:
            received_msg = client.recv(1024000)
            for c in all_clients:
                c.send(received_msg)
        except:
            del all_clients[client]
            client.close()
            print("Client Disconnected")
            break

while True:
    client,addr=server.accept()
    print("Client connected")
    all_clients[client]=client
    thread = Thread(target=client_thread,args=(client,))
    thread.start()