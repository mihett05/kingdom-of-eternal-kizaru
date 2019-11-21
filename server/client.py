import socket
import json
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 48881))
s.connect(("localhost", 48880))

password = "qwerty1488"
hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
s.send(json.dumps({
    "type": "login",
    "login": "mihett05",
    "password": hashed_password
}).encode("utf-8"))
print(s.recv(4096))
s.shutdown(socket.SHUT_RD)
s.close()
