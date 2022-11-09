import curses
from curses.textpad import Textbox, rectangle
import time

class Player:
    def __init__(self, x, y, hp, mana, strength, defense, game_pad, map):
        self.x = x
        self.y = y
        self.hp = hp
        self.mana = mana
        self.strength = strength
        self.defense = defense
        self.floor = ""
        self.game_pad = game_pad
        self.map = map

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_player(self.map, 0, 0)
        
    def get_floor(self, map_arr, offset_x, offset_y, remember_bool):
        if remember_bool == 1:
            self.floor = str(map_arr[self.y+offset_y][self.x+offset_x])
            return self.floor
        elif remember_bool == 0:
            return str(map_arr[self.y+offset_y][self.x+offset_x])

    def draw_player(self, map_arr, offset_x, offset_y):
        map_arr[self.y+offset_y][self.x+offset_x] = "@"
        self.game_pad.addstr(self.y+offset_y, self.x+offset_x, "@")

    def draw_floor(self, map_arr, offset_x, offset_y):
        map_arr[self.y+offset_y][self.x+offset_x] = self.floor
        if self.floor == ".":
            self.game_pad.addstr(self.y+offset_y, self.x+offset_x, f"{self.floor}", curses.A_DIM)
        else:
            self.game_pad.addstr(self.y+offset_y, self.x+offset_x, f"{self.floor}")

    def move_left(self, map_arr):
        if not (self.x > 0 and self.get_floor(map_arr, -1, 0, 0) != "#"):
            return False

        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, -1, 0, 1)
        self.x -= 1
        curses.beep()
        
        self.draw_player(map_arr, 0, 0)
        return True

    def move_right(self, map_arr, game_x):
        if not (self.x < (game_x - 2) and self.get_floor(map_arr, 1, 0, 0) != "#"):
            return False
    
        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 1, 0, 1)
        self.x += 1
        curses.beep()
        
        self.draw_player(map_arr, 0, 0)
        return True

    def move_up(self, map_arr):
        if not (self.y > 0 and self.get_floor(map_arr, 0, -1, 0) != "#"):
            return False
            
        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 0, -1, 1)
        self.y -= 1
        curses.beep()
        
        self.draw_player(map_arr, 0, 0)
        return True

    def move_down(self, map_arr, game_y):
        if not (self.y < game_y and self.get_floor(map_arr, 0, 1, 0) != "#"):
            return False
            
        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 0, 1, 1)
        self.y += 1
        curses.beep()

        self.draw_player(map_arr, 0, 0)
        return True

class Inventory:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def create_inventory(self, stdscr):
        #rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        rectangle(stdscr, self.y, self.x, self.y+self.height, self.x+self.width)
        stdscr.addstr(self.y, self.x + 3, f" Inventory ")
        
        invwin = curses.newwin(self.height, self.width, self.y, self.x)
        #invpad.refresh(self.y+1, self.x+1, 1, 1, self.y+self.height-1, self.x+self.width-1)
        invwin.addstr(2, 2, "Item 1x")
        
        invwin.refresh()

