import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.SettingsScene import SettingsScene


class CharDeleteScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.login, self.password, self.login_button, self.status = None, None, None, None
        self.init_ui()

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('deleteMOKUP.jpg'),
                                          (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None
        self.ok_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 260, self.size[1] / 2, 240, 40), manager=self.ui,
            text="Подтвердить"
        ))
        self.cancel_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 + 20, self.size[1] / 2, 240, 40), manager=self.ui,
            text="Отмена"
        ))
        self.font = pygame.font.Font('data/AtariRevue.ttf', 26)
        self.logined_account = self.font.render("Аккаунт: {}".format(self.account["login"]), False, (0, 0, 0))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.logined_account, (self.size[0] / 40, self.size[1] - self.size[1] / 29))
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "CharDelete":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.cancel_button:
                        self.scene_manager.change("CharsScene", self.scene_manager.last)
                    elif event.ui_element == self.ok_button:
                        self.scene_manager.change("CharsScene", self.scene_manager.last)