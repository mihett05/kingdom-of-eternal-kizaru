import pygame
import os
import pygame_gui
coins = 10
all_goods = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
defend = 0
agility = 0
damage = 0
strength = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    return pygame.image.load(fullname).convert()


class Store:
    def __init__(self):
        global coins
        pygame.init()
        size = (800, 800)
        self.slowar = {0: 'Слабый амулет силы', 1: 'Амулет силы', 2: 'Могучий амулет силы',
                  3: 'Слабый амулет защиты', 4: 'Амулет защиты', 5: 'Могучий амулет защиты',
                  6: 'Слабый амулет ловкости', 7: 'Амулет ловкости', 8: 'Могучий амулет ловкости',
                  9: 'Слабый амулет урона', 10: 'Амулет урона', 11: 'Могучий амулет урона'}
        self.purchased_goods = []
        self.cost = 0
        screen = pygame.display.set_mode(size)
        running = True
        self.count0 = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0
        self.count6 = 0
        self.count7 = 0
        self.count8 = 0
        self.count9 = 0
        self.count10 = 0
        self.count11 = 0
        pygame.display.set_caption('Магазин')
        self.draw()
        self.deltinig = {0: self.lst, 1: self.st, 2: self.pst,
                         3: self.lde, 4: self.de, 5: self.pde,
                         6: self.lag, 7: self.ag, 8: self.pag,
                         9: self.lda, 10: self.da, 11: self.pda}
        clock = pygame.time.Clock()
        pygame.display.flip()
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == 'ui_button_pressed':
                        if event.ui_element == self.lst:
                            if self.count0 == 0:
                                self.purchased_goods.append(0)
                                self.lst.set_text('Выбрано')
                                self.count0 += 1
                                self.cost += 200
                            else:
                                self.lst.set_text(self.slowar[0])
                                self.count0 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 0:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 200
                            self.ned()
                        elif event.ui_element == self.lde:
                            if self.count3 == 0:
                                self.purchased_goods.append(3)
                                self.lde.set_text('Выбрано')
                                self.count3 += 1
                                self.cost += 200
                            else:
                                self.lde.set_text(self.slowar[3])
                                self.count3 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 3:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 200
                            self.ned()
                        elif event.ui_element == self.lda:
                            if self.count9 == 0:
                                self.purchased_goods.append(9)
                                self.lda.set_text('Выбрано')
                                self.count9 += 1
                                self.cost += 200
                            else:
                                self.lda.set_text(self.slowar[9])
                                self.count9 -= 1
                                z = 0
                                self.cost -= 200
                                for i in self.purchased_goods:
                                    if i == 9:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                            self.ned()
                        elif event.ui_element == self.lag:
                            if self.count6 == 0:
                                self.purchased_goods.append(6)
                                self.lag.set_text('Выбрано')
                                self.count6 += 1
                                self.cost += 200
                            else:
                                self.lag.set_text(self.slowar[6])
                                self.count6 -= 1
                                z = 0
                                self.cost -= 200
                                for i in self.purchased_goods:
                                    if i == 6:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                            self.ned()
                        elif event.ui_element == self.st:
                            if self.count1 == 0:
                                self.purchased_goods.append(1)
                                self.st.set_text('Выбрано')
                                self.count1 += 1
                                self.cost += 1000
                            else:
                                self.st.set_text(self.slowar[1])
                                self.count1 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 1:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 1000
                            self.ned()
                        elif event.ui_element == self.de:
                            if self.count4 == 0:
                                self.purchased_goods.append(4)
                                self.de.set_text('Выбрано')
                                self.count4 += 1
                                self.cost += 1000
                            else:
                                self.de.set_text(self.slowar[4])
                                self.count4 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 4:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 1000
                            self.ned()
                        elif event.ui_element == self.ag:
                            if self.count7 == 0:
                                self.purchased_goods.append(7)
                                self.ag.set_text('Выбрано')
                                self.count7 += 1
                                self.cost += 1000
                            else:
                                self.ag.set_text(self.slowar[7])
                                self.count7 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 7:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 1000
                            self.ned()
                        elif event.ui_element == self.da:
                            if self.count10 == 0:
                                self.purchased_goods.append(10)
                                self.da.set_text('Выбрано')
                                self.count10 += 1
                                self.cost += 1000
                            else:
                                self.da.set_text(self.slowar[10])
                                self.count10 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 10:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 1000
                            self.ned()
                        elif event.ui_element == self.pst:
                            if self.count2 == 0:
                                self.purchased_goods.append(2)
                                self.pst.set_text('Выбрано')
                                self.count2 += 1
                                self.cost += 10000
                            else:
                                self.pst.set_text(self.slowar[2])
                                self.count2 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 2:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 10000
                            self.ned()
                        elif event.ui_element == self.pde:
                            if self.count5 == 0:
                                self.purchased_goods.append(5)
                                self.pde.set_text('Выбрано')
                                self.count5 += 1
                                self.cost += 10000
                            else:
                                self.pde.set_text(self.slowar[5])
                                self.count5 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 5:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 10000
                            self.ned()
                        elif event.ui_element == self.pag:
                            if self.count8 == 0:
                                self.purchased_goods.append(8)
                                self.pag.set_text('Выбрано')
                                self.count8 += 1
                                self.cost += 10000
                            else:
                                self.pag.set_text(self.slowar[8])
                                self.count8 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 8:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 10000
                            self.ned()
                        elif event.ui_element == self.pda:
                            if self.count11 == 0:
                                self.purchased_goods.append(11)
                                self.pda.set_text('Выбрано')
                                self.count11 += 1
                                self.cost += 10000
                            else:
                                self.pda.set_text(self.slowar[11])
                                self.count11 -= 1
                                z = 0
                                for i in self.purchased_goods:
                                    if i == 11:
                                        break
                                    else:
                                        z += 1
                                del self.purchased_goods[z]
                                self.cost -= 10000
                            self.ned()
                        elif event.ui_element == self.basket:
                            if self.xvataet_li():
                                self.buy()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            screen.blit(self.background, (0, 0))
            self.manager.draw_ui(screen)
            pygame.display.update()

    def xvataet_li(self):
        global coins
        if coins >= self.cost:
            return True

    def buy(self):
        global coins, all_goods, damage, defend, agility, strength
        for i in self.purchased_goods:
            if i == 0:
                strength += 5
            elif i == 1:
                strength += 25
            elif i == 2:
                strength += 60
                damage += 10
            if i == 3:
                defend += 5
            elif i == 4:
                defend += 25
            elif i == 5:
                defend += 60
                agility += 10
            if i == 6:
                agility += 5
            elif i == 7:
                agility += 25
            elif i == 8:
                agility += 60
                defend += 10
            if i == 9:
                damage += 5
            elif i == 10:
                damage += 25
            elif i == 11:
                damage += 60
                strength += 10
            z = 0
            for j in all_goods:
                if i == j:
                    break
                else:
                    z += 1
            del all_goods[z]
        pygame.display.flip()
        coins -= self.cost
        self.cost = 0
        self.purchased_goods = []
        self.draw()
        self.ned()

    def ned(self):
        text = 'Требуется '
        text += str(self.cost)
        self.need.set_text(text)
        pygame.display.flip()

    def check(self):
        global all_goods, coins
        if len(all_goods) != 0:
            return True

    def draw(self):
        global coins
        size = (800, 800)
        self.fon = pygame.transform.scale(load_image('store.jpg'), size)
        self.background = pygame.Surface((800, 800))
        self.background.blit(self.fon, (0, 0))
        zagalovok = 'Магазин'
        self.fontObj = pygame.font.Font('freesansbold.ttf', 50)
        self.textSurfaceObj = self.fontObj.render(zagalovok, True, pygame.Color('white'))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (400, 25)
        self.manager = pygame_gui.UIManager((800, 800))
        self.background.blit(self.textSurfaceObj, self.textRectObj)
        pygame.display.flip()
        if self.check():
            text = 'У вас '
            text += str(coins)
            self.basket = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 600), (200, 100)),
                                                       text='Купить все',
                                                       tool_tip_text=text, manager=self.manager)
            pygame.display.flip()
            self.draw_goods()
        elif not self.check():
            text = 'Вы все купили'
            self.fontObj = pygame.font.Font('freesansbold.ttf', 75)
            self.textSurfaceObj = self.fontObj.render(text, True, pygame.Color('white'))
            self.textRectObj = self.textSurfaceObj.get_rect()
            self.textRectObj.center = (400, 400)
            self.background.blit(self.textSurfaceObj, self.textRectObj)
            pygame.display.flip()

    def draw_goods(self):
        global all_goods
        if 9 in all_goods:
            self.lda = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 80), (180, 70)),
                                                    text=self.slowar[9], tool_tip_text='цена 200, дает + 5 к урону',
                                                    manager=self.manager)
        if 3 in all_goods:
            self.lde = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 80), (180, 70)),
                                                    text=self.slowar[3], tool_tip_text='цена 200, дает + 5 к защите',
                                                    manager=self.manager)
        if 6 in all_goods:
            self.lag = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 80), (180, 70)),
                                                    text=self.slowar[6], tool_tip_text='цена 200, дает + 5 к ловкости',
                                                    manager=self.manager)
        if 0 in all_goods:
            self.lst = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 80), (180, 70)),
                                                    text=self.slowar[0], tool_tip_text='цена 200, дает + 5 к силе',
                                                    manager=self.manager)
        if 10 in all_goods:
            self.da = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 200), (180, 70)),
                                                    text=self.slowar[10], tool_tip_text='цена 1000, дает + 25 к урону',
                                                    manager=self.manager)
        if 4 in all_goods:
            self.de = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 200), (180, 70)),
                                                    text=self.slowar[4], tool_tip_text='цена 1000, дает + 25 к защите',
                                                    manager=self.manager)
        if 7 in all_goods:
            self.ag = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 200), (180, 70)),
                                                text=self.slowar[7], tool_tip_text='цена 1000, дает + 25 к ловкости',
                                                manager=self.manager)
        if 1 in all_goods:
            self.st = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 200), (180, 70)),
                                                text=self.slowar[1], tool_tip_text='цена 1000, дает + 25 к силе',
                                                manager=self.manager)
        if 11 in all_goods:
            self.pda = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 320), (180, 70)),
                                                    text=self.slowar[11],
                                                    tool_tip_text='цена 10000, дает + 60 к урону,'
                                                                                        ' + 10 к силе',
                                                manager=self.manager)
        if 5 in all_goods:
            self.pde = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 320), (180, 70)),
                                                    text=self.slowar[5], tool_tip_text='цена 10000, дает + 60 к'
                                                                                       ' защите, + 10 к ловкости',
                                                    manager=self.manager)
        if 8 in all_goods:
            self.pag = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 320), (180, 70)),
                                                    text=self.slowar[8], tool_tip_text='цена 10000, дает + 60 к'
                                                                                       ' силе, + 10 к урону',
                                                    manager=self.manager)
        if 2 in all_goods:
            self.pst = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 320), (180, 70)),
                                                    text=self.slowar[2], tool_tip_text='цена 10000, дает + 60 к'
                                                                                       ' защите, + 10 к ловкости',
                                                    manager=self.manager)

        text = 'Требуется '
        text += str(self.cost)
        self.need = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 700), (200, 50)), text=text,
                                                 manager=self.manager)
        self.need.disable()

Store()
