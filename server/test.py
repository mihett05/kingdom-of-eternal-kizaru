import socket
import json
import threading

# Сори за процедурнй стиль, файл временный, для теста сервера

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 0))
run = True


def receive():
    data = s.recv(4096)
    try:
        response = json.loads(data.decode("utf-8"))
        print(response)
        return response
    except json.JSONDecodeError:
        print("json error")


def send(data: dict):
    s.send(json.dumps(data).encode("utf-8"))


s.connect(("localhost", 48880))

send({
    "type": "login",
    "login": "123",
    "password": "123"
})
status = receive()

send({
    "type": "play",
    "char_id": status["data"]["chars"][0][0]
})
receive()

send({
    "type": "find"
})
receive()




send({
    "type": "leave"
})
receive()



send({
    "type": "logout"
})

s.close()
