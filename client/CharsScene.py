import pygame
import pygame_gui
import os
import sys
from client.Scene import Scene
from client.CharMakerScene import CharMakerScene
from client.CharDeleteScene import CharDeleteScene


class CharsScene(Scene):
    def __init__(self):
        self.bg = pygame.sprite.Sprite()
        Scene.__init__(self)
        self.sprites = pygame.sprite.Group()
        self.char_info_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 38.4))
        self.login, self.password, self.login_button, self.status = None, None, None, None

        self.first_char_is_exist = False
        self.first_char_play_button, self.first_char_delete_button, self.first_char_create_button = None, None, None
        self.first_char_name_label, self.first_char_class_label, self.first_char_rank_label,\
            self.first_char_blacklist_label, self.first_char_money_label = None, None, None, None, None
        self.first_char_name, self.first_char_class, self.first_char_money = None, None, None

        self.second_char_is_exist = False
        self.second_char_play_button, self.second_char_delete_button, self.second_char_create_button = None, None, None
        self.second_char_name_label, self.second_char_class_label, self.second_char_rank_label, \
            self.second_char_blacklist_label, self.second_char_money_label = None, None, None, None, None
        self.second_char_name, self.second_char_class, self.second_char_money = None, None, None

        self.third_char_is_exist = False
        self.third_char_play_button, self.third_char_delete_button, self.third_char_create_button = None, None, None
        self.third_char_name_label, self.third_char_class_label, self.third_char_rank_label, \
            self.third_char_blacklist_label, self.third_char_money_label = None, None, None, None, None
        self.third_char_name, self.third_char_class, self.third_char_money = None, None, None
        self.init_ui()

    def char_info_load(self, char_id):
        char, char_exist = None, None
        for i in self.account["chars"]:
            if i['id'] == char_id:
                char = i
                char_exist = True
                break
            char_exist = False
        return char, char_exist

    def load_slot_one(self):
        char, self.first_char_is_exist = self.char_info_load(0)
        if self.first_char_is_exist:
            self.first_char_name, self.first_char_class, self.first_char_money = char['name'], char['class'], char['money']
            self.first_char_name_label = self.char_info_font.render(char['name'], True, (0, 0, 0))
            self.first_char_class_label = self.char_info_font.render(char['class'], True, (0, 0, 0))
            self.first_char_rank_label = self.char_info_font.render('Ранг арены: {}'.format(char['rank']), True, (0, 0, 0))
            self.first_char_blacklist_label = self.char_info_font.render('Черный список: {}/5'.format(char['blacklist']), True, (0, 0, 0))
            self.first_char_money_label = self.char_info_font.render('{}$'.format(char['money']), True, (0, 0, 0))
            self.first_char_play_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 4.2 - 110, self.size[1] - self.size[1] / 2.5, 220, 35),
                manager=self.ui,
                text="Играть"
            ))
            self.first_char_delete_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 4.2 - 110, self.size[1] - self.size[1] / 2.9, 220, 35),
                manager=self.ui,
                text="Удалить"
            ))
        else:
            self.first_char_name = 'Пусто'
            self.first_char_name_label = self.char_info_font.render('Пусто', True, (0, 0, 0))
            self.first_char_create_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 4.2 - 110, self.size[1] / 2 - 50, 220, 60),
                manager=self.ui,
                text="Создать"
            ))

    def load_slot_two(self):
        char, self.second_char_is_exist = self.char_info_load(1)
        if self.second_char_is_exist:
            self.second_char_name, self.second_char_class, self.second_char_money = char['name'], char['class'], char['money']
            self.second_char_name_label = self.char_info_font.render(char['name'], True, (0, 0, 0))
            self.second_char_class_label = self.char_info_font.render(char['class'], True, (0, 0, 0))
            self.second_char_rank_label = self.char_info_font.render('Ранг арены: {}'.format(char['rank']), True, (0, 0, 0))
            self.second_char_blacklist_label = self.char_info_font.render('Черный список: {}/5'.format(char['blacklist']), True, (0, 0, 0))
            self.second_char_money_label = self.char_info_font.render('{}$'.format(char['money']), True, (0, 0, 0))
            self.second_char_play_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 2 - 110, self.size[1] - self.size[1] / 2.5, 220, 35),
                manager=self.ui,
                text="Играть"
            ))
            self.second_char_delete_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 2 - 110, self.size[1] - self.size[1] / 2.9, 220, 35),
                manager=self.ui,
                text="Удалить"
            ))
        else:
            self.second_char_name = 'Пусто'
            self.second_char_name_label = self.char_info_font.render('Пусто', True, (0, 0, 0))
            self.second_char_create_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 2 - 110, self.size[1] / 2 - 50, 220, 60),
                manager=self.ui,
                text="Создать"
            ))

    def load_slot_three(self):
        char, self.third_char_is_exist = self.char_info_load(2)
        if self.third_char_is_exist:
            self.third_char_name, self.third_char_class, self.third_char_money = char['name'], char['class'], char['money']
            self.third_char_name_label = self.char_info_font.render(char['name'], True, (0, 0, 0))
            self.third_char_class_label = self.char_info_font.render(char['class'], True, (0, 0, 0))
            self.third_char_rank_label = self.char_info_font.render('Ранг арены: {}'.format(char['rank']), True, (0, 0, 0))
            self.third_char_blacklist_label = self.char_info_font.render('Черный список: {}/5'.format(char['blacklist']), True, (0, 0, 0))
            self.third_char_money_label = self.char_info_font.render('{}$'.format(char['money']), True, (0, 0, 0))
            self.third_char_play_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 1.32 - 110, self.size[1] - self.size[1] / 2.5, 220, 35),
                manager=self.ui,
                text="Играть"
            ))
            self.third_char_delete_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 1.32 - 110, self.size[1] - self.size[1] / 2.9, 220, 35),
                manager=self.ui,
                text="Удалить"
            ))
        else:
            self.third_char_name = 'Пусто'
            self.third_char_name_label = self.char_info_font.render('Пусто', True, (0, 0, 0))
            self.third_char_create_button = self.new_element(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(self.size[0] / 1.32 - 110, self.size[1] / 2 - 50, 220, 60),
                manager=self.ui,
                text="Создать"
            ))

    @staticmethod
    def load_image_ins(name):
        try:
            return pygame.image.load(os.path.join('data', name))
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def init_ui(self):
        self.bg.image = pygame.transform.scale(self.load_image_ins('charlistback.jpg'), (self.size[0], self.size[1]))
        self.bg.rect = self.bg.image.get_rect()
        self.bg.rect.x = 0
        self.bg.rect.y = 0
        self.sprites.add(self.bg)

        self.status = None

        self.load_slot_one()
        self.load_slot_two()
        self.load_slot_three()
        self.quit_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 2.6, 240, 40), manager=self.ui,
            text="Выйти из игры"
        ))
        self.back_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 2 - 120, self.size[1] / 2 + self.size[1] / 3, 240, 40),
            manager=self.ui,
            text="Назад"
        ))
        self.font = pygame.font.Font('data/AtariRevue.ttf', 26)
        self.logined_account = self.font.render("Аккаунт: {}".format(self.account["login"]), False, (0, 0, 0))

    def draw(self):
        self.sprites.draw(self.screen)
        self.screen.blit(self.first_char_name_label,
                         (self.size[0] / 4.2 - len(self.first_char_name) * self.size[0] / 160,
                          self.size[1] / 2 - self.size[1] / 4.9))
        self.screen.blit(self.second_char_name_label,
                         (self.size[0] / 2 - len(self.second_char_name) * self.size[0] / 175,
                          self.size[1] / 2 - self.size[1] / 4.9))
        self.screen.blit(self.third_char_name_label,
                         (self.size[0] / 1.33 - len(self.third_char_name) * self.size[0] / 175,
                          self.size[1] / 2 - self.size[1] / 4.9))
        if self.first_char_is_exist:
            self.screen.blit(self.first_char_class_label, (self.size[0] / 4.2 - len(self.first_char_class) * self.size[0] / 160,
                                                           self.size[1] / 2 - self.size[1] / 6.5))
            self.screen.blit(self.first_char_rank_label, (self.size[0] / 6, self.size[1] / 2 - self.size[1] / 9.8))
            self.screen.blit(self.first_char_blacklist_label, (self.size[0] / 7.5, self.size[1] / 2 - self.size[1] / 20.8))
            self.screen.blit(self.first_char_money_label, (self.size[0] / 4.2 - (len(str(self.first_char_money)) + 1) * self.size[0] / 160,
                                                           self.size[1] / 2 + 5))
        if self.second_char_is_exist:
            self.screen.blit(self.second_char_class_label, (self.size[0] / 2 - len(self.second_char_class) * self.size[0] / 160,
                                                            self.size[1] / 2 - self.size[1] / 6.5))
            self.screen.blit(self.second_char_rank_label, (self.size[0] / 2 - 12 * self.size[0] / 160, self.size[1] / 2 - self.size[1] / 9.8))
            self.screen.blit(self.second_char_blacklist_label, (self.size[0] / 2 - 17 * self.size[0] / 160, self.size[1] / 2 - self.size[1] / 20.8))
            self.screen.blit(self.second_char_money_label, (self.size[0] / 2 - (len(str(self.second_char_money)) + 1) * self.size[0] / 160,
                                                            self.size[1] / 2 + 5))
        if self.third_char_is_exist:
            self.screen.blit(self.third_char_class_label, (self.size[0] / 1.32 - len(self.third_char_class) * self.size[0] / 160,
                                                            self.size[1] / 2 - self.size[1] / 6.5))
            self.screen.blit(self.third_char_rank_label, (self.size[0] / 1.32 - 12 * self.size[0] / 160, self.size[1] / 2 - self.size[1] / 9.8))
            self.screen.blit(self.third_char_blacklist_label, (self.size[0] / 1.32 - 17 * self.size[0] / 160, self.size[1] / 2 - self.size[1] / 20.8))
            self.screen.blit(self.third_char_money_label, (self.size[0] / 1.32 - (len(str(self.third_char_money)) + 1) * self.size[0] / 160,
                                                            self.size[1] / 2 + 5))
        self.screen.blit(self.logined_account, (self.size[0] / 40, self.size[1] - self.size[1] / 29))
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "CharsScene":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        pygame.quit()
                        sys.exit(0)
                    elif event.ui_element == self.back_button:
                        self.scene_manager.change("MainMenu", self.scene_manager.dumps["MainMenu"])
                    elif event.ui_element == self.first_char_delete_button:
                        self.account["chosen_char_id"] = 0
                        self.scene_manager.change("CharDelete", CharDeleteScene)
                    elif event.ui_element == self.second_char_delete_button:
                        self.account["chosen_char_id"] = 1
                        self.scene_manager.change("CharDelete", CharDeleteScene)
                    elif event.ui_element == self.third_char_delete_button:
                        self.account["chosen_char_id"] = 2
                        self.scene_manager.change("CharDelete", CharDeleteScene)
                    elif event.ui_element == self.first_char_create_button:
                        self.account["chosen_char_id"] = 0
                        self.scene_manager.change("CharMaker", CharMakerScene)
                    elif event.ui_element == self.second_char_create_button:
                        self.account["chosen_char_id"] = 1
                        self.scene_manager.change("CharMaker", CharMakerScene)
                    elif event.ui_element == self.third_char_create_button:
                        self.account["chosen_char_id"] = 2
                        self.scene_manager.change("CharMaker", CharMakerScene)
