import pygame


class Gate(pygame.sprite.Sprite):
    def __init__(self, gate, group):
        super().__init__()
        self.add(group)
        self.pos = gate.pos
        self.image = pygame.Surface((gate.right - gate.left, gate.width), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'green',
                         ((0, 0),
                          (gate.right - gate.left, gate.width)))
        self.rect = pygame.Rect(gate.left, gate.top, gate.right - gate.left, gate.width)
