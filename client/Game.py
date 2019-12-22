import os
import pygame
import pygame_gui
import threading
from LoginScene import LoginScene
from ServerAPI import ServerAPI
from Loader import Loader
from AppData import AppData
from Scene import Scene


class Game:
    def __init__(self):
        pygame.init()
        self.data = AppData()

        self.data.set("load_image", self.load_image)
        self.data.set("account", dict())
        self.data.set("state", {
            "account": dict(),

        })

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.data.set("screen", self.screen)

        with open("server.txt", "r") as f:
            text = f.read()

        self.loader = Loader(self.screen)
        self.data.set("loader", self.loader)

        self.api = ServerAPI(text.split(":")[0], int(text.split(":")[1]))
        self.data.set("api", self.api)

        self.ui = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()))
        self.data.set("ui", self.ui)

        self.clock = pygame.time.Clock()

        self.scene = Scene()
        self.data.set("scene", self.scene)

    @staticmethod
    def load_image(name):
        try:
            return pygame.image.load(os.path.join("data", name)).convert()
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert().convertAlpha()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.loader.draw()
        self.ui.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        self.api.connect()
        threading.Thread(target=self.api.receive_thread).start()
        threading.Thread(target=self.api.broadcast_thread).start()
        run = True
        self.scene.change("login", LoginScene)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                self.scene.scene.process_events(event)
                self.ui.process_events(event)
            self.ui.update(self.clock.tick() / 1000)
            self.draw()
        pygame.quit()
        self.api.logout()
        self.api.close()

