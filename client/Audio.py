import pygame


class Audio:
    def __init__(self, filename):
        self.name = filename
        self.volume = 0.5

    def set_volume(self, vol):
        self.volume = vol
        pygame.mixer.music.set_volume(self.volume)

    def play(self, repeat=False):
        pygame.mixer.music.load(self.name)
        pygame.mixer.music.play(1 if not repeat else -1)

    def stop(self):
        pygame.mixer.music.stop()

    def reset(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.name)
        pygame.mixer.music.play(1)
