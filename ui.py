import curses
import time

class UI:
    def __init__(self):
        self.screen = curses.initscr()
        height, width =self.screen.getmaxyx()
        self.head = curses.newwin(1, width, 0, 0)
        self.body = curses.newwin(height - 3, width, 1, 0)
        self.gift = curses.newwin(1, width, height - 2, 0)
        self.come = curses.newwin(1, width, height - 1, 0)
        self.height = height
        curses.noecho()
        curses.curs_set(0)
        self.body.scrollok(True)
        self.gift.scrollok(True)
        self.come.scrollok(True)
    def start(self, fn):
        while True:
            key = self.body.getch()
            if key == 113:
                fn()
                curses.endwin()
                curses.curs_set(1)
                break
    def change_title(self, title):
        self.head.erase()
        self.head.addstr(0, 0, title)
        self.head.refresh()
    def echo(self, message):
        self.body.addstr(message + "\n")
        self.body.refresh()
    def send_gift(self, message):
        self.gift.addstr("\n" + message)
        self.gift.refresh()
    def come_in(self, message):
        self.come.addstr("\n" + message)
        self.come.refresh()
    def resize(self):
        pass

if __name__ == '__main__':
    ui = UI()
    ui.echo("hello")
    ui.echo("world")
    ui.change_title("title")
    ui.send_gift("aslkjf")
    ui.come_in("233")
    ui.start(lambda :None)
