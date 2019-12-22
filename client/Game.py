import os
import pygame
import pygame_gui
import threading
from LoginScene import LoginScene
from ServerAPI import ServerAPI
from Loader import Loader
from AppData import AppData


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        with open("server.txt", "r") as f:
            text = f.read()
        self.loader = Loader(self.screen)
        self.api = ServerAPI(text.split(":")[0], int(text.split(":")[1]))
        self.ui = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()))
        self.clock = pygame.time.Clock()
        self.state = {
            "scene": "login"
        }

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
        login_scene = LoginScene(self.screen, self.state, self.ui, self.load_image, self.api, self.loader)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if self.state["scene"] == "login":
                    login_scene.process_events(event)
                self.ui.process_events(event)
            self.ui.update(self.clock.tick() / 1000)
            self.draw()
        pygame.quit()
        self.api.logout()
        self.api.close()

