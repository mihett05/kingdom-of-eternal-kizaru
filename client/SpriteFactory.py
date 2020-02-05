import pygame


class SpriteFactory:
    def __init__(self, group_list=None, image=None):
        self.groups = group_list
        self.image = image
        self.map_path = None
        self.window = None

    def set_teleport(self, map_path):
        self.map_path = map_path

    def set_window(self, window_name):
        self.window = window_name

    def create(self, x, y):
        sprite = pygame.sprite.Sprite()
        sprite.image = self.image
        sprite.rect = self.image.get_rect()
        sprite.rect.x = x
        sprite.rect.y = y
        if self.map_path is not None:
            sprite.map_path = self.map_path
        elif self.window is not None:
            sprite.window_name = self.window
        for group in self.groups:
            group.add(sprite)
        return sprite
