import math
import curses
import logging
from curses.textpad import Textbox, rectangle


logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

class Button:
    def __init__(self, win, ul_y, ul_x, lr_y, lr_x, text):
        self.win = win
        self.ul_y = ul_y
        self.ul_x = ul_x
        self.lr_y = lr_y
        self.lr_x = lr_x
        self.text = text
        self.highlight = 0

        rectangle(self.win, self.ul_y, self.ul_x, self.lr_y, self.lr_x)
        self.win.addstr(25, 101, text)


class Window:
    def __init__(self, win_type, y, x, height, width, name, p=None):
        self.win_type = win_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        # creating and filling NUMBER constant for selector
        self.ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        if self.win_type == "stats" and p:
            self.stamina = p.stamina
            self.maxstamina = p.maxstamina
            self.player_lvl = p.player_lvl
            self.strength = p.strength
            self.intelligence = p.intelligence
            self.dexterity = p.dexterity
            self.defense = p.defense

        if self.win_type == "info":
            self.info_array = []
            self.buffer = []

        if self.win_type == "inv":
            self.highlight = 1
            self.quantity_index = 1
            self.max_quantity = 1
            self.min_quantity = 1

        if self.win_type == "menu":
            self.enable_border = False

        if self.win_type == "menu_stats":
            pass

        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.max_y_x = self.win.getmaxyx()

        self.clear_window()

    def updateWindow(self):
        pass

    def delete(self):
        self.win.erase()
        del self

    def addText(self, y, x, text):
        self.win.addstr(y, x, text)

    def update_stats(self, p):
        self.stamina = p.stamina
        self.maxstamina = p.maxstamina
        # self.maxmana = p.maxmana
        self.strength = p.strength
        self.intelligence = p.intelligence
        self.dexterity = p.dexterity
        self.defense = p.defense

    def clear_window(self):
        self.win.erase()
        # self.win.border()
        if self.win_type == "info":
            self.win.border(0, 0, 0, 0, 0, 9516, 0, 0)
        elif self.win_type == "stats":
            self.win.border(0, 0, 0, 0, 0, 0, 9524, 0)
        elif self.win_type == "menu":
            self.win.border(0, 0, 0, 0, 0, 0, 0, 0)
        else:
            self.win.border()

        if self.name != "":
            self.win.addstr(0, 3, f" {self.name} ")
        self.win.refresh()

    # def create_window(self):
    #    self.win = curses.newwin(self.height, self.width, self.y, self.x)
    #    self.clear_window()

    def draw_border(self):
        self.win.erase()
        self.win.border()
        self.win.refresh()

    def print_stats(self, p):
        # self.win.clear()
        self.clear_window()
        self.update_stats(p)
        self.win.addstr(2, 2, f"{p.name} [{self.player_lvl}]")
        self.win.addstr(4, 2, f"HP: 100")
        self.win.addstr(6, 2, f"STR: {self.strength}")
        self.win.addstr(7, 2, f"DEX: {self.dexterity}")
        self.win.addstr(8, 2, f"STA: {self.stamina}")
        self.win.addstr(6, 12, f"INT: {self.intelligence}")
        self.win.addstr(7, 12, f"DEF: {self.defense}")
        self.win.refresh()

    def string_slice(self, string):
        str = []  # variable for sliced string
        str_range = 70  # range of slicing
        result = []

        if len(string) <= str_range:
            return False

        for i in range(0, math.ceil(len(string) / str_range)):
            result.append(string[i * str_range:(i + 1) * str_range])
        result.reverse()

        return result  # final sliced string

    def print_info(self, string, prefix=True):
        #      self.win.erase()
        result = self.string_slice(string)
        if not result:
            self.info_array.insert(0, string)
        else:
            for item in result:
                self.info_array.insert(0, item)
        self.clear_window()

        if len(self.info_array) > self.height - 2:
            for _ in range(len(self.info_array) - 13):
                self.info_array.pop()

        for index, item in enumerate(self.info_array):
            if prefix:
                self.win.addstr(index + 1, 1, f"> {item}")
            else:
                self.win.addstr(index + 1, 1, f"{item}")

        self.win.border(0, 0, 0, 0, 0, 9516, 0, 0)
        self.win.refresh()

    def print_inv(self, p, while_true=False):
        self.clear_window()

        for index, item in enumerate(p.inv_lst, start=1):
            if index == self.highlight and while_true:  # Highlight will appear when come to these condition
                self.win.attron(curses.A_REVERSE)
            self.win.addstr(index + 2, 2, f"{self.ABC[index - 1]}) | {item[0].name} {item[1]}x")
            self.win.addstr(index + 2, self.max_y_x[1] - 9,
                            f"{round(item[0].weight * item[1], 1)} kg")  # Generating item's weight
            self.win.attroff(curses.A_REVERSE)

        p.add_inv_weight()  # Player function that calculates inventory weight

        # Generating labelself.win.addstr("Debug")
        self.win.refresh()
        self.win.addstr(1, self.max_y_x[1] - 12, f"{round(p.inv_weight, 1)}/{p.carry} kg")
        self.win.addstr(1, 2, f"ID | Name")
        self.win.hline(2, 2, "-", self.max_y_x[1] - 4)
        self.win.refresh()

    def delete_info(self):
        self.info_array = []

    def fill_buffer(self):
        self.buffer = self.info_array.copy()

    def clear_buffer(self):
        self.buffer = []

    def restore_info(self):
        self.info_array = self.buffer.copy()

        if len(self.info_array) > self.height - 2:
            self.info_array.pop()
        for index, item in enumerate(self.info_array):
            self.win.addstr(index + 1, 1, f"> {item}")

        self.win.border(0, 0, 0, 0, 0, 9516, 0, 0)
        self.win.refresh()

    def item_quantity_load(self, p):
        self.quantity_index = 1
        self.max_quantity = p.inv_lst[self.highlight - 1][1]
        self.min_quantity = 1


class Menu:
    def __init__(self, height, width, y, x):
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.highlight = 0
        self.menu_arr = []

        self.win = curses.newwin(self.height, self.width, self.y, self.x)

        #self.max_y_x = self.win.getmaxyx()

        #self.max_y = self.max_y_x[0]
        #self.max_x = self.max_y_x[1]

        #self.hmax_y = self.max_y_x[0]//2
        #self.hmax_x = self.max_y_x[1]//2

        logging.debug(f"Menu was created.")

    def add_menu_label(self, *argv):
        for arg in argv:
            self.menu_arr.append(arg)

    def print_menu(self, y, x, y_off=0, x_off=0, spacing=0):
        if len(self.menu_arr) > 0:
            for index, item in enumerate(self.menu_arr):
                if index == self.highlight:
                    self.win.attron(curses.A_REVERSE)
                self.win.addstr((index+spacing) + y+y_off, x+x_off, item)
                self.win.attroff(curses.A_REVERSE)

