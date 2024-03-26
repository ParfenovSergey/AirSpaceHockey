from screeninfo import get_monitors
import os


class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.size = w, h


class Gate:
    def __init__(self, w, pos):
        self.left = int((0.5 - w) * FIELD.w)
        self.right = int((0.5 + w) * FIELD.w)
        self.width = 5
        self.pos = pos
        if pos == 'machine':
            self.top = 0
        elif pos == 'player':
            self.top = FIELD.h - w - 2


# FPS из config.ini или по умолчанию
if os.path.isfile('config.ini'):
    with open('config.ini', 'r') as f:
        lines = f.readlines()
        FPS = int(lines[1].split('=')[1])
        f.close()
else:
    FPS = 60

# Игровое окно займёт 80% высоты экрана. Ширина игрового поля определяется соотношением
# сторон стола для аэрохоккея
game_height = int(0.8 * get_monitors()[0].height)
game_width = 2 * game_height // 1.75
GAME = Size(game_width, game_height)

# Меню больше, чем основное игровое окно
menu_width = int(0.8 * get_monitors()[0].width)
menu_height = int(0.8 * get_monitors()[0].height)
MENU = Size(menu_width, menu_height)

# Игровое поле занимает 2/3 игрового окна
field_height = GAME.h
field_width = int(2 * GAME.w / 3)
FIELD = Size(field_width, field_height)

# Размеры шара и клюшек
BALL_SIZE = int(0.07 * FIELD.w)
STICK_SIZE = int(0.09 * FIELD.w)

# Размеры ворот
gates_width = 0.1
GATE_PLAYER = Gate(gates_width, 'player')
GATE_MACHINE = Gate(gates_width, 'machine')

# Базовые скорости для простого и сложного режима
SPEED = {'Простая': 20, 'Сложная': 30}
