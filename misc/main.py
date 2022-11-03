import os
import sys
import time
from pynput.keyboard import *
#import numpy as np

#keyboard = Controller()

tile_type = {
    "floor": ".",
    "wall": "#",
    "player": "@"
}


class Tile:
    def __init__(self, type):
        self.type = type
        self.char = tile_type[type]


class Player:
    def __init__(self, x, y):
        self.x = x  # horizontal axis - 0 is default value
        self.y = y  # vertical axis - 0 is default value
        self.prex = x
        self.prey = y


class GameField:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def create_game_field(self, playerPos):
        self.array = []
        self.array += [Tile("wall") for _ in range(self.width)]
        for _ in range(self.height-2):
            self.array += [Tile("wall")]
            self.array += [Tile("floor") for _ in range(self.width-2)]
            self.array += [Tile("wall")]
        self.array += [Tile("wall") for _ in range(self.width)]
        self.array[playerPos] = Tile("player")

#    def update_game_field(self, playerPos, prePlayerPos):
#        del self.array[prePlayerPos]
#        self.array[playerPos] += Tile("player")

    def print_game_field(self):
        for _ in range(self.height):
            for _ in range(self.width):
                print(self.array[0].char, end="")
                del self.array[0]
            print("")

    def print_game_field_full(self):
        inc = 0
        for i in range(self.height):
            for j in range(self.width):
                print(self.array[inc].char, end="")
                inc += 1
            print("")


g = GameField(100, 30)

p = Player(1, 1)

playerPos = g.width+1 + p.x + p.y*g.width

os.system("clear")
g.create_game_field(playerPos)
g.print_game_field_full()
print(f"X: {p.x} | Y: {p.y}")


def update():
    os.system("clear")
    g.create_game_field(g.width+1 + p.x + p.y*g.width)
    g.print_game_field_full()
    print(f"X: {p.x} | Y: {p.y}")


######################################################################################################################################################
def on_press(key):
    try:
        if key.char == "d" and g.array[g.width+1 + p.x+1 + p.y*g.width].char != Tile("wall").char:
            p.x += 1
            update()
#            print(g.array[g.width+1 + p.x+1 + p.y*g.width].char)
#            print(g.width+1 + p.x+1 + p.y*g.width)

        elif key.char == "a" and g.array[g.width+1 + p.x-1 + p.y*g.width].char != Tile("wall").char:
            p.x -= 1
            update()
#            print(g.array[g.width+1 + p.x-1 + p.y*g.width].char)
#            print(g.width+1 + p.x-1 + p.y*g.width)

        if key.char == "w" and g.array[(1 + p.x+1 + p.y*g.width)].char != Tile("wall").char:
            p.y -= 1
            update()
#            print(g.array[(1 + p.x+1 + p.y*g.width)].char)
#            print(1 + p.x+1 + p.y*g.width)

        elif key.char == "s" and g.array[(2*g.width)+1 + p.x+1 + p.y*g.width].char != Tile("wall").char:
            p.y += 1
            update()
#            print(g.array[(2*g.width)+1 + p.x+1 + p.y*g.width].char)
#            print((2*g.width)+1 + p.x+1 + p.y*g.width)

        elif key == Key.esc:
            return False
    except AttributeError:
        update()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
