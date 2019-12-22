import json
import socket
import hashlib


class ServerAPI:
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if ServerAPI._instance is None:
            ServerAPI._instance = super(ServerAPI, cls).__new__(cls, *args, **kwargs)
        return ServerAPI._instance

    def __init__(self, ip, port=48880):
        self.ip = ip
        self.port = port
        self._listeners = {}
        self._requests_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def close(self):
        self.socket.close()

    def receive_thread(self):
        while True:
            data = self.socket.recv(4096)
            print(data)
            request = json.loads(data.decode("utf-8"))
            response_type = request["type"]
            if response_type in self._listeners:
                for callback in self._listeners[response_type]:
                    callback(request)

    def broadcast_thread(self):
        while True:
            if len(self._requests_queue) > 0:
                request = self._requests_queue.pop(0)
                print("from client" + str(request))
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

