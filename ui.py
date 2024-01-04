import curses
import time

class UI:
    def __init__(self):
        self.screen = curses.initscr()
        height, width =self.screen.getmaxyx()
        self.head = curses.newwin(1, 0, 0, 0)
        self.body = curses.newwin(height - 1, width, 1, 0)
        self.height = 1
        curses.noecho()
        curses.curs_set(0)
        self.body.scrollok(True)
    def start(self, fn):
        while True:
            key = self.body.getch()
            if key == 113:
                fn()
                curses.endwin()
                curses.curs_set(1)
                break
    def echo(self, message):
        self.body.addstr(message + "\n")
        self.body.refresh()
    def change_title(self, title):
        self.head.erase()
        self.head.refresh()
        self.head.resize(1, len(title) + 1)
        self.head.addstr(0, 0, title)
        self.head.refresh()

if __name__ == '__main__':
    ui = UI()
    ui.echo("hello")
    ui.echo("world")
    ui.change_title("title")
    while True:
        ui.echo("233")
        ui.change_title(str(time.time())[:3])
        time.sleep(1)
    ui.start()
