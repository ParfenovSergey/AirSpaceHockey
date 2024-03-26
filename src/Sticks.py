import pygame
import os
from src.Const import STICK_SIZE


class Stick(pygame.sprite.Sprite):
    def __init__(self, stick, group):
        super().__init__()
        self.centerx = stick.x
        self.centery = stick.y
        self.add(group)
        self.rect = pygame.Rect(stick.x - STICK_SIZE // 2,
                                stick.y - STICK_SIZE // 2,
                                STICK_SIZE,
                                STICK_SIZE)
        self.v_x = stick.v_x
        self.v_y = stick.v_y

    def update(self, group):
        if pygame.sprite.spritecollideany(self, group):
            if os.path.isfile('data/audio/game_base_strike.mp3'):
                pygame.mixer.Sound('data/audio/game_base_strike.mp3').play()


class PlayerStick(Stick):
    def __init__(self, stick, group):
        super().__init__(stick, group)
        if os.path.isfile('data/img/player_stick.png'):
            self.image = pygame.image.load('data/img/player_stick.png')
            self.image = pygame.transform.scale(self.image,
                                                (STICK_SIZE, STICK_SIZE))
        else:
            self.image = pygame.Surface((STICK_SIZE, STICK_SIZE), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image,
                               pygame.color.Color('blue'),
                               (STICK_SIZE // 2, STICK_SIZE // 2),
                               STICK_SIZE // 2)


class MachineStick(Stick):
    def __init__(self, stick, difficulty, group):
        super().__init__(stick, group)
        path = 'data/img/hard_stick.png' if difficulty else 'data/img/easy_stick.png'
        if os.path.isfile(path):
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (STICK_SIZE, STICK_SIZE))
        else:
            self.image = pygame.Surface((STICK_SIZE, STICK_SIZE), pygame.SRCALPHA, 32)
            color = 'red' if difficulty else 'green'
            pygame.draw.circle(self.image,
                               pygame.color.Color(color),
                               (STICK_SIZE // 2, STICK_SIZE // 2),
                               STICK_SIZE // 2)


class StickData:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
