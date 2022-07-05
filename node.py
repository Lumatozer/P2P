import socket,random,threading,uidgen,msgfilter,msggen
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=random.randint(100,1000)
server.bind(('127.0.0.1',port))
print(port)
server.listen()
allc={}
used=[]

def client_handeler(client):
    cc=client
    global allc
    while 1:
        try:
            received_msg=client.recv(1024).decode()
            if msgfilter.filter(received_msg,"type")=="relay":
                if  msgfilter.filter(received_msg,"uid") not in used:
                    used.append(msgfilter.filter(received_msg,"uid"))
                    print(msgfilter.filter(received_msg,"data"))
                    for client in allc:
                        try:
                            client.send(received_msg.encode())
                        except:
                            print("Disconnected")
                            del allc[client]
                            client.close()
        except Exception as e:
            print("Disconnected "+str(e))
            del allc[cc]
            client.close()
            break

def send():
    global allc
    while 1:
        raw_msg=input("").encode()
        uid=uidgen.genz()
        msg=msggen.gen(raw_msg,uid)
        used.append(uid)
        for client in allc:
            try:
                client.send(msg.encode())
            except:
                print("Disconnected")
                del allc[client]

if input("Connect(1) Listen (0) : ")!="0":
    sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sc.connect(('127.0.0.1',int(input("PORT : "))))
    allc[sc]=sc
    t1=threading.Thread(target=client_handeler,args=(sc,))
    t1.start()

t2=threading.Thread(target=send)
t2.start()
while 1:
    client,addr=server.accept()
    print("Got Peer")
    allc[client]=client
    t1=threading.Thread(target=client_handeler,args=(client,))
    t1.start()