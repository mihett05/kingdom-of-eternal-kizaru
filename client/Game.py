import os
import pygame
import pygame_gui
import threading
from client.LoginScene import LoginScene
#from client.CharsScene import CharsScene
from client.ServerAPI import ServerAPI
from client.Loader import Loader
from client.AppData import AppData
from client.SceneManager import SceneManager


class Game:
    def __init__(self):
        pygame.init()
        self.data = AppData()

        self.data["load_image"] = self.load_image
        self.data["account"] = dict()
        self.isfullscreen = 0
        if self.isfullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("Kingdom of Eternal Kizaru")
        icon = pygame.image.load('data/icon.png')
        pygame.display.set_icon(icon)
        self.sprites = pygame.sprite.Group()
        self.data.set("screen", self.screen)

        with open("server.txt", "r") as f:
            text = f.read()

        self.loader = Loader(self.screen)
        self.data["loader"] = self.loader

        self.api = ServerAPI(text.split(":")[0], int(text.split(":")[1]))
        self.data["api"] = self.api

        self.ui = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()))
        self.data["ui"] = self.ui

        self.clock = pygame.time.Clock()

        self.scene = SceneManager()
        self.data["scene"] = self.scene

    @staticmethod
    def load_image(name, colorkey=None):
        try:
            fullname = os.path.join('data', name)
            image = pygame.image.load(fullname)
            if not colorkey:
                color_key = image.get_at((0, 0))
            if colorkey != 'NO':
                image.set_colorkey(color_key)
            return image
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def draw(self):
        if self.screen is not None:
            self.screen.fill((0, 0, 0))
            if self.scene.scene is not None:
                self.scene.scene.draw()
            self.loader.draw()
            try:
                self.ui.draw_ui(self.screen)
            except BaseException:
                pass
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
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_F4:
                        run = False
                self.ui.process_events(event)
                self.scene.scene.process_events(event)
            self.draw()
            try:
                self.ui.update(self.clock.tick() / 1000)
            except BaseException:
                pass
        self.api.logout()
        self.api.close()
        pygame.quit()

