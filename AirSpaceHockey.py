import pygame
from src.Menu import start_menu


def main():
    pygame.init()
    pygame.display.set_caption('Аэрокосмический хоккей')
    # При запуске игры начинаем с меню
    start_menu()


if __name__ == '__main__':
    main()
