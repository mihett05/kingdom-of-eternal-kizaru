import random
from server.models import Skill
from server.Connection import Connection


class Battle:
    def __init__(self, players: tuple, end_callback):
        if not len(players) == 2:
            raise Exception("Count of players must be 2")
        self.end_callback = end_callback
        self.player1 = {
            "conn": players[0],
            "power": 20,
            "health": 100
        }
        self.player2 = {
            "conn": players[1],
            "power": 20,
            "health": 100
        }
        self.step = random.randint(0, 1)

    async def action(self, conn: Connection, skill: Skill):
        player = self.player1 if conn == self.player1["conn"] else\
            self.player2 if conn == self.player2["conn"] else None
        enemy = self.player1 if player == self.player2 else self.player2
        if player is None:
            return "Not in battle"
        if (self.step == 0 and player == self.player1) or (self.step == 1 and player == self.player2):
            if player["power"] >= skill.price:
                self.step = 0 if self.step == 1 else 1
                player["power"] += 10
                enemy["power"] += 10
                player["power"] -= skill.price
                damage = player["conn"].get_attack_damage(skill)
                enemy["health"] -= enemy["conn"].get_damage(damage)
                if enemy["health"] <= 0:
                    if callable(self.end_callback):
                        await self.end_callback(player["conn"], enemy["conn"], self)
                else:
                    await conn.response("battle", {
                        "step": self.__getattribute__("player" + str(self.step + 1))["conn"].char.name,
                        "player": {
                            "power": player["power"],
                            "health": player["health"]
                        },
                        "enemy": {
                            "power": enemy["power"],
                            "health": enemy["health"]
                        }
                    })
                    await enemy["conn"].response("battle", {
                        "step": self.__getattribute__("player" + str(self.step + 1))["conn"].char.name,
                        "enemy": {
                            "power": player["power"],
                            "health": player["health"]
                        },
                        "player": {
                            "power": enemy["power"],
                            "health": enemy["health"]
                        }
                    })
                return "Data"

            else:
                return "Not enough power"
        else:
            return "Not your step"

    async def leave(self, conn: Connection):
        enemy = self.player1["conn"] if conn == self.player2["conn"] else self.player2["conn"]\
            if conn == self.player1["conn"] else None
        if enemy is not None:
            await self.end_callback(enemy, conn, self)
