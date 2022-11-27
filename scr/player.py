import curses
from items import Item
from hud import Window as win
from curses.textpad import Textbox, rectangle
import time


class Player:
    def __init__(self, x, y, hp, mana, strength, defense, game_pad, map):
        self.x = x
        self.y = y
        self.hp = hp
        self.maxhp = self.hp
        self.mana = mana
        self.maxmana = self.hp
        self.strength = strength
        self.defense = defense
        self.floor = ""
        self.game_pad = game_pad
        self.map = map
        self.inv_lst = []

        self.floor = self.get_floor(self.map, 0, 0, 1)
        self.draw_player(self.map, 0, 0)

    def get_floor(self, map_arr, offset_x, offset_y, remember_bool):
        if remember_bool == 1:
            self.floor = str(map_arr[self.y + offset_y][self.x + offset_x][0])
            return self.floor
        elif remember_bool == 0:
            return str(map_arr[self.y + offset_y][self.x + offset_x][0])

    def get_floor_type(self, map_arr, offset_x, offset_y):
        return str(map_arr[self.y + offset_y][self.x + offset_x][1])

    def draw_player(self, map_arr, offset_x, offset_y):
        map_arr[self.y + offset_y][self.x + offset_x][0] = "@"
        self.game_pad.addstr(self.y + offset_y, self.x + offset_x, "@")

    def draw_floor(self, map_arr, offset_x, offset_y):
        map_arr[self.y + offset_y][self.x + offset_x][0] = self.floor
        if self.floor == ".":
            self.game_pad.addstr(self.y + offset_y, self.x + offset_x, f"{self.floor}", curses.A_DIM)
        else:
            self.game_pad.addstr(self.y + offset_y, self.x + offset_x, f"{self.floor}")

    def move_left(self, map_arr):
        if not (self.x > 0 and self.get_floor(map_arr, -1, 0, 0) != "#"):
            return False

        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, -1, 0, 1)
        self.x -= 1

        self.draw_player(map_arr, 0, 0)
        return True

    def can_left(self, map_arr):
        if not (self.x > 0 and self.get_floor(map_arr, -1, 0, 0) != "#"):
            return False
        else:
            return True

    def move_right(self, map_arr, game_x):
        if not (self.x < (game_x - 2) and self.get_floor(map_arr, 1, 0, 0) != "#"):
            return False

        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 1, 0, 1)
        self.x += 1

        self.draw_player(map_arr, 0, 0)
        return True

    def can_right(self, map_arr, game_x):
        if not (self.x < (game_x - 2) and self.get_floor(map_arr, 1, 0, 0) != "#"):
            return False
        else:
            return True

    def move_up(self, map_arr):
        if not (self.y > 0 and self.get_floor(map_arr, 0, -1, 0) != "#"):
            return False

        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 0, -1, 1)
        self.y -= 1

        self.draw_player(map_arr, 0, 0)
        return True

    def can_up(self, map_arr):
        if not (self.y > 0 and self.get_floor(map_arr, 0, -1, 0) != "#"):
            return False
        else:
            return True

    def move_down(self, map_arr, game_y):
        if not (self.y < game_y and self.get_floor(map_arr, 0, 1, 0) != "#"):
            return False

        self.draw_floor(map_arr, 0, 0)
        self.get_floor(map_arr, 0, 1, 1)
        self.y += 1

        self.draw_player(map_arr, 0, 0)
        return True

    def can_down(self, map_arr, game_y):
        if not (self.y < game_y and self.get_floor(map_arr, 0, 1, 0) != "#"):
            return False
        else:
            return True

    def pickup_item(self, map_arr, items_world, offset_x, offset_y):
        if self.get_floor_type(map_arr, offset_x, offset_y) == "i":
            for item in items_world:
                if item.x == self.x and item.y == self.y:
                    self.inv_lst.append(item)
                    map_arr[self.y + offset_y][self.x + offset_x][0] = [Item.floor, "b"][0]
        return len(self.inv_lst)
