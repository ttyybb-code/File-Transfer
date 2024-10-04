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


def receave_file(socket, filename):
    with open(filename, "w") as file:
        full_contents = ""
        new_message = True
        msg_length = 0
        while len(full_contents) - HEADERSIZE != msg_length:
            contents = socket.recv(16)
            if new_message:
                msg_length = int(contents[:HEADERSIZE])
                new_message = False

            full_contents += contents.decode("utf-8")

            if len(full_contents) - HEADERSIZE == msg_length:
                file.write(full_contents[HEADERSIZE:])


def send_file(socket, file_path):
    with open(file_path, "r") as file:
        content = file.read()
        content = f"{len(content):<{HEADERSIZE}}" + content
        msg = bytes(content, "utf-8")
        socket.sendall(msg)


while True:
    clientsocket, address = server.accept()
    print(f"Connection to {address} has been established")
    directory = "storage"
    send_dir(clientsocket, directory)
    while True:
        action = receive_msg(clientsocket)
        if action == "view":
            send_dir(clientsocket, directory)
        elif action == "download":
            filename = receive_msg(clientsocket)
            send_file(clientsocket, f"{directory}/{filename}")
        elif action == "upload":
            file_name = receive_msg(clientsocket)
            print(f"{address} is uploading {file_name}")
            receave_file(clientsocket, f"{directory}/{file_name}")
        elif action is None:
            print(f"Connection with {address} has been terminated")
            break
