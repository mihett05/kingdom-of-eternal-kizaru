import pygame
import os
import pygame_gui
coins = 10000000
inthelect = 0
lib_cost = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    return pygame.image.load(fullname).convert()


class Library():
    def __init__(self):
        global coins, inthelect, lib_cost
        pygame.init()
        size = (800, 800)
        screen = pygame.display.set_mode(size)
        running = True
        pygame.display.flip()
        pygame.display.set_caption('Библиотека')
        self.draw()
        clock = pygame.time.Clock()
        pygame.display.flip()
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == 'ui_button_pressed':
                        if event.ui_element == self.read:
                            self.reading()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            screen.blit(self.background, (0, 0))
            self.manager.draw_ui(screen)

            pygame.display.update()

    def check(self):
        global coins, inthelect, lib_cost
        if coins >= lib_cost and inthelect < 100:
            return True

    def reading(self):
        global coins, inthelect, lib_cost
        inthelect += 1
        coins -= lib_cost
        lib_cost *= 1.02
        lib_cost = int(lib_cost)
        self.draw()

    def draw(self):
        size = (800, 800)
        self.fon = pygame.transform.scale(load_image('books.jpg'), size)
        zagalovok = 'Библиотека'
        self.fontObj = pygame.font.Font('freesansbold.ttf', 50)
        self.textSurfaceObj = self.fontObj.render(zagalovok, True, pygame.Color('white'))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (400, 25)
        self.background = pygame.Surface((800, 800))
        self.background.blit(self.fon, (0, 0))
        self.background.blit(self.textSurfaceObj, self.textRectObj)
        infa = 'Ваш интелект равен '
        infa += str(inthelect)
        self.fontObj = pygame.font.Font('freesansbold.ttf', 25)
        self.textSurfaceObj = self.fontObj.render(infa, True, pygame.Color('white'))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (400, 55)
        self.background.blit(self.textSurfaceObj, self.textRectObj)
        pygame.display.flip()
        self.manager = pygame_gui.UIManager((800, 800))
        podskazka = 'Стоимость равна '
        podskazka += str(lib_cost)
        podskazka += ' , а у вас '
        podskazka += str(coins)
        if self.check():
            self.read = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 545), (200, 100)),
                                                    text='Прочитать книгу',
                                                    tool_tip_text=podskazka,
                                                    manager=self.manager)
        if not self.check():
            if coins <= lib_cost:
                text_error = 'Не хватка монет'
                self.fontObj = pygame.font.Font('freesansbold.ttf', 100)
                self.textSurfaceObj = self.fontObj.render(text_error, True, pygame.Color('white'))
                self.textRectObj = self.textSurfaceObj.get_rect()
                self.textRectObj.center = (400, 400)
                self.background.blit(self.textSurfaceObj, self.textRectObj)
                pygame.display.flip()
            elif inthelect == 100:
                text_error = 'Вы - гений'
                self.fontObj = pygame.font.Font('freesansbold.ttf', 100)
                self.textSurfaceObj = self.fontObj.render(text_error, True, pygame.Color('white'))
                self.textRectObj = self.textSurfaceObj.get_rect()
                self.textRectObj.center = (425, 660)
                self.background.blit(self.textSurfaceObj, self.textRectObj)
                pygame.display.flip()



Library()