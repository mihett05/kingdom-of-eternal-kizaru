import socket
import asyncio
import json
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class Connection:
    def __init__(self, sock: socket.socket, addr, session):
        self.conn = sock
        self.addr = addr
        self.user = None
        self.active_char = None
        self.char_list = []
        self.session = session()

    async def send_msg(self, msg):
        await asyncio.get_event_loop().sock_sendall(self.conn, msg.encode("utf-8"))

    async def send_err(self, desc: str):
        await self.send_msg(json.dumps({
            "status": "err",
            "desc": desc
        }))

    def close(self):
        self.session.close()
        self.conn.close()
        
    def get_user(self, login, password):
        if self.user is None:
            self.user = self.session.query(models.User).filter_by(login=login, password=password).first()
        return self.user

    def get_chars(self):
        if self.user is not None:
            if len(self.char_list) == 0:
                res = self.session.query(
                    models.Char.id, models.Char.name,
                    models.Char.lvl, models.Char.rank
                ).filter_by(user_id=self.user.id).all()
                if len(res) > 0:
                    self.char_list = res.copy()
        return self.char_list

    async def login(self, request, logged: dict):
        if self.get_user(request["login"], request["password"]).id is not None:
            if self.addr in logged:
                logged[self.addr].close()
            logged[self.addr] = self
            await self.send_msg(json.dumps({
                "status": "ok",
                "data": self.get_chars()
            }))
        else:
            await self.send_err("Invalid login or password")

    async def play(self, request, is_logged):
        if is_logged:
            char = list(filter(lambda x: int(x[0]) == int(request["char_id"]), self.char_list))
            if len(char) == 1:
                self.active_char = char[0]
                await self.send_msg(json.dumps({"status": "ok"}))
            else:
                await self.send_err("This is char was removed or hasn't created")
        else:
            await self.send_err("There wasn't login to account")


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
    async def send_msg(conn: socket.socket, msg: str):
        await asyncio.get_event_loop().sock_sendall(conn, msg.encode("utf-8"))

    async def handle_connection(self, sock, addr):
        conn = Connection(sock, addr, sessionmaker(bind=self.engine))
        while True:
            data = await self.loop.sock_recv(conn.conn, 4096)
            if not data:
                if addr in self.logged:
                    self.logged.pop(addr)
                conn.close()
                break
            try:
                request = json.loads(data.decode("utf-8"))
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
                    await conn.send_err("Unknown type")
            except json.JSONDecodeError:
                await conn.send_err("Invalid package")

    async def _start(self):
        while True:
            conn, addr = await self.loop.sock_accept(self.socket)
            asyncio.run_coroutine_threadsafe(self.handle_connection(conn, addr), self.loop)

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._start())


s = Server()
s.start()

