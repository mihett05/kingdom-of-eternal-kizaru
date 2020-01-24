import os
import sys
import threading
import pygame
import pygame_gui
from client.Scenes import LoginScene
from client.ServerAPI import ServerAPI
from client.Loader import Loader
from client.AppData import AppData
from client.SceneManager import SceneManager


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.data = AppData()

        self.data["load_image"] = self.load_image
        self.data["account"] = dict()
        self.isfullscreen = False
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
        self.data["clock"] = self.clock

        self.fps = 60
        self.data["fps"] = self.fps

        self.scene = SceneManager()
        self.data["scene"] = self.scene

        self.data["close"] = self.close
        self.receive_thread = threading.Thread(target=self.api.receive_thread)
        self.broadcast_thread = threading.Thread(target=self.api.broadcast_thread)

    @staticmethod
    def load_image(name, color_key=None):
        try:
            fullname = os.path.join('data', name)
            image = pygame.image.load(fullname)
            if not color_key:
                color_key = image.get_at((0, 0))
            if color_key != 'NO':
                image.set_colorkey(color_key)
            return image
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def close(self):
        pygame.quit()
        self.api.logout()
        self.api.close()
        self.receive_thread.join()
        self.broadcast_thread.join()
        self.running = False
        sys.exit(0)

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
        self.receive_thread.start()
        self.broadcast_thread.start()
        self.scene.change("login", LoginScene)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_F4:
                        self.running = False
                self.ui.process_events(event)
                self.scene.scene.process_events(event)
            self.draw()
            self.clock.tick(self.fps)
            try:
                self.ui.update(self.clock.tick() / 1000)
            except BaseException:
                pass
        self.close()

