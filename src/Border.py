import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, group):
        super().__init__(group)
        self.add(group)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if w == 0:
            self.image = pygame.Surface([1, h])
            self.rect = pygame.Rect(x, y, 1, h)
        if h == 0:
            self.image = pygame.Surface([w, 1])
            self.rect = pygame.Rect(x, y, w, 1)
