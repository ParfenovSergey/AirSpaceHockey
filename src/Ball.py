import pygame
import os
from src.Const import BALL_SIZE, FIELD
from src.Sticks import PlayerStick, MachineStick
from src.Border import Border
from src.Gate import Gate


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball, group):
        super().__init__()
        self.centerx = ball.x
        self.centery = ball.y
        self.add(group)
        if os.path.isfile('data/img/ball.png'):
            self.image = pygame.image.load('data/img/ball.png')
            self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        else:
            self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image,
                               pygame.color.Color('yellow'),
                               (BALL_SIZE // 2, BALL_SIZE // 2),
                               BALL_SIZE // 2)
        self.rect = pygame.Rect(ball.x - BALL_SIZE // 2,
                                ball.y - BALL_SIZE // 2,
                                BALL_SIZE,
                                BALL_SIZE)
        self.v_x = ball.v_x
        self.v_y = ball.v_y

    def update(self, ball, group):
        self.rect.move_ip(self.v_x, self.v_y)
        collision = pygame.sprite.spritecollide(self, group, False)
        if collision:
            if os.path.isfile('data/audio/game_base_strike.mp3'):
                pygame.mixer.Sound('data/audio/game_base_strike.mp3').play()
            collision_object = collision[0]
            if isinstance(collision_object, PlayerStick):
                ball.v_x = collision_object.v_x - ball.v_x
                ball.v_y = collision_object.v_y - ball.v_y
            if isinstance(collision_object, MachineStick):
                ball.v_x = collision_object.v_x - ball.v_x
                ball.v_y = collision_object.v_y - ball.v_y
            if isinstance(collision_object, Border):
                if collision_object.w == 0:
                    ball.v_x = -ball.v_x
                if collision_object.h == 0:
                    ball.v_y = -ball.v_y
            if isinstance(collision_object, Gate):
                return collision_object.pos


class BallData:
    def __init__(self):
        self.x = FIELD.w // 2
        self.y = 5 * FIELD.h // 6
        self.v_x = 0
        self.v_y = 0
