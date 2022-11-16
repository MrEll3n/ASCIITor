items = {
    1: "Weapon",
    2: "Armor",
    3: "Food"
}


def generate_random_item(items, x, y):
    pass


class Item:
    def __init__(self, item_key, x, y):
        self.item_key
        self.x = x
        self.y = y


class Weapon:
    def __init__(self, name, desc, lvl, dmg):
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.dmg = dmg


class Armor:
    def __init__(self, name, desc, lvl, defense):
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.defense = defense


class Food:
    def __init__(self, name, desc, reg):
        self.name = name
        self.desc = desc
        self.reg = reg
