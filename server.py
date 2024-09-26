import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection to {address} has been established")
    clientsocket.send("echo".encode("utf-8"))
