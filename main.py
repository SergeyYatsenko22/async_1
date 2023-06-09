import time
import curses
import asyncio
import random


# def draw(canvas):
#     while True:
#         curses.curs_set(False)

#         row, column = (5, 20)
#         canvas.addstr(row, column, '*', curses.A_DIM)
#         canvas.refresh()
#         time.sleep(2)

#         row, column = (5, 20)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)

#         row, column = (5, 20)
#         canvas.addstr(row, column, '*', curses.A_BOLD)
#         canvas.refresh()
#         time.sleep(0.5)

#         row, column = (5, 20)
#         canvas.addstr(row, column, '*')
#         canvas.refresh()
#         time.sleep(0.3)

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
    print(curses.window.getmaxyx(canvas)[0])
    star_field = []
    coroutines = []
    star_count = 0
    while star_count < 20:
        row_index = random.randint(1, curses.window.getmaxyx(canvas)[0] - 1)
        column_index = random.randint(1, curses.window.getmaxyx(canvas)[1] - 1)
        coords = (row_index, column_index)

        if coords not in star_field:
            star_symbol = random.choice('+*.:')
            star_field.append(coords)
            star_count += 1
            coroutines.append(blink(canvas=canvas, row=row_index, column=column_index, symbol=star_symbol))
        else:
            continue

    # print (coroutines)

    # time.sleep(100)

    # print(coroutine)
    # print(type(coroutine))
    # print(dir(coroutine))

    while True:
        curses.curs_set(False)
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                time.sleep(0.01)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

