import os
import curses
from curses import wrapper
from TextEditor import TextEditor


selected = 0

def draw_file_tree(stdscr ,path = None):
    if path is None:
        path = os.getcwd()
    for index, thingy in enumerate(os.listdir(path)):
        stdscr.addstr(index + 2, 0, f'{thingy}', (curses.A_REVERSE if index == selected else curses.A_NORMAL))

def main(stdscr: curses.window):
    global selected
    text_edit = TextEditor(stdscr)
    stdscr.clear()
    Y, X = stdscr.getmaxyx()
    run = True
    while run:
        stdscr.addstr(0, 0, (' ' * (X//2 - 6)) + 'FILE MANAGER' + (' ' * (X//2 - 6)), curses.A_REVERSE)
        draw_file_tree(stdscr)
        key = stdscr.getch()
        if key == 27:
            run = False
        elif key == curses.KEY_DOWN:
            selected += 1
        elif key == curses.KEY_UP:
            selected -= 1
        elif key == curses.KEY_RIGHT:
            if os.path.isdir(os.listdir()[selected]):
                os.chdir(os.listdir()[selected])
            else:
                text_edit.run(os.listdir()[selected])
            stdscr.clear()
        elif key == curses.KEY_LEFT:
            os.chdir('..')
            stdscr.clear()

        selected %= len(os.listdir())



wrapper(main)