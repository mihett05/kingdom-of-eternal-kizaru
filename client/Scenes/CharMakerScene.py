import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene


class CharMakerScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.quit_button, self.back_button = None, None
        self.font = self.font = pygame.font.Font('data/AtariRevue.ttf', 26)
        self.logined_account, self.chosen_class = None, None
        self.status = None
        self.init_ui()

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

        self.new_element(pygame_gui.elements.UILabel(text="Имя",
                                                     relative_rect=pygame.Rect(self.size[0] / 2 - 25,
                                                                               self.size[1] / 2 - 80, 50, 20),
                                                     manager=self.ui))
        self.char_name = self.new_element(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.size[0] / 2 - 100, self.size[1] / 2 - 60, 200, 30), manager=self.ui))

        self.select_class = pygame_gui.elements.UIDropDownMenu(
            ["Маг", "Воин", "Вор в законе"],
            "Класс",
            manager=self.ui,
            relative_rect=pygame.Rect(
                self.size[0] // 2 - 100,
                self.size[1] / 2 - 20,
                200,
                30
            )
        )

        self.done_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + 60, 240, 40), manager=self.ui,
            text="Создать"
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
        self.logined_account = self.font.render("Аккаунт: {}".format(self.account["login"]), False, (0, 0, 0))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.logined_account, (self.size[0] / 40, self.size[1] - self.size[1] / 29))
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def set_result(self, text):
        self.status = self.new_element(pygame_gui.elements.UILabel(
                text="",
                relative_rect=pygame.Rect(0, self.size[1] / 2 - 115, self.size[0], 20),
                manager=self.ui
            ))
        self.status.set_text(text)

    def process_events(self, event):
        if self.scene_manager.name == "CharMaker":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    self.chosen_class = event.text
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.done_button:
                        if self.char_name.text == '':
                            self.set_result('Имя не может быть пустым')
                        elif ' ' in self.char_name.text:
                            self.set_result('Имя не может содержать пробел')
                        elif self.chosen_class is None:
                            self.set_result('Выберите класс')
                        else:
                            # Создание перса здесь. Все данные ниже.
                            self.account["chars"].append({'id': self.account["chosen_char_id"],
                                                          'name': self.char_name.text,
                                                          'class': self.chosen_class,
                                                          'rank': 0,
                                                          'blacklist': 0,
                                                          'money': 0})
                            # Далее не удалять.
                            self.account["chosen_char_id"] = None
                            self.scene_manager.change("CharsScene", self.scene_manager.last)
                    if event.ui_element == self.back_button:
                        self.scene_manager.change("CharsScene", self.scene_manager.last)
                    elif event.ui_element == self.quit_button:
                        pygame.quit()
                        sys.exit(0)
