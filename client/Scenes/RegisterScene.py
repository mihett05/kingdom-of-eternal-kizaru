import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.Scenes.MainMenuScene import MainMenuScene


class RegisterScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.status = None, None, None
        self.register_button, self.quit_button, self.back_button = None, None, None
        self.init_ui()

        @self.api.on("register")
        @self.check
        def register(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["login"] = self.login.text
                self.account["password"] = self.password.text
                self.account["chars"] = []
                self.api.login(self.account["login"], self.account["password"])
                self.scene_manager.change("MainMenu", MainMenuScene, make_dump=True)
            else:
                self.set_result("Ошибка: Логин занят")

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('greenback4.jpg'),
                                          (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None
        self.new_element(pygame_gui.elements.UILabel(text="Логин",
                                                     relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 - 60, 100, 20),
                                                     manager=self.ui))
        self.login = self.new_element(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 - 40, 200, 30), manager=self.ui))

        self.new_element(pygame_gui.elements.UILabel(text="Пароль",
                                                     relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 + 10, 100, 20),
                                                     manager=self.ui))
        self.password = self.new_element(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 30, 200, 30), manager=self.ui))

        self.register_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 80, 200, 30), manager=self.ui,
            text="Регистрация"
        ))
        self.quit_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 2.6, 240, 40),
            manager=self.ui,
            text="Выйти из игры"
        ))
        self.back_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 3, 240, 40),
            manager=self.ui,
            text="Назад"
        ))

    def draw(self):
        self.sprites.draw(self.screen)
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def set_result(self, text):
        self.status = self.new_element(pygame_gui.elements.UILabel(
            text="",
            relative_rect=pygame.Rect(0, self.size[1] / 2 - 95, self.size[0], 20),
            manager=self.ui
        ))
        self.status.set_text(text)

    def process_events(self, event):
        if self.scene_manager.name == "Register":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.register_button:
                        if self.login.text == '' or ' ' in self.login.text:
                            self.set_result('Логин не может быть пустым или содержать пробел')
                        elif self.password.text == '' or ' ' in self.password.text:
                            self.set_result('Пароль не может быть пустым или содержать пробел')
                        else:
                            self.api.register(self.login.text, self.password.text)
                    elif event.ui_element == self.back_button:
                        self.scene_manager.change("login", self.scene_manager.last)
                    elif event.ui_element == self.quit_button:
                        self.data["close"]()
