import pygame


class AudioManager:
    def __init__(self):
        self.track_num = 0
        self.track_list = []

    def add_track(self, filename):
        self.track_list.append(filename)
        pygame.mixer.music.queue(filename)

    def play(self, filename, play_next=False):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(1)
    
    def pause(self):
        pygame.mixer.music.pause()
        
    def unpause(self):
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

