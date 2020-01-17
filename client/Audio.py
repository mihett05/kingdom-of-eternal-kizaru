import pygame

pygame.init()


class Audio():
    def __init__(self, filename):
        self.name = filename
        self.volume = 0.5

    def set_volume(self, vol):
        self.volume = vol

    def play(self):
        pygame.mixer.music.load(self.name)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def reset(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)


