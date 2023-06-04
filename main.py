import time
import curses
import asyncio


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


def draw(canvas):
    coroutine = blink(canvas=canvas, row=2, column=22)

    # print(coroutine)
    # print(type(coroutine))
    # print(dir(coroutine))

    while True:
        try:
            for delay in (2, 0.3, 0.5, 0.3):
                curses.curs_set(False)
                coroutine.send(None)
                time.sleep(delay)
                canvas.refresh()

        except StopIteration:
            break

    time.sleep(3)


async def blink(canvas, row, column, symbol='*'):
    # while True:

    canvas.addstr(row, column, symbol, curses.A_DIM)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol, curses.A_BOLD)
    await asyncio.sleep(0)

    canvas.addstr(row, column, symbol)
    await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)