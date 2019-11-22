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

    def close(self):
        self.session.close()
        self.conn.close()


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

    async def invalid_pkg(self, conn):
        await self.send_msg(conn, json.dumps({
            "status": "error",
            "desc": "Invalid package"
        }))

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
                    login = request["login"]
                    password = request["password"]
                    user = conn.session.query(models.User).filter_by(login=login, password=password).first()
                    if user.id is not None:
                        if addr not in self.logged:
                            self.logged[addr] = conn
                        else:
                            self.logged[addr].close()
                            self.logged[addr] = conn
                        chars = conn.session.query(
                            models.Char.id, models.Char.name,
                            models.Char.lvl, models.Char.rank
                        ).filter_by(user_id=user.id).all()
                        conn.char_list = chars.copy()
                        await conn.send_msg(json.dumps({
                            "status": "ok",
                            "data": chars
                        }))
                    else:
                        await conn.send_msg(json.dumps({
                            "status": "err",
                            "desc": "Invalid login or password"
                        }))
                elif request["type"] == "logout":
                    if addr in self.logged:
                        self.logged.pop(addr).close()
                elif request["type"] == "play":
                    if addr in self.logged:
                        if "char_id" not in request:
                            raise json.JSONDecodeError
                        char = list(filter(lambda x: int(x[0]) == int(request["char_id"]), conn.char_list))
                        if len(char) == 1:
                            conn.active_char = char[0]
                            await conn.send_msg(json.dumps({
                                "status": "ok"
                            }))
                        else:
                            await conn.send_msg(json.dumps({
                                "status": "err",
                                "desc": "This is char was removed or hasn't created"
                            }))
                    else:
                        await conn.send_msg(json.dumps({
                            "status": "err",
                            "desc": "There wasn't login to account"
                        }))
                else:
                    await conn.send_msg(json.dumps({
                        "status": "err",
                        "desc": "Unknown type"
                    }))
            except json.JSONDecodeError:
                await self.invalid_pkg(conn.conn)

    async def _start(self):
        while True:
            conn, addr = await self.loop.sock_accept(self.socket)
            asyncio.run_coroutine_threadsafe(self.handle_connection(conn, addr), self.loop)

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._start())


s = Server()
s.start()

