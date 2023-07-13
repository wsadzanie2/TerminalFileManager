import curses


class TextEditor:
    def __init__(self, stdscr: curses.window):
        self.screen = stdscr
        self.cursor_pos = [0, 0]
        self.Y, self.X = stdscr.getmaxyx()
        self.screen.nodelay(True)
        self.path = None
        self.file = []

    def run(self, path):
        self.path = path
        run = True
        self.screen.clear()
        # main loop
        with open(path, 'r') as file:
            self.file = list(file)
        Y = 1
        while run:
            right = False
            # draws the text
            if self.cursor_pos[0] >= 0:
                self.screen.addstr(Y + self.cursor_pos[0], 4 + len(self.file[self.cursor_pos[0]]), ' ')
            for index, line in enumerate(self.file):
                if self.Y - 1 <= (index + Y):
                    break
                if self.cursor_pos[0] == index:
                    if line == '\n':
                        self.screen.addstr(Y + index, 5, ' ', curses.A_REVERSE)
                    else:
                        if self.cursor_pos[1] >= len(self.file[self.cursor_pos[0]]) - 1:
                            self.screen.addstr(Y + index, 5, line)
                            self.screen.addstr(Y + index, 4 + len(self.file[self.cursor_pos[0]]), ' ', curses.A_REVERSE)
                        else:
                            self.screen.addstr(Y + index, 5, line[0:self.cursor_pos[1]])
                            self.screen.addstr(Y + index, 5 + self.cursor_pos[1], line[self.cursor_pos[1]],
                                               curses.A_REVERSE)
                            self.screen.addstr(Y + index, 6 + self.cursor_pos[1], line[self.cursor_pos[1] + 1:-1])
                    if self.cursor_pos[0] >= len(line):
                        self.screen.addstr(Y + index, self.cursor_pos[1] + 5, ' ', curses.A_REVERSE)
                else:
                    self.screen.addstr(Y + index, 5, line)

            self.screen.addstr(1, self.X // 2, 'TEXT EDITOR', curses.A_REVERSE)
            self.screen.addstr(0, self.X - 8, str(self.cursor_pos))
            self.screen.addstr(1, self.X - 8, str(len(self.file[self.cursor_pos[0]])))
            self.screen.addstr(2, self.X - 8, str(right))
            # getting keys
            try:
                key = self.screen.getch()
            except curses.error:
                key = None

            # checking keys
            if key == 27:  # if pressed ESCAPE
                run = False
            elif key == curses.KEY_RIGHT:
                right = True
                self.cursor_pos[1] += 1
            elif key == curses.KEY_LEFT:
                self.cursor_pos[1] -= 1
            elif key == curses.KEY_DOWN:
                self.cursor_pos[0] += 1
            elif key == curses.KEY_UP:
                self.cursor_pos[0] -= 1
            elif key == curses.KEY_BACKSPACE:
                if self.cursor_pos[1] == 0:
                    impstr = self.file[self.cursor_pos[0]]
                    self.file.pop(self.cursor_pos[0])
                    self.file[self.cursor_pos[0] - 1] = self.file[self.cursor_pos[0] - 1][:-1]
                    self.file[self.cursor_pos[0] - 1] += impstr
                    self.cursor_pos[0] -= 1
                elif self.cursor_pos[0] > 0:
                    impstr = self.file[self.cursor_pos[0]]
                    self.file[self.cursor_pos[0]] = impstr[:self.cursor_pos[1] - 1] + impstr[self.cursor_pos[1]:]
                    self.cursor_pos[1] -= 1
                self.screen.clear()
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                self.cursor_pos[0] += 1
                self.file.insert(self.cursor_pos[0] - 1, '\n')
                self.cursor_pos[1] = 0
                self.screen.clear()

            # does things if the cursor is on the edge of the line (makes arrows work correctly)
            self.cursor_pos[0] %= len(self.file)
            if self.cursor_pos[1] >= len(self.file[self.cursor_pos[0]]):
                self.cursor_pos[1] = 0
                if right:
                    self.cursor_pos[0] += 1

            if self.cursor_pos[1] < 0:
                self.cursor_pos[0] -= 1
                self.cursor_pos[1] = len(self.file[self.cursor_pos[0]]) - 1

            # decodes the key for the editor ;)
            try:
                char = curses.keyname(key).decode('utf-8')
            except ValueError:
                continue
                # checks if the char is printable, and adds it to the file
            if len(char) == 1 and char.isprintable():
                self.screen.addstr(20, 20, char)
                impstr = self.file[self.cursor_pos[0]]
                self.file[self.cursor_pos[0]] = impstr[:self.cursor_pos[1]] + char + impstr[self.cursor_pos[1]:]
                self.cursor_pos[1] += 1
