import curses
from curses.textpad import Textbox, rectangle



class Window():
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
    
    def update_stats(self, p):
        self.hp = p.hp
        self.maxhp = p.maxhp
        self.mana = p.mana
        self.maxmana = p.maxmana
        self.strength = p.strength
        self.defense = p.defense

    def clear_window(self):
        self.win.clear()
        self.win.border()
        if self.name != "":
            self.win.addstr(0, 3, f" {self.name} ")
        self.win.refresh()

    def create_window(self):
        self.win = curses.newwin(self.height, self.width, self.y, self.x)
        self.clear_window()        
    
    def print_stats(self, p):
        self.clear_window()
        self.update_stats(p)
        self.win.addstr(2, 2, f"HP: {self.hp} / {self.maxhp}")
        self.win.addstr(3, 2, f"MP: {self.mana} / {self.maxmana}")
        self.win.addstr(5, 2, f"STR: {self.strength}")
        self.win.addstr(6, 2, f"DEF: {self.defense}")
        self.win.refresh()

















class Inventory:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inv_lst = []

    def create_inventory_window(self, stdscr):
        #rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        stdscr.addstr(self.y, self.x + 3, f" Inventory ")
        
        invwin = curses.newwin(self.height, self.width, self.y, self.x)
        #invpad.refresh(self.y+1, self.x+1, 1, 1, self.y+self.height-1, self.x+self.width-1)
        invwin.addstr(2, 2, "Item 1x")
        
        invwin.refresh()

class Stats:
    def __init__(self, p, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = p.hp
        self.maxhp = p.maxhp
        self.mana = p.mana
        self.maxmana = p.maxmana
        self.strength = p.strength
        self.defense = p.defense
        

    def update_stats(self, p):
        self.hp = p.hp
        self.maxhp = p.maxhp
        self.mana = p.mana
        self.maxmana = p.maxmana
        self.strength = p.strength
        self.defense = p.defense
        self.print_all()

    def create_stats_window(self, stdscr):
        #rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        stdscr.addstr(self.y, self.x + 3, f" Stats ")
        self.statswin = curses.newwin(self.height, self.width, self.y, self.x)
        #self.statswin = 
        #invpad.refresh(self.y+1, self.x+1, 1, 1, self.y+self.height-1, self.x+self.width-1)
        
        #
        self.statswin.refresh()
        self.print_all()

    def print_hp(self):
        self.statswin.addstr(2, 2, f"HP: {self.hp}/{self.maxhp}")
    
    def print_mana(self):
        self.statswin.addstr(3, 2, f"MP: {self.mana}/{self.maxmana}")
    
    def print_strength(self):
        self.statswin.addstr(4, 2, f"STR: {self.strength}")
    
    def print_defense(self):
        self.statswin.addstr(5, 2, f"DEF: {self.defense}")

    def print_all(self):
        self.print_hp()
        self.print_mana()
        self.print_strength()
        self.print_defense()
        self.statswin.refresh()
