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
        # creating and filling NUMBER constant for selector
        self.ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        if self.win_type == "stats" and p:
            self.hp = p.hp
            self.maxhp = p.maxhp
            self.mana = p.mana
            self.maxmana = p.maxmana
            self.strength = p.strength
            self.defense = p.defense

        if self.win_type == "info":
            self.info_array = []
            self.buffer = []

        if self.win_type == "inv":
            self.highlight = 1

        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.max_y_x = self.win.getmaxyx()

        self.clear_window()

    def update_stats(self, p):
        self.hp = p.hp
        self.maxhp = p.maxhp
        self.mana = p.mana
        self.maxmana = p.maxmana
        self.strength = p.strength
        self.defense = p.defense

    def clear_window(self):
        self.win.clear()
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

    def print_info(self, string, prefix=False):
        self.win.clear()
        self.info_array.insert(0, string)
        self.clear_window()

        if len(self.info_array) > self.height - 2:
            self.info_array.pop()

        for index, item in enumerate(self.info_array):
            self.win.addstr(index + 1, 1, f"> {item}")

        self.win.border(0, 0, 0, 0, 0, 9516, 0, 0)
        self.win.refresh()

    def print_inv(self, p, describing=False):
        self.clear_window()

        for index, item in enumerate(p.inv_lst, start=1):
            if index == self.highlight and describing:
                self.win.attron(curses.A_REVERSE)
            self.win.addstr(index + 2, 2, f"{self.ABC[index-1]}. | {item[0].name} {item[1]}x")
            self.win.addstr(index + 2, self.max_y_x[1] - 9, f"{round(item[0].weight*item[1], 1)} kg")  # Generating item's weight
            self.win.attroff(curses.A_REVERSE)

        p.add_inv_weight()  # Player function that calculates inventory weight

        # Generating labels
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

