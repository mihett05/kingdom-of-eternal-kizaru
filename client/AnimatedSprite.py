import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, frames=None):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.frameslist = []
        self.frames = frames
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frameslist[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        frames_count = 0
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frameslist.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                frames_count += 1
                if frames_count == self.frames:
                    break
            if frames_count == self.frames:
                break

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frameslist)
        self.image = self.frameslist[self.cur_frame]
