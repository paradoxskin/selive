import curses
import time

class UI:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.head = curses.newwin(1, 10, 0, 0)
        self.height = 1
        curses.noecho()
        curses.curs_set(0)
        self.stdscr.scrollok(True)
    def start(self):
        while True:
            key = self.stdscr.getch()
            if key == 113:
                curses.endwin()
                curses.curs_set(1)
                # send exit signal to main thread
                break
    def echo(self, message):
        self.stdscr.addstr(message + "\n")
        self.stdscr.refresh()
        #self.height += 1
    def change_title(self, title):
        #self.head.resize(1, len(title))
        self.head.addstr(title)
        self.head.refresh()

if __name__ == '__main__':
    ui = UI()
    ui.echo("hello")
    ui.echo("world")
    ui.change_title("title")
    while True:
        ui.echo("233")
        time.sleep(1)
    ui.start()
