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

        self.char_name_label, self.char_hp_letters_label, self.char_hp_status_label = None, None, None
        self.opponent_name_label, self.opponent_hp_letters_label, self.opponent_hp_status_label = None, None, None
        self.first_action, self.second_action, self.third_action, self.leave_button = None, None, None, None
        self.status_label = None
        self.status_label_advanced = None

        self.name_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 32))
        self.hp_letters_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 22))
        self.opponent_name_font = pygame.font.Font('data/AtariRevue.ttf', int(self.size[0] / 26))
        self.skills = self.account["battle_skills"]
        self.opponent_name = self.account["battle_enemy"]["name"]
        self.init_ui()

        @self.api.on("result")
        @self.check
        def result(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["rank"] = data["rank"]
                self.scene_manager.change("Game", self.scene_manager.dumps["Game"])

        @self.api.on("battle")
        @self.check
        def battle(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["battle_step"] = data["step"]
                self.account["battle_char"] = {
                    **self.account["battle_char"],
                    **data["player"]
                }
                self.account["battle_enemy"] = {
                    **self.account["battle_enemy"],
                    **data["enemy"]
                }
                self.data["draw"]()

        @self.api.on("action")
        @self.check
        def action(data):
            nonlocal self
            if data["status"] == "ok":
                self.account["battle_step"] = ""
            else:
                if data["desc"] == "data":
                    self.account["battle_step"] = ""
                if data["desc"] == "Not enough power":
                    self.account["battle_status"] = "Не достаточно силы"
                elif data["desc"] == "Not your step":
                    self.account["battle_status"] = "Не ваш ход"

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

        self.opponent.image = pygame.transform.scale(self.load_image_ins("icon.png"),
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

        self.first_action = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.52 - 100, self.size[1] / 1.34, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text=self.skills[0]["name"]
        ))
        self.second_action = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.22 - 100, self.size[1] / 1.34, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text=self.skills[1]["name"]
        ))
        self.third_action = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.52 - 100, self.size[1] / 1.17, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text=self.skills[2]["name"]
        ))
        self.leave_button = self.new_element(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.size[0] / 1.22 - 100, self.size[1] / 1.17, self.size[0] / 8, self.size[1] / 15), manager=self.ui,
            text="Свалить, пока живой"
        ))

    def draw_data(self):
        self.char_name_label = self.name_font.render(self.account["char"]["name"], False, (31, 55, 41))
        self.char_hp_letters_label = self.hp_letters_font.render('HP', False, (31, 55, 41))
        self.char_hp_status_label = self.hp_letters_font.render(f"{self.account['battle_char']['health']}/100", False,
                                                                (31, 55, 41))

        self.opponent_name_label = self.opponent_name_font.render(self.opponent_name, False, (31, 55, 41))
        self.opponent_hp_letters_label = self.hp_letters_font.render('HP', False, (31, 55, 41))
        self.opponent_hp_status_label = self.hp_letters_font.render(
            f"{self.account['battle_enemy']['health']}/{self.account['battle_enemy']['max_health']}",
            False, (31, 55, 41))

        self.status_label = self.hp_letters_font.render(f"Шаг: {self.account['battle_step']}", False, (31, 55, 41))
        self.status_label_advanced = self.hp_letters_font.render(f"Статус: {self.account['battle_status']}", False,
                                                                 (31, 55, 41))

        self.screen.blit(self.char_name_label, (
            int(self.size[0]) / 6.3 - len(self.account["char"]["name"]) * int(self.size[0] / 126), int(self.size[1] / 6)))
        self.screen.blit(self.char_hp_letters_label, (int(self.size[0]) / 15.76, int(self.size[1] / 4.7)))
        self.screen.blit(self.char_hp_status_label, (int(self.size[0]) / 9.3, int(self.size[1] / 4.7)))

        self.screen.blit(self.opponent_name_label, (
            int(self.size[0]) / 1.185 - len(self.opponent_name) * int(self.size[0] / 128), int(self.size[1] / 2.2)))
        self.screen.blit(self.opponent_hp_letters_label, (int(self.size[0]) / 1.32, int(self.size[1] / 1.99)))
        self.screen.blit(self.opponent_hp_status_label, (int(self.size[0]) / 1.24, int(self.size[1] / 1.99)))

        self.screen.blit(self.status_label, (int(self.size[0]) / 10.38, int(self.size[1] / 1.25)))
        self.screen.blit(self.status_label_advanced, (int(self.size[0]) / 10.38, int(self.size[1]) / 1.20))

    def draw(self):
        self.sprites.draw(self.screen)
        self.draw_data()
        for sprite in self.sprites.spritedict.keys():
            sprite.update()

    def process_events(self, event):
        if self.scene_manager.name == "Battle":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.leave_button:
                        self.api.battle_leave()
                    elif event.ui_element == self.first_action:
                        self.api.action(self.skills[0]["id"])
                    elif event.ui_element == self.second_action:
                        self.api.action(self.skills[1]["id"])
                    elif event.ui_element == self.third_action:
                        self.api.action(self.skills[2]["id"])
