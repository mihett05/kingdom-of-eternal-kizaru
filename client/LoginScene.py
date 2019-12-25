import pygame
import pygame_gui
import os
from client.Scene import Scene
from client.AnimatedSprite import AnimatedSprite
from client.CharsScene import CharsScene


class LoginScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()
        self.init_sprites()

        @self.api.on("login")
        def login(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["login"] = self.login.text
                self.account["password"] = self.api.hash_password(self.password.text)
                self.account["chars"] = data["data"]["chars"]
                self.scene_manager.change("chars", CharsScene)
            else:
                self.set_result("Ошибка: Неправильный логин или пароль")

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert().convertAlpha()

    def init_sprites(self):
        AnimatedSprite(self.sprites, self.load_image("1_magicspell_spritesheet.png", colorkey='NO'), 9, 9,
                       self.screen.get_width() - 110, self.screen.get_height() - 110, 75)

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('parallax-demon-woods.jpg'),
                                          (self.size[0] + 50, self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None
        self.new_element(pygame_gui.elements.UILabel(text="Логин",
                                                     relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 - 20, 100, 20),
                                                     manager=self.ui))
        self.login = self.new_element(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2, 200, 30), manager=self.ui))

        self.new_element(pygame_gui.elements.UILabel(text="Пароль",
                                                     relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 + 50, 100, 20),
                                                     manager=self.ui))
        self.password = self.new_element(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 70, 200, 30), manager=self.ui))

        self.login_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 120, 200, 30), manager=self.ui,
            text="Войти"
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
                relative_rect=pygame.Rect(0, self.size[1] / 2 - 60, 1920, 20),
                manager=self.ui
            ))
            self.status.set_text(text)

    def process_events(self, event):
        if self.scene_manager.name == "login":
            if event.type == pygame.MOUSEMOTION:
                self.bg.rect.x = event.pos[0] // 40 - 50
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        self.api.login(self.login.text, self.api.hash_password(self.password.text))


