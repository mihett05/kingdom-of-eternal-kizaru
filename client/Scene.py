import pygame
import pygame_gui
from client.AppData import AppData


class Scene:
    def __init__(self):
        self.data = AppData()
        self.screen = self.data["screen"]
        self.size = (self.screen.get_width(), self.screen.get_height())
        self.ui = self.data["ui"]
        self.load_image = self.data["load_image"]
        self.api = self.data["api"]
        self.loader = self.data["loader"]
        self.account = self.data["account"]
        self.scene_manager = self.data["scene"]
        self.elements = list()

    def new_element(self, element):
        self.elements.append(element)
        return element

    def draw(self):
        pass

    def clear(self):
        for elem in self.elements:
            if elem.__getattribute__("kill"):
                elem.kill()

    def process_events(self, event):
        pass




