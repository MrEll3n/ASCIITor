import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

def main(stdscr):
    stdscr.clear()
    rectangle(stdscr, 2, 1, 5, 10)
    stdscr.refresh()
    stdscr.getch()

if __name__ == '__main__':
    wrapper(main)