import pygame
import pygame_gui


class LoginScene:
    def __init__(self, screen, state, ui, load_image):
        self.screen = screen
        self.size = (self.screen.get_width(), self.screen.get_height())
        self.ui = ui
        self.state = state
        self.load_image = load_image

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

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.login_button:
                    print("1")

    def get(self):
        return {
            "login": self.login.text
        }

