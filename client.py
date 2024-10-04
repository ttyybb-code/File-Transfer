import socket
import pickle
from os import listdir


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))


def receive_pickle(socket):
    full_msg = b""
    new_msg = True
    msg_length = 0
    while True:
        msg = socket.recv(16)
        if not msg:
            print("The connection was closed by the server")
            return None

        if new_msg:
            msg_length = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msg_length:
            return pickle.loads(full_msg[HEADERSIZE:])


def menu():
    action = input("Download, upload, or quit: ").lower()
    while True:
        if action in ("download", "upload", "quit"):
            return action
        else:
            action = input(
                "Please enter 'download', 'upload', or 'quit' ").lower()


def send_msg(socket, msg):
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    msg = bytes(msg, "utf-8")
    socket.send(msg)


def send_file(socket, file_path):
    with open(file_path, "r") as file:
        content = file.read()
        content = f"{len(content):<{HEADERSIZE}}" + content
        msg = bytes(content, "utf-8")
        socket.sendall(msg)


def receave_file(socket, file_name):
    full_msg = ""
    new_msg = True
    msg_length = 0
    while len(full_msg) - HEADERSIZE != msg_length:
        msg = socket.recv(16)
        if new_msg:
            msg_length = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msg_length:
            with open(file_name, "w") as file:
                file.write(full_msg[HEADERSIZE:])


def main():
    files = receive_pickle(s)
    print("Available files to download:")

    dir = "clientFiles"
    if files is None:
        return
    for file in files:
        print(file)
    while True:
        action = menu()
        send_msg(s, action)

        if action == "quit":
            print("going to quit")
            s.close()
            exit()
        elif action == "upload":
            while True:
                print("Available files")
                print(listdir(dir))
                file_name = input("Enter the name of the file: ")
                file_name = f"{dir}/{file_name}"
                try:
                    with open(file_name, 'rb') as file:
                        break
                except (FileNotFoundError, IOError):
                    print("Invalid file selected. Please try again.")
            send_msg(s, file_name[len(dir):])
            send_file(s, file_name)
        elif action == "download":
            file_name = ""
            while file_name not in files:
                file_name = input("Enter the name of the file: ")
                if file_name not in files:
                    print("Invalid file")
            send_msg(s, file_name)
            receave_file(s, f"{dir}/{file_name}")
            if files is None:
                return
            for file in files:
                print(file)


main()
