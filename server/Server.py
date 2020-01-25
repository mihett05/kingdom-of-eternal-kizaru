import socket
import asyncio
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import server.models as models
from server.Connection import Connection
from server.PackageException import PackageException
from server.Battle import Battle


class Server:
    def __init__(self, host="localhost", port=48880):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(16)
        self.socket.setblocking(False)
        self.engine = create_engine("sqlite:///db.db")
        models.User.metadata.create_all(self.engine)
        models.Char.metadata.create_all(self.engine)
        models.Item.metadata.create_all(self.engine)
        models.RealItem.metadata.create_all(self.engine)
        models.Skill.metadata.create_all(self.engine)
        models.Worn.metadata.create_all(self.engine)
        self.logged = dict()
        self.loop = None
        self.finders = set()
        self.battles = list()

    @staticmethod
    def validate(request, need_keys, fatal=True):
        for key in need_keys:
            if key not in request:
                if fatal:
                    raise PackageException
                else:
                    return False
        return True

    async def add_finder(self, conn: Connection):
        if len(self.finders) > 0:
            found = min(self.finders, key=lambda x: abs(x.char.rank - conn.char.rank))
            if found.is_finding and found.char is not None and found.user is not None:
                battle = Battle((found, conn), self.end_callback)
                self.battles.append(battle)
                await found.fight(battle, conn)
                await conn.fight(battle, found)
            else:
                self.finders.remove(found)
                await self.add_finder(conn)
        else:
            self.finders.add(conn)

    async def end_callback(self, winner: Connection, looser: Connection, battle: Battle):
        print(winner.char, looser.char)
        if winner is not None:
            await winner.win()
        if looser is not None:
            await looser.loose()
        self.battles.remove(battle)

    async def del_finder(self, conn: Connection):
        if conn in self.finders:
            self.finders.remove(conn)

    async def handle_connection(self, sock, adr):
        """
        types of requests:
            request - only errors with requests,
            others are in Connection
        """
        try:
            conn = Connection(sock, adr, self.loop, sessionmaker(bind=self.engine))
            try:
                if adr in self.logged:
                    old_conn = self.logged.pop(adr)
                    if isinstance(old_conn, socket.socket):
                        await old_conn.close()
            except OSError:
                pass
            while True:
                try:
                    data = await self.loop.sock_recv(conn.conn, 4096)
                    if not data:
                        if adr in self.logged:
                            self.logged.pop(adr)
                        print(1)
                        await conn.close()
                        break
                except OSError:
                    if adr in self.logged:
                        self.logged.pop(adr)
                    break
                else:
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
                            await conn.play(request)

                        elif request["type"] == "leave":
                            self.validate(request, [])
                            await conn.leave()

                        elif request["type"] == "create_char":
                            self.validate(request, ["name", "race", "class_name"])
                            await conn.create_char(request)

                        elif request["type"] == "delete_char":
                            self.validate(request, ["id"])
                            await conn.delete_char(request)

                        elif request["type"] == "get_inventory":
                            self.validate(request, [])
                            await conn.get_inventory()

                        elif request["type"] == "get_real_item_by_id":
                            self.validate(request, ["real_item_id"])
                            await conn.get_real_item_by_id(request)

                        elif request["type"] == "sell_item":
                            self.validate(request, ["real_item_id"])
                            await conn.sell_item(request)

                        elif request["type"] == "buy_item":
                            self.validate(request, ["item_id"])
                            await conn.buy_item(request)

                        elif request["type"] == "wear_item":
                            self.validate(request, ["real_item_id", "slot_name"])
                            await conn.wear_item(request)

                        elif request["type"] == "find":
                            self.validate(request, [])
                            await conn.find(request, self.add_finder)

                        elif request["type"] == "stop_find":
                            self.validate(request, [])
                            await conn.stop_finding(request, self.del_finder)

                        elif request["type"] == "battle_leave":
                            self.validate(request, [])
                            await conn.battle_leave(request)
                        else:
                            await conn.send_err("request", "Unknown type")
                    except json.JSONDecodeError:
                        await conn.send_err("request", "Invalid package")
                    except PackageException as e:
                        await conn.send_err("request", e.txt)
        except BaseException as e:
            print(e)

    async def _start(self):
        print("Started")
        while True:
            conn, adr = await self.loop.sock_accept(self.socket)
            print("New con: " + str(adr))
            asyncio.run_coroutine_threadsafe(self.handle_connection(conn, adr), self.loop)

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._start())
