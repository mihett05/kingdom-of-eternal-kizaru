import pygame
import os
from client.AppData import AppData


class Char:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.data = AppData()
        self.sprite = pygame.sprite.Sprite(self.group)
        self.sprite.image = None
        self.set_side("left")
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = 256
        self.sprite.rect.y = 512
        self.sprite.rect.w = 48
        self.sprite.rect.h = 48
        self.default_speed = 3

    def load_sprite(self, side, color_key=None):
        try:
            image = pygame.image.load(os.path.join("data", "sprites", f"char{('_' + side) if side else ''}.png"))
            if not color_key:
                color_key = image.get_at((0, 0))
            if color_key != 'NO':
                image.set_colorkey(color_key)
            return pygame.transform.scale(image, (self.data["block"]["width"], self.data["block"]["height"]))
        except pygame.error:
            print("Can't load image data/sprites/char{}.png".format(('_' + side) if side else ''))
            return pygame.image.load(os.path.join("data", "default.png")).convert()

    def set_side(self, side: str):
        if side == "left":
            self.sprite.image = self.load_sprite("l")
        elif side == "right":
            self.sprite.image = self.load_sprite("r")
        elif side == "up":
            self.sprite.image = self.load_sprite("u")
        elif side == "down":
            self.sprite.image = self.load_sprite("")

    def draw(self):
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

    def moving(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.set_side("up")
            if self.moving_check_for_ability(pygame.Rect(
                self.sprite.rect.x,
                self.sprite.rect.y - self.default_speed,
                self.sprite.rect.w,
                self.sprite.rect.h
            )):
                self.sprite.rect.y -= self.default_speed  # Fuck pygame(говно) преобразует все значения в int
        if keys[pygame.K_a]:
            self.set_side("left")
            if self.moving_check_for_ability(pygame.Rect(
                    self.sprite.rect.x - self.default_speed,
                    self.sprite.rect.y,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.sprite.rect.x -= self.default_speed  # Следовательно к time привязать не получилось
        if keys[pygame.K_s]:
            self.set_side("down")
            if self.moving_check_for_ability(pygame.Rect(
                    self.sprite.rect.x,
                    self.sprite.rect.y + self.default_speed,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.sprite.rect.y += self.default_speed
        if keys[pygame.K_d]:
            self.set_side("right")
            if self.moving_check_for_ability(pygame.Rect(
                    self.sprite.rect.x + self.default_speed,
                    self.sprite.rect.y,
                    self.sprite.rect.w,
                    self.sprite.rect.h
            )):
                self.sprite.rect.x += self.default_speed
        teleport = self.check_for_teleport()
        if teleport:
            self.data["map_manager"].set_map(teleport.map_path)
            self.sprite.rect.x = 256
            self.sprite.rect.y = 512

    def process_event(self, event):
        pass
