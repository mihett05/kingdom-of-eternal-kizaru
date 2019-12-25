import json
import socket
import hashlib


class ServerAPI:
    def __init__(self, ip, port=48880):
        self.ip = ip
        self.port = port
        self.connected = False
        self._listeners = {}
        self._requests_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def connect(self):
        self.socket.connect((self.ip, self.port))
        self.connected = True

    def close(self):
        self.connected = False
        self.socket.close()

    def receive_thread(self):
        while self.connected:
            data = self.socket.recv(4096)
            try:
                response = json.loads(data.decode("utf-8"))
                response_type = response["type"]
                if response_type in self._listeners:
                    for callback in self._listeners[response_type]:
                        callback(response)
            except json.JSONDecodeError:
                pass

    def broadcast_thread(self):
        while self.connected:
            if len(self._requests_queue) > 0:
                request = self._requests_queue.pop(0)
                self.socket.send(request.encode("utf-8"))

    def on(self, resp_type):
        def decorator(func):
            nonlocal resp_type
            self._add_listener(resp_type, func)
            return func
        return decorator

    def _add_listener(self, resp_type, callback):
        if resp_type not in self._listeners:
            self._listeners[resp_type] = []
        self._listeners[resp_type].append(callback)

    def request(self, req_type, data=None):
        if data is None:
            data = {}
        self._add_request(json.dumps({
            "type": req_type,
            **data
        }))

    def _add_request(self, request):
        self._requests_queue.append(request)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def login(self, login, hashed_password):
        self.request("login", {
            "login": login,
            "password": hashed_password
        })

    def logout(self):
        self.request("logout")

    def play(self, char_id):
        self.request("play", {
            "char_id": char_id
        })

    def register(self, login, password):
        self.request("register", {
            "login": login,
            "password": password
        })

    def create_char(self, name, class_name, race):
        self.request("create_char", {
            "name": name,
            "class_name": class_name,
            "race": race
        })

    def get_inventory(self, char_id):
        self.request("get_inventory", {
            "char_id": char_id
        })

