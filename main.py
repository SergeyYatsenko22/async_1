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

    print(coroutine)
    print(type(coroutine))
    print(dir(coroutine))

    while True:
        try:
            coroutine.send(None)
        except StopIteration:
            break

    time.sleep(10)


async def blink(canvas, row, column, symbol='*'):
    while True:
        curses.curs_set(False)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        print("1")
        await asyncio.sleep(2)

        canvas.addstr(row, column, symbol)
        print("2")
        await asyncio.sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0.5)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)