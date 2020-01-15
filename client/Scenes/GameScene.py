import pygame
import pygame_gui
from client.Scene import Scene
from client.Interface import Interface


class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.interface = Interface()

    def draw(self):
        pass

    def clear(self):
        super().clear()
        self.interface.clear()

    def process_events(self, event):
        if self.scene_manager.name == "Game":
            self.interface.process_events(event)



