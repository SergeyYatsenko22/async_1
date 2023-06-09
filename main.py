import time
import curses
import asyncio
import random
from itertools import cycle

TIC_TIMEOUT = 0.1
BORDER_WIDTH = 1

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        canvas.nodelay(True)
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


async def rocket(canvas, row, column, frames, canvas_size=(24, 49), rocket_size=(9, 5)):
    for frame in cycle(frames):

        step = 0
        while step in range(2):
            row_direction, column_direction, pause = read_controls(canvas)
            canvas_rows, canvas_columns = canvas_size
            rocket_rows, rocket_columns = rocket_size
            new_row = row + row_direction
            new_column = column + column_direction
            if row in range(BORDER_WIDTH + 1, (canvas_rows - rocket_rows - BORDER_WIDTH)):
                row = new_row

            if column in range(BORDER_WIDTH + 1, (canvas_columns - rocket_columns - BORDER_WIDTH)):
                column = new_column
            draw_frame(canvas, row, column, frame)

            await asyncio.sleep(0)

            draw_frame(canvas, row, column, frame, negative=True)
            step += 1


def draw_frame(canvas, start_row, start_column, frame, negative=False):
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(frame.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def fire(canvas,
               start_row,
               start_column,
               rows_speed=-0.3,
               columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def get_frame_size(text):
    """Calculate size of multiline text fragment, return pair — number of rows and colums."""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


async def blink(canvas, row, column, offset_tics, symbol="*"):
    while True:
        for delay in range(offset_tics):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for delay in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for delay in range(4):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for delay in range(6):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for delay in range(4):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    gun_coroutine = fire(canvas, 14, 30)

    with open("rocket/shape_1.txt", "r") as file_1:
        frame_1 = file_1.read()

    with open("rocket/shape_2.txt", "r") as file_2:
        frame_2 = file_2.read()

    start_row = 14
    start_column = 43
    frames = (frame_1, frame_2)

    canvas_size = canvas.getmaxyx()

    rocket_size = get_frame_size(frame_1)

    ship_coroutine = rocket(canvas, start_row, start_column, frames, canvas_size, rocket_size)

    coroutines = [gun_coroutine, ship_coroutine]

    star_count = 0
    while star_count < 10:
        row_index = random.randint(1, curses.window.getmaxyx(canvas)[0] - 1)
        column_index = random.randint(1, curses.window.getmaxyx(canvas)[1] - 1)
        star_symbol = random.choice('+*.:')
        star_count += 1
        coroutines.append(
            blink(canvas=canvas,
                  row=row_index,
                  column=column_index,
                  offset_tics=random.randint(1, 10),
                  symbol=star_symbol))

    while True:
        curses.curs_set(False)

        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
