import pygame
import pygame_gui
from client.Scene import Scene
from client.Interface import Interface
from client.Map import Map
from client.Char import Char
from client.AppData import AppData
from client.MapManager import MapManager


class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.data = AppData()
        self.interface = None
        self.map_manager = MapManager()
        self.char = None
        self.start()

    def start(self):
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

    def process_events(self, event):
        if self.scene_manager.name == "Game":
            self.interface.process_events(event)
            self.char.process_event(event)



