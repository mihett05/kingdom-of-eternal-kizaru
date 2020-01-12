import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.CharDeleteScene import CharDeleteScene
from client.SettingsScene import SettingsScene


class CharsScene(Scene):
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
        self.bg.image = pygame.transform.scale(self.load_image_ins('chargreenback.jpg'),
                                          (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None

        self.quit_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 2.6, 240, 40), manager=self.ui,
            text="Выйти из игры"
        ))
        self.char1_play_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 5.5, self.size[1] - self.size[1] / 2.5, 220, 35),
            manager=self.ui,
            text="Играть"
        ))
        self.char1_delete_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 5.5, self.size[1] - self.size[1] / 2.9, 220, 35),
            manager=self.ui,
            text="Удалить"
        ))
        self.char2_play_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 110, self.size[1] - self.size[1] / 2.5, 220, 35), manager=self.ui,
            text="Играть"
        ))
        self.char2_delete_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 110, self.size[1] - self.size[1] / 2.9, 220, 35), manager=self.ui,
            text="Удалить"
        ))
        self.char3_create_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.42, self.size[1] / 2 - 50, 220, 60),
            manager=self.ui,
            text="Создать"
        ))

    def draw(self):
        self.sprites.draw(self.screen)
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "CharsScene":
            if event.type == pygame.MOUSEMOTION:
                pass
                #self.bg.rect.x = event.pos[0] // 40 - 50
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        pygame.quit()
                        sys.exit(0)
                    elif event.ui_element == self.char1_delete_button \
                            or event.ui_element == self.char2_delete_button:
                        self.scene_manager.change("CharDelete", CharDeleteScene)
