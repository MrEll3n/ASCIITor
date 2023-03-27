import math
import curses
import logging


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

        # rectangle(self.win, self.ul_y, self.ul_x, self.lr_y, self.lr_x)
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
            self.maxhp = p.maxhp
            self.hp = p.hp
            self.strength = p.strength
            self.intelligence = p.intelligence
            self.dexterity = p.dexterity
            self.defense = p.defense
            self.luck = p.luck
            self.player_lvl = p.entity_lvl

        if self.win_type == "info":
            self.info_array = []
            self.buffer = []

        if self.win_type == "inv":
            self.highlight = 1
            self.quantity_index = 1
            self.max_quantity = 1
            self.min_quantity = 1

        if self.win_type == "menu":
            self.highlight = 1

        if self.win_type == "menu_stats":
            pass
        
        if self.win_type == "fight":
            self.health_bar = 0
            self.current_x = self.x
            self.current_y = self.y

        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.max_y_x = self.win.getmaxyx()

        self.clear_window()

    def draw_exp_bar(self, player):
        result = player.entity_exp

        outcome = ''.ljust(math.floor(result*(self.width-6)), '*')  # calculating of EXP bars via percentile
        filling = ''.ljust((self.width-6)-len(outcome), ".") # calculating of filling for EXP

        return f"{outcome}{filling}"  # constant length bar

    def draw_hp_bar(self, entity):
        result = entity.hp/entity.maxhp

        outcome = ''.ljust(math.floor(result*(self.width-6)), '*')  # calculating of HP bars via percentile
        filling = ''.ljust((self.width-6)-len(outcome), ".") # calculating of filling for HP

        return f"{outcome}{filling}"  # constant length bar

    def redraw(self):
        self.win.redrawwin()
        self.win.refresh()
    
    def delete(self):
        self.win.erase()
        del self

    def addText(self, y, x, text):
        self.win.addstr(y, x, text)

    def update_stats(self, p):
        self.stamina = p.stamina
        self.maxhp = p.maxhp
        self.hp = p.hp
        self.strength = p.strength
        self.intelligence = p.intelligence
        self.dexterity = p.dexterity
        self.defense = p.defense
        self.luck = p.luck
        self.player_lvl = p.entity_lvl

    def clear_window(self):
        self.win.erase()
        # self.win.border()
        if self.win_type == "info":
            self.win.border(0, 0, 0, 0, 0, 0, 0, 0) #  9516
        elif self.win_type == "stats":
            self.win.border(0, 0, 0, 0, 0, 0, 0, 0) #  9524
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

    def print_stats(self, p):
        # self.win.clear()
        self.clear_window()
        # self.update_stats(p)
        self.win.addstr(2, 2, f"{p.name} [{p.entity_lvl}] - {p.entity_race} {p.entity_class}")
        self.win.addstr(4, 2, f"HP: {p.hp} / {p.maxhp}")
        self.win.addstr(6, 2, f"STR: {p.sum_strength}")
        self.win.addstr(7, 2, f"DEX: {p.sum_dexterity}")
        self.win.addstr(8, 2, f"INT: {p.sum_intelligence}")
        self.win.addstr(6, 12, f"STA: {p.sum_stamina}")
        self.win.addstr(7, 12, f"DEF: {p.sum_defense}")
        self.win.addstr(8, 12, f"LUC: {p.sum_luck}")
        self.win.addstr(10, 2, f"|{self.draw_exp_bar(p)}|")
        self.win.refresh()

    def string_slice(self, string):
        str_range = self.width-5  # range of slicing
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

        self.win.border(0, 0, 0, 0, 0, 0, 0, 0) #  9516
        self.win.refresh()

    def print_inv(self, p, while_true=False):
        self.clear_window()

        for index, item in enumerate(p.inv_lst, start=1):
            if index == self.highlight and while_true:  # Highlight will appear when come to these condition
                self.win.attron(curses.A_REVERSE)

            if item[1] == 1:
                self.win.addstr(index + 2, 2, f"{self.ABC[index - 1]}) | {item[0].name}")
                self.win.addstr(index + 2, self.max_y_x[1] - 9,
                                f"{round(item[0].weight * item[1], 1)} kg")  # Generating item's weight
            else:
                self.win.addstr(index + 2, 2, f"{self.ABC[index - 1]}) | {item[0].name} {item[1]}x")
                self.win.addstr(index + 2, self.max_y_x[1] - 9,
                                f"{round(item[0].weight * item[1], 1)} kg")  # Generating item's weight

            if item[0].__class__.__name__ == "Weapon" or item[0].__class__.__name__ == "Armor":
                if item[0].is_equiped:
                    self.win.addstr(index + 2, 32, "E")

            self.win.attroff(curses.A_REVERSE)

        p.add_inv_weight()  # Player function that calculates inventory weight

        # Generating labelself.win.addstr("Debug")
        self.win.refresh()
        self.win.addstr(1, self.max_y_x[1] - 12, f"{round(p.inv_weight, 1)}/{p.carry} kg")
        self.win.addstr(1, 2, "ID | Name")
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

    def del_stats_values(self, y, x):
        self.win.addstr(y, x, "  ")
        self.win.addstr(y+1, x, "  ")
        self.win.addstr(y+2, x, "  ")
        self.win.addstr(y+3, x, "  ")
        self.win.addstr(y+4, x, "  ")
        self.win.addstr(y+5, x, "  ")
        self.win.refresh()

    def print_stats_label(self, y, x):
        self.win.addstr(y, x, "STR")
        self.win.addstr(y+1, x, "INT")
        self.win.addstr(y+2, x, "DEX")
        self.win.addstr(y+3, x, "STA")
        self.win.addstr(y+4, x, "DEF")
        self.win.addstr(y+5, x, "LUC")
        self.win.refresh()

    def print_race_stats(self, y, x, highlight, races_instances):
        self.win.addstr(y, x, "{:2d}".format(races_instances[highlight].strength))
        self.win.addstr(y+1, x, "{:2d}".format(races_instances[highlight].intelligence))
        self.win.addstr(y+2, x, "{:2d}".format(races_instances[highlight].dexterity))
        self.win.addstr(y+3, x, "{:2d}".format(races_instances[highlight].stamina))
        self.win.addstr(y+4, x, "{:2d}".format(races_instances[highlight].defense))
        self.win.addstr(y+5, x, "{:2d}".format(races_instances[highlight].luck))
        self.win.refresh()

    def print_role_stats(self, y, x, highlight, roles_instances):
        self.win.addstr(y, x, "{:2d}".format(roles_instances[highlight].strength))
        self.win.addstr(y+1, x, "{:2d}".format(roles_instances[highlight].intelligence))
        self.win.addstr(y+2, x, "{:2d}".format(roles_instances[highlight].dexterity))
        self.win.addstr(y+3, x, "{:2d}".format(roles_instances[highlight].stamina))
        self.win.addstr(y+4, x, "{:2d}".format(roles_instances[highlight].defense))
        self.win.addstr(y+5, x, "{:2d}".format(roles_instances[highlight].luck))
        self.win.refresh()

    def stats_sum(self, race_values, role_values, race_highlight, role_highlight):
        stats_sum = []
        stats_sum.append(10+race_values[race_highlight].strength+role_values[role_highlight].strength)
        stats_sum.append(10+race_values[race_highlight].intelligence+role_values[role_highlight].intelligence)
        stats_sum.append(10+race_values[race_highlight].dexterity+role_values[role_highlight].dexterity)
        stats_sum.append(10+race_values[race_highlight].stamina+role_values[role_highlight].stamina)
        stats_sum.append(10+race_values[race_highlight].defense+role_values[role_highlight].defense)
        stats_sum.append(10+race_values[race_highlight].luck+role_values[role_highlight].luck)
        return stats_sum

    def print_summer_stats(self, y, x, stats_sum):
        self.win.addstr(y, x, "{:2d}".format(stats_sum[0]))
        self.win.addstr(y+1, x, "{:2d}".format(stats_sum[1]))
        self.win.addstr(y+2, x, "{:2d}".format(stats_sum[2]))
        self.win.addstr(y+3, x, "{:2d}".format(stats_sum[3]))
        self.win.addstr(y+4, x, "{:2d}".format(stats_sum[4]))
        self.win.addstr(y+5, x, "{:2d}".format(stats_sum[5]))
        self.win.refresh()


class Menu:
    def __init__(self, height, width, y, x):
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.highlight = 0
        self.menu_arr = []

        self.win = curses.newwin(self.height, self.width, self.y, self.x)

        # self.max_y_x = self.win.getmaxyx()

        # self.max_y = self.max_y_x[0]
        # self.max_x = self.max_y_x[1]

        # self.hmax_y = self.max_y_x[0]//2
        # self.hmax_x = self.max_y_x[1]//2

        # logging.debug(f"Menu was created.")

    def redraw(self):
        self.win.redrawwin()
        self.win.refresh()
    
    def add_menu_label(self, *argv):
        for arg in argv:
            self.menu_arr.append(arg)

    def print_menu(self, y, x, y_off=0, x_off=0):
        if len(self.menu_arr) > 0:
            for index, item in enumerate(self.menu_arr):
                if index == self.highlight:
                    self.win.attron(curses.A_REVERSE)
                self.win.addstr(index + y+y_off, x+x_off, item)
                self.win.attroff(curses.A_REVERSE)

    def print_menu_adv(self):
        label1 = "Save Game"
        label2 = "Help"
        label3 = "Exit"

        def print_label(y, label):
            self.win.addstr(y, (self.width//2)-(len(label)//2), f"{label}")

        def highlight(highlight, y, label):
            if self.highlight == highlight:
                self.win.attron(curses.A_REVERSE)
            print_label(y, label)
            self.win.attroff(curses.A_REVERSE)

        highlight(1, 2, label1)
        highlight(2, 4, label2)
        highlight(3, 7, label3)

        self.win.refresh()

def game_over(stdscr, p, rows, cols):   
    hrows = rows // 2
    hcols = cols // 2
    label1 = "You've died!"
    label2 = f"{p.name} - {p.entity_lvl} lvl"
    label3 = "Back to Menu..."


    stdscr.clear()
    
    with open("gameover.txt", "r") as f:
        for i in range(23):
            stdscr.addstr(i+2, hcols - 42, f.readline())
        f.close()
    
    stdscr.addstr(10, (hcols-len(label1)//2), label1)
    stdscr.addstr(13, (hcols-len(label2)//2), label2)
    stdscr.addstr(rows - 2, hcols + 55 - len(label3), label3)
    
