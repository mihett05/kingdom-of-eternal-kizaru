import socket
import json
import threading

# Сори за процедурнй стиль, файл временный, для теста сервера

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 0))
run = True


def receive_thread():
    global run
    while run:
        print("waiting")
        data = s.recv(4096)
        try:
            response = json.loads(data.decode("utf-8"))
            print(response)
        except json.JSONDecodeError:
            print("json error")


def send(data: dict):
    s.send(json.dumps(data).encode("utf-8"))


s.connect(("localhost", 48880))
threading.Thread(target=receive_thread, args=()).start()

send({
    "type": "register",
    "login": "123",
    "password": "123"
})
print("sended")

run = False
s.close()


