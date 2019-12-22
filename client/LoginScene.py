import pygame
import pygame_gui
from AppData import AppData


class LoginScene:
    def __init__(self):
        self.data = AppData()
        self.screen = self.data.screen()
        self.size = (self.screen.get_width(), self.screen.get_height())
        self.ui = self.data.ui()
        self.load_image = self.data.load_image()
        self.api = self.data.api()
        self.loader = self.data.loader()
        self.account = self.data.state()["account"]
        self.scene = self.data.scene()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()

        @self.api.on("login")
        def login(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["login"] = self.login.text
                self.account["password"] = self.api.hash_password(self.password.text)
                print(data["data"])
            else:
                self.set_result("Ошибка: Неправильный логин или пароль")

    def init_ui(self):
        bg = pygame.sprite.Sprite()
        bg.image = pygame.transform.scale(self.load_image("bg.png"), self.size)
        bg.rect = bg.image.get_rect()
        bg.rect.x = 0
        bg.rect.y = 0
        self.loader.add_static(bg)

        self.status = None
        pygame_gui.elements.UILabel(text="Логин",
                                    relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 - 20, 100, 20),
                                    manager=self.ui)
        self.login = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2, 200, 30), manager=self.ui)

        pygame_gui.elements.UILabel(text="Пароль",
                                    relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 + 50, 100, 20),
                                    manager=self.ui)
        self.password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 70, 200, 30), manager=self.ui)

        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 120, 200, 30), manager=self.ui,
            text="Войти")

    def set_result(self, text):
        if isinstance(self.status, pygame_gui.elements.UILabel):
            self.status.set_text(text)
        else:
            self.status = pygame_gui.elements.UILabel(
                text="",
                relative_rect=pygame.Rect(0, self.size[1] / 2 - 60, 1920, 20),
                manager=self.ui
            )
            self.status.set_text(text)

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.login_button:
                    self.api.login(self.login.text, self.api.hash_password(self.password.text))

