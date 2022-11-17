import json
import random

if __name__ == "__name__":
    with open('Items.json', 'r') as f:
        item_list = json.load(f)
    print(item_list["weapons"][0]["name"])

    for i in range(0, 100):
        if random.randrange(0, 100) < 1:
            match random.randrange(0, 3):
                case 0:
                    print(f"#{i + 1} - 1")
                # items_world.append(items.Weapon())
                case 1:
                    print(f"#{i + 1} - 2")
                # items_world.append(items.Armor())
                case 2:
                    print(f"#{i + 1} - 3")
                # items_world.append(items.Weapon())



# items = {
#    1: "Weapon",
#    2: "Armor",
#    3: "Food"
# }


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
