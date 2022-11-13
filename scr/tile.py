import curses
from curses.textpad import Textbox, rectangle

tile_type = {
    "space": " ",
    "grass1": ".",
    "grass2": ":",
    "wall": "#",
    "flower": "W",
    "item": "$",
}


class Tile():
    def __init__(self, type):
        self.type = type
        self.char = tile_type[type]

    def add_tile(self):
        pass
