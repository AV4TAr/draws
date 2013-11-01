#!/usr/bin/env python
import curses
import sys
import random
import csv
import time
import math


LOGO_SOURCE = 'logo.txt'


class Draw(object):

    def __init__(self, filename):
        self.__start()
        with open(filename) as input:
            self.users = [row for row in csv.DictReader(input)]
        random.shuffle(self.users)
        self.start = 0
        self.lines = 15
        self.active_line = int(self.lines / 2)
        self.width = 59

        self.offset_x = 0
        self.offset_y = 4

        logo = open(LOGO_SOURCE)
        self.logo = logo.readlines()
        logo.close()

    def __start(self):
        screen = curses.initscr()
        screen.refresh()
        self.screen = screen
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.color = curses.color_pair(2)
        self.active_color = curses.color_pair(3)

    def __end(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def __box(self):
        maxh, maxw = self.screen.getmaxyx()

        h, w = self.lines + 2, self.width + 2
        y, x = (maxh - h) / 2 + self.offset_y, (maxw - w) / 2 + self.offset_x
        box = curses.newwin(h, w, y, x)
        box.box()
        box.refresh()
        self.box = box

    def __winner(self, name):
        maxh, maxw = self.screen.getmaxyx()

        for i in range(1, self.width - 10)[::2]:
            h, w = 3, i
            y, x = (maxh - h) / 2 + self.offset_y, (maxw - w) / 2 + self.offset_x
            box = curses.newwin(h, w, y, x)
            box.box()
            box.refresh()
            time.sleep(0.01)

        box.addstr(1, 1, name)
        box.refresh()

    def __logo(self):
        maxh, maxw = self.screen.getmaxyx()
        x = maxw / 2 - len(self.logo[0]) / 2
        for i, line in enumerate(self.logo):
            self.screen.addstr(i + 1, x, line.center(self.width, ' '))
        self.screen.refresh()

    def __print(self):
        for i in range(self.lines):
            winner_name = self.users[(self.start + i) % len(self.users)]['name']
            self.box.addstr(i + 1, 1, winner_name.center(self.width, ' '), self.active_color if self.active_line == i else self.color)
            if self.active_line == i:
                self.winner_name = winner_name
        self.box.refresh()

    def __draw(self):
        selected = len(self.users) * 5 + random.randrange(len(self.users)) - self.active_line

        total = selected

        while selected > 0:
            self.start += 1
            selected -= 1
            self.__print()

            speed = math.sqrt(selected)
            if speed > 0:
                time.sleep(1 / speed / 10)

        time.sleep(1)
        self.__winner(self.winner_name)

    def loop(self):
        self.__logo()
        self.__box()
        self.__print()
        try:
            while True:
                self.__draw()
                self.screen.getch()
        finally:
            self.__end()


if __name__ == '__main__':
    Draw(sys.argv[1]).loop()
