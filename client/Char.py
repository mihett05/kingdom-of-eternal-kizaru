import pygame
import os
import math
from client.AppData import AppData
from client.AnimatedSprite import AnimatedSprite
from client.Windows.Store import Store
from client.Windows.Inventory import Inventory
from client.MetaSingleton import MetaSingleton


class Char:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.data = AppData()
        self.default_x_speed = math.ceil(self.data["screen"].get_width() / 300)
        self.default_y_speed = math.ceil(self.data["screen"].get_height() / 200)
        scale = (
                (self.data["screen"].get_width() // 25) // 4 * 3,
                (self.data["screen"].get_height() // 14) // 4 * 3
        )
        self.sprites = {
            "up": AnimatedSprite((), self.load_image("sprites/char/up.png"), 1, 1, 128, 320, scale, "up"),
            "left": AnimatedSprite((), self.load_image("sprites/char/left.png"), 3, 1, 128, 320, scale, "left"),
            "down": AnimatedSprite((), self.load_image("sprites/char/down.png"), 3, 1, 128, 320, scale, "down"),
            "right": AnimatedSprite((), self.load_image("sprites/char/right.png"), 3, 1, 128, 320, scale, "right"),
            "up_run": AnimatedSprite((), self.load_image("sprites/char/up_run.png"), 10, 1, 128, 320, scale,
                                     "up_run", False),
            "left_run": AnimatedSprite((), self.load_image("sprites/char/left_run.png"), 10, 1, 128, 320, scale,
                                       "left_run", False),
            "down_run": AnimatedSprite((), self.load_image("sprites/char/down_run.png"), 10, 1, 128, 320, scale,
                                       "down_run", False),
            "right_run": AnimatedSprite((), self.load_image("sprites/char/right_run.png"), 10, 1, 128, 320, scale,
                                        "right_run", False)
        }
        self.sprite = self.sprites["down"].clone(self.group)
        self.side = None
        self.can_go_next = True
        self.x = self.data["map_manager"].map.spawn_point[0] * self.data["map_manager"].map.width
        self.y = self.data["map_manager"].map.spawn_point[1] * self.data["map_manager"].map.height

    @staticmethod
    def load_image(name, scale_size=None, color_key=None):
        try:
            fullname = os.path.join('data', name)
            image = pygame.image.load(fullname)
            if not color_key:
                color_key = image.get_at((0, 0))
            if color_key != 'NO':
                image.set_colorkey(color_key)
            if scale_size is not None:
                return pygame.transform.scale(image, scale_size)
            return image
        except pygame.error:
            print("Can't load image data/{}".format(name))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def draw(self):
        if self.data["windows"].active_window is None:
            self.sprite.update()
            self.moving()
        self.group.draw(self.data["screen"])

    def moving_check_for_ability(self, new_rect: pygame.rect.RectType) -> bool:
        for sprite in self.data["map_manager"].map.blockers:
            if sprite.rect.colliderect(new_rect):
                return False
        return True

    def check_for_teleport(self):
        for sprite in self.data["map_manager"].map.teleports:
            if sprite.rect.colliderect(self.sprite.rect):
                return sprite
        return False

    def check_for_window(self):
        for sprite in self.data["map_manager"].map.windows:
            if sprite.rect.colliderect(self.sprite.rect):
                return sprite
        return False

    def update_sprite(self, name):
        if name in self.sprites:
            if self.sprite is not None:
                if not self.sprite.name == name:
                    self.group.empty()
                    self.sprite = self.sprites[name].clone(self.group)
            else:
                self.group.empty()
                self.sprite = self.sprites[name].clone(self.group)

    def moving(self):
        self.can_go_next = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.side = "up"
            if self.moving_check_for_ability(pygame.Rect(
                self.x,
                self.y - self.default_y_speed,
                self.sprite.rect.w,
                self.sprite.rect.h
            )):
                self.y -= self.default_y_speed  # Fuck pygame(говно) преобразует все значения в int
                self.can_go_next = True

        if keys[pygame.K_s]:
            self.side = "down"
            if self.moving_check_for_ability(pygame.Rect(
                    self.x,
                    self.y + self.default_y_speed,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.y += self.default_y_speed
                self.can_go_next = True

        if keys[pygame.K_a]:
            self.side = "left"
            if self.moving_check_for_ability(pygame.Rect(
                    self.x - self.default_x_speed,
                    self.y,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.x -= self.default_x_speed  # Следовательно к time привязать не получилось
                self.can_go_next = True

        if keys[pygame.K_d]:
            self.side = "right"
            if self.moving_check_for_ability(pygame.Rect(
                    self.x + self.default_x_speed,
                    self.y,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.x += self.default_x_speed
                self.can_go_next = True

        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            if keys[pygame.K_w] and keys[pygame.K_s]:
                if keys[pygame.K_a] and keys[pygame.K_d]:
                    self.update_sprite(self.side if self.side is not None else "down")
                elif keys[pygame.K_a]:
                    self.update_sprite("left_run")
                elif keys[pygame.K_d]:
                    self.update_sprite("right_run")
                else:
                    self.update_sprite(self.side if self.side is not None else "down")
            elif keys[pygame.K_a] and keys[pygame.K_d]:
                if keys[pygame.K_w]:
                    self.update_sprite("up_run")
                elif keys[pygame.K_s]:
                    self.update_sprite("down_run")
                else:
                    self.update_sprite(self.side if self.side is not None else "right")
            else:
                self.update_sprite(self.side + ("_run" if self.can_go_next else ""))
        else:
            self.update_sprite(self.side)

        teleport = self.check_for_teleport()
        if teleport:
            self.data["map_manager"].set_map(teleport.map_path)
            self.x = self.data["map_manager"].map.spawn_point[0] * self.data["map_manager"].map.width
            self.y = self.data["map_manager"].map.spawn_point[1] * self.data["map_manager"].map.height
        window = self.check_for_window()
        if window:
            self.y += self.data["map_manager"].map.height * 2
            if window.window_name == "Store":
                if MetaSingleton._instances.get(Store, None) is None:
                    self.data["windows"].create(Store)
            elif window.window_name == "Inventory":
                if MetaSingleton._instances.get(Inventory, None) is None:
                    self.data["windows"].create(Inventory)

        if self.sprite is not None:
            self.sprite.rect.x = self.x
            self.sprite.rect.y = self.y

    def process_event(self, event):
        pass
