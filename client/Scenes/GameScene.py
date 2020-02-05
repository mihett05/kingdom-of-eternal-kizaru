import pygame
import pygame_gui
from client.Scene import Scene
from client.Interface import Interface
from client.Char import Char
from client.AppData import AppData
from client.MapManager import MapManager
from client.AudioManager import AudioManager


class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.data = AppData()
        self.data["account"]["status"] = ""
        self.interface = None
        self.map_manager = MapManager()
        self.char = None
        self.audio = AudioManager()
        self.audio.add_track("data/music/iraq.mp3")

        @self.api.on("get_char_info")
        def char_info(data):
            if data["status"] == "ok":
                self.account["char"] = {
                    **self.account["char"],
                    **data["char"]
                }
            else:
                print("Network error")

        @self.api.on("find")
        @self.check
        def found(data):
            if data["status"] == "ok":
                self.account["battle_step"] = data["step"]
                self.account["battle_enemy"] = data["enemy"]
                self.account["battle_char"] = data["player"]
                self.account["battle_skills"] = data["skills"]
                self.account["battle_status"] = ""
                self.scene_manager.change("Battle", self.scene_manager.dumps["Battle"])
            elif data["desc"] == "Not enough money":
                self.account["status"] = "Не достаточно денег, чтобы начать бой (мин.: 10 руб.)"
            else:
                print("Network error")

        self.start()

    def start(self):
        self.api.get_char_info()
        self.interface = Interface()
        self.data["map_manager"] = self.map_manager
        self.map_manager.set_map("forest.zip")
        self.char = Char()

    def draw(self):
        self.map_manager.draw()
        self.char.draw()

    def clear(self):
        super().clear()
        self.interface.clear()
        self.map_manager.clear_map()

    def resume(self):
        self.interface.init_ui()

    def process_events(self, event):
        if self.scene_manager.name == "Game":
            self.interface.process_events(event)
            self.char.process_event(event)



