import socket
import asyncio
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from Connection import Connection


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

    async def handle_connection(self, sock, addr):
        """
        types of requests:
            request - only errors with requests,
            others are in Connection
        """
        conn = Connection(sock, addr, self.loop, sessionmaker(bind=self.engine))
        while True:
            data = await self.loop.sock_recv(conn.conn, 4096)
            if not data:
                if addr in self.logged:
                    self.logged.pop(addr)
                conn.close()
                break
            try:
                request = json.loads(data.decode("utf-8"))
                print(request)
                if "type" not in request:
                    raise json.JSONDecodeError
                if request["type"] == "login":
                    if "login" not in request and "password" not in request:
                        raise json.JSONDecodeError
                    await conn.login(request, self.logged)

                elif request["type"] == "logout":
                    if addr in self.logged:
                        self.logged.pop(addr).close()

                elif request["type"] == "play":
                    if "char_id" not in request:
                        raise json.JSONDecodeError
                    await conn.play(request, conn.addr in self.logged)
                else:
                    await conn.send_err("request", "Unknown type")
            except json.JSONDecodeError:
                await conn.send_err("request", "Invalid package")

    async def _start(self):
        while True:
            conn, addr = await self.loop.sock_accept(self.socket)
            print("New con: " + str(addr))
            asyncio.run_coroutine_threadsafe(self.handle_connection(conn, addr), self.loop)

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._start())
