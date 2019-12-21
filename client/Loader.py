import pygame


class Loader:
    def __init__(self, screen):
        self.screen = screen
        self.static = pygame.sprite.Group()
        self.animated = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()

    def add_static(self, sprite):
        self.static.add(sprite)

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def add_animated(self, sprite):
        self.animated.add(sprite)

    def draw(self):
        self.static.draw(self.screen)
        self.sprites.draw(self.screen)
        self.animated.draw(self.screen)



