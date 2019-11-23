import socket
import json
import hashlib
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 0))
s.connect(("localhost", 48880))

password = "qwerty1488"
hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
s.send(json.dumps({
    "type": "login",
    "login": "mihett05",
    "password": hashed_password
}).encode("utf-8"))
res = json.loads(s.recv(4096).decode("utf-8"))
print(res)
info = json.dumps({
    "type": "play",
    "char_id": res["data"][0][0]
}).encode("utf-8")
s.sendall(info)
print(json.loads(s.recv(4096).decode("utf-8")))
s.close()
