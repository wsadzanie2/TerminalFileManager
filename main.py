import os
import subprocess
import curses
from curses import wrapper

selected = 0

text_editor = 'nvim'

def draw_file_tree(stdscr, path=None):
    if path is None:
        path = os.getcwd()
    for index, thingy in enumerate(os.listdir(path)):
        stdscr.addstr(index + 2, 0, f'{thingy}', (curses.A_REVERSE if index == selected else curses.A_NORMAL))


def main(stdscr: curses.window):
    global selected
    stdscr.clear()
    curses.use_default_colors()
    Y, X = stdscr.getmaxyx()
    run = True
    while run:
        stdscr.addstr(0, 0, (' ' * (X // 2 - 6)) + 'FILE MANAGER' + (' ' * (X // 2 - 6)), curses.A_REVERSE)
        draw_file_tree(stdscr)
        key = stdscr.getch()
        if key in [27, ord('q')]:
            run = False
            return
        elif key in [curses.KEY_DOWN, ord('j')]:
            selected += 1
        elif key in [curses.KEY_UP, ord('k')]:
            selected -= 1
        elif key in [curses.KEY_RIGHT, ord('l')]:
            if os.path.isdir(os.listdir()[selected]):
                os.chdir(os.listdir()[selected])
            else:
                subprocess.run([text_editor, str(os.listdir()[selected])])
            stdscr.clear()
        elif key in [curses.KEY_LEFT, ord('h')]:
            os.chdir('..')
            stdscr.clear()

        selected %= len(os.listdir())


wrapper(main)
