import pygame
import pygame_gui
from client.Window import Window


class Inventory(Window):
    def __init__(self):
        self.quit_button = None
        self.find_battle_button = None

        self.nick_label = None
        self.class_label = None
        self.race_label = None
        self.rank_label = None
        self.balance_label = None
        self.strength_label = None
        self.agility_label = None
        self.smart_label = None
        self.user_id_label = None

        self.head_label = None
        self.body_label = None
        self.legs_label = None
        self.boots_label = None
        self.weapon_label = None

        self.protect_label = None
        self.damage_label = None

        self.select_item = None
        self.info = None
        self.status_bar = None

        super().__init__("Инвентарь")

    def init_ui(self):
        super().init_ui()
        self.data["api"].get_char_info()
        self.nick_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 60, 300, 25),
            text="Ник: " + self.data["account"]["char"]["name"],
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.class_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 100, 300, 25),
            text="Класс: " + self.data["account"]["char"]["class"],
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.rank_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 140, 300, 25),
            text="Ранг: " + str(self.data["account"]["char"]["rank"]),
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.balance_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 180, 300, 25),
            text=f"Баланс: {self.data['account']['char']['balance']} руб.",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.strength_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 240, 300, 25),
            text=f"Сила: {self.data['account']['char']['strength']}/100",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.agility_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 280, 300, 25),
            text=f"Ловкость: {self.data['account']['char']['agility']}/100",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.smart_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 320, 300, 25),
            text=f"Интеллект: {self.data['account']['char']['smart']}/100",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.head_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 60, 300, 25),
            text="Броня: ",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.body_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 100, 300, 25),
            text="Оружие: ",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.protect_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 280, 300, 25),
            text=f"Защита: {int(self.data['account']['char']['protect'])}%",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.damage_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 320, 300, 25),
            text=f"Урон: {int(self.data['account']['char']['attack'])}%",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.find_battle_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 360, 300, 25),
            text="Найти битву",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.get_container().rect.size[0] - 320, 400, 300, 25),
            text="Выйти из игры",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self
        )

        self.select_item = pygame_gui.elements.UIDropDownMenu(
            ["Меч Бомжа", "1", "2", "3"],
            "Предмет",
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self,
            relative_rect=pygame.Rect(
                self.get_container().rect.size[0] // 2 - 100,
                60,
                200,
                30
            )
        )

        self.info = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(380, 100, self.get_container().rect.size[0] - 320 - 60 - 380, 500),
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self,
            html_text=""
        )

        self.status_bar = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                5, self.get_container().rect.size[1] - 24 - 4,
                self.get_container().rect.w - 10, 24
            ),
            manager=self.data["ui"],
            container=self.get_container(),
            parent_element=self,
            text="Статус: " + self.data["account"]["status"]
        )

    def process_event(self, event: pygame.event.Event):
        super().process_event(event)
        if self.data["scene"].scene.name == "Game":
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button:
                        self.data["close"]()
                    elif event.ui_element == self.find_battle_button:
                        self.data["api"].find()
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    print(event.text)  # TO-DO

