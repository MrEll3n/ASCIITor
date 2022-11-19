import json
import random
import os

class Item:
    def


class Weapon(Item):
    def __init__(self, x, y, name, desc, lvl, dmg):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.dmg = dmg
        self.char = "("

        print(f"Weapon: {self.name}\n"
              f"desc: {self.desc}\n"
              f"lvl: {self.lvl}\n"
              f"dmg: {self.dmg}\n"
              f"character: {self.char}\n"
              f"pos: {self.x}, {self.y}\n")
        print("---------------------------\n")


class Armor(Item):
    def __init__(self, x, y, name, desc, lvl, defense):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.lvl = lvl
        self.defense = defense
        self.char = "T"
        self.floor

        print(f"Armor: {self.name}\n"
              f"desc: {self.desc}\n"
              f"lvl: {self.lvl}\n"
              f"defense: {self.defense}\n" 
              f"character: {self.char}\n"
              f"pos: {self.x}, {self.y}\n")
        print("---------------------------\n")


class Food(Item):
    def __init__(self, x, y, name, desc, reg):
        self.x = x
        self.y = y
        self.name = name
        self.desc = desc
        self.reg = reg
        self.char = "F"
        self.floor

        print(f"Food: {self.name}\n"
              f"desc: {self.desc}\n"
              f"regen: {self.reg}\n"
              f"character: {self.char}\n"
              f"pos: {self.x}, {self.y}\n")
        print("---------------------------\n")


# Debugging
if __name__ == "__main__":
    os.system("cls")
    with open('Items.json', 'r') as f:
        item_list = json.load(f)
    # print(item_list["weapons"][0]["name"])

    items_world = []
    for i in range(0, 100):
        if random.randrange(0, 100) < 1:
            match random.randrange(0, 3):
                # Weapon creation
                case 0:
                    print(f"#{i + 1} - Weapon\n")
                    weapon_arr = [item for item in item_list["weapons"][random.randrange(len(item_list["weapons"]))].values()]
                    items_world.append(Weapon(i, 0, weapon_arr[0], weapon_arr[1], weapon_arr[2], weapon_arr[3]))

                # Armor creation
                case 1:
                    print(f"#{i + 1} - Armor\n")
                    armor_arr = [item for item in item_list["armor"][random.randrange(len(item_list["armor"]))].values()]
                    items_world.append(Armor(i, 0, armor_arr[0], armor_arr[1], armor_arr[2], armor_arr[3]))

                # items_world.append(items.Armor())

                # Food creation
                case 2:
                    print(f"#{i + 1} - Food\n")
                    food_arr = [item for item in item_list["food"][random.randrange(len(item_list["food"]))].values()]
                    items_world.append(Food(i, 0, food_arr[0], food_arr[1], food_arr[2]))
                # items_world.append(items.Weapon())

    for object in items_world:
        print(f"{object.name} - {object.char}")
