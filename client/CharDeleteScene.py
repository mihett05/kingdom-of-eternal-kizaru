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
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 2.6, 240, 40), manager=self.ui,
            text="Подтвердить"
        ))
        self.cancel_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 - self.size[1] / 7, 240, 50), manager=self.ui,
            text="Отмена"
        ))
        self.name = 'MrEluzium'
        self.font = pygame.font.Font('data/AtariRevue.ttf', 20)
        self.logined_account = self.font.render("Аккаунт: {}".format(self.name), False, (0, 0, 0))
        #self.new_element(pygame_gui.elements.  UILabel(text="Аккаунт: {}".format(self.name),
        #                                             relative_rect=pygame.Rect(self.size[0] / 40, self.size[1] - self.size[1] / 32, 85 + 8 * len(self.name), 22),
        #                                             manager=self.ui))

    def draw(self):
        self.sprites.draw(self.screen)
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "MainMenu":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        self.scene_manager.change("CharsScene", CharsScene)
                    elif event.ui_element == self.settings_button:
                        self.scene_manager.change("Settings", SettingsScene)
                    elif event.ui_element == self.quit_button:
                        pygame.quit()
                        sys.exit(0)