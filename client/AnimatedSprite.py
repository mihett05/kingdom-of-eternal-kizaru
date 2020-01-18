import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, x, y, scale=None, name=None, is_slow=True, frames=None):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.name = name
        self.frameslist = []
        self.scale = scale
        self.frames = frames
        self.sheet = sheet
        self.cols = columns
        self.rows = rows
        self.x, self.y = x, y
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frameslist[self.cur_frame]
        self.count = 0
        self.need_count = 20 if is_slow else 5
        self.rect = self.rect.move(x, y)
        if scale is not None:
            self.rect.w = scale[0]
            self.rect.h = scale[1]

    def cut_sheet(self, sheet, columns, rows):
        frames_count = 0
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if self.scale is not None:
                    self.frameslist.append(
                        pygame.transform.scale(
                            sheet.subsurface(
                                pygame.Rect(frame_location, self.rect.size)
                            ),
                            self.scale
                        )
                    )
                else:
                    self.frameslist.append(
                        sheet.subsurface(
                            pygame.Rect(frame_location, self.rect.size)
                        )
                    )
                frames_count += 1
                if frames_count == self.frames:
                    break
            if frames_count == self.frames:
                break

    def update(self):
        self.count += 1
        if self.count == self.need_count:
            self.cur_frame = (self.cur_frame + 1) % len(self.frameslist)
            self.image = self.frameslist[self.cur_frame]
            self.count = 0

    def clone(self, group):
        return AnimatedSprite(
            group, self.sheet, self.cols, self.rows,
            self.x, self.y, self.scale, self.name, self.need_count == 20)

