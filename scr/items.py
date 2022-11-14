items = [
    "Weapon",
    "Armor",
    "Food"
]


def generate_item_rand(x, y):



class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Weapon(Item):
    def __init__(self, name, desc, lvl, dmg):
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.dmg = dmg


class Armor(Item):
    def __init__(self, name, desc, lvl, defense):
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.defense = defense


class Food(Item):
    def __init__(self, name, desc, reg):
        self.name = name
        self.desc = desc
        self.reg = reg
