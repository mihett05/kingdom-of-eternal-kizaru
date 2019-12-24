import json
import socket
import asyncio
import hashlib
import server.models as models


class Connection:
    def __init__(self, sock: socket.socket, adr, loop: asyncio.AbstractEventLoop, session):
        self.conn = sock
        self.adr = adr
        self.loop = loop
        self.user = None
        self.active_char = None
        self.char_list = []
        self.session = session()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    async def response(self, response_type, data=None, is_ok=True):
        if data is None:
            data = {}
        await self.send_msg(json.dumps({
            "type": response_type,
            "status": "ok" if is_ok else "err",
            **data
        }))

    async def send_msg(self, msg):
        await self.loop.sock_sendall(self.conn, msg.encode("utf-8"))

    async def send_err(self, response_type, desc: str):
        await self.response(response_type, {"desc": desc}, is_ok=False)

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
        user = self.get_user(request["login"], request["password"])
        if user is not None and user.id is not None:
            if self.adr in logged:
                logged[self.adr].close()
            logged[self.adr] = self
            await self.response("login", {
                "data": {
                    "chars": self.get_chars()
                }
            })
        else:
            await self.send_err("login", "Invalid login or password")

    async def play(self, request, is_logged):
        if is_logged:
            char = list(filter(lambda x: int(x[0]) == int(request["char_id"]), self.char_list))
            if len(char) == 1:
                self.active_char = char[0]
                await self.response("play")
            else:
                await self.send_err("play", "This is char was removed or hasn't created")
        else:
            await self.send_err("play", "You didn't login in account")

    async def register(self, request):
        if self.session.query(models.User).filter_by(login=request["login"]).first() is None:
            self.session.add(models.User(login=request["login"], password=self.hash_password(request["password"])))
            self.session.commit()
            await self.response("register")
        else:
            await self.send_err("register", "Login is not available")

    async def create_char(self, request, logged):
        if self.adr in logged:
            if self.session.query(models.Char).filter_by(name=request["name"]).first() is None:
                self.session.add(models.Char(
                    name=request["name"],
                    lvl=1,
                    rank=1,
                    user_id=logged[self.adr],
                    balance=0,
                    class_name=request["class_name"],
                    race=request["race"],
                    strength=1,
                    agility=1,
                    smart=1
                ))
                self.session.commit()
                await self.response("create_char")
            else:
                await self.send_err("create_char", "Name is not available")
        else:
            await self.send_err("create_char", "You didn't login in account")
