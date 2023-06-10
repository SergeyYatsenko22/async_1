import time
import curses
import asyncio
import random
from itertools import cycle


async def rocket(canvas, start_row, start_column, frames):
    for frame in cycle(frames):
        draw_frame(canvas, start_row, start_column, frame)
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, frame, negative=True)
        continue
        draw_frame(canvas, start_row, start_column, frame)
        canvas.refresh()
        await asyncio.sleep(0)


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


async def blink(canvas, row, column, symbol="*"):
    while True:

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for delay in range(random.randint(2, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for delay in range(1, 4):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for delay in range(1, 6):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for delay in range(1, 4):
            await asyncio.sleep(0)


def draw(canvas):
    coroutine_gun = fire(canvas, 14, 30)

    while True:
        try:
            curses.curs_set(False)
            coroutine_gun.send(None)
            time.sleep(0.2)
            canvas.refresh()
        except StopIteration:
            break
    time.sleep(1)

    with open("rocket/shape_1.txt", "r") as file_1:
        frame_1 = file_1.read()

    with open("rocket/shape_2.txt", "r") as file_2:
        frame_2 = file_2.read()

    start_row = 14
    start_column = 30
    frames = (frame_1, frame_2)

    ship_coroutine = rocket(canvas, start_row, start_column, frames)

    star_field = []
    coroutines = [ship_coroutine]
    star_count = 0
    while star_count < 50:
        row_index = random.randint(1, curses.window.getmaxyx(canvas)[0] - 1)
        column_index = random.randint(1, curses.window.getmaxyx(canvas)[1] - 1)
        coords = (row_index, column_index)

        if coords not in star_field:
            star_symbol = random.choice('+*.:')
            star_field.append(coords)
            star_count += 1
            coroutines.append(
                blink(canvas=canvas,
                      row=row_index,
                      column=column_index,
                      symbol=star_symbol))
        else:
            continue

    while True:
        curses.curs_set(False)

        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break

        time.sleep(0.1)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
