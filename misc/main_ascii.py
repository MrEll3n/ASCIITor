import curses
from curses import wrapper

stdscr = curses.initscr()

def main(srdscr):
    stdscr.clear()
    stdscr.addstr(20, 100, "Whazaap niga!")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)