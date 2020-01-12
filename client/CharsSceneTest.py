import pygame
import pygame_gui
from client.Scene import Scene


class CharsScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.chars = None
        self.enter_button = None
        self.init_ui()

    def init_ui(self):
        if len(self.account["chars"]) > 0:
            chars_names = list(map(lambda x: x[1], self.account["chars"]))
            self.chars = self.new_element(pygame_gui.elements.UIDropDownMenu(
                chars_names,
                chars_names[0],
                manager=self.ui,
                relative_rect=pygame.rect.Rect(self.size[0] - 350, 50, 300, 100)
            ))
            self.enter_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 + 120, 200, 30), manager=self.ui,
                text="Войти"
            ))
        else:
            pass  # Открытие создания перса

    def process_events(self, event):
        if self.scene_manager.name == "chars":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.enter_button:
                        print(1)