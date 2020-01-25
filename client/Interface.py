import pygame
import pygame_gui
from client.AppData import AppData
from client.Windows.Inventory import Inventory


class Interface:

    def __init__(self):
        self.data = AppData()
        self.screen = self.data["screen"]
        self.ui = self.data["ui"]
        self.scene_manager = self.data["scene"]
        self.inventory_button = None
        self.elements = list()

        self.init_ui()

    def new_element(self, element):
        self.elements.append(element)
        return element

    def clear(self):
        for item in self.elements:
            item.kill()

    def init_ui(self):
        self.inventory_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.screen.get_width() - 10 - 80, 10, 80, 30),
            text="Инвентарь",
            manager=self.ui
        ))

    def process_events(self, event):
        if self.scene_manager.name == "Game":
            if event.type == pygame.USEREVENT:
                if event.ui_element == self.inventory_button:
                    if Inventory._instance is None:
                        Inventory()




