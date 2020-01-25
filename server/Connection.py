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
        self.char = None
        self.char_list = []
        self.session = session()
        self.is_finding = False
        self.in_fight = False
        self.battle = None

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

    async def close(self):
        if self.battle is not None:
            await self.battle.leave(self)
        self.user = None
        self.char = None
        self.is_finding = False
        self.in_fight = False
        self.battle = None
        self.session.close()
        self.conn.close()

    def get_user(self, login, password):
        if self.user is None:
            self.user = self.session.query(models.User).filter_by(login=login, password=password).first()
        return self.user

    def get_chars(self):
        if self.user is not None:
            res = self.session.query(models.Char).filter_by(user_id=self.user.id).all()
            self.char_list = list(map(lambda x: (x.id, x.name, x.class_name, x.rank), res))
        return self.char_list

    async def login(self, request, logged: dict):
        user = self.get_user(request["login"], self.hash_password(request["password"]))
        if user is not None and user.id is not None:
            if self.adr in logged:
                logged[self.adr].close()
            logged[self.adr] = self
            self.char_list = self.get_chars()
            await self.response("login", {
                "chars": self.char_list
            })
        else:
            await self.send_err("login", "Invalid login or password")

    async def play(self, request):
        if self.user is not None:
            char = self.session.query(models.Char).filter_by(id=request["char_id"], user_id=self.user.id).first()
            if char is not None:
                self.char = char
            else:
                await self.send_err("play", "This is char was removed or hasn't created")
        else:
            await self.send_err("play", "You didn't login in account")

    async def leave(self):
        if self.user is not None and self.char is not None:
            self.char = None
            if self.is_finding:
                self.is_finding = False
            await self.response("leave")
        else:
            await self.send_err("leave", "You didn't login in account")

    async def register(self, request):
        if self.session.query(models.User).filter_by(login=request["login"]).first() is None:
            self.session.add(models.User(login=request["login"], password=self.hash_password(request["password"])))
            self.session.commit()
            await self.response("register")
        else:
            await self.send_err("register", "Login is not available")

    async def create_char(self, request):
        if isinstance(self.user, models.User):
            if self.session.query(models.Char).filter_by(name=request["name"]).first() is None:
                char = models.Char(
                    name=request["name"],
                    lvl=1,
                    rank=1,
                    user_id=self.user.id,
                    balance=0,
                    class_name=request["class_name"],
                    race=request["race"],
                    strength=1,
                    agility=1,
                    smart=1
                )
                self.session.add(char)
                self.session.commit()
                self.char_list = self.get_chars()
                await self.response("create_char", {
                    "id": char.id,
                    "chars": self.char_list
                })
            else:
                await self.send_err("create_char", "Name is not available")
        else:
            await self.send_err("create_char", "You didn't login in account")

    async def delete_char(self, request):
        if isinstance(self.user, models.User):
            char = self.session.query(models.Char).filter_by(id=request["id"]).first()
            if char is not None:
                self.session.delete(char)
                self.session.commit()
                self.char_list = self.get_chars()
                await self.response("delete_char", {
                    "chars": self.char_list
                })
            else:
                await self.send_err("delete_char", "Char wasn't created")
        else:
            await self.send_err("delete_char", "You didn't login in account")

    async def get_inventory(self):
        if self.user is not None and self.char is not None:
            inventory = self.session.query(models.RealItem).filter_by(char_id=self.char.id).all()
            await self.response("get_inventory", {
                "inventory": inventory if inventory is not None else []
            })
        else:
            await self.send_err("get_inventory", "You didn't login in account")

    async def get_real_item_by_id(self, request):
        if self.user is not None and self.char is not None:
            real_item = self.session.query(models.RealItem).filter_by(id=request["real_item_id"]).all()
            await self.response("get_real_item_by_id", {
                "real_item": real_item
            })
        else:
            await self.send_err("get_real_item_by_id", "You didn't login in account")

    async def sell_item(self, request):
        if self.user is not None and self.char is not None:
            real_item = self.session.query(models.RealItem).filter_by(id=request["real_item_id"]).first()
            if real_item is not None:
                price = self.session.query(models.Item).filter_by(id=real_item.item_id).first().price
                self.char.balance += price * 0.75  # 3/4 of buyer's price
                self.session.delete(real_item)
                self.session.commit()
            else:
                await self.send_err("sell_item", "Error with real_item_id")
        else:
            await self.send_err("sell_item", "You didn't login in account")

    async def buy_item(self, request):
        if self.user is not None and self.char is not None:
            item = self.session.query(models.Item).filter_by(id=request["item_id"]).first()
            if item is not None:
                if item.price <= self.char.balance:
                    self.session.add(models.RealItem(item.id, self.char.id))
                    self.session.commit()
                else:
                    await self.send_err("buy_item", "Not enough money")
            else:
                await self.send_err("buy_item", "Error with item_id")
        else:
            await self.send_err("buy_item", "You didn't login in account")

    async def wear_item(self, request):
        if self.user is not None and self.char is not None:
            real_item = self.session.query(models.RealItem).filter_by(id=request["real_item_id"]).first()
            if real_item is not None:
                if request["slot_name"] == "head":
                    self.char.head = real_item.id
                elif request["slot_name"] == "body":
                    self.char.body = real_item.id
                elif request["slot_name"] == "legs":
                    self.char.legs = real_item.id
                elif request["slot_name"] == "boots":
                    self.char.boots = real_item.id
                else:
                    await self.send_err("wear_item", "Error with slot_name")
            else:
                await self.send_err("wear_item", "Error with real_item_id")
        else:
            await self.send_err("wear_item", "You didn't login in account")

    async def find(self, request, add_finder):
        if self.user is not None and self.char is not None:
            if not self.is_finding and not self.in_fight:
                self.is_finding = True
                await add_finder(self)
            else:
                await self.send_err("find", "You already in finding or in battle")
        else:
            await self.send_err("find", "You didn't login in account")

    async def stop_finding(self, request, del_finder):
        if self.user is not None and self.char is not None:
            self.is_finding = False
            del_finder(self)
        else:
            await self.send_err("find", "You didn't login in account")

    async def fight(self, battle, enemy):
        self.is_finding = False
        self.in_fight = True
        self.battle = battle
        await self.response("find", {
            "step": battle.__getattribute__("player" + str(battle.step + 1))["conn"].char.name,
            "enemy": {
                "name": enemy.char.name,
                "class_name": enemy.char.class_name,
                "rank": enemy.char.rank,
                "power": 20,
                "health": 100,
                "max_health": 100
            },
            "player": {
                "power": 20,
                "health": 100
            }
        })

    async def action(self, request):
        if self.user is not None and self.char is not None and self.in_fight and self.battle is not None:
            status = await self.battle.action(self, self.session.query(models.Skill).filter_by(
                id=request["skill_id"]
            ).first())
            if status == "ok":
                await self.response("action")
            else:
                await self.send_err("action", status)
        else:
            await self.send_err("action", "Not in fight")

    def get_protect_by_real_item(self, real_item_id):
        if real_item_id is None:
            return 0
        return self.session.query(models.Item.protect).filter_by(
            id=self.session.query(models.RealItem.id).filter_by(id=real_item_id).first()
        ).first()

    def get_damage_by_real_item(self, real_item_id):
        if real_item_id is None:
            return 0
        return self.session.query(models.Item.damage).fitler_by(
            id=self.session.query(models.RealItem.id).filter_by(id=real_item_id).first()
        ).first()

    @staticmethod
    def get_remains_protect(value: int):
        return (100 - value) / 100

    @staticmethod
    def get_remains_attack(value: int):
        return (100 + value) / 100

    def get_damage(self, damage):
        for item in [
            self.get_protect_by_real_item(self.char.head),
            self.get_protect_by_real_item(self.char.body),
            self.get_protect_by_real_item(self.char.legs),
            self.get_protect_by_real_item(self.char.boots),
            self.get_protect_by_real_item(self.char.weapon)
        ]:
            damage *= self.get_remains_protect(item)
        return damage

    def get_attack_damage(self, skill: models.Skill):
        if skill.class_name == self.char.class_name:
            damage = skill.damage
            bonus = 0
            if self.char.class_name == "Воин":
                bonus = self.char.strength
            elif self.char.class_name == "Вор в законе":
                bonus = self.char.agility
            elif self.char.class_name == "Маг":
                bonus = self.char.smart
            for item in [
                bonus,
                self.get_damage_by_real_item(self.char.head),
                self.get_damage_by_real_item(self.char.body),
                self.get_damage_by_real_item(self.char.legs),
                self.get_damage_by_real_item(self.char.boots),
                self.get_damage_by_real_item(self.char.weapon)
            ]:
                damage *= self.get_remains_attack(item)
            return damage
        return 0

    async def win(self):
        self.in_fight = False
        self.is_finding = False
        self.char.rank += 1
        self.session.commit()
        await self.response("result", {
            "is_win": True,
            "rank": self.char.rank
        })

    async def loose(self):
        self.in_fight = False
        self.is_finding = False
        if self.char.rank > 1:
            self.char.rank -= 1
            self.session.commit()
        await self.response("result", {
            "is_win": False,
            "rank": self.char.rank
        })

    async def battle_leave(self, request):
        if self.battle is not None:
            await self.battle.leave(self)
        await self.response("battle_leave")

