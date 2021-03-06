import pygame
import pygame_gui
import os
from client.Scene import Scene
from client.Scenes import SettingsScene


class CharDeleteScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.ok_button, self.cancel_button = None, None
        self.logined_account, self.delete_label = None, None
        self.account_font = pygame.font.Font('data/AtariRevue.ttf', 26)
        self.mainfont = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 26.3))
        char_id = self.account["chosen_char_id"]
        if char_id is not None and char_id < len(self.account["chars"]):
            self.char = self.account["chars"][char_id]
            self.char_inlist_place = char_id
        self.init_ui()

        @self.api.on("delete_char")
        @self.check
        def delete_char(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["chars"] = list(map(self.api.char_data_convert, data["chars"]))
                self.account["chosen_char_id"] = None
                self.scene_manager.change("CharsScene", self.scene_manager.last)
            else:
                print("Deleting char error")

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

        self.delete_label = self.mainfont.render("Удалить персонажа {}?".format(self.char['name']), True, (0, 0, 0))

        self.ok_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 260, self.size[1] / 2, 240, 40), manager=self.ui,
            text="Подтвердить"
        ))
        self.cancel_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 + 20, self.size[1] / 2, 240, 40), manager=self.ui,
            text="Отмена"
        ))
        self.logined_account = self.account_font.render("Аккаунт: {}".format(self.account["login"]), False, (0, 0, 0))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.logined_account, (self.size[0] / 40, self.size[1] - self.size[1] / 29))
        self.screen.blit(self.delete_label, (self.size[0] / 2 - (len(self.char["name"]) + 18) * (self.size[0] / 107), self.size[1] / 2 - self.size[1] / 8))
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "CharDelete":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.cancel_button:
                        self.scene_manager.change("CharsScene", self.scene_manager.last)
                    elif event.ui_element == self.ok_button:
                        self.api.delete_char(self.char["id"])
