import json
import socket
import hashlib
from time import time


class ServerAPI:
    def __init__(self, ip, port=48880):
        self.ip = ip
        self.port = port
        self.connected = False
        self._listeners = dict()
        self._one_time_listeners = dict()
        self._requests_queue = []
        self.cached = dict()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def connect(self):
        """
        Makes connection with server
        """
        self.socket.connect((self.ip, self.port))
        self.connected = True

    def close(self):
        """
        Breaks connection with server
        """
        self.connected = False
        self.socket.close()

    def __send_to_listener(self, response_type, response):
        if response_type in self._listeners:
            for callback in self._listeners[response_type]:
                callback(response)

    def receive_thread(self):
        """
        Thread with receiving data from server
        """
        try:
            while self.connected:
                data = self.socket.recv(8192)
                try:
                    response = json.loads(data.decode("utf-8"))
                    print(response)
                    response_type = response["type"]
                    self.__send_to_listener(response_type, response)
                except json.JSONDecodeError:
                    pass
        except ConnectionAbortedError as e:
            print(e)

    def broadcast_thread(self):
        """
        Thread with sending data to server
        """
        try:
            while self.connected:
                if len(self._requests_queue) > 0:
                    request = self._requests_queue.pop(0)
                    self.socket.send(request.encode("utf-8"))
        except OSError as e:
            print(e)

    def on(self, resp_type):
        """
        Adds listener to dict for receiving.
        Listener - callback with response from server
        :param resp_type: type of response from server
        """
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
        """
        Adds request to requests' queue
        :param req_type: type of request
        :param data: dict, that will be converted to json
        """
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

    def login(self, login, password):
        """
        Login in server
        :param login: username
        :param password: password, lol
        """
        self.request("login", {
            "login": login,
            "password": password
        })

    def logout(self):
        """
        Disconnect user from server
        """
        self.request("logout")

    def play(self, char_id):
        """
        Enter to the game with char with id=char_id
        :param char_id: id of char
        """
        self.request("play", {
            "char_id": char_id
        })

    def register(self, login, password):
        """
        Register new user
        :param login:
        :param password:
        """
        self.request("register", {
            "login": login,
            "password": password
        })

    def create_char(self, name, class_name, race=""):
        """
        Create new char
        :param name: name of new char
        :param class_name: class of new char
        :param race: race of new char
        """
        self.request("create_char", {
            "name": name,
            "class_name": class_name,
            "race": race
        })

    def delete_char(self, char_id):
        self.request("delete_char", {
            "id": char_id
        })

    def get_inventory(self):
        """
        Get inventory of char in game
        """
        if "get_inventory" in self.cached:
            if time() - self.cached["get_inventory"]["time"] >= 5.0:
                self.request("get_inventory")
            else:
                self.__send_to_listener("get_inventory", self.cached["get_inventory"]["data"])
        else:
            self.request("get_inventory")

    def get_real_item_by_id(self, real_item_id):
        """
        Get item from it's id
        :param real_item_id: id of item
        """
        self.request("get_real_item_id", {
            "real_item_id": real_item_id
        })

    def sell_item(self, real_item_id):
        """
        Sell item
        :param real_item_id: id of item in inventory
        """
        self.request("sell_item", {
            "real_item_id": real_item_id
        })

    def buy_item(self, item_id):
        """
        Buy item with item_id
        :param item_id: id of model of real item
        """
        self.request("buy_item", {
            "item_id": item_id
        })

    def wear_item(self, real_item_id, old_real_item_id=-1):
        """
        Set item to slot
        :param real_item_id: id of item in inventory
        """
        self.request("wear_item", {
            "real_item_id": real_item_id,
            "slot_name": "null",
            "old_real_item_id": old_real_item_id
        })

    @staticmethod
    def char_data_convert(char_server_data):
        return dict(zip(
            ("id", "name", "class", "rank", "money", "blacklist"), (*char_server_data, 0, 0)
        ))

    def find(self):
        self.request("find")

    def stop_find(self):
        self.request("stop_find")
        
    def battle_leave(self):
        self.request("battle_leave")

    def action(self, skill_id):
        self.request("action", {
            "skill_id": skill_id
        })

    def get_char_info(self):
        if "get_char_info" in self.cached:
            if time() - self.cached["get_char_info"]["time"] >= 5.0:
                self.request("get_char_info")
            else:
                self.__send_to_listener("get_char_info", self.cached["get_char_info"]["data"])
        else:
            self.request("get_char_info")
