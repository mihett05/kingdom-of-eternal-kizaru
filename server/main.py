import socket
import asyncio
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models


class Server:
    def __init__(self, host="localhost", port=48880):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(100)
        session = sessionmaker()
        self.engine = create_engine("sqlite:///db.db", echo=False)
        models.User.metadata.create_all(self.engine)
        models.Char.metadata.create_all(self.engine)
        session.configure(bind=self.engine)

        self.session = session()
        self.logged = []

    async def invalid_pkg(self, conn):
        await self.send_msg(conn, json.dumps({
            "status": "error",
            "desc": "Invalid package"
        }))

    @staticmethod
    async def send_msg(conn: socket.socket, msg: str):
        await asyncio.get_event_loop().sock_sendall(conn, msg.encode("utf-8"))

    async def db_fetch_all(self, query):
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.db.cursor().execute(query).fetchall()
        )

    async def handle_connection(self, conn, addr):
        data = await asyncio.get_event_loop().sock_recv(conn, 4096)
        try:
            request = json.loads(data.decode("utf-8"))
            if "type" not in request:
                raise json.JSONDecodeError
            if request["type"] == "login":
                if "login" not in request and "password" not in request:
                    raise json.JSONDecodeError
                login = request["login"]
                password = request["password"]
                res = self.session.query(models.User.id).filter_by(login=login, password=password).first()
                if res is not None:
                    if addr not in self.logged:
                        self.logged.append(addr)

                    await self.send_msg(conn, json.dumps({
                        "status": "ok",
                        "data": self.session.query(models.Char.id, models.Char.name, models.Char.lvl,
                                                   models.Char.rank).filter_by(user_id=res[0]).all()
                    }))
                else:
                    await self.send_msg(conn, json.dumps({
                        "status": "err",
                        "desc": "Invalid login or password"
                    }))
            elif request["type"] == "logout":
                if addr in self.logged:
                    self.logged.remove(addr)
        except json.JSONDecodeError:
            await self.invalid_pkg(conn)

        conn.close()

    async def _start(self):
        while True:
            conn, addr = await asyncio.get_event_loop().sock_accept(self.socket)
            await asyncio.create_task(self.handle_connection(conn, addr))

    def start(self):
        asyncio.get_event_loop().run_until_complete(self._start())


s = Server()
s.start()

