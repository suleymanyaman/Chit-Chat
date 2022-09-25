import socket
from threading import Thread
import random
import sys



def get_key(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]


def accept_incoming_connections():
    while True:
        client, client_adress = SERVER.accept()
        client.send("Welcome to Chit-Chat ! {} people is online.".format(str(len(clients))).encode())
        print("%s:%s has connected" % client_adress)
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    #Make sure that every client has a distinct id
    global target_client
    while 1:
        client_id = client.recv(1024).decode("utf-8")
        if client_id not in list(clients.values()):
            clients[client]=client_id
            status[client_id]="AVAILABLE"
            break
        else:
            continue


    #Make sure that every client has a distinct peer

    while 1:
        msg = client.recv(100000000).decode("utf-8")


        if msg == "?pRG=gmxHD74cEm":
            if client_id in list(match.keys())+list(match.values()):
                try:
                    del match[client_id]
                    get_key(clients, target_client).send("Your partner has left the chat :(".encode())
                    status[target_client]="AVAILABLE"


                except KeyError:
                    del match[get_key(match, client_id)]
                    get_key(clients, target_client).send("Your partner has left the chat :(".encode())
                    status[target_client] = "AVAILABLE"

            target_client = random.choice(list(clients.values()))
            if client_id!=target_client and status[target_client]=="AVAILABLE":
                match[client_id] = target_client
                status[client_id] = "FULL"
                status[target_client] = "FULL"
                client.send("You have been connected to someone!".encode())
                get_key(clients,target_client).send(
                    "You have been connected to someone!".encode())


            else:
                client.send("We couldn't find a match for you, try again".encode())
                continue

        elif msg == "4t7w!z%C":
            client.close()
            try:
                get_key(clients, target_client).send("Your partner has left the chat :(".encode())
                status[target_client] = "AVAILABLE"
            finally:
                del clients[client]
                del status[client_id]
                break

        else:
            frm = clients[client]
            try:
                to = match[frm]
            except KeyError:
                to = get_key(match, frm)


            to_client = get_key(clients, to)
            to_client.send((client_id+":"+msg).encode("utf-8"))



clients={}
status={}
match={}





HOST = "0.0.0.0"
PORT = 5000
ADDR = (HOST,PORT)

SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__== "__main__":
    SERVER.listen(5)
    print("Waiting for connection.....")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()




