import sqlite3
import os
import pygame
import datetime as dt
from src.Const import MENU


# Рендер истории игр, хранимой в БД
def show_history():

    screen = pygame.display.set_mode(MENU.size)

    if os.path.isfile('history.sqlite'):
        con = sqlite3.connect('history.sqlite')
        cur = con.cursor()

        game_history = cur.execute('''SELECT * FROM main_history''').fetchall()
        con.close()

        history_dict = {}
        for elem in game_history:
            n, date, result, score, dif = elem
            date = dt.datetime.strptime(date, '%d.%m.%Y %H:%M')
            history_dict[n] = {'date': date,
                               'result': result,
                               'score': score,
                               'difficulty': 'Простая' if dif == 1 else 'Сложная'}

        left, right = 1, 5

        font_path = 'data/font.ttf'
        if not os.path.isfile(font_path):
            font_path = None
        font_size = int(0.03 * MENU.h)
        font = pygame.font.Font(font_path, font_size)

        running = True

        while running:
            screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        if left < n:
                            left += 1
                            right += 1
                    else:
                        if right > n:
                            left -= 1
                            right -= 1
            top = MENU.h // 5
            title_render = font.render('История игр', True, pygame.color.Color('white'))
            title_rect = title_render.get_rect()
            title_rect.top = MENU.h // 10
            title_rect.left = int(0.05 * MENU.w)
            screen.blit(title_render, title_rect)

            for i in range(left, right + 1):
                if i in history_dict.keys():
                    line = '  '.join((str(i),
                                     history_dict[i]['date'].strftime('%d/%m/%y %H:%M'),
                                     str(history_dict[i]['result']),
                                     str(history_dict[i]['score']),
                                     history_dict[i]['difficulty']))
                    history_rendered = font.render(line, True, pygame.color.Color('white'))
                    history_rect = history_rendered.get_rect()
                    history_rect.top = top
                    top += int(MENU.h * 0.15)
                    history_rect.left = int(0.05 * MENU.w)
                    screen.blit(history_rendered, history_rect)
            pygame.display.flip()
