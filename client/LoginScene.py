import pygame
import pygame_gui


class LoginScene:
    def __init__(self, screen, state, ui, load_image, api):
        self.screen = screen
        self.size = (self.screen.get_width(), self.screen.get_height())
        self.ui = ui
        self.state = state
        self.load_image = load_image
        self.api = api
        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()

        @api.on("login")
        def login(data):
            nonlocal self
            if data["status"] == "ok":
                self.state["login"] = self.login.text
                self.state["password"] = self.api.hash_password(self.password.text)
            else:
                self.status.set_text("Ошибка: Неправильный логин или пароль")

    def init_ui(self):
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
                relative_rect=pygame.Rect(self.size[0] / 2 - 50, self.size[1] / 2 - 60, 100, 20),
                manager=self.ui
            )

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.login_button:
                    self.api.login(self.login.text, self.api.hash_password(self.password.text))

    def get(self):
        return self.state

