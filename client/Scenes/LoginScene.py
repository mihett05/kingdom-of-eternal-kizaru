import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.Scenes.RegisterScene import RegisterScene
from client.Scenes.MainMenuScene import MainMenuScene


class LoginScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()

        @self.api.on("login")
        def login(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["login"] = self.login.text
                self.account["password"] = self.api.hash_password(self.password.text)
                self.account["chars"] = data["data"]["chars"]
                self.scene_manager.change("MainMenu", MainMenuScene)
            else:
                self.set_result("Ошибка: Неправильный логин или пароль")

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

        self.login_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 80, 200, 30), manager=self.ui,
            text="Войти"
        ))
        self.register_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 3, 240, 40),
            manager=self.ui,
            text="Регистрация"
        ))
        self.quit_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 2.6, 240, 40), manager=self.ui,
            text="Выйти из игры"
        ))

    def draw(self):
        self.sprites.draw(self.screen)
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def set_result(self, text):
        if isinstance(self.status, pygame_gui.elements.UILabel):
            self.status.set_text(text)
        else:
            self.status = self.new_element(pygame_gui.elements.UILabel(
                text="",
                relative_rect=pygame.Rect(0, self.size[1] / 2 - 95, 1920, 20),
                manager=self.ui
            ))
            self.status.set_text(text)

    def process_events(self, event):
        if self.scene_manager.name == "login":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        #self.api.login(self.login.text, self.api.hash_password(self.password.text))
                        self.account["login"] = 'MrEluzium'
                        self.account["password"] = self.api.hash_password(self.password.text)
                        self.account["chars"] = [{'id': 1, 'name': '0', 'class': '0',
                                                  'rank': 0,  'blacklist': 0, 'money':  0},
                                                 {'id': 2, 'name': '0', 'class': '0',
                                                  'rank': 0,  'blacklist': 0, 'money':  0}]
                        backup = [{'id': 0, 'name': 'Кабанчик Рома', 'class': 'Вор в законе',
                                                  'rank': 3, 'blacklist': 3, 'money': 100},
                                                 {'id': 1, 'name': 'Михетт', 'class': 'Росгвардеец',
                                                  'rank': 8, 'blacklist': 5, 'money': 750},
                                                 {'id': 2, 'name': 'Михетт', 'class': 'Росгвардеец',
                                                  'rank': 8, 'blacklist': 5, 'money': 750}]
                        print(self.account)
                        self.scene_manager.change("MainMenu", MainMenuScene, make_dump=True)
                    elif event.ui_element == self.register_button:
                        self.scene_manager.change("Register", RegisterScene)
                    elif event.ui_element == self.quit_button:
                        self.data["close"]()
