import pygame
import os
from src.Const import FPS, MENU
from src.History import show_history
from src.Game import start_game


# Формируем меню игры
def start_menu():
    screen = pygame.display.set_mode(MENU.size)
    screen.fill('black')
    clock = pygame.time.Clock()

    # Возможные пункты меню
    menu_index = 0
    menu_options = ['Новая игра (простая)',
                    'Новая игра (сложная)',
                    'История игр',
                    'Выключить музыку',
                    'Выход']

    difficulty = None

    # Режим игры
    modes = {'menu': True,
             'game': False,
             'history': False}

    # Или читаем информацию о звуке, или по умолчанию музыка есть
    if os.path.isfile('config.ini'):
        with open('config.ini', 'r') as config_file:
            sound = config_file.readlines()[0].split('=')[1].rstrip('\n')
            sound = True if sound == 'ON' else False
            config_file.close()
    else:
        sound = True

    audio_path = 'data/audio/menu_music.mp3'
    if os.path.isfile(audio_path):
        pygame.mixer.music.load(audio_path)
        if sound:
            pygame.mixer.music.play(-1, 0.0)

    # Текст в меню меняется если музыку не надо запускать при старте
    if not sound:
        menu_options[menu_options.index('Выключить музыку')] = 'Включить музыку'

    # Основной цикл меню
    while modes['menu']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                modes['menu'] = False
            elif event.type == pygame.KEYDOWN:
                if os.path.isfile('data/audio/menu_items.mp3'):
                    pygame.mixer.Sound('data/audio/menu_items.mp3').play()

                if event.key == pygame.K_DOWN and menu_index != len(menu_options) - 1:
                    menu_index += 1
                elif event.key == pygame.K_UP and menu_index != 0:
                    menu_index -= 1
                elif event.key == pygame.K_RETURN:
                    chosen_option = menu_options[menu_index]
                    if chosen_option == 'Выход':
                        modes['menu'] = False
                    elif chosen_option == 'Выключить музыку':
                        pygame.mixer.music.stop()
                        sound = False
                        menu_options[menu_index] = 'Включить музыку'
                    elif chosen_option == 'Включить музыку':
                        pygame.mixer.music.play(-1, 0.0)
                        sound = True
                        menu_options[menu_index] = 'Выключить музыку'
                    elif chosen_option == 'История игр':
                        modes['menu'] = False
                        modes['history'] = True
                    elif 'Новая игра' in chosen_option:
                        modes['menu'] = False
                        modes['game'] = True
                        # Так как новая игра однозначно в начале пунктов меню,
                        # по индексу можно определить сложность
                        difficulty = menu_index

        with open('config.ini', 'w') as config_file:
            config_file.write('SOUND=ON' if sound else 'SOUND=OFF')
            config_file.write(f'\nFPS={FPS}')
            config_file.close()

        if modes['menu']:
            show_menu_options(screen, menu_index, menu_options)
        elif modes['history']:
            show_history()
            modes['history'] = False
            modes['menu'] = True
        elif modes['game']:
            start_game(difficulty)
            modes['game'] = False
            modes['menu'] = True

        clock.tick(FPS)
        pygame.display.flip()

    if not any(modes.values()):
        pygame.quit()


# Рендер пунктов меню
def show_menu_options(screen: pygame.display,
                      index: int,
                      options: list):
    background_path = 'data/img/menu_background.jpg'
    font_path = 'data/font.ttf'
    logo_path = 'data/img/menu_logo.png'

    if not os.path.isfile(background_path):
        screen.fill('black')
    else:
        background_image = pygame.image.load(background_path)
        background_image = pygame.transform.scale(background_image, MENU.size)
        screen.blit(background_image, (0, 0))

    if os.path.isfile(logo_path):
        logo_image = pygame.image.load(logo_path)
        logo_size = int(0.4 * MENU.h)
        logo_image = pygame.transform.scale(logo_image, (logo_size, logo_size))
        logo_pos = int(0.5 * MENU.w - 0.2 * MENU.h), int(0.15 * MENU.h)
        screen.blit(logo_image, logo_pos)

    if not os.path.isfile(font_path):
        font_path = None
    font_size = int(0.05 * MENU.h)
    font = pygame.font.Font(font_path, font_size)

    text_coord = int(0.6 * MENU.h)
    for i, option in enumerate(options):
        color = pygame.Color('green') if i == index else pygame.Color('red')
        option_rendered = font.render(option, True, color)
        option_rect = option_rendered.get_rect()
        text_coord += int(0.4 * font_size)
        option_rect.top = text_coord
        option_rect.x = int(0.2 * MENU.w)
        text_coord += option_rect.height
        screen.blit(option_rendered, option_rect)

    font_size = int(0.06 * MENU.h)
    font = pygame.font.Font(font_path, font_size)

    title_rendered = font.render('Аэрокосмический хоккей',
                                 True,
                                 pygame.Color('white'))
    title_rect = title_rendered.get_rect()
    title_rect.top = int(0.05 * MENU.h)
    title_rect.centerx = MENU.w // 2
    text_coord += title_rect.height
    screen.blit(title_rendered, title_rect)
