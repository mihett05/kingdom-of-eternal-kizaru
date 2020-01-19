import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene


class BattleScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        self.opponent = pygame.sprite.Sprite()
        self.cover = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()

        self.status = None
        self.opponent_name = "Orc"

        self.char_name_label, self.char_hp_letters_label, self.char_hp_status_label = None, None, None
        self.opponent_name_label, self.opponent_hp_letters_label, self.opponent_hp_status_label = None, None, None
        self.first_button, self.second_button, self.third_button, self.fourth_button = None, None, None, None
        self.status_label = None

        self.name_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 32))
        self.hp_letters_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 22))
        self.opponent_name_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 26))

        char_id = self.account["chosen_char_id"]
        for i in self.account["chars"]:
            if i['id'] == char_id:
                self.char = i
                break
        self.init_ui()

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('battleback.jpg'),
                                          (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.opponent.image = pygame.transform.scale(self.load_image_ins("{}.png".format(self.opponent_name)),
                                               (int(self.size[0] / 4.8), int(self.size[1] / 1.8)))
        self.opponent.rect = self.opponent.image.get_rect()
        self.opponent.rect.x = int(self.size[0] / 1.63)
        self.opponent.rect.y = int(self.size[1] / 36)
        self.sprites.add(self.opponent)

        self.cover.image = pygame.transform.scale(self.load_image_ins("cover.png"),
                                                     (int(self.size[0] / 3.6), int(self.size[1] / 6.2)))
        self.cover.rect = self.cover.image.get_rect()
        self.cover.rect.x = int(self.size[0] / 1.4)
        self.cover.rect.y = int(self.size[1] / 2.3)
        self.sprites.add(self.cover)

        self.status = None

        self.char_name_label = self.name_font.render(self.char['name'], False, (31, 55, 41))
        self.char_hp_letters_label = self.hp_letters_font.render('HP', False, (31, 55, 41))
        self.char_hp_status_label = self.hp_letters_font.render('100/100', False, (31, 55, 41))

        self.opponent_name_label = self.opponent_name_font.render(self.opponent_name, False, (31, 55, 41))
        self.opponent_hp_letters_label = self.hp_letters_font.render('HP', False, (31, 55, 41))
        self.opponent_hp_status_label = self.hp_letters_font.render('250/250', False, (31, 55, 41))

        self.status_label = self.hp_letters_font.render('Текст', False, (31, 55, 41))

        self.first_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.52 - 100, self.size[1] / 1.34, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text="Батон I"
        ))
        self.second_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.22 - 100, self.size[1] / 1.34, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text="Батон II"
        ))
        self.third_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.52 - 100, self.size[1] / 1.17, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text="Батон III"
        ))
        self.fourth_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.22 - 100, self.size[1] / 1.17, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text="Батон IV"
        ))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.char_name_label, (int(self.size[0]) / 6.3 - len(self.char['name']) * int(self.size[0] / 126), int(self.size[1] / 6)))
        self.screen.blit(self.char_hp_letters_label, (int(self.size[0]) / 15.76, int(self.size[1] / 4.7)))
        self.screen.blit(self.char_hp_status_label, (int(self.size[0]) / 9.3, int(self.size[1] / 4.7)))

        self.screen.blit(self.opponent_name_label, (int(self.size[0]) / 1.185 - len(self.opponent_name) * int(self.size[0] / 128), int(self.size[1] / 2.2)))
        self.screen.blit(self.opponent_hp_letters_label, (int(self.size[0]) / 1.32, int(self.size[1] / 1.99)))
        self.screen.blit(self.opponent_hp_status_label, (int(self.size[0]) / 1.24, int(self.size[1] / 1.99)))

        self.screen.blit(self.status_label, (int(self.size[0]) / 10.38, int(self.size[1] / 1.25)))

        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "Battle":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    pass
                    # if event.ui_element == self.play_button:
