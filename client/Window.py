import pygame
import pygame_gui
from client.AppData import AppData
from client.MetaSingleton import MetaSingleton


class Window(pygame_gui.core.UIWindow, metaclass=MetaSingleton):
    def __init__(self, title: str):
        self.data = AppData()
        self.__title = title
        super().__init__(
            pygame.Rect(100, 100, self.data["screen"].get_width() - 200, self.data["screen"].get_height() - 200),
            self.data["ui"],
            ["store"]
        )

        self.close_button = None
        self.title_label = None
        self.init_ui()

    def init_ui(self):
        self.get_container().image = pygame.transform.scale(
            self.data["load_image"]("window.jpg", 255), self.get_container().rect.size
        )

        self.close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.get_container().rect.right - 150, 5, 45, 45),
            text="X",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(15, 15, 300, 25),
            text=self.__title,
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

    def kill(self):
        super().kill()
        MetaSingleton.remove(self.__class__)

    def process_event(self, event: pygame.event.Event):
        if self.data["scene"].scene.name == "Game":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.close_button:
                        if isinstance(self.data["windows"].active_window, self.__class__):
                            self.data["windows"].close()



