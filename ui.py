import curses
from time import sleep
from threading import Thread

class UI:
    def __init__(self):
        self.screen = curses.initscr()
        height, width =self.screen.getmaxyx()
        self.head = curses.newwin(1, width, 0, 0)
        self.come = curses.newwin(1, width, 1, 0)
        self.gift = curses.newwin(1, width, 2, 0)
        self.body = curses.newwin(height - 3, width, 3, 0)
        self.height, self.width = height, width
        curses.noecho()
        curses.curs_set(0)
        self.body.scrollok(True)
        self.gift.scrollok(True)
        self.come.scrollok(True)
        self.resize_listen = Thread(target=self.resize)
        self.alive = True
    def start(self, fn):
        self.resize_listen.start()
        while self.alive:
            key = self.body.getch()
            if key == 113:
                self.alive = False
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
        while self.alive:
            height, width =self.screen.getmaxyx()
            if height != self.height or width != self.width:
                self.head.resize(1, width)
                self.body.resize(height - 3, width)
                self.gift.resize(1, width)
                self.come.resize(1, width)
                self.height, self.width = height, width
            sleep(1)
        pass

if __name__ == '__main__':
    ui = UI()
    ui.echo("hello")
    ui.echo("world")
    ui.change_title("title")
    ui.send_gift("aslkjf")
    ui.come_in("233")
    ui.start(lambda :None)
