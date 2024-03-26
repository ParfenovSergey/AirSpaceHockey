import pygame
import os
import random
import math
import sqlite3
import datetime as dt

from src.Const import GAME, FIELD, MENU, FPS, SPEED, GATE_PLAYER, GATE_MACHINE
from src.Ball import Ball, BallData
from src.Border import Border
from src.Sticks import PlayerStick, MachineStick, StickData
from src.Gate import Gate


def start_game(difficulty: int):
    game_time = 0
    results = {'player': 0,
               'machine': 0}

    player = StickData(FIELD.w // 2, int(0.9 * FIELD.h))
    machine = StickData(FIELD.w // 2, int(0.1 * FIELD.h))

    ball = BallData()

    base_speed = SPEED['Простая'] if difficulty == 0 else SPEED['Сложная']

    screen = pygame.display.set_mode((GAME.w, GAME.h))

    set_game_sound()

    draw_game_field(screen)
    draw_sprites(screen, difficulty, player, machine, ball)
    pygame.display.flip()

    # Три секунды на подготовку
    start_count(screen, 3)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if ((event.pos[0] - FIELD.w // 2) ** 2
                        + (event.pos[1] - FIELD.h) ** 2 <=
                        (0.3 * FIELD.w) ** 2):
                    player.x = event.pos[0]
                    player.y = event.pos[1]
                    player.v_x = event.rel[0]
                    player.v_y = event.rel[1]

        if ball.x > machine.x:
            machine.v_x = random.randint(0, base_speed)
        else:
            machine.v_x = -random.randint(0, base_speed)
        machine.x += machine.v_x
        machine.v_y = random.randint(-base_speed, base_speed)
        machine.y += machine.v_y
        if machine.x < 0:
            machine.x = 0
        if machine.x > FIELD.w:
            machine.x = FIELD.w
        if machine.y < 0:
            machine.y = 0
        if machine.y > FIELD.h // 3:
            machine.y = FIELD.h // 3

        ball.x += base_speed * ball.v_x // FPS
        ball.y += base_speed * ball.v_y // FPS

        if ball.x < 0:
            ball.x = int(0.05 * FIELD.w)
            ball.v_x = base_speed
        if ball.x > FIELD.w:
            ball.x = int(0.95 * FIELD.w)
            ball.v_x = -base_speed
        if ball.y < 0:
            ball.y = int(0.05 * FIELD.h)
            ball.v_y = base_speed
        if ball.y > FIELD.h:
            ball.y = int(0.95 * FIELD.h)
            ball.v_y = -base_speed

        draw_game_field(screen)
        winner = draw_sprites(screen, difficulty, player, machine, ball)

        if winner:
            if os.path.isfile('data/audio/game_goal.mp3'):
                pygame.mixer.Sound('data/audio/game_goal.mp3').play()
            player.x, player.y = FIELD.w // 2, int(0.9 * FIELD.h)
            machine.x, machine.y = FIELD.w // 2, int(0.1 * FIELD.h)
            ball.x = FIELD.w // 2
            ball.v_x = 0
            ball.v_y = 0
            if winner == 'machine':
                results['player'] += 1
                ball.y = 1 * FIELD.h // 6
            else:
                results['machine'] += 1
                ball.y = 5 * FIELD.h // 6

        draw_game_info(screen, difficulty, results, game_time)

        game_time += clock.get_time() / 1000

        clock.tick(FPS)
        pygame.display.flip()

        if 7 in results.values():
            if results['player'] == 7:
                if os.path.isfile('data/audio/game_win.mp3'):
                    pygame.mixer.Sound('data/audio/game_win.mp3').play()
            if results['machine'] == 7:
                if os.path.isfile('data/audio/game_lose.mp3'):
                    pygame.mixer.Sound('data/audio/game_lose.mp3').play()
            running = False

            if os.path.isfile('history.sqlite'):
                con = sqlite3.connect('history.sqlite')
                cur = con.cursor()
                insert = """INSERT INTO main_history 
                                (date, game_duration, result, difficulty)
                                VALUES
                                (?, ?, ?, ?)
                             """
                insert_tuple = (dt.datetime.now().strftime('%d.%m.%Y %H:%M'), round(game_time, 1),
                                f'{results["player"]}:{results["machine"]}', difficulty + 1)
                cur.execute(insert, insert_tuple)
                con.commit()
                con.close()

    pygame.display.set_mode((MENU.w, MENU.h))


# Подготовка звука основной игры
def set_game_sound():
    if os.path.isfile('config.ini'):
        with open('config.ini', 'r') as config_file:
            sound = config_file.readlines()[0].split('=')[1].rstrip() == 'ON'
            config_file.close()

    audio_path = 'data/audio/game_music.mp3'
    if os.path.isfile(audio_path):
        pygame.mixer.music.load(audio_path)
        if sound:
            pygame.mixer.music.play(-1, 0.0, 7000)


def start_count(screen: pygame.display,
                n: int):

    font_path = 'data/font.ttf'
    if not os.path.isfile(font_path):
        font_path = None
    font_size = int(0.1 * GAME.h)
    font = pygame.font.Font(font_path, font_size)
    for i in range(n, 0, -1):
        pygame.draw.rect(screen,
                         'black',
                         ((FIELD.w + 1, 0),
                          (GAME.w - FIELD.w, GAME.h)))
        color = pygame.color.Color('red') if i != 1 else pygame.color.Color('green')
        count = font.render(str(i), True, color)
        count_rect = count.get_rect()
        count_rect.top = int(0.5 * GAME.h)
        count_rect.right = int(0.85 * GAME.w)
        screen.blit(count, count_rect)
        pygame.display.flip()
        pygame.time.wait(1000)


# Рендер в левой части игры игрового поля
def draw_game_field(screen: pygame.display):

    background_path = 'data/img/game_background.jpg'
    if os.path.isfile(background_path):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, FIELD.size)
        screen.blit(background, (0, 0))
    else:
        screen.fill('black')

    pygame.draw.line(screen, 'white', (FIELD.w, 0), FIELD.size)
    pygame.draw.line(screen, 'white', (0, FIELD.h // 2), (FIELD.w, FIELD.h // 2))

    arc_part = 0.6
    pygame.draw.arc(screen, 'white',
                    (int((1 - arc_part) * FIELD.w / 2),
                     -int(arc_part * FIELD.w / 2),
                     int(arc_part * FIELD.w),
                     int(arc_part * FIELD.w)),
                    math.pi, 0)
    pygame.draw.arc(screen, 'white',
                    (int((1 - arc_part) * FIELD.w / 2),
                     int(FIELD.h - arc_part * FIELD.w / 2),
                     int(arc_part * FIELD.w),
                     int(arc_part * FIELD.w)),
                    0, math.pi)


# Рендер спрайтов поверх поля
def draw_sprites(screen: pygame.display,
                 difficulty: int,
                 player: StickData,
                 machine: StickData,
                 ball: BallData):

    sticks = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()
    gates = pygame.sprite.Group()

    player_stick = PlayerStick(player, sticks)
    machine_stick = MachineStick(machine, difficulty, sticks)

    ball_sprite = Ball(ball, ball_group)

    borders = pygame.sprite.Group()
    Border(0, 0, 0, FIELD.h, borders)
    Border(0, 0, FIELD.w, 0, borders)
    Border(0, FIELD.h, FIELD.w, 0, borders)
    Border(FIELD.w, 0, 0, FIELD.h, borders)

    player_gate = Gate(GATE_PLAYER, gates)
    machine_gate = Gate(GATE_MACHINE, gates)

    borders.draw(screen)
    sticks.draw(screen)
    ball_group.draw(screen)
    gates.draw(screen)
    ball_sprite.update(ball, borders)
    ball_sprite.update(ball, sticks)
    winner = ball_sprite.update(ball, gates)
    return winner


# Рендер в правой части игры текущей информации
def draw_game_info(screen: pygame.display,
                   difficulty: int,
                   results: dict,
                   time: float):
    white = pygame.Color('white')
    red = pygame.Color('red')
    green = pygame.Color('green')

    fps_color = green if FPS >= 60 else red
    difficulty_color = green if difficulty == 0 else red
    results_color = green if results['player'] >= results['machine'] else red

    font_path = 'data/font.ttf'
    if not os.path.isfile(font_path):
        font_path = None
    font_size = int(0.03 * GAME.h)
    font = pygame.font.Font(font_path, font_size)

    pygame.draw.rect(screen,
                     'black',
                     (FIELD.w + 1, 0, GAME.w - FIELD.w, GAME.h))

    fps_rendered = font.render(str(FPS), True, fps_color)
    fps_rect = fps_rendered.get_rect()
    fps_rect.top = int(0.02 * GAME.h)
    fps_rect.right = int(0.98 * GAME.w)
    screen.blit(fps_rendered, fps_rect)

    text = (('Сложность:', white),
            ('Сложная' if difficulty else 'Простая', difficulty_color),
            ('Счёт:', white),
            (f'{results["player"]} : {results["machine"]}', results_color),
            ('Время:', white),
            (f'{time:.1f}', white))

    position = int(0.3 * GAME.h)
    for line, color in text:
        text_rendered = font.render(line.capitalize(), True, color)
        text_rect = text_rendered.get_rect()
        text_rect.top = position
        text_rect.x = int(0.7 * GAME.w)
        screen.blit(text_rendered, text_rect)
        position += int(0.08 * GAME.h)
