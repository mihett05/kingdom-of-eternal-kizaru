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

    def action(self, conn: Connection, skill: Skill):
        player = self.player1 if conn == self.player1["conn"] else\
            self.player2 if conn == self.player2["conn"] else None
        enemy = self.player1 if player == self.player2 else self.player2
        if player is None:
            return "Not in battle"
        if (self.step == 0 and player == self.player1) or (self.step == 1 and player == self.player2):
            self.step = 0 if self.step == 1 else 1
            if player["power"] >= skill.price:
                player["power"] -= skill.price
                enemy["health"] -= enemy["conn"].get_damage(skill.damage)
                if enemy["health"] <= 0:
                    if callable(self.end_callback):
                        self.end_callback(player["conn"], enemy["conn"])
            else:
                return "Not enough power"
        else:
            return "Not your step"

