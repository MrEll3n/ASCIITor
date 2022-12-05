import curses
from curses.textpad import Textbox, rectangle


class Window:
    def __init__(self, win_type, y, x, height, width, name, p=None):
        self.win_type = win_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

        if self.win_type == "stats" and p:
            self.hp = p.hp
            self.maxhp = p.maxhp
            self.mana = p.mana
            self.maxmana = p.maxmana
            self.strength = p.strength
            self.defense = p.defense

        if self.win_type == "info":
            self.info_array = []

        if self.win_type == "inv":
            pass

        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.clear_window()

    def update_stats(self, p):
        self.hp = p.hp
        self.maxhp = p.maxhp
        self.mana = p.mana
        self.maxmana = p.maxmana
        self.strength = p.strength
        self.defense = p.defense

    def clear_window(self):
        #self.win.clear()
        # self.win.border()
        if self.win_type == "info":
            self.win.border(0, 0, 0, 0, 0, 9516, 0, 0)
        elif self.win_type == "stats":
            self.win.border(0, 0, 0, 0, 0, 0, 9524, 0)
        else:
            self.win.border()

        if self.name != "":
            self.win.addstr(0, 3, f" {self.name} ")
        self.win.refresh()

    # def create_window(self):
    #    self.win = curses.newwin(self.height, self.width, self.y, self.x)
    #    self.clear_window()

    def print_stats(self, p):
        self.win.clear()
        self.clear_window()
        self.update_stats(p)
        self.win.addstr(2, 2, f"HP: {self.hp} / {self.maxhp}")
        self.win.addstr(3, 2, f"MP: {self.mana} / {self.maxmana}")
        self.win.addstr(5, 2, f"STR: {self.strength}")
        self.win.addstr(6, 2, f"DEF: {self.defense}")
        self.win.refresh()

    def print_info(self, string):
        self.win.clear()
        self.info_array.insert(0, string)
        self.clear_window()

        if len(self.info_array) > self.height - 2:
            self.info_array.pop()
        for index, item in enumerate(self.info_array):
            self.win.addstr(index + 1, 1, f"> {item}")

        self.win.refresh()

    def print_inv(self, p):
        self.clear_window()
        self.total_weight = 0.0

        for index, item in enumerate(p.inv_lst, start=1):
            maxyx = self.win.getmaxyx()
            self.win.addstr(index + 2, 2, f"{index}. - {item.name}")
            self.win.addstr(index + 2, maxyx[1] - 8, f"{item.weight} kg")

        for item in p.inv_lst:
            self.total_weight += item.weight

        self.win.addstr(1, maxyx[1] - 11, f"{round(self.total_weight, 1)}/{p.carry} kg")
        self.win.refresh()
