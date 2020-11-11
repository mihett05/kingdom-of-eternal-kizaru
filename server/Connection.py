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
            cached_items = dict()

            def process(real_item):
                nonlocal self, cached_items
                item_id = real_item.item_id
                if item_id not in cached_items:
                    item = self.session.query(models.Item).filter_by(id=item_id).first()
                    if item:
                        json_item = {
                            "id": real_item.id,
                            "item_id": item.id,
                            "name": item.name,
                            "price": item.price * 0.75,
                            "damage": item.damage,
                            "protect": item.protect,
                            "strength": item.strength,
                            "agility": item.agility,
                            "smart": item.smart
                        }
                        cached_items = json_item.copy()
                        return json_item
                else:
                    return {
                        **cached_items[item_id],
                        "id": real_item.id
                    }
                return {
                    "id": -1,
                    "item_id": -1,
                    "name": "",
                    "price": 0,
                    "damage": 0,
                    "protect": 0,
                    "strength": 0,
                    "agility": 0,
                    "smart": 0
                }
            await self.response("get_inventory", {
                "inventory": list(map(process, inventory)) if inventory else []
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
                    self.char.balance -= item.price
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
            real_item = self.session.query(models.RealItem).filter_by(
                id=request["real_item_id"], char_id=self.char.id
            ).first()
            if real_item is not None:
                item = self.session.query(models.Worn).filter_by(owner=self.char.id,
                                                                  realitem_id=request["old_real_item_id"]).first()
                if item:
                    item.realitem_id = real_item.id
                else:
                    self.session.add(models.Worn(request["real_item_id"], self.char.id))
                self.session.commit()
            else:
                await self.send_err("wear_item", "Error with real_item_id")
        else:
            await self.send_err("wear_item", "You didn't login in account")

    async def find(self, request, add_finder):
        if self.user is not None and self.char is not None:
            if not self.is_finding and not self.in_fight:
                if self.char.balance >= 10:
                    self.is_finding = True
                    await add_finder(self)
                else:
                    await self.send_err("find", "You haven't enough money")
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
        skills = self.session.query(
            models.Skill.id, models.Skill.name,
            models.Skill.price, models.Skill.damage).filter_by(
            class_name=self.char.class_name
        ).order_by(models.Skill.price).all()
        await self.response("find", {
            "step": battle.__getattribute__("player" + str(battle.step + 1))["conn"].char.name,
            "skills": list(map(lambda x: {
                "id": x[0],
                "name": x[1],
                "price": x[2],
                "damage": x[3]
            }, skills)),
            "enemy": {
                "name": enemy.char.name,
                "class_name": enemy.char.class_name,
                "rank": enemy.char.rank,
                "power": 20,
                "health": 100,
                "max_health": 100
            },
            "player": {
                "name": self.char.name,
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

    def get_char_items(self, char_id):
        return self.session.query(models.Worn.realitem_id).filter_by(owner=char_id).all()

    def get_damage(self, damage):
        items = self.get_char_items(self.char.id)
        if items:
            for item in list(map(self.get_protect_by_real_item, items)):
                damage *= self.get_remains_protect(item)
        return damage

    def get_bonus_from_item(self, real_item_id):
        bonus = self.session.query(models.RealItem.item_id).filter_by(id=real_item_id).first()
        if bonus:
            bonus = self.session.query(models.Item).filter_by(id=bonus).first()
            if bonus:
                if self.char.class_name == "Воин":
                    return bonus.strength
                elif self.char.class_name == "Вор в законе":
                    return bonus.agility
                elif self.char.class_name == "Маг":
                    return bonus.smart
        return 0

    def get_bonus_from_items(self, items):
        bonus = 0
        if self.char.class_name == "Воин":
            bonus = self.char.strength
        elif self.char.class_name == "Вор в законе":
            bonus = self.char.agility
        elif self.char.class_name == "Маг":
            bonus = self.char.smart
        bonus_from_items = sum(map(self.get_bonus_from_item, items))
        if 100 - bonus >= bonus_from_items:
            return bonus_from_items
        return 0

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
            items = self.get_char_items(self.char.id)
            bonus += self.get_bonus_from_items(items)
            damage *= self.get_remains_attack(bonus)
            if items:
                for item in map(self.get_damage_by_real_item, items):
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

    async def get_char_info(self, request):
        if self.user is not None and self.char is not None:
            items = self.session.query(models.Worn.realitem_id).filter_by(owner=self.char.id).all()
            slot1 = None
            slot2 = None
            if items:
                slot1 = self.session.query(models.RealItem.item_id).filter_by(id=items[0]).first()
                if slot1:
                    slot1 = self.session.query(models.Item.name).filter_by(id=slot1).first()
                if len(items) > 1:
                    slot2 = self.session.query(models.RealItem.item_id).filter_by(id=items[1]).first()
                    if slot2:
                        slot2 = self.session.query(models.Item.name).filter_by(id=slot2).first()
            await self.response("get_char_info", {
                "char": {
                    "rank": self.char.rank,
                    "balance": self.char.balance,
                    "strength": self.char.strength,
                    "agility": self.char.agility,
                    "smart": self.char.smart,
                    "slot1": {
                        "id": items[0] if slot1 else -1,
                        "name": slot1 if slot1 else ""
                    },
                    "slot2": {
                        "id": items[1] if slot2 else -1,
                        "name": slot2 if slot2 else ""
                    },
                    "protect": self.get_damage(100) - 100,
                    "attack": self.get_attack_damage(models.Skill("test", 0, 1, self.char.class_name)) - 1
                }
            })
        else:
            await self.send_err("get_char_info", "You didn't login in account")

