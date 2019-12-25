import socket
import asyncio
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import server.models as models
from server.Connection import Connection
from server.PackageException import PackageException


class Server:
    def __init__(self, host="localhost", port=48880):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(10)
        self.socket.setblocking(False)
        self.engine = create_engine("sqlite:///db.db")
        models.User.metadata.create_all(self.engine)
        models.Char.metadata.create_all(self.engine)
        self.logged = dict()
        self.loop = None

    @staticmethod
    def validate(request, need_keys, fatal=True):
        for key in need_keys:
            if key not in request:
                if fatal:
                    raise PackageException
                else:
                    return False
        return True

    async def handle_connection(self, sock, adr):
        """
        types of requests:
            request - only errors with requests,
            others are in Connection
        """
        try:
            conn = Connection(sock, adr, self.loop, sessionmaker(bind=self.engine))
            while True:
                data = await self.loop.sock_recv(conn.conn, 4096)
                if not data:
                    if adr in self.logged:
                        self.logged.pop(adr)
                    conn.close()
                    break
                try:
                    request = json.loads(data.decode("utf-8"))
                    print(request)
                    self.validate(request, ["type"])
                    if request["type"] == "login":
                        self.validate(request, ["login", "password"])
                        await conn.login(request, self.logged)

                    elif request["type"] == "logout":
                        if adr in self.logged:
                            self.logged.pop(adr).close()

                    elif request["type"] == "register":
                        self.validate(request, ["login", "password"])
                        await conn.register(request)

                    elif request["type"] == "play":
                        self.validate(request, ["char_id"])
                        await conn.play(request, self.logged)

                    elif request["type"] == "create_char":
                        self.validate(request, ["name", "race", "class_name"])
                        await conn.create_char(request, self.logged)

                    elif request["type"] == "get_inventory":
                        self.validate(request, ["char_id"])
                        await conn.get_inventory(request, self.logged)

                    else:
                        await conn.send_err("request", "Unknown type")
                except json.JSONDecodeError:
                    await conn.send_err("request", "Invalid package")
                except PackageException as e:
                    await conn.send_err("request", e.txt)
        except BaseException as e:
            print(e)

    async def _start(self):
        while True:
            conn, adr = await self.loop.sock_accept(self.socket)
            print("New con: " + str(adr))
            asyncio.run_coroutine_threadsafe(self.handle_connection(conn, adr), self.loop)

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._start())
