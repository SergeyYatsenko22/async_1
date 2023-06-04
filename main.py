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


async def draw(canvas, symbol='*'):
    while True:
        curses.curs_set(False)
        row, column = (5, 20)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(2)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0.5)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0.3)

        time.sleep(10)


if __name__ == '__main__':

    curses.update_lines_cols()
    coroutine = curses.wrapper(draw)
    print(coroutine)
    print(type(coroutine))
    print(dir(coroutine))

    while True:
        try:
            coroutine.send(None)
        except StopIteration:
            break
