import socket
import pickle
from os import listdir

HEADERSIZE = 10


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))
server.listen(1)


def send_dir(socket, directory):
    files = listdir(directory)
    msg = pickle.dumps(files)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    socket.send(msg)
    return


def receive_msg(socket):
    full_msg = ""
    new_msg = True
    msg_length = 0
    while len(full_msg) - HEADERSIZE != msg_length:
        msg = socket.recv(16)
        if not msg:
            print("Connection has been terminated by the client")
            return None

        if new_msg:
            msg_length = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msg_length:
            return full_msg[HEADERSIZE:]


while True:
    directory = "storage"
    clientsocket, address = server.accept()
    print(f"Connection to {address} has been established")
    directory = "storage"
    send_dir(clientsocket, directory)
    while True:
        action = receive_msg(clientsocket)
        if action == "view":
            send_dir(clientsocket, directory)
        elif action == "download":
            ...
        elif action == "upload":
            ...
        elif action is None:
            print(f"Connection with {address} has been terminated")
            break
