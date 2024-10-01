import socket
import pickle

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
    action = input("Download, upload, or view files: ").lower()
    while True:
        if action in ("download", "upload", "view", "view files", "quit"):
            if action == "view files":
                action = "view"
            return action
        else:
            action = input(
                "Please enter 'download', 'upload', 'view', or 'quit' ").lower()


def send_msg(socket, msg):
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    msg = bytes(msg, "utf-8")
    socket.send(msg)


def main():
    files = receive_pickle(s)
    print("Available files:")

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
        elif action == "view":
            print("Available files:")
            files = receive_pickle(s)
            if files is None:
                return
            for file in files:
                print(file)


main()
