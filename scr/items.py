class Item:
    def print_item():
        pass

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




